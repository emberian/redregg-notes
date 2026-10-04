# SCHOLAR-OS — the OS as a whole, built from language technology: lineage for Mini (2026-10-04)

**Brief:** `/Users/ember/dev/redregg/work/PROGRAM-MODEL-BRIEF-20261004.md`. This scholar covers *the OS as a
whole*. Three sibling scholars cover Bread, calls and concurrency (actors, ocaps, durable execution,
smart-contract object models) and laws and contracts. Ember's framing: "answering your program model
questions is basically design the whole OS".

**How this was produced.** SCHOLAR-OS (Opus 5.5) wrote the brief to five reading lanes (Opus) and read
directly as well:
- **Read by SCHOLAR-OS:** Faré's Houyhnhnm corpus (§F), the persistence retrospectives and critiques (§G),
  and dynamic software updating (§H).
- **Lane A** (§2): language-based OSes.
- **Lane B** (§3): capability OSes, namespaces and orthogonal persistence.
- **Lane C** (§4): world computers as OSes.
- **Lane D** (§5): naming and metering.
- **Lane E** (§6): live and malleable systems, and presentation.

Each lane read its primary sources in full where its tags say READ, saved them under
`~/paperbin/world-program-model/` with a `pdftotext` `.txt` beside each PDF, and wrote its section. SCHOLAR-OS
read every lane section in full and spot-checked quotations against the saved texts. Ten load-bearing quotes
were checked, all found, with two attributions corrected:
- Morningstar, "you save it all, indiscriminately";
- Salehi et al., "48% of systems could be upgraded with the breach of a single signing key";
- Agoric, "Promises Are Broken";
- Theseus, "385 µs";
- Heiser & Elphinstone, clans and chiefs "most cursed";
- Ungar, orthogonal persistence "a flawed concept";
- Motoko, "evolutionary dead end";
- Duffy, "Distributed transactions are evil". This is in *Asynchronous Everything*, not *15 Years of
  Concurrency*.
- ICP: the docs say "In Motoko, `await` always commits the current state". The phrase "await is a commit
  point" is our paraphrase.
- Liedtke, "the fixpoint stabilises a corrupted system".

**Tags.** **READ** means the text was read (partial reads name their sections). **SKIMMED** means abstract,
headings or selected parts only. **INFERRED** means our connection to Mini, not the authors' claim. Each
entry gives:
- the OS-level decisions;
- the evidence;
- what failed and why;
- the lesson for Mini: which fork, what it pushes, what to build, and the cost.

**Searches.** Kagi: about 34 successful queries across all lanes. The brief's `GET ?q=` form returns 404,
because Kagi v1 is POST JSON; the helper is `scratchpad/scholar-os/kagi.sh`. Scry over Hacker News was used
for practitioner critiques, about 12 queries. Paywalls were not needed; every source used a free copy.

**Not read** (named so nobody assumes otherwise):
- the Coyotos retrospective;
- the Aurora HotOS companion;
- the Twizzler TOS 2021 journal version;
- Fuchsia API-level and versioning docs;
- the Cooper & Wise 1996 critique (abstract only);
- the Cambria PaPoC paper (the essay was read);
- Goldberg 1984 (quoted second-hand from Hacker News);
- the Filecoin paper;
- Waldspurger's stride scheduling.

**Mini facts used beyond the brief.** These come from `/Users/ember/dev/redregg/work/ORIENT-A-LANGUAGE-COMPUTE-20261004.md`, read by SCHOLAR-OS:
- Main proves `typed_yield_quiescent`: every yield is a safe point.
- Core4 activity Plans are first-order, non-recursive sums with one action per yield.
- "No kernel delivers responses or persists an activity yet."
- ORIENT-A lists three open contradictions: charge (measured ticks vs a signed envelope); the admission
  executor (Lean `runBounded`, the C machine, or the `@[csimp]` fast machine); and in-turn termination.
- `Compiler/Evaluator.registry` is `[nock]`, so admission is by re-execution only.

---
## Part I — Synthesis: a proposed shape for Mini as a distributed OS

Mini's spine (a deterministic kernel admitting ordered, signed inputs by re-execution over an atomic,
versioned store) is not the risky part: Urbit, ICP, Agoric, Croquet, Azimuth L2 and Ethereum share it, and
KeyKOS and EROS ran it for years (§3, §4). Across roughly 100 works, failures cluster in five places:
upgrading live state (above all suspended computations); who pays (above all for kernel work done on
someone's behalf); state changing under an activity while it waits; administering authority and names; and
presentation without a model. Mini's assets (a proved machine, an exact checkpoint codec, effects as a type,
decidable laws that explain refusals) answer all five only if aimed at them on purpose. § numbers point
into Part II.

### 1. Object and process model
- **The object is a cell with a stable id, and that id is never the package hash.** Croquet made session
  identity a hash of the code, so any code change created a new world (§4). The cell holds:
  - durable state;
  - a law hash;
  - a *package pin* = (interface type, package hash), the Inferno `load` shape (§3);
  - an **upgrade policy** set at creation: frozen, owner, threshold, or governed-with-delay. It may only be
    tightened. Salehi et al. found 48% of upgradeable Ethereum systems one key away from a rewrite (§4).
  - a continuity counter (Urbit's `rift`), and its activities.
- **Sealed and coarse.** New code enters a live object only by a governed re-pin; reflection goes through
  capability-gated mirrors (Singularity, Self; §2). One law over a rich structure, not a cell per record
  (KeyNIX regretted a domain per inode; §3).
- **Split durable state from continuations** (the literature's strongest pushback on the brief). A
  full-machine checkpoint as the long-lived form is what Electric Communities found "effectively
  intractable" to migrate; PJama never solved it, Motoko's first design died of it, Urbit avoided it (§3,
  §4). Keep the checkpoint/heap design (it makes yield/resume exact) but classify what it stores:
  - *durable state* is declared, first-order, **stable-typed** Core4 data and capabilities;
  - *activity checkpoints* are pinned to the package that created them, epoch-tagged, and short-lived by
    policy.
- **Services keep no per-client tables:** clients hold opaque typed receipts and pay their storage
  (Theseus, Tock grants; §2).

### 2. Communication (fork 1)
The root's lean holds (Midori prompt/eventual, Spritely near/far, RedLeaf's ban on mutable borrows;
Ethereum re-entrancy is the counterexample; §2, §4). Making it *rich* means adding:
- **One uniform `Invoke(cap, msg)` action** to a badged endpoint or facet, never a raw cell id (EROS, L4,
  Agoric c-lists; §3, §4); membranes, revocation and monitoring come free.
- **Exchangeable payloads:** forced data, capabilities, linear assets, never thunks; a lazy thunk *is* a
  pointer into the sender's heap (Sing#; §2). In-turn reads name a root, so re-execution reads the same
  bytes.
- **The await is the commit point, and the only one.** ICP's "`await` always commits" produced re-entrancy,
  check-then-act bugs and lost locks, and DFINITY's remedy is a hand-written journal (§4). Mini commits the
  Plan and the checkpoint in one turn, so the checkpoint *is* that journal. Every awaited response is a sum,
  `Reply | Refused(explanation) | Unknown | TimedOut | Upgraded`, and failure arrives only on receive,
  inside the protocol. Sing# admitted its contracts never checked error paths; this closes that gap (§2).
- **Awaits are joins with deadlines.** An await is an `alt` over typed sources (Sing#, Inferno, seL4
  notifications), carries a block-height deadline and escrows its resume and timeout fees (ICP). No
  wall-clock timeouts (L4 abandoned them; §3).
- **Promise pipelining and three-party handoff** (Midori, CapTP) across domains, where round trips cost
  consensus; replies route by a printable continuation id (Urbit's duct).
- **Channels as cells** whose law is a finite-state session protocol; Sing#'s send-and-receive-per-cycle
  rule bounds the mailbox, so it can be prepaid.
- **Embargo outbound effects** until the turn (BFT: block) commits; messages carry the turn id, so receipt
  is idempotent (Agoric, Aurora, TreeSLS, Faré; §3, §4, §F).
- **Cross-version calls** go through lenses at the interface boundary (Cambria; §H); durable state is never
  kept in two shapes (Dark; §6).

### 3. Concurrency (fork 3)
- **Turns stay atomic; interleaving happens only at yields** (Midori, Oberon, seL4). Main already proves
  `typed_yield_quiescent`.
- **Several activities per object:** many may be suspended; a resume is admitted by declared footprints
  (readers share, writers exclusive, re-validate what was read before the await), finishing Duffy's design
  (§2). Fallback: one active at a time plus an inbox (KeyKOS, a decade; §3).
- **Parallel execution of independent turns.** Invocations declare read/write sets, which is also the fix
  Broken Metre names for metering (§5). Plan action kinds carry Lean-proved commutation laws (House-style,
  §2). Reed's 1978 pseudo-time gives the correctness definition (§4). No speculation is needed.
- **Cross-domain atomicity is never an implicit two-phase commit** ("Distributed transactions are evil",
  Duffy; Grasshopper; Faré's per-domain atomicity; §2, §3, §F). Use a *purposeful cell* (Naked Objects'
  Transfer, Reed's "possibility"): parties contribute admitted turns; a final execute turn becomes real on
  a commit certificate or times out.

### 4. Persistence and the heap (fork 5)
- **The Host holds nothing not derivable from the root** (KeyKOS, EROS); await index, inboxes and timers
  are cells charged to their requester (seL4 Untyped; §3).
- **Before the root moves, decode and type-check every checkpoint written in the turn.** EROS: "once
  committed, an inconsistent checkpoint lives forever". In Mini it would live forever *replicated*.
- **The codec is a versioned wire format.** On a Core4 machine change, either ship a checked
  `decode_old → encode_new` or drain residents and refuse old checkpoints loudly. L3 and PJama lost their
  stores this way (§3).
- **GC at yield, before encoding, and charge the post-GC encoded delta.** In KeyKOS, half of all dirtied
  state died within one checkpoint interval (§3).
- **Storage as refundable deposits,** not rent: unfunded objects freeze, then evict to their Merkle hash,
  restorable by anyone with the preimage who pays; insolvency is `AwaitsFunding` or a typed abort, never
  deletion (Ethereum rent stalled; Solana dropped it; ICP uninstalls; §5, §4).
- **Plan derived index cells for queries over non-resident data.** Dearle et al. name this as what lost
  orthogonal persistence its market (§G).
- **A replay kit:** packages plus receipts suffice for anyone to re-execute, so the Host is a sequencer,
  not an oracle (§6); block roots are certified and chained (ICP, §4).

### 5. Naming
- **Three kinds of name:** hashes for code and keys (multihash; hash recursive `fix`/mixin groups as one
  unit, as Unison does); SDSI linked local names in a namespace cell per principal (also the human "edge
  names"); per-viewer petnames rendered by the projection.
- **"Which version" is a law-governed pointer cell** (IPNS, git refs). Every reference says whether it pins
  a hash or follows a pointer (Twizzler's foreign-object table; §5, §3).
- **An object's namespace is its caps record:** first-class and transmissible. That fixes Plan 9's admitted
  regret that a name space could only be inherited. Local names follow global conventions.
- **Delegation is checked, not searched.** The client finds the chain; admission checks a compressed
  derivation in linear time (Clarke et al.). Group membership is Datalog-shaped, so it needs a separate
  certified checker whose verdict is a law atom. Validity intervals over heights are already difference
  logic (SPKI's VIntersect).

### 6. Scheduling and metering
- **The unit is Core4 steps from the Lean semantics** (better than Agoric's engine-defined computrons; §4),
  but **steps are necessary, not sufficient.** Broken Metre found EVM gas uncorrelated with CPU time and
  programs over 100× slower per unit of gas than typical ones (§5). So:
  price store reads, forcing, codec work, law checks and Merkle updates by input size, cold; charge
  refused turns outside the atomic turn; gate on a gas-per-time fuzzer and aim for a Lean
  metering-soundness theorem.
- **Meters are capabilities** (KeyKOS meter chain, Agoric Meter, Drexler–Miller expense accounts).
  Subdividable, conserved across forks; exhaustion parks the activity and hands a keeper a resume
  capability. Passive callees run on the caller's meter (seL4 donation); active residents pay their own;
  kernel work is charged to its turn (resource containers).
- **Scheduling.** Use deterministic virtual-finish-time, weighted by funding, never by the number of
  entities ("round-robin is a commons"). No lotteries. Optionally a per-meter rate cap (seL4 MCS). A posted
  price applies only between independent sequencers (Roughgarden; §5).

### 7. Security kernel: laws plus capabilities
- **No ambient authority.** No clock, no global lookup, no caller identity beyond badges. `Cap` is an
  unforgeable Core4 sort (KeyKOS's negative list). Time is an admitted input.
- **Laws stay decidable and are the stable contract across upgrades.** They are Hayden's client-oriented
  specs (§H) and Holochain's integrity zomes (§4). Changing a law is more governed than changing code; it
  bumps the continuity counter and shows on the card.
- **Refusals carry information.** Each one returns its *residual* predicate (SDSI's hint) and is
  three-valued (TRUE / FALSE / FAIL-needs-evidence). A refusal can be routed to a *keeper* cell to
  repair-and-retry (KeyKOS keepers, seL4 timeout handlers; §3). That makes fork 2 rich without making laws
  Turing-complete.
- **One evaluator, no jets (Faré ch. 10, §F):** fast paths are proved refinements of the Lean semantics,
  which favours the `@[csimp]` fast machine over the differentially tested C machine (ORIENT-A's open
  executor choice).
- **Integrity, not confidentiality** (Spectre, §2; unredactable history, §3, §6): secrets never enter
  cells in the clear.

### 8. Upgrade (fork 4)
An upgrade is one admitted turn per object. The *new* code owns the migration (Gall `on-load`, Agoric
`buildRootObject`). Old code never gets a veto: ICP's `pre_upgrade` can brick a canister (§4). The turn
checks:
1. **Types.** If the stable old type is a subtype of the new one, the migration is free (Motoko). Otherwise
   it requires a typed, *linear* migration `Old ⊸ New` (Faré ch. 5) with explicit initialisation of every
   field (Self) and renames distinguished from delete-plus-add.
2. **Interfaces.** The method table is a superset for every exported facet still referenced (Agoric). The
   package's `uses`/`exposes` manifest stays compatible (Fuchsia, Singularity).
3. **The law obligation `law(fwd s)`.** Check it per cell, or once by validity when both laws and `fwd` stay
   in the difference-logic fragment (§6).
4. **A disposition for each activity.** **Drain** on the pinned old package (the default; Erlang's two live
   versions), **Replay** (Agoric asyncFlow; Mini's check is exact over the `(Plan_i, Response_i)` log),
   **Map** (typed resume-point adapters, Kitsune's control migration), or **Abort** (a typed `Upgraded`).
5. **Record the migration chain in the cell** (Motoko); give governance a `simulate` dry run (Faré's
   "virtual fork") and a replay diff over recent receipts (Dark).
6. **Cost scales with types, not heap;** large objects migrate over several turns, closed, or hit Motoko's
   "evolutionary dead end".

### 9. Presentation
Strong agreement. Specify it as a kernel meta-protocol (9P's lesson; Ingalls' Reactive Principle).
- **Every object answers `describe`, `affordances` and `history`.**
- **The Card** = {title, state, fields filtered by authority, affordances, provenance, layout key}.
  - Each affordance is `Hidden`, `Disabled(reason)` or `Enabled` with argument validators. The reason comes
    from authority or from the law's satisfiability check, so the card and admission share one decision.
  - Provenance is the cell, root, package and renderer hashes, plus a Merkle path to a certified root.
- **Projection code is `Activity`-free, so it cannot perform.** Writes happen only through signed
  invocations (Croquet: the view never writes the model), and a renderer may anticipate their result.
- **Renderers are plural and task-shaped** (Constantine; Causeway); per-viewer layout is local-first; cards
  offer `why`/`whynot` (Eve); the meta-card uses a kernel-pinned renderer.
- **"Using is programming" as a ladder:** invoke; customise your view; personal mixin (hash in the signed
  invocation); proposed mixin; fork. Safe because mixins only *propose* Plans (Ink & Switch's unsolved
  problem; §6).

### Agreement and disagreement with the root's model
**Agrees.** Package as a content-addressed cell; code proposes, law disposes; the Plan; residents as paid
turns; the projection.

**Disagrees, or adds:** object identity independent of the package hash; continuation checkpoints not
archival; versioned in-turn reads and exchangeable payloads; Plans with several actions (Core4 now allows
one first-order action per yield) and awaits with joins and deadlines; a payer per cell, deposits and
hibernation; metering that covers kernel work; upgrade as a governed turn with an explicit disposition per
activity, not just "typed migration".

## Where the sources disagree, and how Part I resolves it

1. **The exact whole-machine checkpoint.**
   - *The pushback:* Electric Communities found migrating "save it all" state "effectively intractable"
     (Morningstar 2006, §3). PJama never persisted threads compatibly with evolution, Motoko discards
     continuations on upgrade, and Urbit's authors avoided persistent promises (§3, §4).
   - *On the other side:* the brief says Ember is fine with the checkpoint/heap design, and Agoric
     `asyncFlow` shows suspended activations *can* cross upgrades by replay (§4).
   - *Resolution:* keep the design, but split *durable state* (stable-typed, first-order) from
     *continuation checkpoints* (pinned, epoch-tagged, short-lived, and each given an explicit disposition
     on upgrade). Of every point here, this is the one most likely to be decided wrongly by default.
2. **Lenses vs one-shot migration.**
   - SCHOLAR-OS (§H, Cambria) argued for lenses on cross-version calls. Lane E (§6) argues that permanent
     lenses over authority state keep "two shapes that agree today" alive forever, against the repo's own
     doctrine.
   - *Resolution:* durable state migrates in the upgrade turn (or lazily, on that object's next turn, if it
     follows a pointer cell). Lenses live only at the *interface* boundary for old clients.
3. **Eager vs lazy population migration.**
   - Lane B (PJama, Motoko) wants lazy migration on first touch, with cost proportional to the number of
     types. Lane E (Dark) wants eager migration in the upgrade turn.
   - *Resolution:* upgrades are per object, since each object pins its own package. Objects that follow a
     version pointer cell migrate in their next admitted turn. Large objects migrate over several turns
     with the object closed.
4. **Several activities per object.**
   - Lane B: KeyKOS's one-at-a-time domains plus queues shipped for a decade, and the async-interrupt pain
     is solvable with an inbox.
   - Lane A: Midori's open re-entrancy problem needs declared footprints.
   - *Resolution:* many *suspended* activities; admission by footprints; the inbox model as the
     conservative default.
5. **Transactions.**
   - Faré says "Database Transactions are the wrong Abstraction" and wants atomic sections plus barriers
     (§F). Mini's turn is transaction-shaped.
   - *Resolution (INFERRED):* the programmer never writes begin/commit. The cut points are the yields,
     which communication forces, so a Mini activity *is* Faré's persistent process. Never add a
     user-visible transaction API; add multi-action Plans and purposeful cells instead.
6. **A fixed deterministic VM.**
   - Faré's critique of Urbit (§F) attacks frozen deterministic semantics. He concedes, though, that they
     are needed to "replay and verify other random people's computations", which is exactly Mini's
     admission.
   - *Resolution:* determinism is earned. Freeze only Core4, the Plan vocabulary, the codec and the
     message/timer interface, each with an epoch (wicrum, §4). Allow no jets.

---

# Part II — Annotated bibliography

## §F. Faré's Houyhnhnm computing, its sources, and its critics (read by SCHOLAR-OS directly)

Local sources: `~/dev/fareoo/sources/` (fetched 2026-10-01; each file names its URL) and the connected
account `~/dev/fareoo/FAREOO.md` (itself tagged READ/INFERRED). Where I quote, I quote the source file, not
FAREOO.md, except where noted.

#### F1. Houyhnhnm Computing, ch. 5 "Non-Stop Change" — upgrade as a first-class, typed, linear transaction
- **Cite:** Rideau, F.-R. (2015). *Chapter 5: Non-Stop Change*. Houyhnhnm Computing blog. https://ngnghm.github.io/blog/2015/09/08/chapter-5-non-stop-change/ . Local: `~/dev/fareoo/sources/houyhnhnm-ch05.md`. **[READ, in full]**
- **OS-level decisions:** Code and data are saved *together*, so "you can simply fork the old data together with the correct version of the code that knows how to create and manipulate it" — "computation itself is immortal". Upgrades are "transactions for code and data upgrade, that can be composed and applied atomically"; "each change is always run in its own virtual fork of the system, where failure is quite acceptable"; the type system "maintain[s] for the programmer a to-do list for those parts of the system that haven't been updated"; every type change carries "a well-typed upgrade function, taking an object in the old type and returning an object in the new type"; "linear logic to ensure that ... you must explicitly drop any data that you don't care about anymore"; upgrade functions "can be overridden at the granularity of individual variables"; renames are tracked as distinct from delete+add; releases follow an *effective* history (coherent upgrade steps) not the *actual* history; histories merge in "a monotonic algebra". Representation-only changes upgrade by "decompile and recompile".
- **Evidence:** None empirical; it is a design essay. Its two cited human precedents are Common Lisp (`update-instance-for-redefined-class`, with "no automated enforcement of consistency between such methods and the types") and Erlang ("it is always clearly defined which function calls will go to the old version of the code").
- **Critiques:** It is unimplemented (Faré himself, ch. 10: "no implementation of Houyhnhnm Computing system is available"). HN, 2016 (thread https://news.ycombinator.com/item?id=11797718, read via Scry): JulianMorrison argues transience "allows us to be wrong" and that a one-world component platform (cf. Taligent/OpenDoc) "can only tolerate tyranny" — a real objection to "platforms, not applications" when components disagree on data models. **[READ]**
- **Lesson for Mini (fork 4, fork 5):** This chapter is the spec for Mini's upgrade subsystem and it is more demanding than "governed upgrade with typed migration". Concretely: (a) an upgrade is a *package-to-package transaction* `P1 → P2` carrying a migration function per changed type, checked by the certifying type checker; (b) migration must be *linear*: Core4 data dropped by the migration is dropped by an explicit `drop` the checker can see (a total function `Old → New` silently forgets fields; demand `Old ⊸ New × Dropped` or an explicit discard list in the migration's type); (c) it is run *in a fork* first — Mini can do this for free, because admission is re-execution: run the migration against the current Merkle root as a dry turn, have every affected cell's law judge the result, and report the to-do list (cells whose state did not migrate, activities parked in old code) before committing; (d) renames are first-class edits, not diffs. AGREES with the root's fork 4, but says the migration is the easy half: the hard half is *activities* parked in old code (see F6/E4 below, and Kitsune/Erlang).

#### F2. Houyhnhnm Computing, ch. 10 "Houyhnhnms vs Martians" — the critique of Urbit, and of fixed deterministic VMs
- **Cite:** Rideau, F.-R. (2016). *Chapter 10: Houyhnhnms vs Martians*. https://ngnghm.github.io/blog/2016/06/11/chapter-10-houyhnhnms-vs-martians/ . Local: `~/dev/fareoo/sources/houyhnhnm-ch10.md`. **[READ, in full]**
- **OS-level decisions criticised:** Urbit's single, frozen, low-level persistence mechanism ("Martians provide a single mechanism for persistence at a very low-level"); a VM (Nock) "forever fixed" and the jets that reimplement it ("you must implement things twice ... And how do you ensure the equivalence ... You can fail to, or lie, and then Urbit is all a sham"; the Markdown jet "not bug compatible, so it's all a lie"); resource use "all defined and hidden in u3, out of sight and out of control"; the runtime dropping events that time out (a DoS vector he names); a centralized, informal metasystem (u3) "not actually bound to behave as a faithful implementation".
- **The key concession:** "A global consensus on deterministic computation semantics only matters if you want to replay and verify other random people's computations, i.e. for crypto-currencies with 'smart contracts' like Ethereum ... such computation replay in a hostile environment indeed has issues of its own (such as misincentives, or resource abuse)". And the fix he names: "if only you had an advanced metaprogramming infrastructure capable of manipulating arbitrary program semantics in a formally correct way! You might then automatically generate both the Nock code ... and the supporting u3 code ... and be confident they are equivalent."
- **Lesson for Mini (security kernel, metering, fork 5):** Mini is *exactly* in the case Faré concedes needs a global deterministic semantics: multi-party admission by re-execution is replaying "other random people's computations" in a hostile environment. So the determinism is earned, not dogma — but his two warnings land squarely: (1) **No jets.** Any fast path that is not the Lean-defined Core4 semantics (a Rust interpreter, a native "accelerator" for a hot method) is the Urbit sham unless it is generated from, or proven against, the Lean definition. The repo's own "ZERO Rust-authored AIRs / Lean must be the implementation" law is the same rule; extend it explicitly to *execution*: there is one evaluator, the Lean one (compiled), and optimisations are verified refinements of it, never twins. (2) **Resource use must be in the semantics.** Faré's complaint that Nock hides time and memory is answered in Mini only if fuel (`runBounded`) and storage are *part of the admitted semantics* — counted by the evaluator that admits, priced in the Plan, visible to the program — not a runtime-side timeout. A turn that times out must be a *deterministic, admitted refusal with a charged fee*, not a dropped event (Urbit's u3 drops it, which he calls a DoS). (3) "Future-proofing the wrong thing": a frozen kernel is a bug; Mini's Core4 must itself be upgradable by a governed kernel-epoch transaction (re-genesis is the degenerate form).

#### F3. Houyhnhnm Computing, ch. 8 "Inter-process Communication" — presentation and servers belong to the meta-level
- **Cite:** Rideau, F.-R. (2016). *Chapter 8: Inter-process Communication*. https://ngnghm.github.io/blog/2016/01/03/chapter-8-inter-process-communication/. Local: `~/dev/fareoo/sources/houyhnhnm-ch08.md`. **[READ, in full]**
- **OS-level decisions:** "presenting data to the end-user is the job of a meta-program separate from the activity that displays the data"; clips "include source domain information, so that the user can't unintentionally paste sensitive data into untrusted activities"; typed composition "of programs of arbitrary types, with arbitrary numbers of inputs and outputs"; servers move "completely to a separate meta-program that controls the process you communicate with; thus the base-level process can be written as a simple program"; "persistence ... means you can give a stable name to a stable activity"; sandboxing by full abstraction — "There is no supported way for code to distinguish between 'normal' and 'virtualized' machines"; "metaprogramming requires free availability of sources".
- **Lesson for Mini (presentation, fork 1):** Strong AGREEMENT with the root's "Presentation = a projection": the card is not drawn by the object; a meta-level renderer derives it from the object's type, its authorized view, and its affordances. Two concrete additions: (a) every projected datum should carry its *source domain/provenance* (which cell, under which law, at which root) so that copy-out/paste-in between domains is a checked, law-judged act, not a string copy; (b) residents should not contain "server loops": an object's methods are *exported functions*, and the Host (meta-level) is the server that receives invocations and turns them into admitted turns. That is already the root's model; ch. 8 is the argument for keeping it and refusing per-object event loops. Also: because packages are published source + checked core, Mini already satisfies "free availability of sources" for the meta-level — keep the source in the package cell, not just the core.

#### F4. Orthogonal Persistence, The Model (2024 reframing; LambdaConf 2025)
- **Cite:** Rideau, F.-R. (2024/2025). *Orthogonal Persistence, The Model* (gerbil-persist `persist.md`). https://github.com/mighty-gerbils/gerbil-persist/blob/master/persist.md ; slides: Rideau (2025), *Orthogonal Persistence: the Model*, LambdaConf 2025, http://fare.tunes.org/files/cs/persist/slides-2025-lambdaconf.html . Local: `~/dev/fareoo/sources/persist-model.md`, `~/dev/fareoo/sources/persist-slides-2025.md`. **[READ, in full]**
- **OS-level decisions:** Persistence *of processes* ("Durable Execution"); the remaining issues are "persistence domains, atomicity, synchronization, publishing, resource exhaustion and schema upgrade". *Domains*: logical persistent identities mapped onto substrates; "atomicity is specific to a given persistence domain. Changes across multiple persistence domains are not atomic by default" and need "common management" or "some costly consensus protocol". *Atomicity* by *atomic sections* ("don't cut the computation here", local knowledge, composable) instead of transactions ("cut the computation exactly here", global knowledge, "Don't Compose, Always too small or too big"). *Synchronization* by memory barriers: "every asynchronous message sent to a persistent process must (1) be idempotent, and (2) can only be sent after a memory barrier"; output effects are queued until commit. *Publishing* = tagging a version + granting a capability. *Resource exhaustion*: per-domain quotas; "processes are stopped when they run out of space, and can be resumed after space issues are solved; space is reserved so special debugging processes can run inside the scope of a stopped process". *Schema upgrade* is ordinary development. Two implementation routes: low-level (VM snapshots, e.g. Golem) or high-level ("Continuation-Passing Style will make stack frames into objects; lambda-lifting will make lexical scope into objects; various explicit monads will make the context of as many effects into objects"). Long-range issues: persistent corruption, static languages make schema upgrade "hell", reflection needs capabilities, "Forms of PCLSRing with respect to *user* invariants ... are necessary to cleanly kill processes, but also to stop, inspect, migrate, upgrade them".
- **Lesson for Mini (forks 3, 5, metering):** Mini already *is* Faré's high-level route: Core4's exact checkpoint codec of the whole machine state is "persisting continuations", and `Activity<P,R,A>` is "explicit monads make the context of effects into objects". Four specific pushes: (1) **A Mini turn is an atomic section, a yield is a memory barrier.** The root's "each resume is one admitted turn" matches Faré's model precisely if the Plan's outbound messages are released only after the turn commits (barrier) and are *idempotent by construction* (each carries the turn id; receivers dedupe). Make both kernel invariants, not conventions. (2) **Domains are the unit of atomicity.** Mini's "committee domain" (Simplex mesh) is a persistence domain; atomicity across two domains is not free and should be an explicit, separately-priced protocol (escrow/2PC/HTLC-style), never implied by a cross-domain call — this pushes fork 3's "multi-party atomicity across domains" to be a *library protocol over async messages* with typed outcomes, and the same-domain case to be the cheap default. (3) **Resource exhaustion = stop, don't kill.** A resident that exhausts its storage or fuel budget should be *suspended at its last checkpoint* with a reserve so a debugging/owner turn can inspect, GC, top up and resume — not destroyed. (4) **Faré is against transactions as the programmer's unit**; Mini's whole turn is transaction-shaped. The reconciliation (INFERRED): in Mini the programmer never writes "begin/commit"; the cut points are the *yields*, which are forced by communication, so a Mini activity reads as Faré's persistent process whose atomic sections are "everything between yields". Keep it that way — do not add a user-visible transaction API; add atomic multi-object Plans instead.

#### F5. Climbing Up the Semantic Tower — at Runtime / First-Class Implementations
- **Cite:** Rideau, F.-R. (2018). *Climbing Up the Semantic Tower — at Runtime*. Off the Beaten Track @ POPL 2018; arXiv:2606.04034 (2026). https://fare.tunes.org/files/climbing/climbing.html . Local: `~/dev/fareoo/sources/climbing.md`; companion: Rideau (2017) *First-Class Implementations*, `~/dev/fareoo/sources/fci2017.md`. **[READ climbing in full; fci via FAREOO §8 quotes — SKIMMED]**
- **Content:** Implementations are partial functors from concrete to abstract computations; properties: sound (functoriality), complete, live, *observable* ("an observable abstract state can be recovered given any intermediate state at which the concrete computation is interrupted"). Constructive proofs of these yield a runtime protocol (`observe`, etc.). "Recovering an abstractly observable safe point also enables safely killing threads and upgrading code"; orthogonal persistence, access control, time-travel debugging are "natural transformations of implementations". Effects should be first-class ("simulate" vs "perform"); "achieving simulate requires rewriting the entire system if the existing implementation does not offer a suitable reflection protocol". Status: "The ideas above remain largely unimplemented."
- **Lesson for Mini (forks 4, 5, security kernel):** Mini has, by construction, most of what Faré says is missing: Lean adequacy is his soundness; the checkpoint codec gives observability *at Core4 level*. The gap is observability *at the Objective Bend level*: a checkpoint taken mid-step is a Core4 state, not an `.obend`-meaningful state. **Define the safe points**: the yields of an activity are the only observable abstract states, and upgrade/migration/kill/inspect operate only there (this is PCLSRing, F6). And since `Activity` makes effects data, Mini can offer *simulate*: run a turn against a Plan interpreter that does not perform — which is exactly the dry-run fork F1(c) wants. Build: a `simulate` admission mode that returns the Plan and every law verdict without committing.

#### F6. PCLSRing: Keeping Process State Modular
- **Cite:** Bawden, A. (1989). *PCLSRing: Keeping Process State Modular*. MIT AI Lab working paper; hosted at http://fare.tunes.org/tmp/emergent/pclsr.htm . Local: `~/dev/fareoo/sources/pclsring-bawden.md`. **[READ, §§1-5]**
- **Content:** ITS's rule that "no process ever catches another process (including itself) in the act of executing a system call"; interrupted calls are backed out with their arguments "updated in place to reflect any work already accomplished", so a restart continues; system calls "may not run indefinitely without presenting opportunities to be PCLSRed".
- **Lesson for Mini (fork 3, fork 5):** Mini's atomic turns give PCLSRing for free at the turn boundary — no observer (another object, a renderer, an upgrade) ever sees an object mid-turn. Keep the third rule too: a long computation must yield (or be fuel-bounded) so that it presents safe points; a method that cannot finish in one fuel budget should be expressed as an activity with progress-carrying yields (ITS's updated-arguments trick = the activity's typed state at each yield). INFERRED.

---

## §2. Language-based operating systems (reading lane A)

Scope: systems that put isolation, communication and evolution inside a language and its checker instead of (or beside) MMU hardware. Read for Mini's five forks: (1) calls across objects, (2) laws and contracts, (3) concurrency, (4) evolution, (5) checkpoints and heap. Every paperbin path below is under `~/paperbin/world-program-model/`; each `.pdf` has a `pdftotext -layout` `.txt` beside it, and each blog post is saved as `.html` plus `.txt`.

Reading depth, stated plainly: the five mandatory groups (Singularity ×3, Midori, Theseus, RedLeaf, Tock) were READ from the full text. The rest were read in targeted sections, and each entry's tag says which. A Kagi miss at the start of the lane cost 2 queries, and 5 more were made after, for 7 in all. Two Scry queries pulled Hacker News critiques.

---

#### Singularity (system) — an OS built from software-isolated processes, contract channels and manifests
- **Cite:** Hunt, G. C. & Larus, J. R. (2007). *Singularity: Rethinking the Software Stack*. ACM SIGOPS OSR 41(2). https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osr2007_rethinkingsoftwarestack.pdf. Local: `hunt-singularity-rethinking-2007.pdf`. **[READ]**
- **OS-level decisions:**
  - *Process model.* A Software-Isolated Process (SIP) is a "closed object space". Code inside it is sealed: no dynamic loading and no code generation. Each SIP has its own runtime and its own GC, picked per SIP from 5 collectors.
  - *Isolation.* Type and memory safety, checked by the MSIL verifier plus an ownership checker, does the job that page tables normally do. Kernel and SIPs can share one ring-0 address space.
  - *Communication.* Channels are the only path between SIPs. A channel is bidirectional with exactly two endpoints (Imp/Exp), lossless and in order, and is governed by a *contract*: message declarations plus a finite-state protocol.
  - *Endpoints are capabilities.* A SIP gets one only from its manifest at start, or inside a message.
  - *Memory independence invariant.* A pointer may target only the SIP's own heap or exchange-heap blocks that the SIP owns. That is what makes per-SIP GC and kill-without-cooperation possible.
  - *Kernel ABI.* 192 functions, strongly versioned. No ioctl-style calls. No ABI call can change another process's state, the "state isolation invariant".
  - *Manifest-Based Programs.* No code runs without a manifest. The manifest declares the code, the resources and capabilities needed, dependencies, and the channel contracts used. It is checked at install time: type safety, no privileged instructions, conformance to contracts, use of declared contracts only, ABI version. Code is compiled to native at install, not by a JIT.
  - *Principals.* A principal is the application identity taken from the signed manifest, plus an optional role and a delegation chain. A "user" is a role that an application runs in.
  - *Scheduling.* Two FIFO lists (unblocked and preempted). A thread woken by a message inherits the waker's quantum, which allows a 394-cycle switch between SIPs.
  - *Reflection.* Runtime reflection is replaced by *compile-time reflection* (pattern/template "transforms" applied at compile or install time). The authors' stated reason is that runtime reflection "can be used to circumvent system security and information-hiding".
- **Evidence:**
  - Table 1: API call 80 cycles (FreeBSD 878, Linux 437, Windows 627). Message ping/pong 1,040 (FreeBSD 13,300, Linux 5,800, Windows 6,340). Process creation 388K cycles vs 1.03M / 719K / 5.38M.
  - *Unsafe code tax* (WebFiles, Fig. 5). Turning on 4 KB paging costs +6.3%. A separate ring-0 domain costs +18.9%, ring 3 +33%, a full microkernel layout +37.7%. Run-time safety checks cost under 5%.
  - The contract verifier, once it came online, flagged within seconds a NO_DATA protocol bug that had lived in the web server for about a year.
  - Over 90% of the kernel is Sing#. The GC is 48% of the unsafe code, and about 6% of the kernel is C++.
- **What failed / critiques:**
  - The authors gave up compatibility and had to "rewrite or port every line of code".
  - Their TCB includes the large optimizing Bartok compiler and the unsafe GCs. They were moving toward typed assembly language (TAL) and a verified GC to shrink it.
  - Practitioner critique (HN 33575904, origin_path, 2022) argues that single-address-space OSes end up re-creating a process-like unit anyway. The commenter asks what plays the role of SIGKILL, of a CPU graph, and of a deadlocked driver callback, and calls the exchange heap a "convoluted ... quasi-RPC approach".
  - The project never shipped. HN commenters (pjmlp, 43183187 and 46002332) blame leadership and politics rather than technology.
- **Lesson for Mini (forks 1, 2, 4, security kernel):**
  - Singularity's three pillars map almost one to one onto Mini. SIP = object, contract channel = cross-object call, manifest = package. This **agrees** with the proposed model.
  - What Singularity adds that Mini lacks: (a) a *manifest* on each package listing the capabilities and contracts it uses. This makes a package's effect footprint statically checkable at publish time, for example "this package can never emit a `Transfer`". (b) The state isolation invariant as a hard kernel law: the only way to change another cell is a Plan action that the target's law judges, never a kernel primitive.
  - Cost: one manifest schema plus a publish-time checker over checked Core4. That is cheap, because Core4 already has a certifying type checker.

#### Sing# channels and the exchange heap — session-typed IPC with zero-copy ownership transfer
- **Cite:** Fähndrich, M., Aiken, M., Hawblitzel, C., Hodson, O., Hunt, G., Larus, J. R. & Levi, S. (2006). *Language Support for Fast and Reliable Message-based Communication in Singularity OS*. EuroSys 2006, 177–190. https://www.microsoft.com/en-us/research/wp-content/uploads/2006/04/singsharp.pdf. Local: `fahndrich-singularity-channels-2006.pdf`. **[READ]**
- **OS-level decisions:**
  - *Contracts.* A contract is a state machine over messages, with direction signs (`!` from the exporting side Exp, `?` from the importing side Imp). The paper states that it has "the same expressive power" as session types (Gay et al.).
  - *What the compiler checks.* That every send is legal in the endpoint's current protocol state, and that every `switch receive` is exhaustive.
  - *Finiteness rule.* Every cycle in a contract's state graph must contain at least one send and at least one receive. That bounds every queue, so endpoint buffers are laid out up front and **send and receive never allocate**.
  - *Failure semantics.* Sends are non-blocking and never fail. Failure is seen *only on receive*, as an implicit `ChannelClosed` message.
  - *Moving endpoints.* An endpoint may be sent only while it is in a "send state", where its next operation is a send. This rules out, statically, the race where the endpoint's owner changes while a message is in flight to it.
  - *Exchange heap.* It holds "exchangeable types" only: scalars, rep structs, and pointers into the exchange heap itself. Ownership is linear ("tracked pointers"), and `[Claims]` marks a parameter whose ownership transfers for good.
  - *Escape hatch.* `TCell` turns static ownership into dynamic checks. `expose` blocks open one struct field or vector slot at a time.
  - *Joins.* `switch receive` takes conjunctions of patterns across several endpoints, which is join-calculus-like. Endpoint sets and maps let one thread wait on an unbounded number of clients.
- **Evidence:**
  - In use for 8 months at writing: 43 contracts, about 500 messages, 135 protocol states.
  - 146 messages carry exchange-heap pointers and 42 carry endpoints. "The ability to configure the communication network dynamically by transferring endpoints is quite important."
  - The cost of sending a block is flat at about 1,200 cycles from 1 B to 64 KB. Linux and Windows rise past 1 KB.
  - Cross-process message ping/pong is only about 15% slower than a thread wait-set ping/pong inside one process.
  - Two redundant ownership verifiers run, one on source and one on MSIL, to catch bugs in the verification itself.
- **What failed / critiques:**
  - "One serious shortcoming": *exceptional paths were not checked*, because the code carried no exception specifications.
  - No read-only sharing ("one of its main drawbacks").
  - Deadlock prevention, cross-machine channels and contract inheritance were all listed as future work. Cross-machine was sketched as generated proxies that check the protocol dynamically.
  - In the Sealing paper's SPECweb99 run, `switch receive` dispatch costs 16.6% of CPU, with a minimum overhead of about 1,600 cycles.
- **Lesson for Mini (fork 1, fork 2, fork 3, metering):**
  - **The contract of a channel is a law.** Make a channel a cell, or a capability stored in one. Its law is the finite-state protocol, which is a decidable predicate of a different shape from difference logic but entirely in the spirit of "law judges every write".
  - Each Plan `Send` is admitted only if it is legal in the endpoint's current protocol state. Separately, the certifying checker statically proves that an activity's code conforms, as Sing#'s compiler does. That gives two independent checks, matching Singularity's two verifiers.
  - Adopt the **finiteness rule** as the metering rule: a contract with a send-and-receive in every cycle has a bounded mailbox, so its storage can be *prepaid at channel creation*. That suits "storage charged" in fork 5.
  - Adopt **failure-on-receive-only**: a resident that emits a Plan never sees a refusal at send time. Refusals (the explanations from laws), peer upgrade and peer deletion all arrive as typed messages at the awaiting activity, like `ChannelClosed`. **Put the refusal messages into the contract itself.** That fixes the hole Singularity never closed: exceptional paths left outside the protocol.
  - Generalise a resident's "what it awaits" to a **join pattern over several endpoints**. Today the brief names a single reply, message, or time. `switch receive` with conjunctions and endpoint sets is the existence proof, and the matrix-based compilation is cheap.
  - The exchange-heap rule becomes, for Mini: **Plan payloads must be an "exchangeable" type**. That means forced first-order Core4 data, cell and capability references, and linear assets — **no thunks and no closures over the sender's heap**. In a lazy machine an unforced thunk is precisely "a pointer into a private heap". That is INFERRED, but direct.

#### Sealed processes — a process whose code is fixed at start and whose state no one else touches
- **Cite:** Hunt, G., Aiken, M., Fähndrich, M., Hawblitzel, C., Hodson, O., Larus, J., Levi, S., Steensgaard, B., Tarditi, D. & Wobber, T. (2007). *Sealing OS Processes to Improve Dependability and Safety*. EuroSys 2007. https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/EuroSys2007_SealedProcesses.pdf. Local: `hunt-sealing-processes-2007.pdf`. **[READ]**
- **OS-level decisions:**
  - *Four invariants.* Fixed code; state isolation; explicit communication, with an identified sender and admission control by the receiver; and a closed API.
  - *Extensions.* An extension always runs as a *child process* that receives channel endpoints at creation.
  - *Identity.* Because all code is known before execution, a process's identity can be checked against its publisher's certificate. The principal is user + program + publisher.
  - *Interpreters.* They remain allowed: "the interpreted program just invokes code that is part of the process."
  - *Debuggers.* They are privileged exceptions. The authors suggest production systems drop them or make them read-only.
- **Evidence:**
  - Tree-shaking, sound only because code is sealed, cuts code size: kernel 46%, web server 72%, SPECweb plug-in 77%, IDE driver 75%.
  - Removing the CLR's code-access-security machinery shrank `mscorlib.dll` by 30%. The authors present that machinery as a cost paid only because processes are open.
  - Moving Bartok's register allocator into a child SIP cost +10.9% (215.9 vs 194.7 billion cycles), with marshalling of median 2,400 objects (85 KB) per call. Code change was under 0.25%.
  - Extending the Cassini web server took +26% code: 263 lines of IPC, 52 of contract, 76 of extension stub.
  - SPECweb99: Singularity sustained 244 connections vs Windows/IIS 519 (Singularity CPU-bound, Windows disk-bound), with average response time within 5%.
  - IPC cost is flat at about 920–940 cycles from 4 B to 64 KB. Linux goes from 5.5K to 88K cycles and Windows from 6.6K to 187K.
- **What failed / critiques:**
  - The authors' own limits: no JIT and no inline regular-expression compilation, since code generation must go to a new process. Sharing libraries conflicts with per-process optimisation. Hosts must design real interfaces. Resource accounting is harder when servers multiplex clients.
  - Macrobenchmark throughput was half of Windows.
- **Lesson for Mini (fork 4, naming, security kernel):**
  - **Mini's pinned package hash *is* a sealed process.** This strongly **agrees** with the model. Three consequences follow.
  - (a) *Code-identity principals.* A law, or a capability check, may name the *package hash* of the calling object. For example, "only objects running package P may call `settle`". Singularity's principal = program + publisher shows the pattern. Cost: expose `caller.package` to the law language.
  - (b) *Reflection must not break the seal.* Core4 has reflection. It must be unable to install new code into a live object. New code arrives only by publishing a package cell and then creating an object or running a governed upgrade. Interpreting data as code stays legal, as the paper says, because the law still judges every effect.
  - (c) *Upgrade = re-seal.* Singularity has no in-place evolution. Mini must define upgrade as a governed transition that swaps the pinned hash and gives the object a new identity epoch. Theseus supplies the mechanics.
  - The +11% / +26% figures are also a warning for fork 1: forcing everything across an explicit boundary costs code and marshalling, so make the *in-turn pure call* (read only, no Plan) cheap and copy-free.

#### Midori — Duffy's account of a capability, async-everything, language-based OS
- **Cite:** Duffy, J. (2015–2016). Blog series on Midori. joeduffyblog.com. Read in full: "A Tale of Three Safeties" (2015-11-03), "Objects as Secure Capabilities" (2015-11-10), "Asynchronous Everything" (2015-11-19), "The Error Model" (2016-02-07). Read in sections (permission/ownership model, message-passing races, evolution, inspirations): "15 Years of Concurrency" (2016-11-30). Skimmed by search: "Safe Native Code" (2015-12-19). Downloaded but not read: "Performance Culture" (2016-04-10). URLs: http://joeduffyblog.com/2015/11/03/blogging-about-midori/ and the linked posts. Local: `duffy-midori-*.html/.txt`. **[READ for the four posts named; SKIMMED for the rest]**
- **OS-level decisions:**
  - *Three safeties* (memory, type, concurrency), with a small encapsulated unsafe TCB. The scheduler and memory manager are written in safe code. The compiler is part of the TCB.
  - *Capabilities are objects.* Object references are unforgeable. **No mutable statics** at all, so a capability cannot be cached in a global. **No ambient time**: you need a `Clock` capability. As a result, a function with no IO is pure, memoizable and evaluable at compile time. Revocation works by handing out a wrapping subclass. Casting is restricted, because a downcast breaks the encapsulation a capability depends on.
  - *Eventual vs prompt capabilities.* Most capabilities are "eventual": async references to objects in another process. A few are "prompt", such as Clock, which wraps a syscall.
  - *Async everything.* Synchronous blocking is "flat-out disallowed", and there is no demand paging. The type system gives `T`, `Async<T>`, `Result<T>` and `AsyncResult<T>`. Each process is single-threaded with an event loop, and **each iteration is a "turn"**. Interleaving happens *only at await points*. One chain of async calls is an **"activity"**, which allocates once ("async could cost something, but await was free") and runs on linked stacks of 128 B to 8 KB.
  - *Messaging.* Marshalable types are primitives, PODs, stream references, references to async objects, and `SharedData` (immutable, refcounted, in a kernel-managed shared heap). Message passing is lock-free and user-mode. It uses **pipelining** and **three-party handoff** to cut out middlemen.
  - *Error model.* **Bugs → abandonment.** The whole lightweight process is torn down, with no user code run, on cast/null/bounds errors, overflow, OOM, stack overflow, and contract or assertion failure. **Recoverable errors** are typed exceptions declared in the signature (`throws`), with a mandatory `try` at each call site so that control flow stays visible. Other pieces: `Result<T>` for dataflow-style errors; `requires`/`ensures` contracts that are part of the signature and *always checked*, elided only when the compiler proves them; undeniable "aborts" that can be reset only by presenting a capability token; and "keepers", which are recovery capabilities consulted in place instead of unwinding.
  - *Concurrency (15 Years).* Reference permissions `mutable`/`readonly`/`immutable` plus the ownership mode `isolated`, published at OOPSLA'12. An isolated graph can be frozen into an immutable one or sent by reference without copying. A "vat", a sub-process actor, turned out to be "really just an isolated bubble of state".
- **Evidence:**
  - An entire OS (kernel, drivers, filesystem, network stack, browser, multimedia, compiler) written in the safe model.
  - Exceptions beat return codes by 7% in code size and 4% in speed (geomean).
  - Abandonment outnumbered recoverable errors by about 10:1. About 90% of the uses of exceptions in .NET would have been preconditions. About 90% of contracts were nullability or range checks.
  - The best available theorem prover took "over a day" on the core system module, so contracts were checked at runtime and optimised by compiler range analysis instead.
  - Millions of lines were converted from callbacks to async/await.
  - Per an HN comment (46002332, pjmlp, 2025) quoting Microsoft Research's project page, Midori at one point served Microsoft's natural-language search for the West Coast and Asia.
- **What failed / critiques, per Duffy himself:**
  - *State management across awaits*: reentrancy and TOCTOU. "Saying that message passing systems don't have race conditions is an outright lie." His fix, permissions on asynchronous activities, was unfinished.
  - *Resource management*: async-everything removes the natural throttle that blocking provides, producing fork-bomb-like floods. He calls it "solved to my least satisfaction". The most promising experiments priced every system resource in a market.
  - *Distributed transactions*: "we didn't go there. Distributed transactions are evil."
  - *Ordering*: "distributed systems are unordered. ... Don't fight it."
  - Non-null types and invariants were never deployed. The cause was a C#-compatibility mindset, and Duffy calls the late arrival of non-null types one of his biggest regrets.
  - The permission system's "sheer permutations ... could be overwhelming".
  - Practitioner critiques: "mostly just a PL nerdout" that spent its design budget turning C# into C++ (HN 33575904). Killed by leadership rather than technology (HN 43183187).
- **Lesson for Mini (forks 1, 2, 3; metering):**
  - *Fork 1.* Midori's **prompt/eventual split is exactly the root's lean**: reads and pure calls are prompt and in-turn, effects go via the Plan, and messages between residents are eventual. It **agrees**. Build two more things on top of it:
    - **promise pipelining**: send to the *result* of an outstanding call, so the Plan can name a not-yet-resolved reply;
    - **three-party handoff**: pass a capability to a third resident without routing replies back through the middle. Both matter more across BFT domains, where every round trip is a consensus delay.
  - *Fork 3.* Mini's "turn" and "activity" are Midori's words for the same mechanism, so **Midori's open problem is Mini's**. When a resident awaits and another invocation on the same object runs, the invariants seen before the await can be stale. Concrete design, INFERRED from Duffy's unfinished plan:
    - each activity declares a **state footprint**: the fields or cells it reads or writes across awaits;
    - the kernel admits another invocation on the object only if its footprint is compatible, with readers sharing and writers exclusive;
    - an activity that read field *f* before an await gets a re-validation obligation on *f* after resuming, expressed as a law on the resume.
    This is deterministic and decidable, and it serves "several activities per object" without locks. Default to Duffy's ranking: *isolation first* (one activity per sub-object or session), *then* reader/writer dispatch, and *never* cross-domain distributed transactions as the default. Multi-party atomicity should be an escrow or commit protocol *expressed as contracts*, not a hidden two-phase commit.
  - *Fork 2.*
    - Make **contracts part of the method signature and always checked at admission**, with the certifying checker free to discharge them statically. That is Midori's final policy, and it fits Mini's decidable law fragment exactly. Note that difference logic covers the 90% "range" class.
    - Map **abandonment = refused turn**: Mini's atomic turns are a *stronger* abandonment, since there is nothing to tear down.
    - Make **law refusals typed recoverable errors** that callers must `try`, so they cannot be silently dropped. Midori made an ignored return value a compile error.
    - **Effect-polymorphic signatures** (`effect E`, which Midori designed but never shipped) are what Activity<P,R,A> already gives.
  - *Metering.* Mini's paid turns are the market allocation Duffy found most promising. Add the self-control knob he resorted to as well: Plans and activities should declare **maximum outstanding sends** (his "wide loops"). Otherwise one resident's fan-out floods a domain.
  - **Cancellation** should be a capability that crosses objects and domains, as Midori's CancellationToken was rebuilt atop messaging, revoking whole async objects.

#### Theseus — an OS of many tiny "cells" built to minimise state spill and allow live evolution
- **Cite:** Boos, K., Liyanage, N., Ijaz, R. & Zhong, L. (2020). *Theseus: an Experiment in Operating System Structure and State Management*. OSDI 2020. https://www.usenix.org/system/files/osdi20-boos.pdf. Local: `boos-theseus-2020.pdf`. **[READ]**
- **OS-level decisions:**
  - *State spill* is defined as one component holding changed state, caused by another component's interaction, that its future correctness depends on. It produces fate sharing.
  - *Cells.* One Rust crate = one object file = one loaded set of sections. Cells have runtime-persistent bounds and bidirectional per-section dependency metadata. Everything runs in one address space at one privilege level, matching the compiler's runtime model.
  - *Intralingual design.* OS invariants are expressed in types: `MappedPages` with drop handlers, and task spawn typed by `<F,A,R>`. Interfaces must be *lossless*, so type, lifetime and ownership survive the crossing.
  - *Opaque exportation.* The **client owns the state representing its progress** with a server, as an object of a server-defined type it cannot look inside. The server keeps no handle tables.
  - *Stateless communication.* Each request carries everything it needs.
  - *Soft state* (caches) is allowed. The unavoidable rest (hardware tables, interrupt context) goes into `state_db` and is serialised when `state_db` itself is swapped.
  - *Live evolution by cell swapping*, in four steps:
    1. load the new cells into an isolated `CellNamespace`;
    2. check dependencies in both directions;
    3. rewrite relocations and on-stack references and transfer state;
    4. swap atomically.
    State transfer functions are written by hand in the language, as `Into` conversions. Generating them is listed as "ongoing work".
  - *Fault recovery* escalates through three stages: unwind the task; restart it (allowed only if its entry function is `Fn + Clone`); reload the corrupted cells.
- **Evidence:**
  - About 38K lines of Rust, 72 `unsafe` sites in 21 crates.
  - Live-evolved its IPC from synchronous rendezvous to async buffered channels *while messages were in flight*, with median downtime 385 µs. Also swapped round-robin for a priority scheduler, and upgraded an Ethernet driver together with the update client.
  - Fault injection: 800,000 injected faults, of which 665 showed up as failures. It recovered from 69%. Of the 13 deterministic IPC-layer faults, it recovered 11, while MINIX 3 recovered 0 (its kernel crashed in 11).
  - LMBench-style microbenchmarks beat Linux, e.g. 1-byte async IPC round trip 1.06 µs vs 3.65 µs.
  - A safe heap costs up to 22.5% over an unsafe one.
- **What failed / critiques:**
  - 31% of manifested faults went unrecovered, mainly because Rust/LLVM lacks *asynchronous* unwinding tables.
  - Fully spill-free filesystem semantics would break POSIX, so the FS cells keep spill.
  - It still must trust rustc.
  - Asterinas (2025) counts unsafe use in 32% of Theseus's crates.
  - HN (37357785) argues that bolting on a compatibility layer would defeat the intralingual validation.
- **Lesson for Mini (forks 4, 5, 1):**
  - **Suspended activities are Mini's biggest state-spill hazard for upgrade.** A checkpointed resident holds a continuation of the *old* code: it is a "stack" that cell swapping would have to rewrite. Theseus's answer is to make components quiescent and stateless across interactions. Translated (INFERRED):
    - (a) **design residents so a checkpoint is first-order data plus a named yield point** (a defunctionalised continuation), not a heap of thunks closing over old code. Then a typed migration function `(oldYieldPoint, oldLocals) -> (newYieldPoint, newLocals)` can be written and checked, the analogue of Theseus's `Into`-based transfer;
    - (b) upgrade is admitted only when every suspended activity is at a yield point the migration covers. Otherwise the activity is drained or explicitly abandoned, with its awaiters notified;
    - (c) mark **soft fields** in the object's law (caches that migration may drop);
    - (d) run Theseus's step-2 check in both directions at upgrade-admission time: the new package must satisfy every contract the object's live channels are in, and every capability the new code needs must already be held.
  - **Opaque exportation is a pattern for services in Mini.** A service object should not keep a per-client table. The *client* holds a linear, service-typed, opaque receipt/token that it presents on each call. That removes fate sharing, lets a service object be upgraded or replaced without migrating client tables, and makes storage naturally charged to the client.
  - It **disagrees** with any design where a shared "registry" object accumulates per-caller state as a convenience.

#### RedLeaf — language-based isolation domains in Rust, with an ownership-tracked shared heap
- **Cite:** Narayanan, V., Huang, T., Detweiler, D., Appel, D., Li, Z., Zellweger, G. & Burtsev, A. (2020). *RedLeaf: Isolation and Communication in a Safe Operating System*. OSDI 2020. https://www.usenix.org/system/files/osdi20-narayanan_vikram.pdf. Local: `narayanan-redleaf-2020.pdf`. **[READ]**
- **OS-level decisions:**
  - *Domains* are units of information hiding, loading and fault isolation, all in ring 0.
  - *Heap isolation.* No domain holds a pointer into another's private heap, so a crashed domain's heap is freed in bulk without running destructors.
  - *Shared heap.* `RRef<T>` lives on a global shared heap with metadata: the owning domain, a borrow count, and a type id.
  - *Exchangeable types*: `RRef`, Copy primitives, composites of those, and trait references whose methods take exchangeable types.
  - *Moves and borrows.* Cross-domain calls *move* `RRef`s or *borrow them immutably*. **Mutable borrows across domains are forbidden**, because a crash mid-call would hand a half-updated object back to the caller.
  - *Proxies.* IDL-generated trusted proxies check that the callee is alive, save a continuation so a crashed callee can be unwound, and update ownership.
  - *Return type.* Every cross-domain method returns `RpcResult<T>`.
  - *Recovery.* Shadow drivers replay the initialisation protocol after a crash. Immutable borrows let the caller re-issue a failed call without backup copies.
  - *Threads.* The model is "migrating threads" (calls that carry the caller's thread into the callee), not messages.
  - *Loading.* Domains load dynamically from a *trusted compilation environment* that signs a fingerprint of the IDL files, the compiler version and the flags.
- **Evidence:**
  - Null cross-domain call 124 cycles, +17 per `RRef` passed. seL4 IPC is 834, a VMFUNC call/reply 396.
  - Ixgbe driver at line rate (14.2 Mpps) with batch 32. With batch 1 it is 6.5 Mpps vs DPDK's 6.7.
  - NVMe at SPDK parity (457K vs 452K IOPS).
  - Key-value store reached only 61–86% of the C/DPDK version in safe Rust, because of `Vec` copies.
  - Restarting the driver every second cost 5% read / 16% write throughput.
- **What failed / critiques:**
  - TCB includes rustc, the IDL compiler, trusted crates and the microkernel.
  - A safe-only rule cost performance, and unsafe was banned in domains.
  - Asterinas (2025) counts unsafe use in 62% of RedLeaf crates, including drivers.
  - The same group's next system, Atmosphere (2025), is a *hardware-isolated* verified microkernel. That is INFERRED as a shift of emphasis; the authors do not call it a retreat.
- **Lesson for Mini (forks 1, 3, 5):**
  - RedLeaf's rules translate directly. **Callee may receive (move) assets and read-only snapshots, but may never mutate caller state in-turn.** A mutation is a Plan action judged by the target's law. That **agrees** with "code proposes, law disposes" and is the strongest outside evidence for it: the *reason* for the rule is that partial failure must never expose a half-written object.
  - **Immutable borrow = content-addressed cell version.** A cross-object read in Mini should name a version/root, so a retried or re-executed turn sees the same bytes. That is also what deterministic re-execution needs.
  - `RpcResult<T>` on every boundary = make "callee refused/abandoned" part of every cross-object call's type.
  - The signed build-environment fingerprint is Mini's package hash. RedLeaf needed it because separately compiled domains must agree on *type meaning*. Mini must likewise pin the *interface types* (contracts, exchangeable types) to content hashes, not names. INFERRED, and also the memory note that "a display name is not a key".

#### Tock — multiprogramming a 64 KB microcontroller with Rust capsules plus MPU processes
- **Cite:** Levy, A., Campbell, B., Ghena, B., Giffin, D. B., Pannuto, P., Dutta, P. & Levis, P. (2017). *Multiprogramming a 64 kB Computer Safely and Efficiently*. SOSP 2017. https://doi.org/10.1145/3132747.3132786 (PDF: https://patpannuto.com/pubs/levy17multiprogramming.pdf). Local: `levy-tock-2017.pdf`. **[READ]**
- **OS-level decisions:**
  - *Two isolation tiers.*
    - **Capsules**: Rust structs in the kernel, isolated by the type and module system, cooperatively scheduled on one stack, and "trusted only to eventually yield". They cannot be loaded at runtime.
    - **Processes**: any language, MPU-isolated, preemptive, loadable.
  - *Syscall interface* is non-blocking: `command`, `allow`, `subscribe`, `memop`, `yield`.
  - *Grants*: kernel state kept *on behalf of a process* is allocated **inside that process's memory block**, growing down from the top while the process heap grows up. Process code cannot read it (MPU). Capsules reach it only through `enter(proc_id, closure)` or `each(closure)`, whose lifetimes stop references from escaping, and the return type must be `Copy`. When a process dies, all its grant memory is reclaimed at once with no refcount or GC. Kernel components therefore keep per-process lists instead of global lists.
  - *Threat model* with four stakeholders: board integrator, capsule author, app author, end user.
- **Evidence:**
  - The core kernel is 3,554 lines of Rust. The board fits in 8.4 KB of SRAM plus a 4 KB stack.
  - Capsule isolation costs essentially nothing beyond one reference word per dependency. The kernel is comparable to TinyOS and FreeRTOS in footprint.
  - Statically pre-allocating every syscall request, as TOSThreads does, wastes about 80% of the RAM it reserves.
  - Deployed in Signpost city-sensing modules and prototyped as a USB security key.
- **What failed / critiques:**
  - Capsules can starve the CPU, since cooperative scheduling trusts them for liveness, and cannot be loaded dynamically.
  - Iterating over every process's grant to service an event is acceptable only because processes are few (under 10).
  - RedLeaf criticises Tock for providing no fault isolation for capsules.
  - Asterinas counts unsafe use in 93% of Tock's crates.
- **Lesson for Mini (fork 5, metering, fork 1):**
  - **Grants are the right storage-charging model for services.** State that object S keeps for client C is allocated *in C's storage budget*, typed by S, opaque to C, and reclaimed in one step when C is deleted or its rent lapses. That turns "storage charged" into "storage charged to the party it serves". It composes with Theseus's opaque exportation: same idea, kernel-mediated.
  - Concretely, a cell kind `grant<S,C,T>` whose law says S may write and C pays, and which is reclaimed when C goes. The cost is one kernel cell kind plus rent rules.
  - Tock's two tiers also show Mini's fuel-bounded `runBounded` is worth keeping. Tock needed hardware preemption precisely because language isolation alone cannot bound CPU, while Mini's deterministic fuel gives preemption inside the language.

#### House — an OS in Haskell built on a small specified "hardware monad"
- **Cite:** Hallgren, T., Jones, M. P., Leslie, R. & Tolmach, A. (2005). *A Principled Approach to Operating System Construction in Haskell*. ICFP 2005. https://web.cecs.pdx.edu/~apt/icfp05.pdf. Local: `hallgren-house-2005.pdf`. **[SKIMMED: intro, P-Logic, H-monad sections]**
- **OS-level decisions:**
  - Hardware is reached only through a restricted monad `H`, not the full IO/FFI. `H` covers paging, user-mode execution of arbitrary binaries, and port/MMIO IO.
  - `H` is memory-safe except for DMA misuse.
  - Its behaviour is specified as **P-Logic assertions**. These include algebraic *independence* properties such as `Commute c d` and `IndependentSetSet`, and claims like "executing user code does not affect kernel data".
  - There is also a pure-Haskell model of `H` for validating that the properties are consistent.
  - House adds drivers, a window system, a network stack and a shell. Osker is an L4-style microkernel aimed at separation proofs.
- **Evidence:** Runs on bare IA32 under a modified GHC runtime. Mechanised Isabelle proofs were in progress (not in this paper).
- **What failed / critiques:**
  - DMA is a hole.
  - The GHC runtime (C) and its GC are in the TCB.
  - Practitioner remark (HN 34238599): an FP OS "ends up needing to do everything in a monad anyway".
- **Lesson for Mini (fork 3, fork 2):**
  - Specify the **Plan's action sum the way House specified `H`**: each action kind comes with *declared commutation/independence laws*. For example, two `Write`s to disjoint cells commute, and two `Credit`s to the same balance commute.
  - These laws, proved once in Lean over the kernel model, are exactly what licenses **deterministic parallel execution of independent turns**. Two Plans whose actions pairwise commute can be applied in any order, so in parallel, with the same root.
  - The cost is a Lean commutation lemma per action pair, plus a scheduler that consults declared footprints. That is INFERRED, not House's own claim.

#### JX — a Java OS with heap-isolated domains connected by portals
- **Cite:** Golm, M., Felser, M., Wawersich, C. & Kleinöder, J. (2002). *The JX Operating System*. USENIX ATC 2002. https://www.usenix.org/legacy/event/usenix02/full_papers/golm/golm.pdf. Local: `golm-jx-2002.pdf`. **[SKIMMED: architecture, portals, performance]**
- **OS-level decisions:**
  - Domains have their own heaps and GC. Code arrives as components that are loaded, verified, and translated to native code.
  - *Portals* are the inter-domain RPC. A call blocks the caller and runs in a service thread.
  - **All parameters are deep-copied**, under a *per-call quota*. Portals themselves pass by reference.
  - An object that implements a portal interface is *promoted to a service automatically* when it is passed out of its domain, giving location transparency. Same-domain calls skip copying.
  - Services are refcounted and deactivated when their count reaches zero.
- **Evidence:** Portal IPC 650 cycles (L4Ka 818; KaffeOS 27,270). Filesystem benchmark at 40–100% of Linux, NFS at about 80%.
- **What failed / critiques:**
  - Copying loses object identity.
  - The Sealing paper criticises JX's dynamic class loading as an *open* process architecture.
- **Lesson for Mini (fork 1, multi-domain):**
  - JX's argument for **copy semantics** is that domains can then interfere only at call time and the design "can be extended to a distributed system without much effort". That is the right default *across BFT domains*.
  - **Per-call parameter quota** = charge and bound the Plan payload size.
  - Automatic promotion of a passed object to a service is a precedent for Mini's "passing a cell reference across a domain makes it a remote capability".

#### Project Oberon — a single-process, command-oriented, extensible workstation OS
- **Cite:** Wirth, N. & Gutknecht, J. (1992; revised edition 2013). *Project Oberon: The Design of an Operating System, a Compiler, and a Computer*. https://people.inf.ethz.ch/wirth/ProjectOberon/PO.System.pdf. Local: `wirth-project-oberon-system-2013.pdf`. **[SKIMMED: ch. 2–3 (commands, tasks, central loop) read; ch. 6 loader and ch. 8 storage in parts]**
- **OS-level decisions:**
  - *Commands.* The unit of action is the **command**, an exported parameterless procedure `M.P`, separate from the unit of compilation, the module. Clicking `M.P` in *any visible text* loads M if it is absent. Modules stay loaded, so global variables persist between commands. Commands read their parameters from text or selections and do not interact with the user while they run.
  - *One process.* A **single process** runs a central loop that polls tasks. Task switches happen *only between commands*, so there are no locks and "deadlocks are not a topic".
  - *GC.* The garbage collector is itself a background task, run when the **stack is empty after a command**. Its only roots are the modules' global pointers.
  - *Visible state.* The "Oberon Programming Style" is to avoid hidden state, since "the state of the system is practically determined by what is visible to the user". Tool texts serve as user-composed menus.
  - *Traps.* A trap aborts the command and leaves global state as it was, inconsistent or not.
- **Evidence:** A complete system (compiler, editor, file system, network, GUI) from two authors, rebuilt on an FPGA RISC in 2013.
- **What failed / critiques:**
  - Wirth himself calls global variables between commands "Pandora's box" because they are hidden state.
  - A trap leaves state "possibly inconsistent".
  - Coarse granularity suits only a single user. He would delegate long computations to compute servers.
- **Lesson for Mini (fork 5, presentation, fork 3):**
  - Oberon is the closest precedent for **Mini's turn = command**: atomic, no interaction mid-command, interleaving only between commands, and **GC exactly when the stack is empty**. That validates "GC at yield": at a yield, the only roots are the object's state plus the checkpoint.
  - Mini strictly improves on Oberon's trap semantics, because atomic turns *roll back* rather than leaving half-updated globals.
  - For presentation, "any visible text is a command line" plus "no hidden state" argues that a card should render the object's *law-relevant state and affordances together*, so the user sees what a call will be judged against.

#### Symbolics Genera — an open, single-address-space Lisp machine environment
- **Cite:** Walker, J. H., Moon, D. A., Weinreb, D. L. & McMahon, M. (1987). *The Symbolics Genera Programming Environment*. IEEE Software 4(6). https://doi.org/10.1109/MS.1987.232087 (scan: https://archive.org/details/smbx-genera-programming-env-1987). Local: `walker-genera-1987.pdf`. **[SKIMMED: OCR damaged in places]**
- **OS-level decisions:**
  - "No protected core or kernel": everything lives in one shared virtual memory, and a user function is "just as good" as a system function.
  - Reliability rests on typed, tagged data, bounds and type checks in hardware, and GC.
  - Incremental compile/link/patch, with a dependency database used for incremental patching and distribution.
  - "Advice" wraps behaviour around system functions.
  - **Presentation types**: displayed objects are typed presentations, and input accepts "an object of a specified type" by pointing at a presentation.
- **Evidence:** Commercial product used for large systems.
- **What failed / critiques, self-reported "hazards":**
  - "Open systems have no 'keep out' signs", so users reach for primitives.
  - Documentation must carry the abstraction layers.
  - Layer boundaries "are mostly invisible, with no formal definition". The fourth hazard is illegible in the scan.
- **Lesson for Mini (presentation, fork 2):**
  - **Presentation types are Mini's card model in 1987.** A card's affordance should *accept typed objects by pointing at presentations of them*, for example dragging a capability card onto a method parameter. It should not be text forms. That makes web, Discord and AI residents all handle typed references, not strings. INFERRED.
  - Genera's hazards argue *for* Mini's laws: laws are the formal "keep out" signs and visible layer boundaries that Genera lacked.

#### Self — prototypes, mirrors, and a live object world
- **Cite:** Ungar, D. & Smith, R. B. (2007). *Self*. HOPL III. https://doi.org/10.1145/1238844.1238853 (PDF: https://www.cs.tufts.edu/~nr/cs257/archive/david-ungar/self-hopl.pdf). Local: `ungar-self-hopl-2007.pdf`. **[SKIMMED: §4.4 mirrors, §5.5 transporter]**
- **OS-level decisions:**
  - Prototype objects with parent slots.
  - Reflection *only through mirrors*. A mirror is created by a single primitive, so "introspection can be disabled by shutting off the mirror creation operation".
  - Reflective mutation primitives make *altered copies*. Only `define` redirects references to the new object, so only `define` invalidates compiled code.
  - The **transporter** turns sets of slots in a live world back into source files.
- **Evidence:** The 40K-line Self environment moved to transporter-based development in 1994.
- **What failed / critiques:**
  - Ungar's "fundamental realization" was that **orthogonal persistence "was, at least in this context, a flawed concept"**. Installing slots into another world so they "function as they did in their original home is difficult, and probably even impossible in the general case".
  - Each slot needed explicit annotations, including *initialisation instructions*: keep the old value, or evaluate an expression.
- **Lesson for Mini (fork 4, reflection):**
  - With Fare-style prototypes, Mini's "program" includes prototype *state*. Self's transporter failure says a **package must be source plus core, never a heap image**, and every **migration must state, per new or changed field, how it is initialised**. That is exactly the typed migration of fork 4, with the field-initialisation part made mandatory.
  - **Mirror-gated reflection**: give Core4's reflection a capability (a mirror) that the law can withhold. Reflection then cannot be used like Midori's downcast to break a capability's encapsulation.
  - Self's copy-then-`define` pattern is a clean model for an *upgrade as one atomic redirection*.

#### MirageOS / unikernels — sealed, single-language, compile-time-specialised appliances
- **Cite:** Madhavapeddy, A., Mortier, R., Rotsos, C., Scott, D., Singh, B., Gazagnaire, T., Smith, S., Hand, S. & Crowcroft, J. (2013). *Unikernels: Library Operating Systems for the Cloud*. ASPLOS 2013. https://anil.recoil.org/papers/2013-asplos-mirage.pdf. Local: `madhavapeddy-unikernels-2013.pdf`. **[SKIMMED: §1–2 and design sections]**
- **OS-level decisions:**
  - Application plus libraries compile into one OCaml VM image.
  - **Configuration is folded into compilation**, so dead code is removed and reconfiguration means recompilation.
  - One language inside, with type safety replacing user/kernel separation.
  - **Sealing via hypercall**: W^X page tables are then frozen, so the heap cannot grow and memory is pre-allocated.
  - **Interop happens at the network-protocol level**, with non-OCaml code kept in separate VMs. Isolation *between* appliances stays with the hypervisor.
- **Evidence:** DNS appliance image 200 kB vs over 400 MB for BIND, and 45% faster than BIND 9.
- **What failed / critiques:** Reconfiguring needs a rebuild. Isolation between appliances still relies on hardware (the hypervisor).
- **Lesson for Mini (interop, fork 4):**
  - Mirage's split, *type safety inside, protocol plus hardware boundary outside*, is Mini's split: Lean/Core4 inside the Host, **Rust clients and other domains speak only signed protocol messages**. It **agrees**.
  - "Configuration is code, sealed at build" supports putting object configuration in the package (or in law parameters fixed at creation), not in mutable settings.

#### Asterinas — a framekernel: a small unsafe privileged framework with all OS services in safe Rust
- **Cite:** Peng, Y., Tian, H., Zhang, J., Li, R., Chen, C., Jiang, J., Xian, J., Wang, X., Xu, C., Zhou, D., Luo, Y., Yan, S. & Zhang, Y. (2025). *Asterinas: A Linux ABI-Compatible, Rust-Based Framekernel OS with a Small and Sound TCB*. USENIX ATC 2025. https://www.usenix.org/system/files/atc25-peng-yuke.pdf. Local: `peng-asterinas-2025.pdf`. **[SKIMMED: abstract, §1–2, §4.4]**
- **OS-level decisions:**
  - One address space. Only the OSTD framework may use `unsafe`. All services, *including drivers*, are safe Rust built on OSTD's APIs, which include an "untyped memory" abstraction for MMIO and DMA.
  - **Safe policy injection**: schedulers and allocators are written in safe Rust and registered with the framework. The TCB keeps mechanisms only, while defending against a "safe-but-buggy" policy, such as one that schedules a task on two CPUs at once.
- **Evidence:**
  - Over 210 Linux syscalls, performance on par with Linux.
  - The memory-safety TCB is about 14% of the code.
  - Unsafe-using crates in prior systems: Linux RFL 55%, Tock 93%, RedLeaf 62%, Theseus 32%.
- **What failed / critiques:** This is a TCB-minimality design, not a fault-isolation one. Services share fate inside the kernel (INFERRED from the architecture; the paper's focus is memory safety).
- **Lesson for Mini (security kernel, fork 2):**
  - "Mechanism in the TCB, policy injected as safe code that the TCB still guards" is the right shape for Mini's kernel. The Lean kernel applies Plans and checks laws (mechanism). Schedulers, fee policies and governance policies are Core4 packages whose outputs the kernel re-checks against invariants.
  - The "safe-but-buggy scheduler" example is a direct warning: injected policy must not be able to break atomicity or double-apply a turn.

#### Atmosphere — a verified Rust microkernel (follow-on to RedLeaf by the same group)
- **Cite:** Chen, X., Li, Z., Zhang, J., Narayanan, V. & Burtsev, A. (2025). *Atmosphere: Practical Verified Kernels with Rust and Verus*. SOSP 2025. https://doi.org/10.1145/3731569.3764821 (PDF: https://mars-research.github.io/doc/2025-sosp-atmo.pdf). Local: `chen-atmosphere-2025.pdf`. **[READ: §1–4 and §5 TCB; eval skimmed]**
- **OS-level decisions:**
  - A *hardware-isolated* microkernel: address spaces, IOMMU, threads, endpoints, and **containers** with guaranteed memory and CPU quotas, passed down a tree.
  - Functional correctness is proven as refinement of a high-level spec in Verus.
  - Design choices that make the proofs tractable:
    - **flat permission maps** for every recursive structure, so invariants are non-recursive;
    - **manual memory management with leak freedom proven**, because "automatic memory management creates a semantic gap" with whole-system specs such as "one domain cannot exhaust the memory of the system";
    - **no fine-grained revocation**: resources return only when a container is terminated.
  - A **non-interference** theorem between isolated containers, plus user-level proofs for a shared verified container.
- **Evidence:**
  - 6K lines of executable code and 20.1K lines of proof (3.32:1). Verification takes under 20 s.
  - About 2.5 person-years in total. Three clean-slate rewrites.
  - IPC 1,058 cycles vs seL4's 1,026.
- **What failed / critiques:**
  - A big kernel lock.
  - Timing channels are outside the theorem.
  - The TCB is listed honestly: the Verus front end, Z3, rustc, core, about 700 lines of unverified axioms, about 3,000 lines of trusted Rust, about 172 lines of assembly, the boot loader, the CPU.
- **Lesson for Mini (fork 5, metering, security kernel):**
  - Two points transfer directly to a Lean-owned kernel.
  - (1) **Global resource properties need explicit accounting in the spec.** Atmosphere gave up implicit memory management to state "no domain can exhaust memory". Mini's storage charging should likewise be a *kernel-state quantity with a proven conservation law* (bytes allocated = sum of charged cells), not an emergent GC property.
  - (2) **Flat permission maps** are the Lean-proof-friendly representation for the cell store and capability graph.
  - The group's move from RedLeaf's pure language isolation to a verified kernel with hardware containers (INFERRED reading) is a datum for the next entry.

#### "Spectre is here to stay" — the limit of language-enforced confidentiality
- **Cite:** McIlroy, R., Sevcik, J., Tebbi, T., Titzer, B. L. & Verwaest, T. (2019). *Spectre is here to stay: An analysis of side-channels and speculative execution*. arXiv:1902.05178. https://arxiv.org/pdf/1902.05178. Local: `mcilroy-spectre-here-to-stay-2019.pdf`. **[SKIMMED: abstract, §1, conclusion]**
- **OS-level decisions (reported):** V8 and Chrome concluded that "speculative vulnerabilities on today's hardware defeat all language-enforced confidentiality with no known comprehensive software mitigations". Chrome moved to **site isolation** in separate processes.
- **Evidence:** A universal read gadget built from untrusted code in the same address space.
- **Lesson for Mini (security kernel):**
  - **Language isolation still holds for *integrity*, which is what Mini's laws protect, but not for *confidentiality*.** Mini's state is a public Merkle root, so this costs nothing today.
  - If Mini ever hosts *private* objects, they cannot rely on Core4 isolation inside a shared Host process. They need cryptographic hiding (commitments, encryption) or a separate trust domain.
  - Write this into the threat model now, so nobody later reads "Lean-checked isolation" as "confidential".

---

### Fork-by-fork summary of what this cluster pushes

- **Fork 1, calls.**
  - Prompt reads and pure calls in-turn; eventual sends via Plan (Midori).
  - Typed **contract-governed channels** whose protocol state is a cell law (Sing#).
  - **Exchangeable payloads** only: forced data, capability refs, linear assets, no thunks (Sing#, RedLeaf).
  - **Move or immutable-borrow, never mutable-borrow** across objects (RedLeaf).
  - Failure observed only at the receiver, as typed messages that include law refusals (Sing#).
  - Copy semantics plus a per-call quota across domains (JX).
  - Pipelining and three-party handoff (Midori, E).
- **Fork 2, laws and contracts.**
  - Contracts in signatures, always checked at admission, discharged statically when the checker can (Midori).
  - Protocol laws are finite-state and decidable (Sing#).
  - Refusals are typed and must be handled (Midori).
  - Package manifests give static effect footprints (Singularity MBP).
  - Laws are the keep-out signs that open systems lacked (Genera).
- **Fork 3, concurrency.**
  - Turns interleave only at awaits (Midori, Oberon).
  - **Declared activity footprints** with reader/writer admission and re-validation after await (Midori's unfinished plan).
  - **Commutation laws on Plan actions** license deterministic parallel application (House).
  - Isolation over locks, and no hidden distributed two-phase commit (Midori).
- **Fork 4, evolution.**
  - Package hash = seal (Singularity).
  - Upgrade = governed re-seal with bidirectional dependency and contract checks (Theseus).
  - Checkpoints as **defunctionalised first-order continuations** so typed migration is writable (Theseus).
  - Explicit per-field initialisation in migrations (Self).
  - Soft fields (Theseus).
  - Reflection through capability-gated mirrors so it cannot re-open the seal (Self, Singularity).
- **Fork 5, heap and checkpoints.**
  - GC when the stack is empty: GC at yield (Oberon).
  - Per-object heaps with no cross-object pointers (Singularity memory independence).
  - **Grants**: service state charged to the client it serves and reclaimed with it (Tock, Theseus opaque exportation).
  - Storage conservation as a proven kernel invariant (Atmosphere).

### Cluster synthesis (§2)

Read together, these systems show that a language checker can carry an operating system's isolation, communication and upgrade story. They also show clearly where it stops. For Mini, six lessons carry the most weight.

**1. The process boundary comes back no matter what; make it the object and make it sealed.** Singularity, Midori, RedLeaf, JX and Theseus all started from "one address space, pass objects freely". Each then rebuilt a process-like unit: SIP, domain, cell, isolated bubble. That unit has its own heap, its own failure scope, and a rule that no pointer reaches into another unit's heap. The HN critique (33575904) names why: you need something to kill, to account against, and to fail as a unit. Mini already has that unit, the object cell with a pinned package hash. Singularity's sealing invariants (fixed code, state isolation, explicit communication, closed API) are the right contract for it. Reflection and upgrade are the two ways that contract could be breached, so both must go through capabilities and governance.

**2. Cross-object calls want session types, and the protocol state belongs to the law.** Sing# contracts caught a protocol bug that had sat in the web server for a year. They made zero-allocation, zero-copy messaging possible through one structural rule (a send and a receive in every cycle). They are equivalent in power to session types. Mini's decidable laws can host the protocol state machine directly: a channel is a cell, and its law is its contract. Two refinements are needed. Sing# never fixed its blind spot on exceptional paths, so Mini should model law refusals, peer upgrade and peer deletion as protocol messages. And waiting should be a join pattern over several endpoints.

**3. The data that crosses a boundary must be closed and linear.** The exchange heap, `RRef` with no mutable borrow, JX deep copies and Midori's marshalable types all converge on the same rule. What crosses is forced data, capabilities, and moved resources; never references into the sender's live heap; never in-place mutation of the caller. In a lazy language the thunk is the dangerous reference. RedLeaf's reason for banning mutable borrows (a crash must not expose a half-written object) is the strongest outside justification for "code proposes, law disposes".

**4. Turns-at-await is the correct concurrency model, and its open problem is now Mini's.** Midori, Oberon and Tock all let interleaving happen only at explicit points, and all gained lock-freedom from it. Midori also reports the cost. Reentrancy at awaits produces TOCTOU bugs, the "permissions on activities" fix was never finished, and async-everything floods the machine without throttling. Mini can finish Duffy's design: declared activity footprints, reader/writer admission, re-validation after an await, commutation laws on Plan actions, and paid turns as the throttle.

**5. Upgrading under suspended computations is the hard part of evolution; design checkpoints for it now.** Theseus achieved live evolution by eliminating state spill and quiescing components, and still needed hand-written transfer functions. Self found that "orthogonal persistence" of programs-with-state fails without per-field initialisation instructions. A Mini checkpoint full of thunks that close over old code is the worst case. Checkpoints should be named yield points plus first-order locals, so that typed migration is a checkable function. Opaque exportation and Tock's grants also keep services migratable and put their storage on the clients they serve.

**6. Language isolation replaces hardware for integrity, not for confidentiality, and the trusted base moves into the checker.** Singularity measured a 6–38% unsafe-code tax against under 5% for safety checks. RedLeaf crosses domains in 124 cycles. But every system's TCB grew to include a compiler (Bartok, rustc), and Spectre ended language-enforced confidentiality inside one address space. Atmosphere, from the RedLeaf group, verifies a hardware-isolated kernel instead, and makes resource conservation an explicit proven invariant. Mini's position is unusually strong. Integrity is checked by re-execution in Lean with no native code generation in admission, and state is public. That only lasts if the threat model says so explicitly, and if storage and fuel are kernel quantities with proven conservation rather than emergent properties.

---

## §3. Capability OSes, namespaces, orthogonal persistence and single-level stores (reading lane B)

Scope: KeyKOS, EROS, seL4/L4, Zircon/Fuchsia, Plan 9/Inferno, orthogonal persistence (PS-algol/Napier88,
PJama, Grasshopper), Twizzler, Aurora, plus DFINITY's 2024 "enhanced orthogonal persistence" for Motoko.
Every "Lesson for Mini" is aimed at the proposed model in PROGRAM-MODEL-BRIEF-20261004 (cell = state + law +
pinned package hash + activities; method call = admitted, re-executed invocation returning a Plan; residents
checkpointed by an exact Core4 codec; five forks). Entries tagged READ were read in full from the local text.
Skipped per parent instruction (covered elsewhere): Dearle/Kirby/Morrison 2009, Cooper & Wise 1996, Liedtke
1993 EUMEL/L3 paper itself, TreeSLS 2023.

---

### 3.1 KeyKOS / GNOSIS

#### KeyKOS Architecture — the pure-capability, persistent, metered microkernel (Tymshare, production 1983–)
- **Cite:** Hardy, N. (1985). *The KeyKOS Architecture*. ACM Operating Systems Review 19(4):8–25 (8th ed. KL028-08,
  Key Logic, Dec 1990). http://cap-lore.com/CapTheory/upenn/OSRpaper.html .
  Local: ~/paperbin/world-program-model/hardy-keykos-architecture-1985.{html,txt}. **[READ]**
- **OS-level decisions:**
  - *Authority:* "objects have no intrinsic authority, and rely totally upon their keys". A domain has no
    terminal, directory, priority, address space, implicit caller stack, or system calls beyond key invocation
    (CALL/RETURN/FORK) plus traps routed to its keeper. "No key, no access" — even for debugging.
  - *Object model:* domains (single-threaded actors, 16 general key slots) obey a program in an address segment;
    a domain = Smalltalk-style object at system level. Kernel primitives: pages (data), nodes (16 key slots),
    and three "special objects" built from nodes — domains, segments, meters. Number keys, wait objects,
    Discrim (key equality), Keybits, Returner, Domain tool (the sole rights-amplification primitive, via a
    per-creator *brand*).
  - *Communication:* unbuffered rendezvous messages (parameter word + ≤4096 bytes + 4 keys). CALL synthesises
    a *resume key* (first-class continuation, at-most-once: invoking any copy nulls all copies). Start keys
    queue callers while the domain is busy — the domain is its own mutex ("exclusion and queuing" are bundled
    into the domain). Co-routines = CALLing a resume key. Kernel never buffers messages "which potentially
    could be held forever".
  - *Keepers:* each domain, segment and meter has a keeper slot; on an exceptional state (trap, invalid
    segment reference, meter exhausted) the kernel CALLs the keeper with a *service key* and a resume key so
    the fault can be repaired and the faulter resumed unaware. Stated motive: "remove policy … from the
    microkernel. Fixed policies … inhibit the evolution of the system" and allow "multiple policies to be
    simultaneously supported".
  - *Metering:* a domain runs only if its meter slot holds a key to a valid meter chain ending at the primitive
    meter; every meter on the chain records consumption; a meter key both provides and *limits* resource; its
    holder can build inferior meters; counter reaching zero calls the meter keeper with the faulter's resume
    key — "the meter keeper is in a position to perform scheduling … over all the domains served by that meter".
  - *Storage:* space banks (domains) sell nodes/pages; sub-banks with limits; "reclaim all pages and nodes
    ever bought from that bank". Factories create confined compartments and *certify* discretion by
    inspecting the initial key set (the confinement mechanism, US patent 4,584,639).
  - *Naming:* the kernel has none; "directories" are ordinary objects mapping names to keys, held only by the
    user's command system; a program sees a directory only if a key to it is passed.
  - *Sense keys:* transitive read-only (anything fetched through a sense key is itself diminished) — fixes the
    classic "read-only key to a tree still yields writable subtrees" hole.
- **Evidence:** production on S/370 since Jan 1983 (VISA transaction processing, Tymnet hosts); ports of BSD4.3,
  Minix, VM/CP, reduced MVS, EDX via domain keepers with binary compatibility; >150 ready-made object types.
- **What failed / critiques:** commercial failure (Key Logic closed 1991, per Shapiro 1999). Hardy's text admits
  the formal-security reasoning relies on the fixed logic of trusted factories. Administration ("Fred may not
  use this") is hard without reference monitors (see EROS entry).
- **Lesson for Mini:**
  - *Security kernel:* AGREES with "code proposes, law disposes" only if Mini also adopts KeyKOS's negative
    list: a cell/object has NO ambient authority — no implicit caller identity it can consult, no global name
    lookup, no clock, no "the store". Every Plan action must name a capability the activity holds. Concretely:
    a Plan action type `Invoke(cap, msg)` where `cap` is a value in the activity's own state, and admission
    refuses any action whose target is not reachable from a held cap. Cost: the Core4 value domain needs an
    unforgeable `Cap` sort (opaque, no constructor in user code) — a typing-rule addition and a data-soundness
    obligation, not a runtime cost.
  - *Fork 1 (calls):* the resume key is the right model for Mini's activity reply: CALL = perform a plan that
    hands the callee a one-shot reply capability; the caller's activity is checkpointed waiting on it. The
    at-most-once semantics ("all copies become null when one is invoked") maps directly onto a linear reply cap.
    The start-key-queues-while-busy rule gives Mini a default concurrency semantics for fork 3: one activity
    per object serves at a time, others queue — KeyKOS shipped 9+ years on it.
  - *Fork 2 (laws):* keepers are the historical precedent for "the policy lives outside the mechanism, invoked
    on exceptional states". DISAGREES in one way: a KeyKOS keeper is arbitrary code with a service key (full
    power over the faulter); Mini's law is a decidable predicate. A Mini "keeper" would be a law *refusal
    handler*: when the law refuses, instead of aborting, the kernel may route the refused Plan + explanation to
    a designated keeper object that can repair-and-retry. That is the rich-fork-2 shape KeyKOS suggests.
  - *Metering:* adopt the meter chain literally (see Bomberger entry).
  - *Naming:* KeyKOS says the kernel should know no names. AGREES with a content-addressed Merkle store
    (hashes are not names-with-authority) and argues against any global mutable name registry in the kernel.

#### KeyKOS checkpoint mechanism — consistent whole-system snapshots, every ~5 minutes
- **Cite:** Landau, C. R. (1992). *The Checkpoint Mechanism in KeyKOS*. Proc. 2nd IEEE Int'l Workshop on Object
  Orientation in Operating Systems (IWOOOS), 86–91. http://cap-lore.com/CapTheory/upenn/Checkpoint.html .
  Local: ~/paperbin/world-program-model/landau-keykos-checkpoint-1992.{html,txt}. **[READ]**
- **OS-level decisions:** *all* state lives in pages and nodes (processes, registers, locks, address spaces);
  the kernel holds only caches derivable from them (page tables). Checkpoint = stop all processes, mark
  changed pages copy-on-write and copy changed nodes to buffers (no I/O while stopped), restart, write the
  "Next Checkpoint" versions to the working swap area, flip a header (the commit), then *migrate* to home
  locations at low priority. Two swap areas alternate. Pages redirtied before migration need no migration.
  *Journaling* escape hatch: an authorised program may commit a selected **page** synchronously; "to ensure
  consistency of the security-related state of the system, journaling of nodes is not allowed" (i.e.
  capabilities never escape the global consistent cut). Tape checkpoints iterate until a consistent image is
  on tape; this is also how KeyKOS was *distributed*.
- **Evidence:** checkpoint every 5 min; stop-the-world ≈1 s on a loaded system, mostly the kernel consistency
  check; systems ran 3 years with processes surviving power and hardware failures; pull-the-plug demo at
  UNIFORUM '90, resumed in 30 s with windows intact; >90% disk channel utilisation; 5× faster TP benchmark;
  "never a need for … fsck"; only damaged checkpoints ever written were during kernel development.
- **What failed / critiques:** §8.2, verbatim: "user software upgrades must be managed more carefully in KeyKOS
  than in less reliable architectures. Non-kernel software does not stop running when the system is rebooted …
  the convenience of storing permanent object data in virtual memory structures or even process registers
  must be weighed against the need to separate the program from its data when it is desired to upgrade the
  program while preserving the data … [upgrade strategies] must be planned in advance." Also: incompatible
  with real-time; external peers (network) cannot be checkpointed and need "ad hoc mechanisms" on restart;
  up to 5 minutes of rollback without journaling.
- **Lesson for Mini:**
  - *Fork 5:* Mini already has the stronger form: each admitted turn is a commit, so the "consistent cut"
    problem disappears (no 5-minute rollback, no ad hoc resync except for off-chain peers). What KeyKOS adds:
    (a) the kernel must hold **no state not derivable from the store** (Mini: the Host process must be
    restartable from the Merkle root alone — any Host-side cache, queue, timer table or pending-await index
    must be a function of committed cells); (b) a pre-commit **consistency check** of the checkpointed state
    (Mini: decode-and-typecheck every activity checkpoint the turn writes, before the root moves — cheap
    because the codec is exact; see the EROS entry for "once committed, an inconsistent checkpoint lives
    forever"); (c) never let authority escape the consistent cut (KeyKOS forbids journaling nodes) — Mini's
    analogue: no capability may be minted or revoked outside an admitted turn.
  - *Fork 4 (evolution):* this is the first statement of the lesson the whole OP literature later repeats:
    persisting process registers/heap makes the program and its data inseparable, so upgrade must be
    *designed in*. Mini's resident = an activity whose checkpoint is an exact Core4 machine state of code
    pinned to a package hash. Upgrading the package does not upgrade a *suspended continuation*. Decision it
    pushes: residents should hold long-lived state in **cell data with a declared type**, and keep the
    continuation short-lived (yield at "quiescent points" whose resume type is a declared, versioned
    interface). Concretely: an activity checkpoint records (package hash, resume-point id, typed locals), and
    an upgrade must supply a migration for each live resume-point id, or the kernel refuses the upgrade while
    such continuations exist (or drains them). Cost: a resume-point table per package plus a refusal path;
    small compared to discovering this after deployment.

#### KeyKOS Nanokernel — stateless kernel, space banks, meters, keepers in production; KeyNIX
- **Cite:** Bomberger, A. C., Frantz, A. P., Frantz, W. S., Hardy, A. C., Hardy, N., Landau, C. R., Shapiro, J. S.
  (1992). *The KeyKOS Nanokernel Architecture*. Proc. USENIX Workshop on Micro-Kernels and Other Kernel
  Architectures, 95–112. http://cap-lore.com/CapTheory/upenn/NanoKernel/NanoKernel.html .
  Local: ~/paperbin/world-program-model/bomberger-keykos-nanokernel-1992.{html,txt}. **[READ]**
- **OS-level decisions:** "hold no critical state in the kernel … all private storage is merely a cache of the
  persistent state"; hence *no dynamic allocation in the kernel* — kernel never runs out of space, no message
  queues to checkpoint. Questions the kernel does not have to answer: out of swap ("it checkpoints"), process
  teardown ("it doesn't"), kernel state across restart ("none"). Meters: "a meter key provides the holder with
  the right to execute for the unit of time held by the meter"; the prime meter = "the present until the end
  of time"; submeters; time slicing = min(entitlement, slice); "political scheduling policies may be
  implemented external to the kernel". Space banks: a department "bought the right to a megabyte" receives a
  bank key holding 256 page keys. Each key carries an 8-bit field the server sees on every message (client
  classes by key). Domains are single-threaded by design; "there is no mechanism for stacking messages".
  Keeper = ordinary domain receiving the faulter's state + resume key.
- **Evidence:** ~20,000 lines C + 2,000 asm; runs in 100 KB; message path 90 instructions (S/370) to 500 cycles
  (88k). KeyNIX (BSD binary-compatible UNIX, one developer, 6 months, ~16 kLOC): one UNIX keeper *per process*
  (a crash in "the OS" kills one process). Benchmarks vs Mach 2.5 on the same Luna/88K: getpid 0.4×, open/close
  0.26×, fork/exit 6.4×, exec 11.6×, sbrk 14×, pipe 0.56×, disk I/O 6.5×.
- **What failed / critiques (theirs):** inode-per-domain was a mistake: "with the benefit of hindsight, we were
  mistaken" — namei put four context switches in the inner loop. Single-threaded domains forced extra
  "queue domains" to receive UNIX signals, halving pipe bandwidth. Lesson they draw: decomposition into
  protected objects pays only above a granularity threshold; they would collapse the file system into one domain.
- **Lesson for Mini:**
  - *Metering (scheduling):* the meter chain is exactly the capability-based metering model Mini needs, and it
    composes with "each resume is one admitted, paid turn". Concretely: every activity/resident cell holds a
    `Meter` capability (a cell with a counter and a parent meter cap); admission debits the whole chain for the
    re-execution's step count (Core4 `runBounded` fuel is already the unit) and storage delta; a meter at zero
    does not *fail* the turn — it parks the activity and notifies the meter's keeper object (a resident that
    may top up or refuse). Sub-meters let a resident hand bounded budget to children it spawns without
    exposing its own. Space banks are the storage half: storage charged per cell, reclaimable as a whole bank
    ("one way to ensure that a subsystem is completely dead is to destroy the space bank" — EROS). AGREES with
    "storage charged — owner fine with it"; adds the *hierarchy* and *bulk reclamation*. Cost: one more cell
    kind and a chain walk per admission (depth-bounded).
  - *Fork 1/3 granularity:* KeyNIX's inode-per-domain regression is a warning for "every object is a cell with
    its own law and activity": cross-cell calls inside a hot path multiply admissions. Mini should let one
    cell hold a rich Core4 data structure (a whole directory, a whole order book) governed by one law, rather
    than pushing per-record cells. The proposed model AGREES if objects are coarse; DISAGREES if "object" is
    read as "every record".
  - *Fork 3:* single-threaded objects + explicit queue objects is a coherent, shipped design; the cost shows up
    exactly where asynchronous notifications (signals) must interrupt a busy object. Mini's "several
    activities per object" fork should be weighed against this evidence: the simple rule worked for a decade,
    and its pain point (async interrupts) is solvable by giving each object an inbox cell rather than
    multi-activity concurrency.

---

### 3.2 EROS

#### EROS: a fast capability system — KeyKOS re-implemented on commodity x86, with a pre-commit consistency check
- **Cite:** Shapiro, J. S., Smith, J. M., Farber, D. J. (1999). *EROS: a fast capability system*. SOSP '99, OSR
  34(5):170–185. https://flint.cs.yale.edu/cs428/doc/eros.pdf .
  Local: ~/paperbin/world-program-model/shapiro-eros-fast-1999.{pdf,txt}. **[READ]**
- **OS-level decisions:** primitive capability types: numbers, nodes (32 caps), data pages, capability pages
  (tagged partition: data and caps never mix), processes, entry and resume caps. "Capability invocation is the
  only 'system call'"; all invocations share one argument shape, so a process can be *transparently
  interposed* in front of any object (logging, mediation, MAC). Revocation: object and capability carry
  version numbers (mismatch = void cap); selective revocation by forwarding objects a reference monitor can
  destroy (KeySafe). *Weak* access right generalises sense keys (transitively read-only and weak). Constructors
  certify, by inspecting a new program's initial capabilities only, that it cannot communicate with third
  parties (confinement; proven correct in Shapiro & Weber 1997). Space banks own all storage; storage for
  page-table mappings is "fully accounted for". Two kernel design rules: "All state resides in pages and
  nodes" and "All kernel operations are atomic" — a stalled invocation is restarted from the trap
  (PCLSRing-style), so no kernel continuation must be checkpointed; the only kernel state checkpointed is the
  stall-queue table.
  Checkpoint: snapshot + consistency check (pointer types, checksums of allegedly read-only cached objects,
  every dirty object in the checkpoint directory, cap types in process slots); failure ⇒ reboot *without
  committing*. "Once committed, an inconsistent checkpoint lives forever." The checker caught "innumerable
  bugs"; EROS now runs it continuously in the background. Bootstrap/installation: an initial image is
  produced by a cross-"linker" that wires processes together by capabilities; the system image *is* a
  checkpoint.
- **Evidence:** 400 MHz PII vs Linux 2.2.5 lmbench analogues: trivial syscall 1.6 µs vs 0.7 µs (worse, by design:
  uniform interposable argument structure "function was favored over performance"); page fault 3.67 µs vs
  687 µs; grow heap 20.4 vs 31.7 µs; process create via constructor 0.664 ms vs fork/exec 1.92 ms; pipe 281 vs
  260 MB/s. Snapshot phase < 50 ms on 256 MB including the sanity check. 17 calendar years (KeyKOS+EROS) with no
  inconsistent checkpoint outside stabilisation-code debugging.
- **What failed / critiques:** "The principal failing of capabilities is difficulty of administration. In the
  absence of a reference monitor, there is no direct way to say 'Fred may not use this object.'" No
  applications ran natively in 1999 ("another year" of several people); EROS never reached deployment and was
  succeeded by Coyotos (itself abandoned). The paper notes L3's persistence broke whenever a kernel table size
  changed ("renders previous checkpoints unusable") — EROS avoided this only because kernel state is a cache of
  pages and nodes.
- **Lesson for Mini:**
  - *Security kernel / fork 2:* the uniform invocation shape is what makes interposition — and therefore
    policy-as-an-object — possible. Mini's Plan actions should have one uniform `Invoke(cap, msg)` shape at the
    kernel boundary so that a *membrane/forwarder cell* (a cell whose law is a revocation flag and whose
    activity forwards) can be placed in front of any object. Revocation then needs no kernel feature beyond
    "a cap to a cell whose law now refuses everything". Cheap; AGREES with "code proposes, law disposes".
  - *Fork 5:* adopt the "consistency check before commit" literally: before the Merkle root moves, the Host
    decodes every activity checkpoint written in the turn with the *certifying* type checker against the pinned
    package's declared resume types. This is the Mini form of "once committed, an inconsistent checkpoint
    lives forever" — and in Mini it lives forever *in a replicated, signed history*, which is worse.
  - *Fork 4 / fork 5 joint:* L3's failure (kernel table size changed ⇒ all checkpoints unusable) is precisely the
    risk of an *exact machine-state codec*: any change to Core4's machine representation (a new stack-frame
    form, a renamed constructor) invalidates every stored continuation. EROS's escape was to make the stored
    form abstract (pages/nodes) and the machine form a cache. Mini's analogue: version the checkpoint codec
    with an epoch tag and require that a Core4 machine change ships a total, checked `decode_old → encode_new`
    translation (or refuses to load old checkpoints loudly, per the repo's greenfield doctrine). Decide now
    that the codec is a versioned *wire format*, not an in-memory dump.
  - *Bootstrap:* EROS's "genesis image is a checkpoint produced by a capability linker" is a clean model for Mini
    re-genesis: genesis = a store root built by a tool that wires cells by capabilities, admitted by the same
    checker as any later state.

#### Design Evolution of the EROS Single-Level Store — three generations of the store, what changed and why
- **Cite:** Shapiro, J. S., Adams, J. (2002). *Design Evolution of the EROS Single-Level Store*. USENIX ATC 2002.
  https://www.usenix.org/legacy/event/usenix02/full_papers/shapiro/shapiro.pdf .
  Local: ~/paperbin/world-program-model/shapiro-eros-sls-evolution-2002.{pdf,txt}. **[READ]**
- **OS-level decisions:** every object has an OID; capability = (type, OID, permissions) — "similar to a page
  table entry that contains the swap location". OIDs correlate to disk locations so no directory I/O is needed.
  Checkpoint area is append-only; snapshot marks dirty objects COW and sets a watermark; a log header write
  commits "a consistent system-wide transaction"; a migrator copies to home locations; next checkpoint cannot
  complete until migration finishes; a checkpoint is forced at an occupancy threshold (65%). Space bank does
  allocation, quota, bulk reclamation and placement; "objects allocated and deallocated within the same
  checkpoint interval" generate no allocation I/O. Gen 1 (KeyKOS layout): typed ranges (nodes vs pages) with
  allocation counts; Gen 2: unified ranges, frames retyped on demand ("we were continuously adjusting our
  directions to the disk formatting program"); Gen 3 (embedded): drivers out of the kernel, "object sources",
  non-persistent ranges for DMA/drivers, checkpoint logic moved to a user-mode persistent-source driver.
  Planned Gen 4: abandon allocation counts and the OID→disk direct map; randomised extent placement;
  separate "storage reservation" from "object name binding".
- **Evidence:** KeyKOS measurements: >85% of reads served from the checkpoint area; >50% of dirty objects die or
  are redirtied before migration. Computed (not measured) 400 KB write: ~231 ms conventional vs ~138 ms
  checkpoint+migration. EROS total ≈104 kLOC vs Linux 2.4's 284 kLOC of file-system code alone. Across all
  generations, "we have changed the capability size, the OID encoding, the checkpoint design, and removed the
  object driver from the kernel. The only application code that changed was the space bank."
- **What failed / critiques:** administration of changing disk configurations "neither efficient nor hands free";
  space bank's red-black trees would thrash beyond ~2.6 TB; no application-level benchmarks even in 2002
  ("a key missing piece"). Grasshopper's transitive-dependency checkpointing called "complex and expensive";
  L3/Fluke lack pre-commit consistency checks, "introducing the likelihood that system state errors … will be
  rendered permanent".
- **Lesson for Mini:**
  - *Fork 5 (storage charged, GC at yield):* the strongest empirical fact here is that half of all dirtied state
    dies within one checkpoint interval. Mini's per-turn exact checkpoint commits *every* turn, so it pays for
    state KeyKOS never wrote. Decision it pushes: GC the activity heap **at yield, before encoding**, and charge
    storage on the *post-GC encoded size delta*, not on allocation — so ephemeral allocation within a turn is
    free (as in EROS's "allocated and freed within an interval ⇒ no I/O"). Cost: a collector over Core4's heap
    at each yield, bounded by the live set.
  - *Fork 4:* the persistence substrate itself was re-designed three times with only the allocator changing,
    *because no interface exposed representation sizes or OID encodings*. Mini should not let Core4 programs or
    laws observe checkpoint bytes, Merkle paths, or cell sizes beyond an abstract `size` charge — otherwise the
    store format freezes. (The repo memory already records a size-field leak class; this is the OS-level
    precedent.)
  - *Naming:* "separate storage reservation from object name binding" (Gen 4) is the same separation a
    content-addressed Merkle store gives for packages; for mutable cells Mini still needs a stable identity
    distinct from content (a cell id), and EROS's allocation-count/version trick is the revocation half:
    a cap = (cell id, epoch); bumping the epoch voids all outstanding caps in O(1).

---

### 3.3 seL4 and the L4 family

#### seL4: Formal Verification of an OS Kernel — what a verified capability kernel had to give up to be provable
- **Cite:** Klein, G., Elphinstone, K., Heiser, G., Andronick, J., Cock, D., Derrin, P., Elkaduwe, D., Engelhardt, K.,
  Kolanski, R., Norrish, M., Sewell, T., Tuch, H., Winwood, S. (2009). *seL4: Formal Verification of an OS Kernel*.
  SOSP '09. https://www.sigops.org/s/conferences/sosp/2009/papers/klein-sosp09.pdf .
  Local: ~/paperbin/world-program-model/klein-sel4-2009.{pdf,txt}. **[READ]**
- **OS-level decisions:** third-generation L4 influenced by EROS: capabilities in CNodes, synchronous and
  asynchronous endpoints without in-kernel buffering, reply capabilities for RPC, user-level drivers and pagers.
  *All kernel memory allocation is explicit and authorised*: physical memory starts as Untyped caps that are
  *retyped* into TCBs, CNodes, endpoints, frames; a *capability derivation tree* (CDT) records derivations so
  revoke finds all descendants, and a *local* check (untyped has no CDT children) proves global absence of
  dangling references. Event-based kernel, single kernel stack, "mostly atomic API", interrupts polled at a
  few preemption points; long-running destruction is made preemptible by storing progress *in the last
  capability* (a "zombie" cap) so any later caller continues it. Design process: Haskell executable prototype
  → Isabelle abstract spec (nondeterministic: the scheduler "picks any runnable thread") → executable spec →
  C, linked by refinement theorems (MC refines ME refines MA).
- **Evidence:** 8,700 lines C + 600 asm; 200,000 lines of Isabelle; ~20 person-years total (11 py
  seL4-specific; estimate 6 py to redo); >150 invariants, ~80% of first-refinement effort went to invariants;
  verification found 144 defects beyond 16 found by use. IPC 224 cycles (optimised C path, then unverified).
  Cost of change: local optimisations cheap; a new batched syscall ≈1 person-week; adding interrupts/ARM page
  tables ≈1.5–2 py; *adding reply capabilities after the first refinement ≈1 py, 17% of the original proof
  effort*, because creating and deleting caps "on the fly" broke cross-cutting capability invariants.
- **What failed / critiques:** assumes compiler, asm, boot code, caches/TLB and hardware (later work closed some);
  uniprocessor only; access-control proof not yet connected to the refinement in 2009; "a cynic might say that
  an implementation proof only shows that the implementation has precisely the same bugs that the
  specification contains" — the authors' own caveat.
- **Lesson for Mini:**
  - *Security kernel:* seL4 is the existence proof that "the kernel adheres to the authority distributed to
    applications for its own data structures" can be verified. Mini's Host has its own bookkeeping (pending
    awaits, message inboxes, timer wake-ups, package index). Each such entry must be *retyped out of a charged
    resource the requesting object holds* — i.e. an await registration costs storage from the resident's bank
    and is reclaimed when the activity is resumed or destroyed. Otherwise a resident can DoS the Host with
    free awaits. Concretely: no unaccounted Host-side table; everything the Host stores is a cell or a field
    of a cell, charged.
  - *Fork 1 (calls) / proofs:* the 17% re-verification cost of retrofitting reply capabilities is the most
    concrete number in this cluster about *deciding the call/continuation model before proving*. Mini has
    adequacy/preservation proofs for Core4 *now*; the reply-capability semantics of method calls and resident
    awaits (one-shot, typed, revocable, owned by whom) should be fixed in Core4's activity semantics before
    more proofs accrete on the current shape.
  - *Fork 3:* seL4's verification stance is "avoid concurrency in the verified core" — event kernel, atomic
    operations, preemption only at explicit points that are continuation points. This *agrees* with Mini's
    atomic turns: activities interleave only at yields (explicit continuation points), never inside a turn.
    The zombie-cap trick generalises: an unbounded operation (destroy a large bank, migrate a big cell) is a
    multi-turn activity whose progress lives in a cell, resumable by anyone authorised — not a long turn.
  - *Fork 2:* the abstract spec's scheduler is nondeterministic and the policy is a refinement. Mini's law
    language can borrow the pattern: a law states the *set* of acceptable post-states (difference-logic
    predicate); the Plan is one witness; refinement = the Plan satisfies the law. This is already Mini's shape;
    seL4 shows it scales to a whole kernel spec.

#### L4 Microkernels: The Lessons from 20 Years — what the L4 community kept, replaced and abandoned
- **Cite:** Heiser, G., Elphinstone, K. (2016). *L4 Microkernels: The Lessons from 20 Years of Research and
  Deployment*. ACM TOCS 34(1), Article 1. https://trustworthy.systems/publications/nicta_full_text/8988.pdf .
  Local: ~/paperbin/world-program-model/heiser-l4-20-years-2016.{pdf,txt}. **[READ]**
- **OS-level decisions (Table IV verdicts):** *Kept:* minimality ("a concept is tolerated inside the µ-kernel only
  if moving it outside … would prevent the implementation of the system's required functionality"),
  generality, synchronous IPC for client–server, user-level drivers, mostly non-preemptible kernel.
  *New:* semaphore-like **notifications** (non-blocking signal; a word of binary semaphores; can be bound to a
  thread so a single-threaded server waits for requests *and* notifications — "a (partial) decoupling of
  synchronisation from communication"). *Replaced:* thread IDs as IPC targets → **endpoints** (global IDs
  leaked server structure and created covert channels) with **badged** caps for client identity; physical →
  virtual message registers; recursive address-space mapping → frame capabilities; process kernel → event
  kernel; lazy scheduling → "Benno" scheduling (for a bounded WCET). *Abandoned:* **long IPC** (nested
  in-kernel page faults; rarely used; shared buffers and pass-by-reference won), **IPC timeouts** ("no theory,
  or even good heuristics, for choosing timeout values"; only 0 and ∞ were ever used; watchdogs are better),
  **clans and chiefs** ("probably the feature most cursed by people trying to build L4-based systems … a prime
  example of a kernel-enforced policy … limiting the design space"; degenerated to a chief per process),
  **hierarchical process management** (task IDs handed out first-come; the initial process grabbed them all),
  per-process kernel heaps / σ1 kernel pager ("only shifts the problem"), assembler, C++.
  *Unresolved:* "principled, policy-free control of CPU time" — the scheduler is "the last major holdout of
  policy in the kernel"; multicore under verification (big lock or clustered multikernel with no memory
  migration between kernels).
- **Evidence:** one-way IPC 0.09 µs (301 cycles) on Haswell; seL4 still ~10 kSLOC after 20 years; billions of
  deployments (Qualcomm modem firmware, Apple secure enclave); recursive mapping database consumed 25–50% of
  kernel memory in real use; verification "has no significant drawbacks" and proof maintenance scaled with
  implementation change.
- **What failed / critiques:** the paper *is* the critique of original L4; residual disagreement in the
  community on recursive address spaces (Dresden retains) and kernel memory (quota vs user-level control).
- **Lesson for Mini:**
  - *What to drop before building it:* (1) **No per-call timeouts** on Mini method calls; awaits are either
    "poll" or "block", and time is a separate first-class event source (a clock/timer object a resident awaits
    on). (2) **No hierarchy baked into the kernel** — no "parent object may intercept children's calls" rule,
    no domain tree as an authority structure; use membranes (capability interposition) instead. Mini's
    multi-party domains should be named by capabilities, not by a kernel-known containment tree. (3) **No
    large payloads in calls** — a Plan action carries small typed values plus capabilities to content-addressed
    blobs/cells (Mini's Merkle store makes pass-by-reference free and integrity-checked).
  - *Fork 1:* call targets should be **endpoints/facets, not raw cell ids**. A cell may export several
    endpoints (facets) with badges; the callee sees the badge, not the caller's identity. Global cell ids as
    call targets would recreate L4's thread-id problems (structure leak, covert channels, no interposition).
  - *Fork 3:* notifications are the right primitive for "a resident awaits several things": a resident cell has
    one inbox plus a notification word; resume is triggered by either. This is smaller and more proven than
    "several activities per object". Multicore lesson: parallelism comes from *partitioning* (clustered
    multikernel, no migration), not from fine-grained concurrency inside the verified core — i.e. Mini should
    get deterministic parallelism by running disjoint-footprint turns concurrently (optimistic, footprints
    declared or recorded) or by sharding domains, keeping each turn's semantics sequential.
  - *Metering:* time remained unprincipled for 20 years; the resolution (next entry) is capability-based.

#### Scheduling-Context Capabilities — time as a first-class, donated, revocable capability (seL4 MCS)
- **Cite:** Lyons, A., McLeod, K., Almatary, H., Heiser, G. (2018). *Scheduling-Context Capabilities: A Principled,
  Light-Weight Operating-System Mechanism for Managing Time*. EuroSys '18. https://doi.org/10.1145/3190508.3190539 ;
  https://trustworthy.systems/publications/csiro_full_text/Lyons_MAH_18.pdf .
  Local: ~/paperbin/world-program-model/lyons-scheduling-context-caps-2018.{pdf,txt}. **[READ]**
- **OS-level decisions:** a *scheduling context* (SC) is a kernel object holding budget C and period T (sporadic
  server replenishment); a thread runs only with an SC that has budget; creating SCs needs Untyped, but setting
  a non-zero budget needs the per-core `sched_control` cap (admission control is a capability). Priority stays a
  thread attribute (orthogonal to SC). **SC donation**: a client calling a *passive* server (no SC of its own)
  lends its SC; "time consumed by the server is billed to the client"; donation chains are tracked by explicit
  **Resume objects** ("modelled after KeyKOS"), replacing seL4's magic reply slot. Budget exhaustion raises a
  **timeout exception** to a per-thread handler — "the temporal equivalent to a (spatial) protection exception
  handler" — which may give an emergency budget, extend, raise system criticality, kill, or **roll the server
  back** to its last consistent state and reply on its behalf. Passive servers at the ceiling priority give the
  immediate priority-ceiling protocol "essentially free". Criticality switches and EDF are *user-level*
  policies over the mechanism. They explicitly distinguish KeyKOS meters: "the KeyKOS model treats time as
  fungible, with no guarantee of when the time will be provided"; time capabilities "cannot support
  hierarchical delegation without loss, and cannot be recursively virtualised" (Mark Miller's real-estate
  analogy).
- **Evidence:** overheads vs base seL4: call +21% ARM / +1% x64, replyRecv +8% / +4%, schedule +45% / +38%;
  Redis YCSB within ~1% of base; UDP latency bounded exactly by a co-located Linux VM's budget; timeout-handler
  actions cost 1–24 µs; ~2,000 lines added (14%); spec in a verification branch, proof in progress.
- **What failed / critiques:** passive-server rollback requires servers to keep double-buffered consistent state
  (application burden); time-capabilities lose utilisation under hierarchical delegation; user-level
  criticality switch is linear in thread count.
- **Lesson for Mini:**
  - *Metering — this is the design to copy for "who pays for a call":* Mini's objects called by a method call
    are *passive servers*: the callee executes under the caller's meter (meter donation along the call chain,
    tracked by the one-shot reply/resume capability). A resident with its own meter is an *active server* and
    runs "for free" from callers' view. That gives a precise answer to fork 1's billing question and is
    compatible with "each resume is one admitted, paid turn" (the resumer donates or the resident pays).
  - *Fork 5 / rollback is free in Mini:* the most expensive seL4 recovery (roll a shared server back to a
    consistent state) is *Mini's default*: a turn that runs out of fuel aborts atomically and nothing is
    written. Mini should advertise this and *not* add partial-progress semantics to calls. What Mini should add
    is the **timeout/out-of-fuel keeper**: the refused Plan (or fuel exhaustion) is reported to a handler cap
    designated by the caller's meter, which may top up and retry — the meter keeper of KeyKOS, the timeout
    handler of seL4 MCS.
  - *Admission as capability:* creating meters is free (from a bank), but *granting budget* needs a capability
    to a parent meter with budget — seL4's `sched_control`. Mini's genesis holds the root meter; committees or
    domains receive sub-meters.
  - *Where Mini differs:* Mini's fuel is fungible (re-execution steps, no deadlines), so KeyKOS-style fungible
    meters suffice for safety; seL4's periodic budgets matter only if Mini wants *rate* fairness (a resident
    may not consume more than C fuel per T blocks of a committee's capacity). That is the right tool for
    protecting a shared committee from one hot resident and should be an SC-like `(budget, period-in-heights)`
    on the meter, enforced at admission.

---

### 3.4 Fuchsia / Zircon

#### Zircon kernel objects, handles, jobs; Component Framework v2 capability routing and per-component namespaces
- **Cite:** Fuchsia authors (Google) (accessed 2026-10-04). *Zircon kernel concepts*
  https://fuchsia.dev/fuchsia-src/concepts/kernel/concepts ; *Handles* …/concepts/kernel/handles ; *Job*
  …/reference/kernel_objects/job ; *Capabilities* …/concepts/components/v2/capabilities ; *Namespaces*
  …/concepts/process/namespaces ; *Component topology* …/concepts/components/v2/topology ; *Realms*
  …/concepts/components/v2/realms ; *Life of a protocol open* (truncated page).
  Local: ~/paperbin/world-program-model/fuchsia-*.{html,txt} (8 pages, ~7,200 words). **[READ for these 8 pages;
  SKIMMED for Fuchsia as a whole — no papers, no retrospectives, FIDL/versioning docs not read]**
- **OS-level decisions:**
  - *Kernel:* objects accessed "almost exclusively via Handles" (per-process 32-bit integers; kernel-side
    (object, rights, owning process)); rights can only be reduced on duplicate/replace; handles move between
    processes by being written into a Channel (they are "in transit", owned by the kernel, and are closed if the
    channel end dies). Objects are refcounted and die with the last handle. 64-bit koids never reused. Three
    syscall classes: a *very few* with no limitation (`zx_clock_get_monotonic`, `zx_nanosleep` — i.e. the clock
    is ambient), handle-taking calls (the vast majority), and object-creating calls whose permission comes from
    the **Job** policy of the caller's process. Jobs form a tree (root job → userboot) that tracks privileges
    and limits memory/CPU; "without a Job Handle, it is not possible … to create another Process or another
    Job". Waiting: up to 32 *signals* per object; wait_one/wait_many/**Ports** (objects bound to a port deliver
    signal packets). Channels: datagram, bounded message size and handle count, no short reads.
  - *Component framework (v2):* every component gets its **own namespace** ("There is no global 'root'
    namespace"; "Object paths may not be meaningful across namespace boundaries"); you can only open objects
    reachable from objects you already hold — "There is no ambient authority"; names belong to the container,
    "Objects are fundamentally nameless". Capabilities are declared in a manifest — `use`, `offer` (to a child or
    collection), `expose` (to parent), `capabilities` (provided) — and the framework populates namespaces only
    along **valid routes**; routes form a graph over a **parent-owns-child instance tree**; cycles are rejected
    unless an edge is marked `weak`; realms are encapsulation and ownership boundaries ("children … cannot be
    reparented and they cannot outlive their parent"). Static children can be audited and statically routed;
    dynamic children (in collections) cannot be statically routed. `/pkg` is the component's package as signed.
- **Evidence:** production on Google Nest devices (not stated in these pages — omitted as a claim). Docs only.
- **What failed / critiques:** not read here (no retrospective found within budget). Observable from the docs:
  Fuchsia *re-introduced a hierarchy* (realm tree, parent-owned children, routing through ancestors) one level
  above a capability kernel — the very thing L4 abandoned in-kernel; the docs carry multiple "TODO"s around
  aggregation from collections, signalling unfinished design for dynamic topology.
- **Lesson for Mini:**
  - *Naming / fork 4:* the manifest is the part to copy. A Mini package should declare `uses` (capability
    *types* it expects to be handed, by interface) and `exposes` (endpoints/facets its objects publish), so that
    governance can audit routes *statically* before an upgrade is admitted, and so that a typed migration
    (fork 4) can check that the new version's `uses/exposes` are compatible with the live wiring. Cheap: a
    declaration section in `.obend` packages plus a checker.
  - *Naming:* per-component namespaces built from handles are a *view*, not a store. AGREES with keeping one
    global content-addressed Merkle store for *packages and data identity*, while each object sees only the
    names its creator wired in (a per-object "namespace" = a record of caps in its state). DISAGREES with any
    global path namespace for mutable cells.
  - *Security kernel / determinism:* Zircon leaves the clock ambient. Mini must not: time enters a turn only as
    an admitted input (the block height / committed timestamp) or via a time capability — required anyway for
    deterministic re-execution.
  - *Structure:* Fuchsia's parent-owns-child realm lifetime ("cannot outlive their parent") is a policy L4 found
    too rigid in-kernel; Mini should keep lifetime governed by *banks* (destroy the bank ⇒ everything bought
    from it dies, KeyKOS/EROS) rather than by a structural parent tree.

---

### 3.5 Plan 9 and Inferno

#### The Use of Name Spaces in Plan 9 — per-process name spaces assembled from served trees
- **Cite:** Pike, R., Presotto, D., Thompson, K., Trickey, H., Winterbottom, P. (1992/1993). *The Use of Name Spaces in
  Plan 9*. Proc. 5th ACM SIGOPS European Workshop; reprinted OSR 27(2):72–76, 1993. https://9p.io/sys/doc/names.html .
  Local: ~/paperbin/world-program-model/pike-plan9-names-1992.{html,txt}. **[READ]**
- **OS-level decisions:** two ideas: "every resource … is represented by a hierarchical file system" and "a user or
  process assembles a private view of the system by constructing a file name space". 9P: 17 messages
  (auth/attach/clone/walk/open/read/write/stat/wstat/create/remove/clunk …); no caching in the protocol
  (caching is an interposed file server). The *mount device* is "the sole bridge" to remote/user-level
  services — "in effect a proxy object"; no RPC stub compiler. `mount(fd, old, flags)`, `bind(new, old, flags)`,
  union directories; `rfork` bits choose whether the child *shares* or *copies* the name space. "Although there
  is no global name space, for a process to function sensibly the local name spaces must adhere to global
  conventions." Interposition by name space: `iostats` runs a process in a local name space that monitors its 9P
  traffic; `8½` (window system) serves `/dev/cons` etc. separately to each window and can run inside itself;
  `import`/`cpu` move pieces of name space across machines. The daily *dump*: at 5 AM dirty blocks go COW, a new
  read-only root named by date appears (`1995/0314`) and is browsable with ordinary tools.
- **Evidence:** kernel 25,000 lines C (SGI MP), <1,500 machine-specific; X under 8½ remotely at ~10% graphics
  degradation; 350 GB WORM file server.
- **What failed / critiques (theirs):** some things refuse the file metaphor: process creation ("too intricate to be
  described easily in a simple I/O operation"), network name spaces, shared memory ("a representation in the file
  system would imply that memory could be imported from remote machines").
- **Lesson for Mini:**
  - *Naming:* Plan 9's answer to "per-process name spaces vs a global store" is **both, layered**: a global store
  (the file server; its dated, immutable roots) plus per-process *views* built by binding. Mini should do the
  same: the Merkle store is the global, content-addressed substrate (Plan 9's WORM dump is literally a sequence of
  committed roots browsable by date — Mini gets that for free from its root history), while each object/resident
  sees only a *local name table* (a Core4 record of capabilities its creator wired in). "Local names, global
  conventions": standard slot names (`self`, `bank`, `meter`, `clock`, `inbox`) are conventions, not kernel
  authority.
  - *Interposition as the debugging and policy tool:* `iostats` and 8½ show that when every access goes through a
  name the parent bound, the parent can interpose anything (monitoring, caching, sandboxing) with no kernel
  feature. Mini analogue: a resident created with forwarder caps in its table can be monitored/metered/mocked by
  its creator. AGREES with the uniform `Invoke(cap,msg)` lesson from EROS.

#### Plan 9 from Bell Labs — the system overview, including what they'd do differently
- **Cite:** Pike, R., Presotto, D., Dorward, S., Flandrena, B., Thompson, K., Trickey, H., Winterbottom, P. (1995).
  *Plan 9 from Bell Labs*. Computing Systems 8(3):221–254. https://9p.io/sys/doc/9.html .
  Local: ~/paperbin/world-program-model/pike-plan9-1995.{html,txt}. **[READ]**
- **OS-level decisions:** three principles: resources are files; one protocol (9P); "disjoint hierarchies … joined
  together into a single private hierarchical file name space". "Plan 9 has local name spaces that obey globally
  understood conventions; it is the conventions that guarantee sane behavior." 9P is stateful (fids), byte-level;
  qid = (path, version) where version changes on every modification (used for cache coherence). Each window gets
  its own name space; `rfork` bit vector for fine-grained sharing; `rendezvous(tag,value)` as the only kernel
  sync primitive; blocking I/O handled by "satellite processes" rather than `select`. Authentication is between
  *users*, bilateral, with a *speaks-for* relation on the auth server (how a CPU server acts for Peter). No
  super-user: the file server's `adm` can configure disks but "not … modify, examine, or change the permissions of
  any files". Guest users get a restricted name space ("a kind of cage"). Data between architectures is text or
  explicitly serialised fields — "the structure is never communicated as a unit".
- **Evidence:** 50 users over 5 years consumed 65% of a 350 GB WORM; "there is no backup system as such"; terminals
  last ~5 years; ps is 95 lines of C. "It is fair to say that the Plan 9 kernel is primarily a 9P multiplexer."
- **What failed / critiques (theirs, "What would we do differently"):** streams unused, should be static queues; the
  separate file-server kernel duplicated drivers and bugs; the WORM held metadata and was the least reliable part;
  and — most relevant — "Although Plan 9 has per-process name spaces, it has **no mechanism to give the
  description of a process's name space to another process** except by direct inheritance" — `cpu` cannot
  reproduce the terminal's name space. Also: dump permissions are frozen forever — "if the file is readable but
  should have been read-protected, it is readable forever". And "it is possible to push the idea of file-based
  computing too far … metaphors can be abused" (`/proc` is "only a view of a process, not a representation").
- **Lesson for Mini:**
  - *Naming (fixes Plan 9's regret by construction):* in Mini an object's "name space" is a value (a record of caps
    in Core4 state), so it *is* transmissible and checkpointable — the thing Plan 9 lacked. Make that explicit:
    a resident's environment is a first-class typed record, passed whole to children or to a migration.
  - *Presentation:* 9P's lesson is that a **fixed, small, universal protocol** every resource speaks lets generic
    tools (ls, cp, grep, the dump) work on everything. Mini's "presentation = projection" should be such a
    protocol: every object answers a fixed set of meta-methods — `describe` (typed view for this viewer),
    `affordances` (methods this viewer may invoke, with argument types), `history` (roots/versions) — so that web,
    Discord and AI-resident renderers are *generic clients*, as 8½/ftpfs/exportfs are generic servers. Plan 9's
    "reducing 'object' to 'file' gets technology for free" is the argument for a fixed meta-protocol over
    per-class UIs. Cost: one interface every package must implement (defaultable from type info).
  - *Persistence / privacy:* an immutable history (WORM dump, Merkle root history) makes every past permission
    mistake permanent. Mini must treat "published state is forever" as a design constraint for laws on confidential
    cells (encrypt-before-commit or keep secrets out of the replicated store); revocation never retracts the past.
  - *Versioning:* qid.version per file is the cheap cache-coherence handle. Mini cells should carry a monotone
    version (or the cell's subroot hash) so presentations and optimistic concurrency (fork 3) can detect staleness
    without reading content.

#### The Inferno Operating System — Plan 9's ideas in a type-safe VM language (Limbo/Dis/Styx)
- **Cite:** Dorward, S., Pike, R., Presotto, D. L., Ritchie, D. M., Trickey, H., Winterbottom, P. (1997). *The Inferno
  Operating System*. Bell Labs Technical Journal 2(1):5–18 (Vita Nuova revision).
  https://www.vitanuova.com/inferno/papers/bltj.html . Local: ~/paperbin/world-program-model/dorward-inferno-1997.{html,txt}. **[READ]**
- **OS-level decisions:** a *language-based* OS: applications in Limbo, compiled to Dis bytecode (3-address VM, JIT),
  "fully type-checked at compile- and run-time", running safely "on a machine without memory-protection
  hardware"; same binary everywhere; runs native or hosted on Unix/Windows/Plan 9. Plan 9's three principles with
  Styx as the protocol. **Modules are loaded explicitly and type-checked at load**: `sys = load Sys Sys->PATH`
  returns nil "if the implementation" does not match "the specified type"; several implementations may serve one
  interface; programs choose load/unload policy. Typed CSP **channels** (can carry channels) connect tasks and can
  be attached to files for cross-machine communication; `alt` selects. GC is refcount + background cycle sweep so
  resources (windows, fds) are freed "the instant the last reference to it has gone away". Security: "resources
  available to applications appear exclusively in the name space of the application … if the network resources
  are removed from an application's name space, then it is impossible for it to establish new network
  connections"; adding servers to a name space is an authenticated operation; object modules may be signed.
- **Evidence:** ran in 1 MB without an MMU; deployed in a Lucent IP switch/router and a firewall (Signet).
- **What failed / critiques:** none stated in the paper (a product launch paper). INFERRED/well known but not read
  here: Inferno did not achieve its commercial target market and was sold to Vita Nuova; tagged INFERRED, not cited.
- **Lesson for Mini:**
  - *Fork 4 / packages:* Limbo's `load T path` — bind an implementation to a variable *only if* its interface type
    matches the declared module type, else nil — is the right primitive for Mini's pinned packages: an object's
    reference to a package is `(interface type, package hash)` and (re)binding to a new hash is admitted only if the
    certifying checker shows the new package implements the interface. That turns "governed upgrade" into a typed
    rebind plus a state migration, with the interface check done by the existing checker.
  - *Security kernel:* Inferno is the closest historical precedent for Mini's stance (safety from the language, not
    hardware; authority from what is in your name space). It confirms the model is buildable small, and warns that
    language safety alone is not authority control — Inferno still needed the name-space restriction to deny
    network access. Mini needs both the type system *and* caps-only reachability.
  - *Fork 3:* typed channels + `alt` is a proven, small concurrency vocabulary for "a resident awaits several
    things": Mini's `await` should be an `alt` over typed sources (reply caps, inbox, clock), each with its declared
    response type — matches the Activity<P,R,A> typing.

---

### 3.6 Orthogonal persistence

#### Orthogonally Persistent Object Systems — the principles, PS-algol/Napier88, and the evolution problem stated
- **Cite:** Atkinson, M., Morrison, R. (1995). *Orthogonally Persistent Object Systems*. VLDB Journal 4(3):319–401.
  https://www.vldb.org/journal/VLDBJ4/P319.pdf . Local: ~/paperbin/world-program-model/atkinson-op-object-systems-1995.{pdf,txt}.
  **[READ]** (§1–7 read; reference list skimmed)
- **OS-level decisions:** three principles — *persistence independence* (code looks the same for short- and
  long-lived data), *data type orthogonality* (every type may persist), *persistence identification by
  reachability* from roots (persistence is GC's dual). A lifetime table runs from "transient results in
  expression evaluation" to row 7 "data that outlives a succession of versions of such a program" and row 8
  "data that outlives versions of the persistent support system". Type safety across the store boundary via an
  infinite-union type (`any`/`dynamic`/`pntr`): the store root is `any`; programs `project … onto` a specific
  type at a few *dynamic checking points*; this lets a program specify "only the part of the schema that they
  require" and "permits localization of schema changes to subgraphs delimited by these points". Binding has
  four axes (L/R-value, time, scope, type-check time); *hyper-programming*: source programs contain direct
  links to persistent values (code and data alike), so source is "non-flat". *Octopuses*: breaking a value's
  bindings into a "wiring diagram" so it can be rebound when moved to another store. Type-safe linguistic
  reflection (compile-time generators and run-time compile+link) as "the basis for system evolution".
  Concurrency: CACS views coordination as movement of data among access sets, so the same data can be in an
  ACID transaction one day and a cooperative computation the next. Distribution: location transparency "does
  not scale indefinitely, fails to accommodate change, and does not have a realistic approach to failures";
  "an important reason for distribution is ownership" (autonomy).
- **Evidence:** a survey; systems listed: PS-algol (1980), Napier88 (1988, v2 1994), Galileo, Amber, Tycoon,
  Fibonacci, persistent C++s; the authors concede: "none of the systems that build up persistence from the
  operating system kernel have received enough developmental effort to enable them to support such
  experimentation" and persistence researchers "have a particularly difficult time verifying that their
  approaches to scale and evolution will actually work".
- **What failed / critiques (theirs):** evolution is the open problem: "It would be unwise for any enterprise to
  commit seriously to a technology purporting to support persistence if they were not confident that it
  adequately could support schema change. Where persistent systems have imprecise type knowledge (e.g., those
  based on C and C++), it is doubtful whether there is enough information to safely support change." Needed but
  missing in 1995: change notations, efficient propagation to instances, dependency/impact analysis, and
  automated "change absorbers" (views, ADTs). Closed-world assumption is "unrealistic".
- **Lesson for Mini:**
  - *Fork 4:* Mini already has the precondition they say is necessary — precise types for every stored value
    (Core4 + certifying checker). The `any`-projection idea maps onto Mini as **typed interface boundaries
    between packages**: a cell's state type is private to its package; other packages see it only through the
    package's exported interface (an existential, in their own terms "abstract witness"). Then a schema change
    inside a package needs a migration only for that package's own cells, and is invisible to clients unless the
    interface changes — i.e. existential types are the "change absorbers". Concretely: the checker enforces that
    no package's code pattern-matches on another package's state constructors.
  - *Fork 4 / naming:* hyper-programming = Mini packages that reference other packages and cells *by hash and
    capability*, not by name. Mini gets referential integrity for free from content addressing — but that also
    means a package pins *old* code forever unless upgrade is explicit. Octopus-style "wiring diagrams" are the
    right model for an upgrade: the new package version declares its dependencies as parameters, and governance
    re-wires them.
  - *Fork 3:* CACS's "same data, different concurrency regimes at different times" argues for laws, not
    language constructs, to state the concurrency contract on a cell (exclusive, commutative-merge, append-only),
    so a cell can move between regimes by law upgrade.
  - *Distribution:* AGREES with Mini keeping multi-party domains *explicit* (ownership/autonomy) rather than a
    location-transparent global heap.

#### PJama review — the most honest post-mortem of orthogonal persistence in a mainstream language
- **Cite:** Atkinson, M., Jordan, M. (2000). *A Review of the Rationale and Architectures of PJama: a Durable,
  Flexible, Evolvable and Scalable Orthogonally Persistent Programming Platform*. Sun Microsystems Laboratories
  TR SMLI TR-2000-90. https://web.archive.org/web/2005id_/http://research.sun.com/techrep/2000/smli_tr-2000-90.pdf .
  Local: ~/paperbin/world-program-model/atkinson-pjama-review-2000.{pdf,txt}. **[READ]** (all 16 chapters and Appendix A)
- **OS-level decisions:** a modified JVM (PJVM) + the Sphere object store; API of ~6 classes
  (`OPRuntime.checkpoint/suspend/halt/roots`, listeners). Persistence by reachability including `Class` (so the
  store is "self-describing and consistent" — behaviour persists with state) and, aspirationally, `Thread`.
  *Resumable programming*: checkpoint/shutdown/resume listeners re-establish external state (sockets, GUI,
  JDBC) on resume. One store per VM, one VM per store ("to prevent a requirement for multi-store commit
  protocols and an unmanageable tangle of inter-store references"). Objects, not pages; ARIES logging;
  indirection everywhere (descriptors, partition map, indirectory) to make evolution and GC incremental.
  *Evolution* (§8): developer edits classes with ordinary tools; a checker verifies the *set of changes is
  complete* and that the final state complies with the JLS (all surviving classes still find the members and
  signatures they use); every replaced class with instances needs a default or developer-written
  transformation that reads an undisturbed **old world** and writes a **new world**, merged atomically; crash
  ⇒ roll back or roll forward. Distribution kept explicit (PJRMI with sessions and leases bounding a store's
  liability for exported references).
- **Evidence:** ~160 evaluation licences; stores up to 5 GB, 60 M objects, a 34 MB single object; evolution
  applied to stores with 60 M objects to transform; ~15% average execution overhead from software barriers
  (9% on pBOB); effort Oct 1995–Apr 2000: **427 engineer-months**, of which *Migration (tracking JDK releases)*
  65, *Evolution* 41, *Transactions* 40, *Durability* 37, *Evaluation* 82. Table 9.1: JDK 1.1.7→1.2 added 3,291
  classes, changed 1,256, and 338 classes required *instance reformatting*.
- **What failed / critiques (theirs):**
  - *Evolution and migration are prerequisites of durability:* "The absence of either evolution technology (E)
    or migration technology (F) results in stores having to be discarded so that the application can change to
    meet new requirements. This causes a complete failure of durability." "Without a mechanism for handling this
    the persistence platform is useless."
  - *Deployed evolution was never solved:* their mechanism is off-line, stop-the-world, development-only;
    deployed evolution (shipping a release to customer stores containing data, customer classes and older
    versions, applied incrementally while in use) "still require[s] research" (Challenges 5–7).
  - *Platform upgrades broke stores:* "Whilst programs have ported straightforwardly to new versions of PJama
    they have not been able to continue using the same stores", because internal C/disk structures "are not
    described in a way that would guide transformation" — only a stop-the-world *logical archive* (reflection
    walk to a canonical, platform-independent form) could carry data across.
  - *Library churn:* "those who provide class libraries must provide evolution transformations corresponding to
    releases. This takes significant time and resources which language developers do not factor into their
    planning."
  - *Threads:* persisting `Thread` was never achieved compatibly with evolution and migration; "threads would
    have to progress to an extractible-point and then halt. Any other model seems impossible to reconcile with
    evolution (E) and migration (F)"; evolution "requires enough information to rearrange the stack when a
    method changes, or to inhibit such a change". Without persistent threads, a checkpoint by one thread could
    capture another's broken invariants, forcing a "do not checkpoint here" API — a violation of persistence
    independence.
  - *Orthogonality gaps cascade:* a few non-persistable classes (AWT) re-introduced "two models and the
    translation code … Two models are precisely what we set out to eliminate!"
  - *Adoption:* the OPJ JSR was rejected on the argument that JDO subsumes it (§13); habits from file/DB
    persistence made porting existing programs hard, while in-memory programs ported easily. The paper does not
    claim schema evolution "killed" PJama; it shows evolution + platform migration as the dominant unsolved costs
    and the hypothesis never independently tested.
- **Lesson for Mini:** this is the central entry for forks 4 and 5.
  - *Fork 5 — Mini's design already sits where PJama said it had to go:* activities persist only at **yield
    points** (PJama's "extractible-points"), never mid-turn. Keep it that way: no checkpoint of an arbitrary
    machine state; the Core4 checkpoint codec is applied only to a yielded activity whose continuation has a
    declared resume type. This is precisely what makes evolution of suspended computations *possible* at all.
  - *Fork 4 — what the typed migration must contain (PJama's checked list, adapted):* an upgrade package =
    (new package hash, migration functions, proof obligations). Admission checks: (1) **completeness** — every
    cell type that changed format has a migration function or provably no live instances (Mini can know this
    exactly: the store is a Merkle map, so the population of cells pinned to the old hash is enumerable);
    (2) **closure** — every other package that depends on the upgraded one still typechecks against the new
    interface (or the upgrade is refused); (3) **suspended activities** — for each live resume-point of the old
    package, either the new package provides a resume-point mapping (old continuation type → new) or the
    upgrade waits/refuses ("inhibit such a change"); (4) **old-world/new-world semantics** — migration functions
    are pure Core4 functions from the old state (read-only, undisturbed) to the new, run inside one admitted
    turn per cell or per batch, with the cell's law judging the new state. Cost: the checker work (exists) + a
    migration runner + an enumeration index of cells by pinned package hash.
  - *Fork 4 — deployed evolution:* Mini is "deployed evolution" from day one (many owners' cells pin the same
    package). PJama's unsolved Challenge 6/7 suggests Mini should **not** do global eager migration: each cell
    migrates *lazily on first touch* (admission sees pinned hash ≠ governing current hash → runs the migration
    in the same turn), with multiple versions coexisting, and with owners able to decline (cell keeps its old
    pinned package). Laws decide who may re-pin.
  - *Fork 5 — platform migration:* PJama could not carry stores across its own platform versions because
    internal representations were undescribed. Mini's exact checkpoint codec is such an internal representation.
    Make Core4's checkpoint format a **described, versioned, canonical form** (a schema-carrying codec) and
    keep a `decode_vN → encode_vN+1` translation as a checked function — or adopt the repo's re-genesis
    doctrine explicitly for Core4 machine changes: old checkpoints refuse to load, residents must be drained to
    a quiescent (data-only) state before a Core4 epoch bump. Either is honest; silently reinterpreting is not.
  - *Stdlib churn:* whoever publishes Mini's standard packages must ship migrations with each release; budget for
    it (PJama's largest single cost line was tracking the platform).
  - *Openness:* PJama's resume listeners for external state are Mini's "awaits": every external interaction is a
    typed await with an explicit re-establish/refusal path. Mini's determinism already forces this; PJama shows
    it is the right shape and that partial coverage (a few non-persistable types) is poison — every value Core4
    can construct must be checkpointable, with no exceptions.

#### Grasshopper — an orthogonally persistent OS: containers, loci, capabilities, managers
- **Cite:** Dearle, A., di Bona, R., Farrow, J., Henskens, F., Lindström, A., Rosenberg, J., Vaughan, F. (1994).
  *Grasshopper: An Orthogonally Persistent Operating System*. Computing Systems 7(3):289–312.
  https://www.usenix.org/legacy/publications/compsystems/1994/sum_dearle.pdf ; preprint
  https://archive.cs.st-andrews.ac.uk/gh/pub/gh-03.pdf . Local: ~/paperbin/world-program-model/dearle-grasshopper-1994.{pdf,txt}
  and dearle-grasshopper-gh03.{pdf,txt}. **[READ]** (preprint text read in full; journal version checked identical in substance)
- **OS-level decisions:** motivation: persistence above a conventional OS "has proven to be poor; researchers
  invariably construct a complete abstract machine above the operating system". Three abstractions: *containers*
  (the only storage abstraction, replacing address spaces and files; fully partitioned — no global address
  space), *loci* (persistent threads; "making the locus persistent … frees the programmer from much
  complexity"), *capabilities* (segregated, in per-container and per-locus lists; chosen over password caps so
  the kernel can garbage-collect by reference count). Containers are composed by DAG-shaped *mappings*; loci get
  private *invocation mappings* (per-locus stacks). Communication is **procedure-oriented**: a locus *invokes* a
  container at its single entry point (Lauer–Needham duality; they argue messages are less flexible). *Managers*
  (user-level, Mach-pager-like) supply container pages and implement each container's stability algorithm,
  including swizzling, encrypting and compressing managers. Global consistency: rather than stop-the-world, the
  kernel tracks causal dependencies among containers, loci and kernel data ("associates") and stabilises an
  associate set with two-phase commit; the kernel itself persists.
- **Evidence:** design paper; prototype "still under construction" (Sun 3/60, then DEC Alpha). No measurements.
- **What failed / critiques:** Shapiro & Adams (2002) call Grasshopper's transitive-dependency strategy "both
  complex and expensive"; Atkinson & Jordan (2000) list Grasshopper among persistent OSes that never hosted the
  applications needed to test the OP hypothesis and "have insufficient information about an application's data
  to perform disk-space reclamation, evolution and migration" (they are type-blind).
- **Lesson for Mini:**
  - *Fork 5:* the *associates* idea (stabilise only the causally connected subset) is what Mini's per-turn commit
    achieves trivially inside one domain; it reappears in Mini only for **multi-party atomicity across domains**
    (fork 3), where the set of domains a turn touched is exactly a Grasshopper associate set and needs a 2PC-like
    commit. Lesson: keep cross-domain turns rare and explicitly declared (the Plan names its foreign domains up
    front), because the general dependency-tracking version was the part of Grasshopper judged too costly.
  - *Persistence substrate typing:* the critique that a type-blind persistent OS cannot do evolution or GC is a
    strong argument FOR Mini's choice to make the store Core4-typed (cells hold typed values, not pages). DISAGREES
    with any proposal to let objects hold opaque byte blobs as primary state.
  - *Fork 1:* Grasshopper's procedure-oriented invocation (thread moves into the callee) vs KeyKOS's message model
    maps to Mini's "passive server executes under the caller's turn" vs "active resident with its own inbox".
    Mini needs both, and the seL4 MCS scheduling-context work shows how to bill each.

#### Practitioner post-mortem: Electric Communities' orthogonal persistence (KeyKOS-inspired) — "save it all" was the mistake
- **Cite:** Morningstar, C. (2006). *Smart people can rationalize anything*. Habitat Chronicles blog, 22 Dec 2006.
  https://habitatchronicles.com/2006/12/smart-people-can-rationalize-anything/ ; found via Hacker News thread
  https://news.ycombinator.com/item?id=603826 (comment 604837, 2009). Corroborating practitioner comment: K. Varda
  (`kentonv`, Cap'n Proto/Sandstorm), HN 2019-04-18, item 19692198: "the other classic problem with 'Orthogonal
  Persistence' is that it becomes nearly impossible to upgrade your software. All your existing data is locked to
  the old version forever (or until some sort of 'migration' can be performed — which requires a way to dump the
  data, which you may or may not have)." Local: ~/paperbin/world-program-model/morningstar-smart-people-rationalize-2006.{html,txt}.
  **[READ]** (the essay section; HN comment read via Scry)
- **OS-level decisions:** Electric Communities (the E/ocap lineage) built an orthogonal-persistence mechanism for its
  distributed object framework, explicitly inspired by KeyKOS ("we were inspired by … KeyKOS").
- **Evidence / what failed (verbatim):** "for most kinds of objects, the amount of state you actually need to save
  persistently is a small fraction of the full run-time state of the object. But in an orthogonal scheme you save
  it all, indiscriminately. The problem is not so much that it's bulky, though it is, but that the volume of
  semantic meaning that you are now committed to maintain in near-perpetuity is vastly increased. That turns out to
  be very expensive. The problem of schema migration as new versions of objects were developed … proved
  effectively intractable. Ultimately we fell back on a scheme that compelled programmers to be much more
  deliberate about what state was checkpointed, and when." Cost: "literally years of development resources".
- **Lesson for Mini (fork 4/5 — the sharpest warning in this lane):** an *exact checkpoint codec of the whole
  machine state* for residents is the EC design, and EC's verdict is that it multiplies the "semantic meaning …
  committed to maintain in near-perpetuity". DISAGREES with making the full Core4 machine state the long-lived
  persistent form. Pushes: (a) residents' durable state = declared, typed cell data (EC's "deliberate about what
  state … and when"); (b) the continuation checkpoint is *short-lived* by policy — bounded number of turns or
  bounded height-span, after which the resident must yield at a declared quiescent resume point whose type is
  part of the package interface; (c) the exact codec remains (it is what makes yield/resume and re-execution
  exact) but is treated as a cache-like, epoch-tagged artefact, not an archival format. Same conclusion as
  Motoko (next) and PJama ("extractible points").

---

### 3.7 Modern single-level stores and data-centric OSes

#### Twizzler — data-centric OS for NVM: global object IDs, per-object foreign-object tables, no processes
- **Cite:** Bittman, D., Alvaro, P., Mehra, P., Long, D. D. E., Miller, E. L. (2020). *Twizzler: a Data-Centric OS for
  Non-Volatile Memory*. USENIX ATC 2020. https://www.usenix.org/system/files/atc20-bittman.pdf .
  Local: ~/paperbin/world-program-model/bittman-twizzler-2020.{pdf,txt}. **[READ]** (2021 ACM TOS version not read)
- **OS-level decisions:** requirements: "remove the kernel from the persistence path" and "design for pointers that
  last forever". Objects (4 KiB–1 GiB) with 128-bit IDs in a global object space; cross-object pointers are 64-bit
  `FOT_idx:offset` through a **per-object Foreign Object Table** (each FOT entry = object ID *or a name plus a
  resolver function*, with r/w/x request bits) — so objects are *self-contained* and shareable across machines
  without fix-ups, and names are **late-bound** ("references to objects which change over time, e.g. shared
  library versions"). "The Death of the Process": threads + *views* (address-space layout as an ordinary object)
  + *security contexts* (persistent lists of per-object rights, enforced by MMU/virtualisation hardware) replace
  processes. Late-binding of security: a program may request rw but faults only on an actual disallowed access.
  Crash consistency via primitives + `TXSTART/TXEND` logging; a `_resume` entry point after power loss.
- **Evidence:** kernel 5.5 kLOC + 5.7 kLOC arch code; pointer translation 0.4 ns intra-object, 3.2 ns cached,
  27.9 ns uncached; object mapping 13× faster than `mmap`; SQLite up to 4.2× faster than PMDK; YCSB 1.1–2.9×
  faster; unixkv needed 36% more code; unixrbt needed 83 manual pointer conversions.
- **What failed / critiques:** no story for schema/type evolution of persisted structures in the paper (INFERRED
  from absence — the data model is untyped bytes plus pointers); security model "still much to do". Practitioner
  context, INFERRED and not read here: the Optane NVM DIMMs it targeted were discontinued by Intel in 2022.
- **Lesson for Mini:**
  - *Naming:* the FOT is the right shape for a cell's outbound references: each cell carries a small table of
    foreign references, and each entry is *either a pinned identity* (content hash / cell id — Mini's default for
    packages) *or a late-bound name with a named resolver* (for "latest version of X" relationships). Making the
    choice explicit per reference is exactly the knob fork 4 needs (pin vs follow upgrades). Also: put rights on
    the reference entry (Twizzler's per-FOT-entry r/w/x), which is a capability table by another name.
  - *Security kernel:* "security contexts" decoupled from execution contexts AGREES with Mini: authority belongs to
    the cell/activity's caps, not to "the process running the turn".
  - *Fork 5 counterpoint:* Twizzler's main lesson is that kernel-free persistence wins when the *data* is the
    durable thing and threads are disposable; it does not persist threads at all beyond a `_resume` hook. Another
    data point for "durable data, ephemeral continuations".

#### Aurora — a modern single-level store for POSIX: persist the object graph of OS state, every 10 ms
- **Cite:** Tsalapatis, E., Hancock, R., Barnes, T., Mashtizadeh, A. J. (2021). *The Aurora Single Level Store
  Operating System*. SOSP '21. https://doi.org/10.1145/3477132.3483563 ; PDF via
  https://web.archive.org/web/2023id_/https://rcs.uwaterloo.ca/~ali/papers/sosp21-aurora.pdf .
  Local: ~/paperbin/world-program-model/tsalapatis-aurora-2021.{pdf,txt}. **[READ]** (HotOS'21 companion
  tsalapatis-aurora-hotos-2021.pdf downloaded, not read)
- **OS-level decisions:** persistence unit = a **consistency group** (processes persisted atomically, default 100×/s)
  with **external synchrony** (buffer outgoing communication until the checkpoint containing its cause is durable);
  the **POSIX object model**: every kernel object (fd, vnode, socket, SysV shm, process, thread) is persisted as
  its own on-disk object, so sharing relationships are stored, not inferred (contrast CRIU, ">100k SLOC" and "only
  added support for UNIX domain sockets seven years after its initial release"); **system shadowing** (COW shadow
  across all writable VM objects of a group, collapse chain ≤2) to flush concurrently; a COW object store that
  retains execution **history** ("time travel debugging and record/replay"); restore on another machine, with
  PID/TID virtualisation (local vs global IDs) and re-injection of the current vDSO; an API for custom apps
  (`sls_memckpt` atomic region, `sls_journal` WAL, `sls_fdctl` to opt connections out of external synchrony).
  Checkpointing quiesces threads *at the kernel boundary*, restarting sleeping syscalls by rewinding the PC.
- **Evidence:** 9.4 kSLOC SLS + 4.7 kSLOC object store + 2.9 kSLOC FS + 2.1 k lines kernel changes (FreeBSD 12.1).
  Redis 500 MiB: stop time 4.0 ms vs CRIU 462 ms; IO 97.6 ms vs 350 ms. Firefox (198 MiB) incremental stop 1.9 ms.
  Memcached transparent persistence: 9–82% overhead depending on period. RocksDB with the API: **81k SLOC of
  persistence code replaced by 109 SLOC, +75% throughput** with the same guarantees. Stop time is dominated by
  *OS-state complexity* (page tables, number of address-space objects), not memory size.
- **What failed / critiques:** in-paper limitations: active TCP sessions incomplete, and "Aurora currently does not
  support external synchrony" — which contradicts the design section that relies on it (an inconsistency in the
  paper itself; noted, not resolved). Transparent mode costs RocksDB 83% throughput vs ephemeral; tail latency
  hurt by stop times. No discussion of *program upgrade* of a persisted application — restoring a checkpoint
  restores the *same* binary.
- **Lesson for Mini:**
  - *Fork 5:* Aurora's two wins transfer: (1) **persist the object graph with explicit sharing, not per-process
    images** — Mini should checkpoint each activity separately and represent shared state only as references to
    cells (never as duplicated heap), so two residents sharing a value share a cell id; (2) **external synchrony**
    — Mini already has it structurally: nothing leaves the system (outbox messages to off-chain peers, replies to
    clients, Discord posts) until the turn's root is committed. Make it a rule of the Host: effects to the outside
    are emitted only from committed state.
  - *Execution history:* Aurora's retained checkpoint history = Mini's root history; a resident's checkpoints across
    roots give time-travel debugging for free. Worth exposing as a first-class presentation affordance ("show this
    resident's last N states").
  - *Cost shape:* Aurora's stop time tracks *structure count* not bytes. INFERRED for Mini: Core4 checkpoint cost
    will track the number of live closures/thunks at yield more than raw data — another reason to GC at yield and
    to charge by encoded size.
  - *What it does not solve:* Aurora, like KeyKOS, restores the *same program*. Mini's evolution problem is untouched
    by single-level-store engineering; the answer has to come from the language (next entry).

#### Motoko enhanced orthogonal persistence on the Internet Computer — typed stable state, transient continuations
- **Cite:** Bläser, L., Russo, C., Greif, G., Vandersmith, R., Ibrahim, J. (2024). *Smarter Contract Upgrades with
  Orthogonal Persistence*. VMIL '24 (SPLASH workshop). https://doi.org/10.1145/3689490.3690401 ; PDF
  https://internetcomputer.org/whitepapers/Smarter%20Contract%20Upgrades%20with%20Orthogonal%20Persistence.pdf .
  Local: ~/paperbin/world-program-model/dfinity-smarter-upgrades-op-2024.{pdf,txt}. **[READ]**
- **OS-level decisions:** actors (canisters) run atomic, instruction-limited transactions; Wasm main memory is now
  **retained across upgrades**; the heap is self-describing (persistent metadata: stable heap version, the stable
  subset of the main actor, a **type descriptor table** of stable types, GC state). Actor fields are `stable`
  (persist across upgrades by reachability, deep, with sharing/cycles) or `flexible` (re-initialised on upgrade).
  **Stable types exclude function types and futures** ("both function values and future values reference local
  code"); and **"any continuations awaiting inter-actor calls" are transient roots, discarded on upgrade**.
  Upgrade = a governed operation; compatibility checked statically before deploy and dynamically in the upgrade
  transaction: each retained stable variable's old type must be a **subtype** of its new type (implicit,
  representation-preserving migration: add/drop record fields, widen variants, Nat→Int, …; mutable fields only to
  equivalent types); anything else is rejected and needs **explicit migration** in three releases (add new stable
  variable → initialise from old in user code → drop old). A "migration path of last resort": incremental
  self-describing graph serialisation (Cheney-style) split across multiple transactions.
- **Evidence:** upgrade cost constant (tens of thousands of instructions, depends on number of types, not heap size)
  vs the previous serialise-on-upgrade design whose cost grew past 100 billion instructions against a 200 billion
  per-upgrade cap — "leaving the program in an evolutionary dead end, unable to upgrade"; the old serialiser also
  duplicated shared immutable objects and overflowed stacks. Persistence code: 1 keyword in Motoko vs ~17 SLOC per
  benchmark in Rust stable structures; data access orders of magnitude cheaper than stable-memory structures.
  Rust stable structures upgrade 10× cheaper but "only because Rust performs no compatibility check on upgrade and
  is unsafe".
- **What failed / critiques:** their own history is the critique: serialise-on-upgrade hit transaction limits and
  became an evolutionary dead end. Remaining limits: no persisted closures or continuations; type changes beyond
  subtyping need multi-release choreography; paper is by the implementers (no independent evaluation).
- **Lesson for Mini:** the closest living relative of Mini's model (atomic metered turns, governed upgrade, a
  replicated store), and its choices answer forks 4 and 5 concretely:
  - *Fork 4 — adopt the stable/flexible split and the subtype rule:* a Mini package declares which parts of an
    object's state are durable across upgrades and gives them **stable types** (first-order Core4 data and
    capabilities; no closures, no thunks, no activity continuations). Upgrade admission: for each durable field,
    old type ≤ new type ⇒ zero-cost implicit migration; otherwise a typed migration function is required. Mini can
    do better than Motoko's three-release dance because the certifying checker can verify a migration function
    `old → new` inside a single upgrade package.
  - *Fork 5 — continuations are the hard edge:* Motoko simply *drops* pending continuations on upgrade (callers see
    a failure). Mini wants residents with long-running activities, so it must choose explicitly, per resume point:
    **drain** (upgrade waits until no activity of this package is suspended at a non-declared point), **map**
    (the new package supplies `resumeᵥ₁→ᵥ₂` for each declared resume point, typechecked), or **abort** (the
    activity is cancelled with a typed failure delivered to its awaiters). Default should be drain-or-refuse; map
    is the rich option the owner asked for.
  - *Fork 5 — upgrade cost must be O(types), not O(heap):* the serialise-everything design died on the transaction
    limit. Mini's per-cell lazy migration on first touch (see PJama entry) keeps each migration inside one metered
    turn; never require a single turn to migrate a whole population.
  - *Metering:* Motoko's instruction cap per transaction is Mini's `runBounded` fuel; their upgrade dead-end is a
    warning that any operation whose cost grows with total state (GC of a big heap, re-encoding a big checkpoint)
    must be incremental across turns or it will eventually be un-admittable.

---

### Not read (named in the lane brief, honestly skipped)
- Coyotos specification/retrospective (Shapiro et al., 2004–2008): not fetched within budget.
- Aurora HotOS'21 companion (local tsalapatis-aurora-hotos-2021.pdf): downloaded, not read.
- Twizzler ACM TOS 2021 version: not fetched.
- Fuchsia beyond the 8 concept pages (FIDL versioning/"API levels", component lifecycle): not read — so Fuchsia's
  answer to interface evolution is NOT represented here.

### Cluster synthesis (§3)

Read together, these systems are one long experiment in a single question Mini is now answering: *if authority is
only capabilities and state never dies, what must the kernel own, and what breaks first?* The answer across forty
years is consistent, and it is not the thing the systems advertised.

**1. Capabilities-only authority works and stays small; the policy hierarchy is what rots.** KeyKOS (20 kLOC),
EROS and seL4 (~10 kLOC for twenty years) all kept the kernel down to "keys, invocation, keepers". What L4 threw
away after twenty years — clans and chiefs, hierarchical task IDs, IPC timeouts, long IPC, global thread IDs as
targets — were all *kernel-enforced structure or policy*. For Mini: one uniform `Invoke(cap, msg)` action shape,
endpoints/facets (badged) rather than raw cell ids as targets, no per-call timeouts (time is an awaited source),
no containment tree as authority, small typed payloads plus caps to content-addressed blobs.

**2. Exceptional states belong to designated handler objects — this is where rich laws live.** KeyKOS keepers
(domain, segment, meter) and seL4 MCS timeout handlers both turn "the mechanism refused" into a message to an
authorised handler holding a resume/service capability. Mini's law should stay a decidable predicate, but a
refusal (or fuel exhaustion) should route the Plan, the explanation and a one-shot retry capability to a keeper
cell named by the target or the caller's meter. That gives fork 2 its rich form without making laws Turing-complete.

**3. Metering is a capability chain, and calls should donate it.** KeyKOS meters (chain to the prime meter, keeper
on zero, sub-meters) plus space banks (hierarchical storage with bulk reclamation) are exactly "paid turns, storage
charged". seL4 scheduling-context donation supplies the missing rule for fork 1: a passive callee runs on the
caller's budget, tracked by a one-shot resume capability; an active resident pays its own. Every Host-side record
(await registrations, inbox entries) must be retyped from a resource the requester holds (seL4 Untyped), or the
Host is DoS-able.

**4. Whole-system persistence was solved engineering by 1983; evolution never was.** KeyKOS ran processes for
years and EROS never wrote an inconsistent checkpoint. But Landau already warned
that storing "permanent object data in … process registers" makes upgrade something that "must be planned in
advance"; L3 lost every checkpoint when a kernel table changed size; PJama could not carry stores across its own
releases and never solved deployed evolution; Electric Communities found schema migration of "save it all" state
"effectively intractable"; Motoko's serialise-on-upgrade hit "an evolutionary dead end". Mini already has the two
preconditions the OP literature said were necessary — precise types for every stored value and atomic, metered
turns — so it can succeed where they failed only if it adopts their hard-won shape: **durable state is declared,
first-order, typed cell data; continuations are short-lived and persist only at declared yield points.** Upgrades
check old ≤ new (subtyping ⇒ free) or require a checked migration function; migrate lazily per cell on first touch
so cost is O(types) per turn, never O(heap); for each live resume point choose drain, typed map, or typed abort.

**5. Version the checkpoint codec as a wire format.** The exact Core4 codec is Mini's equivalent of PJama's
undescribed internal structures and L3's kernel tables. Epoch-tag it, typecheck every checkpoint before the root
moves ("once committed, an inconsistent checkpoint lives forever" — and Mini's lives forever replicated), and on a
Core4 machine change either ship a checked translation or refuse old checkpoints loudly after draining residents.
GC at yield and charge storage on post-GC encoded size: half of all dirtied state in KeyKOS died within one
checkpoint interval.

**6. Naming: a global immutable substrate plus per-object local views.** Plan 9 (WORM dump + per-process
bind/mount), Fuchsia (no global root, namespaces built from handles) and Twizzler (global IDs plus a per-object
foreign-object table with pinned-or-late-bound entries) converge: Mini's Merkle store is the substrate; each
object's caps record is its namespace — first-class, transmissible (fixing Plan 9's admitted regret) — and each
outbound reference says explicitly whether it pins a hash or follows a resolver. A fixed universal meta-protocol
(9P's lesson) is the right basis for presentation: every object answers describe/affordances/history so web,
Discord and AI renderers are generic clients.

---

## §G. Persistence: retrospectives and critiques (read by SCHOLAR-OS directly; lane B covers KeyKOS/EROS/Grasshopper/Twizzler/Aurora/PJama)

#### G1. Orthogonal Persistence Revisited (2010)
- **Cite:** Dearle, A., Kirby, G. N. C., Morrison, R. (2010). *Orthogonal Persistence Revisited*. ICOODB 2009, LNCS 5936; arXiv:1006.3448. https://arxiv.org/abs/1006.3448 . Local: `~/paperbin/world-program-model/dearle-orthogonal-persistence-revisited-2010.pdf` (.txt beside). **[READ, in full]**
- **Content:** The three principles (persistence independence, data type orthogonality, persistence identification → in practice "persistence by reachability"). PS-algol (structural types, `pntr` as an infinite union checked dynamically on dereference — "partial and incremental specification of the structure of the data at the expense of a dynamic check"); Napier88 (whole environment in a typed persistent store, `any`/`environment` infinite unions, *hyper-code*: "source programs could include direct links to values that already exist in the persistent environment", structural reflection for "type-safe evolution" where generators "stop part of an executing system ... inspect its state ... change the part ... and rebind it"). Why OP lost commercially: "proprietary closed storage formats", lack of "declarative queries over non-resident data", "limited scalability", and OODB tight coupling ("the schema and the code being highly coupled"). The OODB code-in-database argument: if code is not stored with data, a subtype written by another program cannot be late-bound — "relying on being able to load code from the file system—which is manifestly unsafe—or placing code in the database". Objects tied to external state (file descriptors, GUI, channels) defeat orthogonality everywhere.
- **Lesson for Mini (fork 5, fork 4, naming):** Mini avoids three of the four historical killers by construction: code *is* in the store (package = content-addressed cell, pinned per object — the Richardson anomaly cannot occur); there is no ambient external state (all I/O is Plan actions judged by laws); the format is not "proprietary" if the checkpoint codec and cell encoding are published Lean definitions with an independent decoder. The fourth killer — **queries over non-resident data** — is still open: Mini needs a declarative, law-respecting read/query surface over cells (indexes as derived, recomputable cells), or it repeats the OODB failure. Hyper-code is the right model for "using is programming" in Mini's presentation: an `.obend` source that links directly to live cells by content/identity rather than by name.

#### G2. A Persistent System in Real Use — Experiences of the First 13 Years (EUMEL/L3)
- **Cite:** Liedtke, J. (1993). *A Persistent System in Real Use — Experiences of the First 13 Years*. IWOOOS '93, IEEE. https://os.itec.kit.edu/downloads/publ_1993_liedtke_persistent-system-in-real-use.pdf . Local: `~/paperbin/world-program-model/liedtke-persistent-system-real-use-1993.pdf` (.txt, .raw.txt beside). **[READ, in full]**
- **OS-level decisions:** "Both data and processes, in principle all objects are persistent, files are implemented by means of persistent objects (not vice versa)"; ">2000 Eumel systems and 500 L3 systems" shipped 1979-1993; tasks and threads are first-class persistent objects; no data outside a task; synchronous IPC by thread id with *clans & chiefs* (a chief intercepts every message crossing its clan boundary and decides whether to pass it — a user-level reference monitor); whole-machine *fixpoints* via copy-on-write (2-5 ms atomic pause, 7-150 s background write-back, ~one per 3 min); restart is "activating the last valid fixpoint" ("There is no relevant difference" between shutdown and crash); kernel calls are atomic, so threads restart at user level.
- **Evidence and what failed:** Very stable in production ("crashes ... due to software are less frequent than those due to hardware"); persistence cost ~30% extra RAM and disk = 3x RAM. But: "the fixpoint stabilises a corrupted system in the same way" — some kernel bugs "led to serious and permanent low level defects"; and "a 'worldwide' fixpoint is not reasonable, especially not in a heterogenous distributed system. Therefore explicit (and sometimes application specific) recovery policies are necessary". Users took persistence for granted; secretaries were told only that a power failure loses a few minutes.
- **Lesson for Mini (fork 5, fork 3, security kernel):** (1) Persistence makes every admitted bug permanent — Mini's defence is that every write passes a *law*, and admission re-executes, so a corrupting write must get past both the program and the law. The residual risk is a bug in the Lean admission itself; therefore keep the *full history* (Merkle roots per turn) so that recovery can re-execute from an earlier root under fixed semantics (Mini's re-genesis-is-free stance is the degenerate case). (2) No global fixpoint across domains: each BFT domain checkpoints itself; cross-domain consistency is a protocol (agrees with F4). (3) Clans & chiefs ≈ Mini's laws placed on a *boundary* rather than a cell — worth having: a "domain law" that judges every message crossing a domain or object-group boundary (INFERRED).

#### G3. TreeSLS: whole-system persistence on a capability tree (2023)
- **Cite:** Wu, F., Dong, M., Mo, G., Chen, H. (2023). *TreeSLS: A Whole-system Persistent Microkernel with Tree-structured State Checkpoint on NVM*. SOSP '23. https://doi.org/10.1145/3600006.3613160 ; PDF https://ipads.sjtu.edu.cn/_media/publications/wu-sosp23.pdf . Local: `~/paperbin/world-program-model/wu-treesls-2023.pdf` (.txt beside). **[SKIMMED: abstract, §1-2 read; design/eval skimmed]**
- **Content:** Organises "whole-system state in a capability tree for efficient incremental state checkpointing"; checkpoints the whole system "in around 100 µs and even take a checkpoint every 1 ms"; *delayed external visibility* gives "transparent external synchrony" (outputs released only after the checkpoint that produced them).
- **Lesson for Mini (fork 5):** Two confirmations: state shaped as a capability/Merkle *tree* makes incremental checkpoints cheap (Mini's sparse Merkle root is that tree), and "delayed external visibility" is Faré's barrier-before-send done by the OS — Mini should hold every externally visible effect of a turn (bridge messages, notifications, renders) until the turn's root is committed (for a BFT domain: finalized).

#### G4. Orthogonal persistence as an anti-pattern (practitioner critique)
- **Cite:** Cedanet Pty Ltd (2023). *Anti-pattern: orthogonal persistence*. https://cedanet.com.au/antipatterns/orthogonal-persistence.php . Local: `~/paperbin/world-program-model/cedanet-op-antipattern.txt`. **[READ]** Also cites Cooper, T. B., Wise, M. (1996). *Critique of orthogonal persistence*. IWOOOS '96. https://doi.org/10.1109/IWOOOS.1996.557900 — **[SKIMMED: abstract only, via Kagi snippet: "we argue that orthogonal persistence is undesirable"]**.
- **Content:** "everything persists, including all the finite state machines. This raises the question of how to find a consistent cut"; quoted practitioner: transparent persistence loses relational query performance and causes object-at-a-time traffic.
- **Lesson for Mini:** The consistent-cut objection is dissolved in Mini by atomic turns (every committed root is a consistent cut). The query objection stands (see G1): plan a query/index subsystem.

---

## §4. Replicated, deterministic world computers as operating systems (reading lane C)

Scope: Urbit, the Internet Computer (ICP), Agoric SwingSet, Ethereum, Spritely Goblins, Holochain,
Croquet/TeaTime (and its Reed-1978 ancestor), read as **whole operating systems**: kernel,
process/object model, persistence, upgrade, naming/identity, scheduling, metering, I/O, presentation.
Call-level actor/ocap semantics belong to another lane; this lane cites them only where the OS-level
consequence differs.

Every paperbin path below is under `~/paperbin/world-program-model/`. Tags: **READ** = I read the
text (sections named when partial), **SKIMMED** = abstract/headings/grep only, **INFERRED** = my
connection, not the authors'.

---

### 4.1 Urbit

#### Urbit whitepaper — the "solid-state interpreter" / "operating function"
- **Cite:** Yarvin, Monk, Dyudin, Pasco (2016). *Urbit: A Solid-State Interpreter*. Tlon whitepaper.
  https://media.urbit.org/whitepaper.pdf . Local: `yarvin-urbit-solid-state-interpreter-2016.{pdf,txt}`.
  **[READ]** (all of §1–6, §8–13; Hoon syntax/polymorphism §7.3–7.5 skimmed).
- **OS-level decisions:**
  - *Kernel as a pure function of history.* The whole lifecycle is `L : History → State`, concretely the
    Nock formula `[2 [0 3] [0 2]]`: the first (larval) event is a formula applied to the rest of the log.
    The transition function is `T : (State, Input) → (State, Output)` where output is "a hint" the runtime
    may or may not send (§4.1). Arvo is a core with two arms, `poke` (apply one step → list of effects +
    new Arvo) and `peek` (a referentially transparent global namespace that may answer "unknown yet",
    "never bound", or a marked value) (§8.1).
  - *Persistence = log + snapshot.* "Its event log is its transaction log. It persists by saving dirty
    pages to a snapshot and/or replaying log entries" (§2.3). Uniform/single-level store: no
    memory/disk split exposed to programs (§3.1).
  - *Atomicity and interruption.* "An interrupted event never happened … the event log is a log of
    successful transactions … replaying this log is not Turing-complete. The log is an existence proof
    that every event within it terminates" (§3.4). Nondeterministic crash information is turned into
    input: "we write our step history with the crash report, not the original step" (§4.3).
  - *Structured events.* One external step becomes a cascade of internal *moves* processed depth-first
    as one transaction; a `duct` is a stack of `wire`s (causes) — "the dual of a call stack": `%pass` is a
    call, `%give` a return (§8.3). Yarvin explicitly recommends *against* storing promises/closures in
    persistent state: "if the state machine contains promises, closures, which represent in some sense
    blocked sequential processes, upgrading it may be an unnecessarily interesting problem" (§8.3).
  - *Upgrade.* Nock is frozen; everything above it (Hoon, Arvo, vanes, apps) hot-upgrades over the
    air from the revision store Clay. "If the type of live state changes, the new code must supply a
    function from old to new state" (§2.3). Vanes are held as `vase`s (type, value) so they can be reloaded
    from source and asked "to copy the relevant state from the old core" (§8.2). Identity is the one
    thing that is never upgraded: "If you want a new identity, create a new instance" (§4.2).
  - *Network as facts.* "A packet is a fact and a command is an order" (§3.2). Because both endpoints
    never lose state, a per-pair permanent sequence number makes delivery exactly-once (§9.6). Acks are
    end-to-end and *transactional*: the ack of the last fragment reports that the receiving app's handler
    committed; a nack carries the crash trace; nacks are stored forever because duplicates must get
    duplicate acks (§9.8). Unknown-protocol messages are *silently dropped* so the sender backs off until
    the receiver upgrades (§9.9).
  - *Identity/naming.* 128-bit "ships" are both identity and routing address; class by width (galaxy 8,
    star 16, planet 32, moon 64, comet 128), parent signs child, children can escape to a new sponsor
    (§9.1–9.4). Keys form a self-validating will of deeds; "key revocation is key renewal".
  - *Security model.* Single-homed: all vane code fully trusted by `our`; app moves carry a security
    mask (who tainted / whom it may leak to) — noted as "not implemented at all" (§11).
  - *Jets.* Accelerators bound to a pure Nock definition, recognised by hash of the formula (§6.3).
- **Evidence:** 30 kloc full stack, self-hosting, small live network (2016). Admits "Urbit is not yet
  secure or reliable … sometimes we still reboot the universe (declare a flag day, or 'continuity
  breach')" (§11).
- **What failed / critiques:** see §1.3 below.
- **Lesson for Mini:**
  - *Event log + deterministic kernel* (AGREES): Urbit is the purest statement of Mini's admission by
    re-execution, and its two refinements are worth copying verbatim: (a) **only committed turns enter
    the log; a turn that runs out of budget "never happened"**, so replay is total; (b) **nondeterminism
    is logged as input** — if Mini ever records a refusal or crash explanation, the log entry is the
    explanation, not the attempted invocation. Cost: none; this is a statement about what the Host appends.
  - *Fork 1 (calls):* Arvo's duct (a stack of causes carried on every message, with the reply routed back
    on the same duct) is a cheap, printable, keyable *continuation identity*. Mini's "what the resident
    awaits" should be a duct-like path, not an opaque pointer, so a reply can be matched, audited and
    rendered (INFERRED).
  - *Fork 4/5 (residents):* Urbit's authors *deliberately avoided* persistent closures/promises because
    of upgrade. Mini's proposed model keeps exactly those (checkpointed activities). This is the central
    tension of this lane; see Agoric asyncFlow (§3.2) for the only system that tried the other way, and the
    synthesis for the recommended disposition rule.
  - *Network semantics:* adopt "fact, not command" for inter-domain messages: per-(sender, receiver)
    sequence numbers, idempotent receipt, end-to-end ack = "the receiving turn committed" (INFERRED).

#### Urbit today — Gall agents, threads, Azimuth, Layer-2 "naive rollups"
- **Cite:** Urbit Foundation docs (2025–26): *App School 4: Lifecycle*
  https://docs.urbit.org/build-on-urbit/app-school/4-lifecycle ; *Core Academy 12: Gall and Userspace*
  https://docs.urbit.org/build-on-urbit/core-academy/ca11 ; *Threads: Fundamentals*
  https://docs.urbit.org/urbit-os/base/threads/basics/fundamentals ; *Life and Rift*
  https://docs.urbit.org/urbit-id/life-and-rift ; *Layer 2* https://docs.urbit.org/urbit-id/l2 .
  Local: `urbit-docs-*-2026.md`. **[READ]** (lifecycle, ca11 prose, threads intro, life/rift, L2 summary
  and state sections).
- **OS-level decisions:**
  - *Process model.* A Gall agent is a door with exactly ten arms (`on-init`, `on-save`, `on-load`,
    `on-poke`, `on-watch`, `on-leave`, `on-peek`, `on-agent`, `on-arvo`, `on-fail`); every arm returns
    `(quip card _this)` = (effects, new self). "Every event happens in an atomic transaction, so the state
    is never inconsistent" (ca11).
  - *Upgrade.* On a Clay commit: old agent's `on-save` exports state as a `vase`, new code is built,
    new `on-load` receives the vase and migrates it. Convention: tagged `versioned-state` union
    `$%(state-0 state-1 …)` switched on in `on-load`. Crucially: "If there is a crash in any `+on-load`
    calls or in the handling of any effects they emit … then the whole event crashes, canceling the commit.
    This effectively gives any agent the ability to abort a commit by crashing" (ca11).
  - *Two process kinds.* Permanent agents (pure data state) vs. transient *threads*: "A thread is like a
    transient gall agent. Unlike an agent, it can end and it can fail", used for multi-step I/O so that
    "a mishandled intermediary state" cannot corrupt permanent state (threads doc). Threads are monadic
    strands (`form`/`pure`/`bind`).
  - *Identity epochs.* Every point carries `life` (key revision) and `rift` (continuity/breach count).
    A breach (`rift`++) resets all networking state with that ship (life-and-rift).
  - *Azimuth L2.* Ethereum is used as an ordered transaction log only: "the EVM no longer checks the
    validity or computes the state transitions … the business logic … has been offloaded to your urbit";
    every ship runs `naive.hoon` over L1 logs + L2 batches and keeps its own canonical PKI state. ≥65×
    gas reduction for ~30-tx batches; one-way trip (L2 ships cannot return) (L2 doc).
  - *Presentation.* Apps ship a "glob" of HTML/JS served by the Eyre HTTP vane; front ends are React
    talking to agents over a poke/subscribe channel (docket/full-stack docs, SKIMMED).
- **Evidence:** a running network for a decade; L2 in production since 2022 (docs).
- **What failed / critiques:** threads are *not* persistent, so long-running effectful work is exactly the
  part Urbit refuses to persist; network-wide "continuity breaches" were the actual upgrade mechanism
  for the hardest changes (whitepaper §11; life-and-rift distinguishes network-wide breaches from
  personal ones).
- **Lesson for Mini:**
  - *Fork 4:* Gall's "new code's `on-load` may crash ⇒ the upgrade commit aborts" is the right
    atomicity: migration is one turn, all-or-nothing, and **the new code (not the old) owns it**. Contrast
    ICP `pre_upgrade` below. Mini should make "upgrade object O to package P' with migration m" a single
    admitted turn in which `m` runs, the result is type-checked against P''s state type, *and O's law
    judges the migrated state*; any failure leaves O on P. Cost: one more Plan action kind.
  - *Fork 3:* the agent/thread split is the conservative answer to "activities over persistent state":
    keep permanent state first-order; put multi-step I/O into a disposable process. Mini's activities
    collapse the two; that is more expressive but inherits the upgrade problem Urbit avoided.
  - *Multi-party:* **naive rollups are Mini's admission model applied to identity**: an external ordering
    service (Ethereum) + every interested party re-executes a small deterministic validator and keeps its
    own state. This is direct evidence that "ordering + re-execution by each interested party" works for
    a real multi-party registry at scale, and it suggests a cheap multi-party domain for Mini: a BFT
    committee (or any log) only orders; each party re-executes the turns touching cells it holds
    (INFERRED).
  - *Naming:* adopt an explicit `rift`-style continuity counter per cell/domain so a re-genesis or a
    law change is visible to peers rather than silently reinterpreting state (INFERRED; matches the
    repo's "refuse to load, never reinterpret" rule).

#### Urbit retrospectives and practitioner critiques
- **Cite:** ~wicrum-wicrun (2023). *Plunder and Urbit* (gist by a former Urbit Foundation core dev).
  https://gist.github.com/wicrum-wicrun/b308b298721ccbe0de9c6c73a6ee4242 . Local:
  `wicrum-plunder-and-urbit-2023.md`. **[READ]**. — Wejn (2021). *Urbit: The good, the bad, and the
  insane*. https://wejn.org/2021/02/urbit-good-bad-insane/ . Local: `wejn-urbit-good-bad-insane-2021.txt`.
  **[READ]**. — HN threads 21672481 (2019), 27268462 (2021), 37057471 (2023) via Scry. **[SKIMMED]**.
- **Critiques, and why:**
  - *"Urbit is a ball of mud"* (wicrum): Nock is formally neutral but the runtime can run only one
    Arvo-shaped noun, I/O drivers assume vane internals, so "users need to accept the whole package deal".
    Freezing Nock is fine; trying to standardise (kelvin-version) a whole OS, application model and
    language is not achievable — "the OS is *exactly* the layer where you want innovation to happen".
    Plunder instead freezes the **VM + a small set of hardware interfaces (message send, timer, spawn)**
    and lets many independent "cogs" run on it.
  - *Centralisation through upgrade.* Because the network protocol (`ames.c`/`ames.hoon`) and Gall are not
    frozen and are shipped by one foundation, "the ground can shift under you"; Wejn adds that OTA updates
    were transport-encrypted but **not signed**, so a compromised sponsor could push arbitrary code.
  - *Jets as the real bytecode / performance.* Nock's tree addressing fights caches; jet matching
    requires reproducing Hoon's exact nouns, so "Nock is not a compile target"; data jets are lost across
    `jam`/`cue`. Plunder's "pins" (content-addressed, globally deduplicated functions) fix jet identity
    across the network.
  - *Laziness unsupported.* "Nock-Hoon is also unfriendly to laziness … once all references to a thunk
    is gone, it should be deleted, not persisted" (wicrum).
  - *Encryption at rest absent; scarce identity priced by Ethereum gas* (Wejn).
- **Lesson for Mini:**
  - *Kernel freeze boundary (security kernel):* freeze **Core4 semantics, the Plan/action vocabulary,
    the checkpoint codec and the message/timer interface**; version everything else as ordinary
    packages. Do not try to freeze an application model. Cost: a written list of frozen interfaces with
    epochs.
  - *Code identity:* Plunder's pins = Mini's content-addressed packages; the lesson is that code
    identity must be **by content hash at every boundary** (including inside messages and checkpoints),
    so a received continuation resolves to the receiver's own verified copy (INFERRED).
  - *Upgrade authority must be authenticated and visible*, not merely transported over an encrypted
    channel (Wejn's point) — see Salehi below.
  - *Laziness in checkpoints (fork 5):* Mini's call-by-need machine will persist thunks; the critique
    says unreachable thunks must be collected, not persisted. Mini's "GC at yield" is exactly that — keep
    it mandatory, and charge for what survives (INFERRED).

---

### 4.2 Internet Computer (ICP)

#### The Internet Computer for Geeks
- **Cite:** DFINITY Team (2022, v1.4 Dec 2023). *The Internet Computer for Geeks*. IACR ePrint 2022/087.
  https://eprint.iacr.org/2022/087 (fetched from https://internetcomputer.org/whitepaper.pdf because
  ePrint served a Cloudflare challenge). Local: `dfinity-internet-computer-for-geeks-2022.{pdf,txt}`.
  **[READ]** §1–2, §6–8; §3–5 (threshold BLS, DKG, consensus proofs) **[SKIMMED]**.
- **OS-level decisions:**
  - *Kernel.* "A network of interacting replicated state machines"; each subnet is a BFT RSM
    (f < n/3, safety under asynchrony, liveness under partial synchrony) (§1.2–1.4). Consensus only orders;
    message routing + execution are deterministic and "allowed to run a bit ahead" of each other (§2.3).
  - *Process model.* A canister = Wasm program + state, "roughly the same as the notion of a process"
    (§1.7). Per-canister input queues: one for ingress, one per peer canister; per-canister output queues;
    subnet-to-subnet streams (§6). "The execution layer processes one input at a time" (§7).
  - *Certification.* Each round, a Merkle tree over *part* of the state (streams, ingress history,
    per-canister metadata, 32-byte "certified variables") is threshold-signed, **chained to the previous
    round's root**. The chaining exists to make accidental nondeterminism detectable: without it, one
    Byzantine replica could co-sign an incoherent sequence of individually-valid states (§6.1, worked
    example P1–P4). Full-state Merkle root only once per epoch in a "catch-up package" (CUP), used for
    garbage collection, fast-forward and state sync (§8.2–8.3).
  - *Queries vs updates.* Queries run on one replica, may mutate locally, changes never committed; only
    certified variables make query answers authenticatable (§6.2).
  - *Identity.* User principal = hash of public key; canister ids; subnet public key constant over its
    lifetime so outputs verify against one key (§1.6.1, §6.3).
  - *Scheduling.* Deterministic scheduler, fair across canisters, total work per round ≈ fixed number of
    cycles; back-pressure throttles canisters that out-produce their consumers (§7).
  - *Randomness.* "Random tape": a request in round h is answered with a threshold signature from
    round h+1, unpredictable at request time (§7.1).
  - *Metering & money.* Reverse gas: canisters prepay in cycles (burned ICP); governance (NNS DAO)
    sets the ICP→cycles rate and upgrades the protocol itself via CUP epochs (§1.8, §1.10).
  - *Presentation/I/O.* Canisters serve HTTP; boundary nodes return a service worker that verifies
    responses against the hard-coded NNS key (§1.9).
- **Evidence:** production network since 2021; DAO-governed protocol upgrades.
- **Lesson for Mini:**
  - *Event log + deterministic kernel* (AGREES, with an addition): Mini's BFT committee domains should
    sign **a per-turn (or per-block) cell root chained to the previous root**, so a replica whose Lean
    re-execution diverges is caught at the next certificate rather than by an audit. Cost: one hash per
    block plus a signature; the sparse Merkle root already exists.
  - *Presentation:* ICP's "certified variable" is the minimum mechanism for an authenticated card: any
    projection served to a viewer must be provable against the latest certified root (Merkle path to the
    cells rendered). Mini's cards should carry that path (INFERRED).
  - *Queries:* adopt ICP's split explicitly — reads/pure calls that are *not* admitted (single node, no
    log) vs. admitted turns; a card render is a query and must say which certified root it reflects.

#### ICP message execution, inter-canister calls, upgrades (docs + interface spec)
- **Cite:** DFINITY (2025). *Properties of message executions on ICP*
  https://internetcomputer.org/docs/references/message-execution-properties ; *Security best practices:
  Inter-canister calls* …/building-apps/security/inter-canister-calls ; *Security best practices: Canister
  upgrades* …/security/canister-upgrades ; *Canister resource limits* …/canister-management/resource-limits ;
  *Cycles cost formulas* …/references/cycles-cost-formulas ; *IC Interface Specification*
  …/references/ic-interface-spec (all from github.com/dfinity/portal master). Local:
  `dfinity-docs-*-2025.md`, `dfinity-ic-interface-spec-2025.md`. **[READ]** (spec: upgrade, timers,
  stopping, cycles/freezing sections only).
- **OS-level decisions:**
  - *Await is a commit point* (the docs: "In Motoko, `await` always commits the current state"; code after an `await` "is executed as a separate message execution"). Property 1: one message execution at a time per canister, atomic.
    Property 2: code after an `await` on an inter-canister call is a **separate message execution**.
    Property 4: executions of interleaving calls have no reliable order. Property 5: a trap rolls back only
    the current message execution — "not … the state before the entire call". Property 6–9: at-most-once
    delivery, exactly one response (possibly synthetic), bounded-wait calls may return `SYS_UNKNOWN`
    (outcome unknown). Property 3: requests from A to B execute in send order; responses carry no order.
  - *Resulting bug classes* (security doc): time-of-check/time-of-use across an `await`; double spend by
    parallel calls; locks acquired before an `await` never released if the callback traps; a trap in the
    callback leaves a half-applied multi-step change. Recommended fixes: per-caller **guards** released in
    `call_on_cleanup`/`finally`, and **journaling** — "before each failable task, the journal records the
    intent … after the task, the journal records the result"; to make a journal entry durable mid-flow,
    "an inter-canister call can be made to an endpoint on the same canister that does nothing".
  - *Malicious/stalled callees.* A callee can withhold its response as long as it pays; the caller then
    "can no longer be stopped because of the outstanding callback, and thus can no longer be cleanly
    upgraded. Recovery would require wiping the state … by reinstalling it." Call-graph cycles can deadlock.
    Mitigation: bounded-wait calls, stateless proxy canisters.
  - *Upgrade protocol* (spec): `pre_upgrade` on the **old** instance, then `post_upgrade` on the new; the
    pair is atomic. But "If a canister traps or panics in `pre_upgrade`, this can lead to permanently
    blocking the canister"; the spec added `skip_pre_upgrade` as a recovery hatch. "Some canisters may not
    be able to make sense of callbacks after upgrades; these should be stopped first, to wait for all
    outstanding callbacks." Global timers are **deactivated** by any code change and must be re-armed.
  - *Limits.* 40 B instructions per update message, 7 B per round per thread (so long messages are
    sliced over several rounds — deterministic time slicing, INFERRED from the two limits), 300 B per
    install/upgrade, 4 GiB heap, 500 GiB stable memory per canister.
  - *Pricing.* 13-node subnet: 5 M cycles per update + 1 cycle/instruction; storage **127 000 cycles per
    GiB per second**; 1 T cycles = 1 XDR. Freezing threshold: a canister is frozen when its balance would
    not cover idle storage burn for `freezing_threshold` seconds; outgoing calls **reserve** cycles for the
    largest possible response and its callback up front, refunded if unused (spec).
- **Evidence:** these are the platform's own security guidance after several years of production; the
  guards/journaling patterns are cited from real audits (GoldDAO GLDT-swap journal).
- **What failed:** the async model pushed transactional integrity onto every developer; the platform
  team's recommended fix (journaling) is a hand-written write-ahead log *inside* the application.
- **Lesson for Mini:**
  - *Fork 1/3 — make the commit point a type, and give the kernel the journal.* Mini already makes
    effects visible (`Activity<P,R,A>`: a yield is a typed Plan). The ICP lesson is that **every yield is a
    commit point and must be the only one**: the Plan + the activity checkpoint must be committed in the
    same atomic turn, so the checkpoint *is* the journal ICP asks developers to hand-write. Then a resume
    after an unknown outcome (ICP's `SYS_UNKNOWN`) is just the checkpoint plus a typed "outcome unknown"
    response. Concretely: `R` for any cross-domain await must be a sum including `Unknown | Rejected e |
    Reply r`. Cost: none beyond what the proposed model already persists; the gain is that a whole class of
    ICP bugs (lost locks, half-applied callbacks) cannot be written.
  - *Fork 1 — deadlines are mandatory.* Every await must carry a deadline (block height) after which the
    kernel resumes it with `TimedOut`; otherwise a callee can pin a resident forever and (as on ICP) block
    its upgrade. Cost: the kernel keeps a deadline index; the timeout turn is paid from a reservation.
  - *Fork 5 — reserve the resume.* Like ICP's callback reservation, a yield should **escrow the fee for
    its own resume turn** (and for its timeout turn), so a reply can always be admitted and a resident can
    never be stranded by its own empty balance. Storage of the checkpoint is charged per byte-second (ICP's
    GiB·s), with a freezing threshold — but when the threshold is crossed Mini should *abort the activity
    with a typed error and keep the object*, not uninstall code (ICP deactivates timers and can drop the
    module when out of cycles).
  - *Fork 4 — never give the old code a veto.* `pre_upgrade` bricking is the canonical failure: the
    hook that must succeed is controlled by the code being replaced. Mini's migration must be a function
    supplied by the *new* package (as Gall `on-load`, Motoko migration functions, Agoric `buildRootObject`),
    with no old-code hook on the upgrade path.

#### Motoko enhanced orthogonal persistence and migrations
- **Cite:** Bläser, Russo, Greif, Vandersmith, Ibrahim (2024). *Smarter Contract Upgrades with
  Orthogonal Persistence*. VMIL '24, ACM. https://doi.org/10.1145/3689490.3690401 . Local:
  `dfinity-smarter-upgrades-op-2024.{pdf,txt}` (downloaded by a sibling lane). **[READ]** §1, §4.9–7; §2–4.8
  **[SKIMMED]**. — DFINITY (2025). Motoko docs: *Enhanced orthogonal persistence*, *Data persistence*,
  *Enhanced multi-migration*, design note *OrthogonalPersistence.md* (github.com/dfinity/motoko master).
  Local: `motoko-*-2025.md`. **[READ]**.
- **OS-level decisions:**
  - The Wasm main memory is **retained** across upgrades (`wasm_memory_persistence = opt keep`); a fixed,
    version-invariant memory layout; persistent metadata holds a **type descriptor of the stable
    variables**; on upgrade the runtime compares old and new descriptors and **rolls back** if incompatible.
  - Compatibility = "stable subtyping", stricter than ordinary subtyping: add actor fields, add variant
    cases, `Nat`→`Int`, contravariant/covariant shared functions; **no dropping record fields or promotion
    to `Any`** without an explicit migration (tightened in v0.14.6 "to prevent accidental loss of data").
  - Stable types exclude local functions/closures: "the meaning of a function value, consisting of both
    data and code, cannot easily be preserved across an upgrade".
  - Explicit migrations: a migration expression `{old fields} → {new fields}`; *multi-migration*: a
    directory of timestamped migration modules, compiler checks the chain composes, runtime applies only
    unapplied ones; **"the migration chain (not the actor source) is the single source of truth for stable
    variable values"**; stable fields have no initialisers.
  - `preupgrade`/`postupgrade` hooks deprecated (warning M0270): "If `preupgrade` raises a trap, hits the
    instruction limit … the canister is stuck with the existing version."
  - Last-resort *graph-copy* stabilisation, split across many messages, for runtime-layout changes.
- **Evidence:** VMIL paper: upgrade cost becomes constant (≈ tens of thousands of instructions, only the
  type check) versus serialisation cost linear in heap size that exceeded the per-upgrade instruction limit
  at >100 B instructions — "leaving the program in an evolutionary dead end, unable to upgrade" (§5.3);
  17 SLOC of persistence code per Rust benchmark vs one keyword in Motoko (§5.2).
- **What failed:** the earlier serialise-on-upgrade design (Breitner below; VMIL §4.10): duplicated
  sharing, data-dependent stack overflow, canisters > ~2 GB effectively unupgradeable.
- **Lesson for Mini:**
  - *Fork 4 (strongly AGREES with a typed-migration model):* Mini can do Motoko's check *better*, because
    it has a certifying type checker and pinned content-addressed packages: an upgrade turn is admitted only
    if (i) the new package's state type is a stable-subtype of the old, or (ii) a migration function of
    type `OldState → NewState` is supplied and type-checks, and (iii) the cell's law accepts the migrated
    state. Copy the multi-migration idea: **the object's state is defined by genesis + the ordered chain of
    migrations it has undergone**, recorded in the cell (so any replica can audit why the state has its
    shape). Cost: a stable-subtyping relation on Core4 types (decidable, structural) and a migration
    action in the Plan vocabulary.
  - *Fork 5:* Motoko's rule "no closures in stable state" is the opposite of Mini's checkpointed
    activities. Mini should keep closures in checkpoints but **classify them**: data in object state must be
    first-order (stable), while continuation captures live only in activity checkpoints that are pinned to
    a package hash (see synthesis). Cost: a "stable type" judgement in the type checker.
  - *Fork 5 (cost model):* the VMIL numbers say the cost of an upgrade must not scale with heap size,
    or large objects become unupgradeable. In Mini, if migration is a user function over the whole state, a
    big object may not migrate within one turn's budget — so either (a) allow lazy, per-cell migration
    (Agoric's advice, below), or (b) allow an upgrade to span several admitted turns with the object
    *closed* in between (Motoko graph-copy). Decide this now.

#### Breitner, "How to audit an Internet Computer canister"
- **Cite:** Breitner, J. (2021). *How to audit an Internet Computer canister* (blog, author was on the
  Motoko/IC team). https://www.joachim-breitner.de/blog/788-How_to_audit_an_Internet_Computer_canister .
  Local: `breitner-audit-ic-canister-2021.txt`. **[READ]**.
- **Findings:** rejecting (throw) does *not* roll back while trapping does — audit every
  "state change followed by a throw"; invalid Candid from a malicious callee traps the reply handler;
  `preupgrade` that traps or exceeds the limit makes the canister unupgradeable ("canisters with more than
  2GB of live data will likely be unupgradeable"); stable/non-stable companion variables must form
  bijections or data is lost silently on upgrade; canisters must be **stopped** before upgrade because a
  callback reaching the new instance "could possibly call arbitrary internal functions"; system time is
  monotonic but not strictly, and changes across `await`; cycle-drain DoS from the canister-pays model.
- **Lesson for Mini:** (fork 1) a *reject* must never be a partial commit — in Mini a refusal by law or
  by method must discard the whole Plan; (fork 4) a continuation must be bound to the code version that
  created it, never re-entered by arbitrary new code (pinning, below); (metering) "who pays for a hostile
  invocation" must be the *caller* by default, with sponsored calls as an explicit capability — ICP's
  reverse gas is what makes cycle-drain an attack.

---

### 4.3 Agoric SwingSet

#### SwingSet kernel: vats, c-lists, cranks, transcripts, snapshots, metering, upgrade
- **Cite:** Agoric (2020–2025). SwingSet documentation in github.com/Agoric/agoric-sdk
  `packages/SwingSet/{README.md, docs/vat-upgrade.md, docs/transcript.md, docs/persistence.md,
  docs/state.md, docs/c-lists.md, docs/metering.md, docs/run-policy.md, docs/virtual-objects.md}`,
  https://github.com/Agoric/agoric-sdk/tree/master/packages/SwingSet/docs . Local:
  `agoric-swingset-*-2025.md`. **[READ]** (README, vat-upgrade, transcript, persistence, state, c-lists,
  metering, run-policy fully; virtual-objects and garbage-collection first sections; delivery.md
  **[SKIMMED]**).
- **OS-level decisions:**
  - *Kernel/process.* Vats are "userspace processes" on a kernel; vats talk to the kernel only through
    `syscall` and receive `dispatch.deliver`/`dispatch.notify` (README). Star topology: the kernel owns a
    **c-list per vat** mapping kernel refs (`ko`, `kp`, `kd`) to vat refs (`o+`/`o-`, `p+`/`p-`); "vats
    cannot read the contents … Vats never learn krefs"; a vat can only emit a ref it was granted
    (c-lists.md). Unresolved kernel promises have a **decider** vat, subscribers and a queue.
  - *Atomicity tiers.* Turn (empty call stack → empty call stack) ⊂ **crank** (empty promise queue → empty
    promise queue; one delivery) ⊂ **block** (host-chosen group of cranks). "Cranks are transactional": a
    failed crank (meter exhaustion, fatal syscall) discards all its state changes and the JS heap is rebuilt
    by replay. "The Block is the minimal unit of transactional persistence"; "No outgoing messages may be
    released unless the computation that caused them has been safely written into a block" (state.md);
    outbound messages are embargoed to the block commit to avoid "hangover inconsistency" (run-policy.md).
  - *Persistence.* Orthogonal persistence by **transcript replay**: every delivery and every syscall (with
    its result) is logged; on restart a worker reloads the last heap snapshot (xsnap/XS engine) and replays
    the current span; during replay the kernel **checks that the vat emits the same syscalls** and aborts on
    mismatch (transcript.md, persistence.md). Transcripts are split into **incarnations** (one per upgrade)
    and **spans** (one per snapshot).
  - *Metering.* "Computrons": deterministic engine operation counts that do "*not* depend upon … wall-clock
    time, or type of CPU" but do change with the JS engine version ("SwingSet kernels that participate in a
    consensus machine must be careful to synchronize upgrades to prevent divergence of metering results").
    Per-crank limit (100 M computrons) + optional cumulative **Meter** objects that can be refilled by
    message, with a notifier at a threshold; underflow terminates the vat. Empty delivery ≈ 36 560
    computrons; ERTP `deposit()` ≈ 125 k; contract start ≈ 13 M (metering.md). A host *run policy* ends the
    block by cumulative computrons (run-policy.md).
  - *Upgrade* (vat-upgrade.md): old worker shut down; **"outstanding promises are rejected"**,
    non-durable exports abandoned, heap snapshot and transcript dropped, new bundle started; v2's
    `buildRootObject(vatPowers, vatParameters, baggage)` runs as a single **upgrade-phase crank** and must
    "re-define all durable Kinds created by v1 … with the same facets and methods or a superset thereof";
    if any durable Kind is left undefined or the phase throws, **the upgrade fails and v1 is reinstated**.
    State crosses only via **durable** collections reachable from one durable map, the *baggage*.
    "Upgrade is Semi-Traumatic … preserve long-term state, but abandon any work that was in-progress."
    "Promises Are Broken: Promises do not cross the upgrade boundary." Large migrations should be
    lazy/on-demand because only one crank is available, so code "must be prepared to handle arbitrary
    messages despite the migration not being complete". The upgrade capability is the vat's *adminNode*;
    "The ability to upgrade a vat is also the ability to control its behavior … users … must take into
    account the possibility of upgrade."
  - *Data model.* Three tiers: heap (RAM), virtual (on disk, not preserved across upgrade), durable (on
    disk, preserved); "Durable collections can only hold durable objects" (vat-upgrade.md,
    virtual-objects.md).
- **Evidence:** this is the production kernel of the Agoric chain (Cosmos SDK host); the numbers above are
  measured by Agoric.
- **What failed / critiques:** the persistence doc is candid that transcript replay has "unbounded growth
  … and the O(N) cost of re-executing it on restart", motivating engine heap snapshots; but engine
  snapshots are opaque and engine-version-specific, so **they are deleted at every upgrade** and cannot be
  used for migration. Promise-based programs had to be rewritten for durability (the `vow` package, below).
- **Lesson for Mini:**
  - *Event log + deterministic kernel* (AGREES, and Mini can do better): Agoric's transcript-plus-snapshot
    with syscall checking on replay is Mini's architecture with an *untrusted, engine-specific* snapshot.
    Mini's exact, specified checkpoint codec of the whole Core4 machine is the thing Agoric lacked: it can
    survive engine changes and can be inspected by migrations. Keep replay-with-effect-checking as the
    validation mode (a replica replays a turn and must emit the same Plan), and the checkpoint as the
    persistence mode. Cost: none new.
  - *Fork 3 (atomicity tiers):* copy the turn ⊂ crank ⊂ block tiering explicitly. Mini's "turn" (one
    admitted invocation, Plan applied atomically) corresponds to Agoric's crank; Mini should also name the
    *block* tier and adopt **outbound embargo to block commit** for anything leaving the domain (to other
    domains, Discord, the web), so no outside party sees a state that a crash could roll back.
  - *Naming / security kernel:* the kernel-owned c-list is the right shape for Mini's capabilities:
    objects never hold raw cell ids for authority, only kernel-translated references; the law then judges
    actions in kernel terms (krefs) rather than in object-chosen names (INFERRED).
  - *Fork 4:* Agoric's three rules — (1) the **new** code's first turn must re-bind every exported
    obligation (superset of methods) or the upgrade is rolled back; (2) a single designated root (baggage)
    from which all durable state must be reachable; (3) the upgrade right is a capability whose holder is
    effectively the object's author — should all become Mini kernel checks. Rule (1) is the
    *interface-compatibility* check Motoko only warns about. Cost: the method-signature table of a package
    becomes part of its checked core; an upgrade turn compares tables.
  - *Metering:* Agoric's computrons are deterministic but **defined by an engine implementation**, so an
    engine upgrade is a consensus event. Mini can meter in **Core4 demand-machine steps** (`stepRaw`
    counts), which are defined by the Lean semantics itself — strictly better. Adopt Agoric's two-level
    meter (per-turn ceiling + refillable cumulative Meter object with a notifier) and its run-policy
    (block ends at a computron budget). Cost: count steps in `runBounded` (already bounded).

#### Agoric `asyncFlow` and `vow` — upgrade-surviving activations
- **Cite:** Agoric (2024–2025). `@agoric/async-flow` README and *Async Flow States*; `@agoric/vow`
  README. https://github.com/Agoric/agoric-sdk/tree/master/packages/async-flow ,
  …/packages/vow . Local: `agoric-async-flow-2025.md`, `agoric-async-flow-states-2025.md`,
  `agoric-vow-2025.md`. **[READ]**.
- **OS-level decisions:**
  - *Vows* are durable promises: "Native promises are not compatible with Agoric's durable stores …
    such promises disconnect their clients when their creator vat is upgraded." `watch` survives upgrades
    of both creator and subscriber; `when` survives only the *other* side's upgrade.
  - *asyncFlow* lets an `async` function be "suspended at `await` points" across an upgrade: it "uses a
    membrane to log and replay everything that happened before each upgrade". The guest function must be
    **closed** (no captured mutable state or ambient effects) because it will be re-run. Activation states:
    **Running** (effects real and logged) → on upgrade **Sleeping** (log intact, "program counter" reset)
    → **Replaying** (new code re-run against the log; must "exactly produce its previously logged
    behavior") → Running; or **Failed** ("so it can be repaired by another future upgrade"); **Done** drops
    the log. Upgrade can only happen between cranks, so a Running activation was necessarily awaiting a vow.
- **Evidence:** shipped in agoric-sdk for orchestration contracts that span long cross-chain flows.
- **Lesson for Mini:** this is the closest existing system to Mini's *resident* and it pins down the fork-4
  choice for in-flight activities:
  - Agoric's default (abort in-flight work) is safe but forces every long flow to be re-expressed.
  - asyncFlow (re-run the new code over a log of the old activation's interactions) works and is
    deterministic. **Mini has an advantage:** because effects are a type `Activity<P,R,A>`, the log of an
    activation is exactly the sequence of `(Plan_i, Response_i)` pairs it yielded and received. Replay
    check = "the new code, fed `R_1…R_k`, yields `P_1…P_k`". This is cheap, exact, and decidable per
    activation, and it is a natural *Failed* state if it diverges.
  - Recommended disposition, per activity, chosen by the migration turn (INFERRED): **Drain** (keep
    running on the pinned old package until Done; the default), **Replay** (asyncFlow-style rebinding to
    the new package, admitted only if the replay check passes), or **Abort** (resume with a typed
    `Upgraded` error to whoever awaits). Cost: activities record their package hash and their
    `(P,R)` log since start (or since the last rebind); storage is charged like any checkpoint.

#### Miller & Drexler, "Markets and Computation: Agoric Open Systems"
- **Cite:** Miller, M.S., Drexler, K.E. (1988). *Markets and Computation: Agoric Open Systems*. In
  Huberman (ed.), *The Ecology of Computation*, North-Holland, 133–176.
  https://e-drexler.com/d/09/00/AgoricsPapers/agoricpapers/aos/aos.0.html . Local:
  `miller-markets-computation-1988.{pdf,txt}` (sibling lane's download). **[READ]** §1–2, §4.2–4.5,
  §5.1–5.2; remainder **[SKIMMED]**.
- **OS-level decisions:** foundations = encapsulation and communication of **information, access, and
  resources**. "Extending encapsulation to include computational resources means holding each object
  accountable for the cost of its activity." A round-robin scheduler "treats the processor as a commons";
  instead time-slices are owned and traded (citing Artsy's FOCS). Initial market strategies: processor by
  escalating-bid **auction**; memory by **rent** — "objects paying retainer fees to objects they wish to
  retain in memory; objects that are unwanted and hence unable to pay rent are eventually evicted". Caching
  rule: cache iff storage cost < request rate × recompute cost. Open problem flagged: "no open-systems
  language which provides for ownership and trade of basic computational resources while preserving
  semantic uniformity".
- **Evidence:** a design essay; the companion *Incentive Engineering* paper analyses the strategies.
  ICP's GiB·s storage pricing + freezing threshold and Agoric's Meter objects are its descendants
  (INFERRED).
- **Lesson for Mini (metering, fork 5):** Ember's "storage charged" is the *rent* half of this paper.
  Concretely: every cell and every suspended checkpoint pays rent per byte per block from a balance; a
  resident's awaiting party (the one who wants the reply) may pay a *retainer* to keep it alive; eviction
  on non-payment must be **typed abort of activities**, never silent deletion of object state (the
  ICP-uninstall failure). Meters are first-class capability objects (Agoric), so rent can be sponsored.

---

### 4.4 Ethereum as a world computer, and its upgrade reality

#### Ethereum Yellow Paper (Shanghai version)
- **Cite:** Wood, G. (2025-02-04 revision efc5f9a). *Ethereum: A Secure Decentralised Generalised
  Transaction Ledger — Shanghai Version*. https://ethereum.github.io/yellowpaper/paper.pdf . Local:
  `wood-ethereum-yellow-paper-2024.{pdf,txt}`. **[READ]** §2, §4.1–4.2, §5, §6.1, §7 (prose and §7.1),
  §8 (prose), §9.1–9.2, §14; formal Appendices G/H **[SKIMMED]** (DELEGATECALL entry read).
- **OS-level decisions:** world state `σ` = map address → (nonce, balance, storageRoot, codeHash) in a
  Merkle-Patricia trie; `σ_{t+1} = Υ(σ_t, T)`; blocks are a journal of transactions plus the final state
  root, not the state. Code is immutable ROM addressed by hash. Message calls are **synchronous, nested,
  depth-bounded**; an exceptional halt reverts that frame's state changes. Gas: "Gas does not exist outside
  of the execution of a transaction"; storage is paid once on first write and *refunded* on clear —
  there is **no rent**. `DELEGATECALL` runs another account's code in the caller's storage context.
  The yellow paper's "Future directions" (§14) proposes discarding old trie nodes and expiring idle state
  — never shipped.
- **What failed / critiques:** the formalism contains no notion of reentrancy (grep finds none), yet
  synchronous nested calls with shared mutable storage are exactly what made the DAO exploit possible;
  §7.1 documents "zombie accounts" whose balance is locked forever; state growth with no rent.
- **Lesson for Mini:**
  - *Fork 1:* Ethereum is the counter-example for synchronous cross-object *effects*. Mini's choice —
    pure reads/calls in-turn, effects only via a Plan applied after the method returns — rules out the
    DAO class by construction (no callee can observe the caller mid-update). Keep that line hard.
  - *Fork 5:* no-rent storage was a one-way door; Mini should price storage per byte-time from genesis.

#### Salehi, Clark, Mannan — "Not so immutable: Upgradeability of Smart Contracts on Ethereum"
- **Cite:** Salehi, M., Clark, J., Mannan, M. (2022). *Not so immutable: Upgradeability of Smart
  Contracts on Ethereum*. arXiv:2206.00716 (venue not stated in the PDF; I did not verify the
  workshop publication).
  https://arxiv.org/abs/2206.00716 . Local: `salehi-not-so-immutable-2022.{pdf,txt}`. **[READ]** (§1–5;
  appendices skimmed).
- **OS-level findings:** six upgrade patterns: parameter configuration; functional-component change;
  consensus override (the DAO hard fork); contract migration ("social upgrade"); CREATE2+SELFDESTRUCT
  metamorphosis; CALL-based and DELEGATECALL-based data separation (proxies: transparent, UUPS EIP-1822,
  beacon). DELEGATECALL proxies dominate; their costs: new logic "need[s] to allocate the same variables in
  the same order as the old contract", function-selector clashes between proxy and logic, the upgrade
  function must exist in every future UUPS logic contract "or further updates are impossible".
- **Evidence:** blocks 10.8 M–12.86 M (Sep 2020–Jul 2021): **1,427,215 proxy contracts → 8,225 unique
  upgradeable systems** (7,470 regular, 403 UUPS, 352 beacon); admins: 3,558 EOA, 988 known multisig, 2,924
  other; "**48% of systems could be upgraded with the breach of a single signing key**, and an additional
  13% by potentially a small number of signing keys." Case: Bent Finance, a compromised EOA admin pushed
  logic that moved ~$12 M then upgraded back to a clean version.
- **Lesson for Mini (fork 4, naming, presentation):** upgrade on a platform without first-class upgrade is
  rebuilt as an *unchecked* storage-layout convention plus an *invisible* authority. Mini should make
  (a) **upgradeability a declared, immutable property of each object** (frozen / owner / threshold /
  governed-with-delay), set at creation and changeable only to something stricter; (b) the upgrade
  authority a capability judged by the object's law like any write; (c) the **upgrade policy and current
  package hash part of every card**, so viewers see "this object can be rewritten by key X" before trusting
  it; (d) storage layout never a convention — state type is checked across versions (Motoko/Agoric). Cost:
  one field in the object header and one card affordance.

---

### 4.5 Spritely and Holochain

#### Spritely, "The Heart of Spritely"
- **Cite:** Lemmer-Webber, C., Farmer, R., Sims, J. (2023). *The Heart of Spritely: Distributed Objects
  and Capability Security*. Spritely Networked Communities Institute.
  https://spritely.institute/static/papers/spritely-core.html . Local:
  `lemmerwebber-heart-of-spritely-2023.{pdf,txt}`. **[READ]** §1, §3.2.5, §3.3.6–3.9, §4–7; blog tutorial
  §3.2–3.3 **[SKIMMED]**.
- **OS-level decisions:** nesting `machine ⊃ vat ⊃ actormap ⊃ {ref ↦ behaviour}`. Near objects (same vat)
  call synchronously (`$`), far objects asynchronously with promise pipelining. **Turns are cheap
  transactions**: an unhandled error means the turn is "simply never being committed to the root
  transactional heap"; outgoing async messages "are only sent if the turn completes successfully". The
  transactional heap gives time-travel debugging. Persistence + upgrade (formerly "Aurie"): objects are
  asked for a **self-portrait** through a sealed serializer that "only allows objects to provide
  self-portraits utilizing the permissions they already have", restored by replaying build recipes —
  "restoration as an opportunity for upgrade"; deltas from turn transactions make it incremental. OCapN =
  CapTP (distributed GC, pipelining) over pluggable netlayers (Tor, I2P, libp2p, store-and-forward).
  Unum pattern for objects with presences on many machines; CRDT library planned.
- **Evidence:** working Guile/Racket implementations, demo apps (Terminal Phase time travel added "within
  less than three hours"). No production deployment of a multi-party OS.
- **What is missing:** no metering or resource accounting; no consensus for shared state (each vat is
  authoritative for its objects).
- **Lesson for Mini:** (fork 1/3) Spritely is the clean statement of Mini's root lean: synchronous
  in-turn calls only among co-located objects, eventual sends otherwise, sends embargoed to commit (AGREES).
  (fork 4/5) The self-portrait rule is a *security* constraint on migration: **a migration may only
  re-create authority the object already holds** — Mini should check that the migrated state contains no
  capability not present (or derivable) in the old state + the migration's own granted capabilities.
  Cost: a capability-provenance check over the migrated value (INFERRED).

#### Holochain whitepaper (2018) and current DNA model
- **Cite:** Harris-Braun, E., Luck, N., Brock, A. (2018). *Holochain: scalable agent-centric distributed
  computing*. Draft Alpha 1, 2018-02-15. https://github.com/holochain/holochain-proto/blob/whitepaper/holochain.pdf .
  Local: `harrisbraun-holochain-2018.{pdf,txt}`. **[READ]** §III–IV, VII and appendices; §V–VI
  **[SKIMMED]**. — Holochain (2026). *DNAs* build guide https://developer.holochain.org/build/dnas/ and
  *Upgrade 0.6→0.7* notes. Local: `holochain-docs-*-2026.txt`. **[READ]** (relevant sections).
- **OS-level decisions:** a system is `(N, state = hash-chain X + data D, τ, V validation, I input, P
  processing, E evolution)`. Bitcoin/Ethereum enforce `∀n,m: X_n = X_m`; Holochain gives each agent its own
  **source chain** and puts shared data in a "validating, monotonic, sharded DHT" where every node holding
  an entry runs the application's **validation functions** (from the DNA) on it and records validity;
  provenance (author's chain headers) is kept; misbehaviour is answered by gossiped, signed **warrants** and
  membranes (who may join) rather than by global consensus. The 2018 paper leaves `E` (evolution)
  undefined, and countersigning / notaries / CALM as TODO. Today: a DNA's **integrity zomes** (entry types +
  validation) and "integrity modifiers" determine the **DNA hash = network identity**; "any change to
  integrity modifiers will change the DNA hash and form a new network", while **coordinator zomes**
  (callable functions) can be replaced without changing the network; 0.7 adds DNA-migration seeding of a
  fresh chain.
- **Evidence:** 30 kloc Go prototype (2018) with twitter/slack/DPKI demos; scalability tests "on our
  roadmap" (§VII); current Rust implementation in production use by Holochain apps.
- **What failed / critiques:** the agent-centric model detects forks of a source chain (an agent rewriting
  its history) after the fact rather than preventing them; atomic multi-agent actions needed a later
  countersigning protocol; evolution = new network.
- **Lesson for Mini:**
  - *Fork 2 (laws):* Holochain's **integrity vs coordinator** split is precisely Mini's "law disposes,
    code proposes", independently discovered: laws (validation) define the *identity* of the shared space,
    methods do not. Recommendation: in Mini, **changing a cell's law is a different, more governed act than
    changing its package**; a law change bumps the cell's continuity counter (Urbit `rift`) and its card
    says so. Cost: separate law hash in the object header.
  - *Multi-party domains:* Holochain shows a law can be checked by **any party that holds the data and its
    provenance**, without consensus, if the law is a local decidable predicate over the write and its
    author's history — which Mini's difference-logic laws are. That gives a third domain type besides
    single Host and BFT committee: *agent-centric cells* (a cell owned by one key, its history a signed
    chain, its law checked by every reader), suitable for personal data; contested cells still need
    ordering (INFERRED).

---

### 4.6 Croquet / TeaTime and its ancestor

#### Reed (1978), "Naming and Synchronization in a Decentralized Computer System" (NAMOS)
- **Cite:** Reed, D.P. (1978). *Naming and Synchronization in a Decentralized Computer System*. PhD thesis,
  MIT, MIT/LCS/TR-205. http://publications.csail.mit.edu/lcs/pubs/pdf/MIT-LCS-TR-205.pdf . Local:
  `reed-naming-synchronization-1978.pdf`, OCR text `reed-naming-synchronization-1978.txt` (tesseract over
  the scan; figures garbled). **[READ]** abstract, Ch.3 §3.1–3.5, Ch.7 entire; Ch.4–6 **[SKIMMED]** (TOC).
- **OS-level decisions:** an object is "a sequence of immutable versions"; "the synchronization problem is
  transformed into a naming problem": a *version reference* = (object, **pseudo-time**); a consistent system
  state = all versions at one pseudo-time, defined "independent of time" and without quiescing; programs run
  in **pseudo-temporal environments** (hierarchical, non-overlapping ranges of pseudo-time) so a module's
  transaction is a sub-range; failure atomicity via **possibilities** (tentative update sets converted to
  reality by a commit record, else time out), with *dependent possibilities* for nested modules; commit
  records can be replicated as voters. Limits stated by Reed: performs poorly under high contention (reads
  abort writers); proposes an optimistic central scheduler with NAMOS as the dynamic check.
- **Lesson for Mini (fork 3):** the formal ancestor of multi-version, optimistic, deterministic concurrency.
  For "several activities per object" and "deterministic parallel execution of independent turns", Reed's
  pseudo-time gives the semantics: assign each admitted turn a pseudo-time (block height + index); a turn
  reads the versions at its pseudo-time and *defines* new versions after it; two turns conflict iff one
  defines a version the other read. That is OCC/Block-STM-style execution with a 1978 correctness
  definition, and Reed's "possibility" is exactly the cross-domain tentative Plan that becomes real only
  when a commit record (in Mini: a committee certificate) says so (INFERRED). Cost: versioned cells (the
  sparse Merkle store already is persistent/immutable).

#### Croquet: A Collaboration System Architecture (TeaTime, 2003)
- **Cite:** Smith, D.A., Kay, A., Raab, A., Reed, D.P. (2003). *Croquet: A Collaboration System
  Architecture*. C5 '03 (IEEE); VPRI TR-2003-002. https://tinlizzie.org/VPRIPapers/tr2003001_croq_collab.pdf .
  Local: `smith-croquet-collaboration-architecture-2003.{pdf,txt}`. **[READ]**.
- **OS-level decisions:** posed explicitly as "if we were to create a new operating system and user interface
  knowing what we know today". The VM must run **"bit-identical"** on every platform ("even the bugs are the
  same"). TeaTime: "replicated versioned objects coordinated by a universal timebase embedded in the
  communications protocol"; a TObject's messages are redirected to all replicas; "object internal states are
  maintained as ordered histories, and operations are performed at 'pseudo-time' instants"; device I/O is
  tied to real time; "a coordinated 'distributed two-phase commit'" — behaviours "first computed, contingent
  on completion of all dependent object behaviors, and then … atomically committed. If the behaviors are not
  completed in time, all contingent calculations are undone." No separate dev vs user environment; spaces
  and portals as the UI's linking model; "a capabilities model similar to that used by the 'E' language" as
  future work.
- **Lesson for Mini:** see the Croquet OS entry; the 2003 paper's distinctive claims are that the replicated
  object *is* the computer and that **the UI is just more objects** in the shared world.

#### Croquet OS / Multisynq (2020s)
- **Cite:** Croquet Labs (2024). *Croquet docs*: "Model–View–Reflector", "Writing a Croquet Model",
  "Simulation time and future", "Snapshots", "Persistence"; *Reflector README*.
  https://github.com/croquet/croquet/tree/main/docs/tutorials , …/packages/reflector . Local:
  `croquet-os-docs-*-2025.md`. **[READ]**.
- **OS-level decisions:** an app = **model** (replicated, deterministic; "The state of the model is
  guaranteed to always be identical for all users") + **view** (local, non-replicated, free to use the DOM).
  "The view must NEVER write directly to the model": view→model events are bounced off a **reflector** — "a
  stateless, public, message-passing service" that only time-stamps and fans out events and heartbeat
  ticks; all model↔model and model→view events stay local. Model rules: registered classes, no globals,
  no `Date.now()`, **no Promises/async**, no stored functions; time is *simulation time* advanced only by
  reflector ticks; `future(ms).method()` schedules deterministic self-sends. Snapshots are uploaded
  periodically by a client; a joiner loads the latest snapshot and replays events since. **Session id =
  hash(appId, name, model code, library version)** — "even a small change in code creates a new session"
  and state is lost unless the app explicitly `persistSession()`s JSON-able data to seed the next version's
  `init`. Views may "anticipate the model" for latency and correct when the model catches up.
- **Evidence:** shipped products (Croquet for Unity, Microverse; now Multisynq's reflector network)
  (README; HN 2023–25 via Scry, **[SKIMMED]**). No claim of Byzantine robustness: the reflector does not
  validate events; every client runs the whole model (INFERRED from the docs).
- **Lesson for Mini:**
  - *Event log + deterministic kernel* (AGREES): Croquet is the minimal proof that "order the inputs,
    everyone re-executes" is enough for interactive shared state — the reflector is a sequencer with *no*
    state and *no* semantics. Mini's BFT mesh is a Byzantine reflector plus admission (the law/type check)
    that Croquet lacks.
  - *Presentation* (strongly AGREES with "presentation = projection"): Croquet's model/view rule is exactly
    Mini's card model — the view **reads** the authoritative model directly and **writes only by
    publishing an event that goes through the ordering service**; views differ per user. Croquet adds two
    things Mini should copy: (1) *anticipation* — a card may show the predicted effect of an affordance
    immediately and reconcile when the admitted turn lands; (2) **"don't reply to the model"** — no
    model→view→model loops; in Mini, a card affordance must not be invoked automatically by a render.
  - *Fork 4 (warning):* Croquet's identity-by-code-hash is the degenerate upgrade story — code change ⇒
    new world. Mini's proposed "object pins package hash" must *not* make object identity depend on the
    package hash: the object id must be stable and the package hash a mutable (governed) field.
  - *Time:* Croquet's "model time advances only by reflector ticks" = Mini's decision that `valid_until`
    is a block height; residents awaiting time should await a height, never wall-clock (AGREES).

---

### Cluster synthesis (§4)

Read together, these seven systems are one experiment run seven times: a frozen deterministic core, a
log of ordered inputs, re-execution as the source of truth, and a long struggle with the three things a
log does not solve — **in-flight computation across upgrades, who pays, and who may change the rules.**
Mini's admission-by-re-execution is not exotic; it is the shared spine (Urbit's lifecycle function, ICP's
subnet RSM, Agoric's transcripts, Croquet's reflector, Ethereum's `Υ`, Azimuth's naive rollup). What
distinguishes Mini is that its core is a specified, proved machine with an *exact* checkpoint codec and
*typed* effects. Several lessons follow.

**1. Every await is a commit point — make the checkpoint the journal (forks 1, 3).** ICP's model
(atomic per message, code after `await` is a new message) produced reentrancy, TOCTOU, lost locks and
half-applied callbacks, and DFINITY's official remedy is a hand-written write-ahead journal plus
"call yourself to commit". Agoric (crank), Spritely (turn), Urbit (event + moves) all make the atomic unit
explicit. Mini should commit the Plan and the activity checkpoint in one turn, type every cross-domain
response as `Reply | Rejected | Unknown | TimedOut`, require a deadline (block height) on every await,
and escrow the fee for the resume and timeout turns at yield time. Then the bug classes ICP documents are
not expressible.

**2. Upgrade = preserve durable data, decide in-flight work explicitly (fork 4).** Every system preserves
first-order state and fights over continuations: Urbit and Motoko forbid closures in persistent state;
Agoric rejects promises and abandons non-durable exports ("semi-traumatic"); ICP requires stopping to drain
callbacks and deactivates timers; Croquet discards everything on code change. Only Agoric `asyncFlow`
carries activations across upgrade, by replaying a log against new code that must reproduce it. Mini's
typed effects make that replay check exact and cheap (`(P_i, R_i)` pairs). Recommended per-activity
disposition chosen in the migration turn: **Drain** on the pinned old package (default), **Replay** onto
the new package if the check passes, or **Abort** with a typed `Upgraded` response. Object identity must
not depend on package hash (Croquet's mistake).

**3. The new code owns the migration; the kernel checks it (fork 4).** Failures cluster where old code
holds a veto (ICP `pre_upgrade` bricking; `skip_pre_upgrade` added as a hatch) or where compatibility is a
convention (Ethereum storage layout; Motoko's Candid check is only a warning). The working designs —
Gall `on-load` that aborts the commit on crash, Motoko stable-subtyping + migration chains, Agoric
"re-define every durable Kind with a superset of methods or roll back" — combine into one Mini turn:
type-checked migration supplied by the new package, method-table superset check against exported
capabilities, the cell's law judging the migrated state, and the migration recorded in the cell. Large
states need lazy or multi-turn migration; decide this before objects get big (VMIL: "evolutionary dead
end").

**4. Laws are identity; upgrade authority is visible (forks 2, 4; presentation).** Holochain splits
integrity (validation, which defines the network) from coordinators (functions, swappable); Salehi
measured 48% of Ethereum upgradeable systems one key away from arbitrary rewrites. Mini should treat a law
change as a more-governed act than a code change, bump a continuity counter (Urbit `rift`), and put the
upgrade policy and package/law hashes on every card.

**5. Meter in semantics, rent storage, never delete silently (fork 5).** Agoric's computrons are
deterministic but engine-defined; Mini can meter `stepRaw` steps defined by its own semantics. Miller &
Drexler's rent and ICP's GiB·s pricing with a freezing threshold are the storage model; the lesson from
ICP is that insolvency should abort activities with a typed error rather than uninstall code.

**6. Ordering is cheap; validation is the product (multi-party, presentation).** Croquet's stateless
reflector, Azimuth's naive rollups and Holochain's DHT validators all show that once execution is
deterministic and laws are local predicates, the ordering service can be dumb and validation can be done
by whoever cares. Mini's projection should follow Croquet's rule — read the authoritative state directly,
write only through admission, optionally anticipate — with ICP-style certification so every card is
provable against a chained root.

---

## §5. Naming, identity and federation; scheduling, metering and economics (reading lane D)

SCHOLAR-OS sub-lane D, 2026-10-04. Every downloaded source is in `~/paperbin/world-program-model/`; `.txt` sits beside each `.pdf`/`.html`.
Tags: **READ** = I read the text (the sections I name); **SKIMMED** = I read parts or headings; **INFERRED** = my connection to Mini, not the authors' claim.
Mini facts come from `/Users/ember/dev/redregg/work/PROGRAM-MODEL-BRIEF-20261004.md` (read in full). The one Mini fact I take from memory rather than that brief: `valid_until` is a block height.

---

### 5.1 Naming

#### SDSI 1.1 — linked local name spaces, groups, ACLs, and refusals that are "partially evaluated" definitions
- **Cite:** Rivest, R. L. & Lampson, B. (1996). *SDSI — A Simple Distributed Security Infrastructure* (v1.1 working document). https://people.csail.mit.edu/rivest/pubs/RL96.ver-1.1.html . Local: `~/paperbin/world-program-model/rivest-sdsi-1996.html/.txt`. **[READ]** I read §1–2 and §5–9 in full. §3–4 (S-expression syntax, encodings, compression) I SKIMMED.
- **OS-level decisions:**
  - *Naming.* Principals are public keys. Every principal owns a local name space, and there is no global hierarchy. Name spaces link: `bob's alice` = `(ref: bob alice)`, resolved by the `REF/REF2` procedure, which looks up each component in the previous principal's space. A few "special roots" (`DNS!!`, `VeriSign!!`) are bound identically everywhere, so global names are a convenience, not a necessity.
  - *Pinning a name to content.* `Assert-Hash:` wraps a reference with an expected hash, and resolution fails if the fetched value hashes differently. A mutable name is thereby pinned to content.
  - *Groups.* Groups are algebraic: `OR`, `AND`, `NOT`, `MINUS`, and threshold `ANY: k`. They may refer to other principals' groups.
  - *Membership is three-valued: TRUE, FALSE, FAIL.* A negative needs a positive negative certificate from the group's owner, so absence of evidence is FAIL, never FALSE.
  - *The busy-bureaucrat server.* The server never researches on the client's behalf. It decides from local data plus the credentials the client supplied.
  - *Refusals carry a hint.* On FAIL the server returns a **Hint: a partially evaluated group definition**. Example: `(ANY: 3 A B C D E F)` with A and C proven and D refuted becomes `(ANY: 1 B E F)`. The hint tells the client exactly which credentials would make it pass.
  - *Revocation by reconfirmation, not CRLs.* A signature can require periodic reconfirmation, and a newer certificate for the same local name supersedes an older one.
  - *Delegation certificates* let a group of servers sign objects matching a template on a principal's behalf.
- **Evidence:** A design document. MIT master's theses implemented it (Fredette 1997, Morcos 1998, per Clarke et al. 2001). No deployment numbers.
- **What failed / critiques, and why:**
  - The global special roots were dropped when SDSI merged with SPKI (Clarke et al. 2001 §3: "There are no global names in SPKI/SDSI").
  - Abadi (1998) and Halpern & van der Meyden (1999) contested the semantics of linked names, as cited in Clarke et al. I did not read those.
  - SDSI/SPKI as a whole was never broadly deployed; the IETF RFC is "Experimental".
- **Lesson for Mini (naming, fork 2, presentation):**
  - **Agrees** with the proposed model's per-principal authority: every Mini key can own a *namespace cell*. Its law is "only the owner key writes", and its entries are `identifier → term`, where a term is a key, a cell id, a content hash, or another `(namespace, path)` reference.
  - **Push 1 — refusals as residuals.** The membership hint is exactly the refusal-explanation shape Mini's law checker should emit. When a law over a delegation/group predicate cannot be discharged, return the *residual predicate*: the law partially evaluated against the evidence supplied. Do not return a bare "refused". Difference-logic laws already do satisfiability checks; returning the residual constraint set is the same move. **[INFERRED]**
  - **Push 2 — three-valued admission.** TRUE / FALSE / FAIL-needs-evidence, where FAIL is never treated as FALSE. "Insufficient witness" stays distinct from "violates law". **[INFERRED]**
  - **Push 3 — keep `Assert-Hash`.** A `(ref …)` inside a Plan or a law should optionally carry an expected content hash, so a mutable name can be pinned at use time.
  - **Cost:** one namespace-cell kind, a reference term in Core4 data, and a residual-producing variant of the law checker. Small.

#### Certificate chain discovery in SPKI/SDSI — naming as a decidable rewrite system
- **Cite:** Clarke, D., Elien, J.-E., Ellison, C., Fredette, M., Morcos, A. & Rivest, R. L. (2001). *Certificate chain discovery in SPKI/SDSI*. Journal of Computer Security 9(4):285–322. https://people.csail.mit.edu/rivest/pubs/CEEFx01.pdf . Local: `~/paperbin/world-program-model/clarke-spki-chain-discovery-2001.pdf/.txt`. **[READ]** in full.
- **OS-level decisions:**
  - *Names as rewrite rules.* A local name is `(K, identifier)`; extended names are `K A1 … An`. A name certificate `(K, A, S, V)` means V(K A) ⊇ V(S) and is read as the rewrite rule `K A → S`. Certificates are cumulative, and there are **no negative certificates**.
  - *Auth certs.* They become rules `K □ → S □` (live ticket) or `K □ → S ■` (dead ticket). The ticket symbol enforces the delegation bit, and authorization tags intersect when rules compose.
  - *One inference rule.* Composition (prefix rewriting) is the only rule.
  - *Algorithm.* Compute the **name-reduction closure** C# by composing only with *reducing* certs (`K A → K'`). Then drop names and run DFS from `Self` to the requester's key. Threshold subjects (k-of-m) become placeholder keys plus label propagation.
  - *Proof format.* Chains are emitted in a **compressed format** (each line composes two earlier lines). This can be exponentially shorter than a linear chain and is "easy to check".
- **Evidence:**
  - Theorems 1–2: the closure computes exactly the values of names.
  - Worst case O(n³·l) for n certs with longest subject length l, and the bound is tight.
  - O(n²·l), i.e. proportional to |C#|, for unambiguous certificate sets.
  - Linear for the threshold extension.
- **What failed / critiques, and why:**
  - Distributed discovery (certificates scattered across servers) is left open. Ajmani's DFS was incomplete. The authors assume the prover already holds the certificates.
  - Li (2000) later reinterpreted SPKI/SDSI as logic programs, i.e. Datalog. The authors cite this; I did not read it.
- **Lesson for Mini (fork 2 + naming, security kernel):**
  - **Shape — the prover finds, admission checks.** The client/Rust side runs closure plus DFS *off admission*. The invocation carries the compressed derivation. The Lean admitter only checks it: each line is one composition of two earlier lines, so checking is linear in the proof. This matches RFC 2693 §6.3.4 ("reductions in the order provided by the prover") and suits re-execution, because admission cost is bounded by proof size, which the signer pays for.
  - **Law boundary.** Name resolution is *monotone* and Datalog-shaped. Mini's law fragment is difference logic, and the two are orthogonal.
    - Do **not** try to encode transitive name resolution inside difference-logic laws.
    - Add a separate certified decision procedure: "chain check" over namespace cells, with a soundness theorem against the V(·) least-fixed-point semantics of Definition 8.
    - Let laws refer to its verdict as an atom: `member(signer, ns.path)`.
    - **[INFERRED]**
  - **Disagreement to flag.** If laws are "unified into a decidable Objective Bend fragment" (fork 2, option 3), group membership is the first predicate that fragment must include. It is *not* difference logic.
  - **Cost:** a Lean checker for compressed derivations (≈ the ticket/rewrite rules above), a proof that it agrees with the closure semantics, and a Rust-side discoverer. Moderate. This is the strongest single "law-checkable delegation" artifact in the literature I read.

#### SPKI Certificate Theory (RFC 2693) — authorization over identity, deterministic validity, delegation control
- **Cite:** Ellison, C., Frantz, B., Lampson, B., Rivest, R., Thomas, B. & Ylonen, T. (1999). *SPKI Certificate Theory*. IETF RFC 2693 (Experimental). https://www.rfc-editor.org/rfc/rfc2693.txt . Local: `~/paperbin/world-program-model/ellison-rfc2693-spki-1999.txt`. **[READ]** §1–6 in full; §7 through 7.4. §7.5–8 not read.
- **OS-level decisions:**
  - *Authorization, not identity.* Certificates map `authorization → key`; the `key → name` mapping is only for auditors (§3.3). A global unique name is "politically undesirable and relatively useless" (§2.4–2.6). Where a global ID is unavoidable, use a key or its hash: uniform-looking, with no recognizable sub-field (§2.4, §2.7).
  - *Delegation is a boolean.* Depth control was rejected: "there is no control on the width of the delegation tree, so control on its depth is not a tight control on proliferation" (§4.1.4). A delegator may always mint a fresh key, so separating "may delegate" from "may exercise" is pointless (§4.2).
  - *5-tuple reduction.* `<I1,S1,D1,A1,V1> + <I2,S2,D2,A2,V2> → <I1,S2,D2,AIntersect(A1,A2),VIntersect(V1,V2)>` when `S1 = I2` and `D1` holds. AIntersect is set intersection over tags with `(* set)`, `(* prefix)` and `(* range)` forms. VIntersect is interval intersection.
  - *Deterministic validity.* "Every authorization computation is deterministic, under SPKI rules" (§5.1). "Wandering anti-matter" CRLs are banned; CRLs must be timed with non-overlapping validity intervals (§5.2). One-time revalidations use nonces (§5.5).
  - *Certificate Result Certificates* (§6.6) cache a reduction as a new signed statement.
- **Evidence:** Specification only.
- **What failed / critiques:** SPKI never reached standards track; X.509 won the deployment war. RFC 2693 §5.7.2 itself records Rivest's critique that the *verifier*, not the issuer, should set the required freshness.
- **Lesson for Mini (fork 2, security kernel):**
  - **Strong agreement — determinism.** Mini admits by deterministic re-execution, and SPKI is the one PKI designed so that the authorization verdict is a pure function of inputs. Adopt its rule: no revocation input that can arrive "late". Any revocation is a cell whose state at the turn's height is the input.
  - **VIntersect is difference logic.** Intervals over block heights (`valid_until` is a block height) are bounds `h ≥ a`, `h ≤ b`. Credential validity therefore lives *natively* in Mini's existing law fragment, and the AIntersect lattice is the attenuation lattice of capabilities. **[INFERRED]**
  - **Concrete build:** a Mini capability/credential = a 5-tuple cell; reduction = law-checked composition; validity = difference-logic bounds on height.
  - **Cost:** small. Mostly a vocabulary decision.

#### Petname systems (Stiegler) — Zooko's triangle answered by three names, not one
- **Cite:** Stiegler, M. (2005, updated 2010). *An Introduction to Petname Systems*. http://www.skyhunter.com/marcs/petnames/IntroPetNames.html . Local: `~/paperbin/world-program-model/stiegler-petnames-2005.html/.txt`. **[READ]** in full.
- **OS-level decisions (naming, UI):**
  - *Three names per entity:*
    - a **key** (global, securely unique, not memorable);
    - a **nickname** (global, memorable, not unique: the entity's self-chosen proposal);
    - a **petname** (secure and memorable but *private*).
  - *Alleged names* are names proposed by an introducer, and referrals are key + alleged-name pairs.
  - *Petnames are bidirectional.* Every UI reference to the key renders as its petname. Bookmarks are only one-way "lambda names", which is why they fail against phishing.
  - *Implementation requirements:*
    - at most one petname per key per user per application;
    - assignment only by explicit user action;
    - user-editable;
    - a similarity check against existing petnames at creation;
    - nicknames and alleged names visually distinct from petnames.
- **Evidence:** Informal experiments, e.g. CapDesk, Polaris pilots ("people were aware of and sensitive to the petname markings"), the Waterken petname toolbar, buddy lists. No controlled study.
- **What failed / critiques:** The paper itself names the hard part: transferring *purposeful trust* along with a key. Petname creation must be both painless and mimicry-free, and the paper calls this solvable but unproven. Nickname squatting and the "just click OK" culture around CAs are its examples of what goes wrong.
- **Lesson for Mini (presentation, naming):**
  - The proposed **card = authorized view + affordances** projection is exactly the place to enforce petname logic.
  - Every reference a card renders (a key, a cell id, a package hash) is translated through *the viewer's* petname table. That table is a cell owned by the viewer, with its own law: one key ↔ one petname, written only by the owner.
  - Self-proposed names (an object's nickname field) and introducer-supplied names render in a visually distinct style. Discord, web and AI residents must all render the same tri-partite distinction.
  - An AI resident speaking on a user's behalf must use the user's petnames, never nicknames. Otherwise it becomes the mimicry channel. **[INFERRED]**
  - **Cost:** one per-viewer cell plus a rendering rule shared by all front-ends. Low, but it has to be in the projection contract from day one.

#### Petnames: a humane approach (Spritely) — petnames + edge names + proposed names
- **Cite:** Lemmer-Webber, C., Miller, M. S., Larson, Z., Sills, K. & Yaacoby, E. (2023, last modified 2025-04-25). *Petnames: A humane approach to secure, decentralized naming*. Spritely Institute. https://spritely.institute/static/papers/petnames.html . Local: `~/paperbin/world-program-model/lemmerwebber-petnames-2023.html/.txt`. **[READ]** in full. (The lane brief listed "Farmer"; the actual author list is the one above.)
- **OS-level decisions:**
  - Names come in four kinds:
    - **petnames**, local and private;
    - **edge names**, names an entity publishes for others, forming paths like `Alyssa ⇒ Ben Bitdiddle`. The authors credit the path separator to SPKI/SDSI.
    - **proposed names**, contextual (an email display name);
    - **self-proposed names**, from an entity's profile.
  - DNS becomes "just another naming hub" (`dns ⇒ paypal.com`).
  - Collisions among proposed names render disambiguated (`Pizza Piano.2`, capped at 9, then `Pizza Piano…`).
  - Sort order: petnames first, then one-level edge names.
- **Evidence:** UI scenarios (a contact list, a browser address bar). No implementation numbers.
- **What failed / critiques:** The paper admits it glosses over how edge names are distributed: certificate broadcast versus on-demand query. A naming hub with a "nearby names sold as a package" policy (confusables) is proposed, not built.
- **Lesson for Mini (naming, presentation):**
  - **Edge names *are* SDSI linked local names rendered for humans.** Mini can have one structure serving both machines and people: the namespace cell from the SDSI entry, rendered as `owner ⇒ identifier`. Machine-checked SDSI paths and human edge names are the same data. **[INFERRED]**
  - **Proposed model gap.** The brief has no notion of a published name for an object. Recommend that every object/package cell may carry a self-proposed name, plus that each principal's namespace cell publishes edge names. Petname resolution happens client-side in the projection.
  - **Cost:** none beyond the SDSI namespace cell.

#### IPFS — content-addressed Merkle DAG + self-certifying mutable names
- **Cite:** Benet, J. (2014). *IPFS — Content Addressed, Versioned, P2P File System (Draft 3)*. arXiv:1407.3561. https://arxiv.org/abs/1407.3561 . Local: `~/paperbin/world-program-model/benet-ipfs-2014.pdf/.txt`. **[READ]** in full.
- **OS-level decisions:**
  - *Objects.* Immutable, multihash-addressed objects (`links[] + data`) form a Merkle DAG. Paths are `/ipfs/<hash>/name/path`, and "there is no global root … we simulate the root with content addressing".
  - *Multihash.* A self-describing hash (`<fn code><len><digest>`) so the hash function can evolve.
  - *Mutable names (IPNS).* `/ipns/<NodeId>`, where `NodeId = hash(pubkey)`, is a signed pointer to an immutable object published through the routing system. The immutable-object / mutable-pointer dichotomy is explicitly borrowed from Git refs and Plan 9 Venti/Fossil.
  - *Human-friendly names* via peer links (an SDSI-like web of trust), DNS TXT records, and proquints.
  - *Persistence* is per-node **pinning**.
  - *Incentives.* BitSwap credit ledgers with a sigmoid send probability `P = 1 − 1/(1+exp(6−3r))` over debt ratio r.
- **Evidence:** Draft design. The deployed system came later and is not evaluated in this paper.
- **What failed / critiques, and why:**
  - Pinning is the weak point: nothing pays anyone to keep unpopular content.
  - Practitioners say so repeatedly on HN: "IPFS would normally need a pinning node to keep contents from disappearing … who pays for this?" (theamk, HN 18749761, 2018-12-24); "Neither Filecoin nor IPFS guarantee content is available forever … someone must be pinning it" (Jtsummers, HN 26666530, 2021-04-01). Retrieved via Scry `hackernews.items`. **[READ]**
  - Filecoin's storage market was the later attempt to price persistence. I did not read the Filecoin paper.
- **Lesson for Mini (naming, fork 4, fork 5):**
  - **Agrees** with "package = read-only content-addressed cell". Mini should also copy:
    - (a) **multihash framing** in package ids, so the hash can rotate without reinterpretation, in line with the greenfield "refuse to load the old shape" rule;
    - (b) the **immutable object / mutable pointer split**. "Which version is `@alice/escrow`" is a *pointer cell* governed by a law, not a property of the package. Fork 4's governed upgrade then becomes "move a pointer, under the pointer cell's law", while objects keep pinning exact hashes.
  - **Disagrees** with any notion that content addressing gives persistence for free. In Mini every content-addressed cell must have a *payer or a retention root* (see the storage rent entries). Otherwise Mini reproduces IPFS's "who pins it?" gap. **[INFERRED]**
  - **Cost:** multihash framing is trivial; pointer cells are one law template.

#### Unison — hashes are names; names are metadata
- **Cite:** Unison Computing (accessed 2026-10-04). *The big idea*; *Hashes* (language reference); *Updating code and dependencies*. https://www.unison-lang.org/docs/the-big-idea/ , …/docs/language-reference/hashes/ , …/docs/usage-topics/workflow-how-tos/update-code/ . Local: `~/paperbin/world-program-model/unison-the-big-idea-2026.*`, `unison-hashes-2026.*`, `unison-update-code-2026.*`. **[READ]** all three pages.
- **OS-level decisions:**
  - *Definition identity.* A definition is identified by a SHA3-512 hash of its syntax tree. Bound variables are numbered positionally and dependencies replaced by their hashes, so the hash "pins down all its dependencies".
  - *Recursion and constructors.* Mutually recursive cycles hash together as `#x.n` (canonical order sorted by member hashes); constructors are `#x#c`; builtins are `##Nat`.
  - *Names* are separately stored metadata pointing at hashes.
  - *Consequences the docs claim:*
    - **no builds** (parse/typecheck once, cache never invalidated, deterministic test results cached);
    - **no dependency conflicts** (two `Email` types with different hashes coexist);
    - **typed durable storage** (a persisted value refers to definitions by hash, so it deserializes with the same meaning years later);
    - **code shipping** (the receiver requests missing hashes on the fly).
  - *Updates.* Changing a type re-opens every transitive dependent in a scratch branch, and the codebase is "never in a broken state".
- **Evidence:** A shipping language and the Unison Cloud product. The docs give no numbers.
- **What failed / critiques:** Not in these pages. Known practitioner frictions (text-file tooling, git integration) I did not verify this session, so they are not claimed.
- **Lesson for Mini (fork 4, fork 5, naming):**
  - **Agrees** strongly with "object pins package hash": it is Unison's typed-durable-storage argument. A Mini **checkpoint** that references code only by hash is interpretable forever, so the exact checkpoint codec can never misdecode after an upgrade.
  - **Fork 4 consequence.** A migration is an ordinary checked function `State@hashOld → State@hashNew`. Both types coexist as different hashes, exactly Unison's "two Email types". The governed upgrade = law-checked application of that function plus re-pinning.
  - **Fix/mixins.** Core4's general `fix` and Fare-style mixins with one final self create mutually recursive definitions. Hash the strongly connected component as a unit, as `#x.n` does, so a package hash is canonical. **[INFERRED]**
  - **Presentation.** Since names are metadata, Mini's cards must *render* hashes through petnames/edge names (Stiegler), never show raw hashes as identity.
  - **Cost:** canonical Core4 serialization with SCC hashing. That is a theorem-worthy artifact (hash respects alpha-equivalence) but bounded.

---

### 5.2 Metering, scheduling, economics

#### Resource Containers — separating the resource principal from the protection domain
- **Cite:** Banga, G., Druschel, P. & Mogul, J. C. (1999). *Resource Containers: A New Facility for Resource Management in Server Systems*. OSDI '99. https://www.usenix.org/legacy/events/osdi99/full_papers/banga/banga.pdf . Local: `~/paperbin/world-program-model/banga-resource-containers-1999.pdf/.txt`. **[READ]** in full.
- **OS-level decisions:**
  - A **resource container** is the resource principal for one *independent activity* (e.g. one HTTP connection), and it is decoupled from processes (protection domains) and threads.
  - *Bindings.* A thread's resource binding is dynamic and set by the application; a thread multiplexed over several containers has a *scheduler binding* to the set. Sockets and files can be bound to containers so that **kernel work done on the activity's behalf** (network processing, LRP-style) is charged to the container.
  - *Hierarchy.* Containers form a hierarchy: a child is constrained by its parent's share, which enables "resource sandboxes" for CGI or guest servers.
  - *Containers are descriptors.* They are passed between processes like file descriptors.
- **Evidence:**
  - Primitive costs 1–3 µs, with no throughput change for one container per request.
  - High-priority client latency stays nearly flat under low-priority overload (with a new event API).
  - CGI limited to 30% or 10% of the CPU "enforced almost exactly".
  - Under a 70,000 SYN/s flood, throughput stays at about 73% of maximum.
  - Prototype size: 820 new lines plus about 6,550 lines of integration in Digital UNIX.
- **What failed / critiques:** The authors leave out access control on containers ("space does not permit"). Fixed-share guarantees hold only over tens of seconds. The idea survives in Linux cgroups, not as an application-level primitive.
- **Lesson for Mini (metering, fork 1, fork 3):**
  - The proposed model conflates *who pays* with *who executes*. Mini should separate them: the **meter (resource principal)** charged for a turn is distinct from the **objects (protection domains)** the turn touches. One turn that calls across several objects (fork 1) charges one meter.
  - **Kernel work is charged too.** The LRP point transfers directly: law evaluation, satisfiability checks, Plan application, Merkle path updates and checkpoint encode/decode are "kernel work on behalf of an activity". They must be metered to the invocation's meter, not absorbed by the Host. Absorbed kernel work is precisely the Broken-Metre attack surface (next entries). **[INFERRED]**
  - **Container hierarchy = meter tree** (see KeyKOS below).
  - **Cost:** the metering must cover the admitter's own steps, not just Core4 steps. That is a design invariant, not a big build.

#### Lottery Scheduling — proportional share with tickets and currencies
- **Cite:** Waldspurger, C. A. & Weihl, W. E. (1994). *Lottery Scheduling: Flexible Proportional-Share Resource Management*. OSDI '94. https://www.waldspurger.org/carl/papers/lottery-osdi94.pdf . Local: `~/paperbin/world-program-model/waldspurger-lottery-scheduling-1994.pdf/.txt`. **[READ]** in full.
- **OS-level decisions:**
  - *Tickets.* Resource rights are tickets: abstract, relative and uniform. Each quantum is a lottery, and expected share equals the ticket fraction.
  - *Ticket transfers.* A client blocked on RPC transfers its tickets to the server, which solves priority inversion.
  - *Ticket inflation* is allowed only among mutually trusting clients.
  - *Currencies.* Hierarchical currencies, backed by base-currency tickets, **contain inflation inside a trust boundary**.
  - *Compensation tickets* (inflate by 1/f when only fraction f of a quantum is used) keep I/O-bound clients at their share.
  - *Locks.* A lottery-scheduled mutex funds the holder with all waiters' tickets.
  - *Space-shared resources.* An *inverse lottery* picks which client loses memory.
- **Evidence:**
  - Mach 3.0 prototype. Dhrystone ratios track allocations (2:1 gives 2.01:1; 20:1 gives 19.08:1 over 3 min).
  - Client-server queries at 8:3:1 gave response-time ratios of 7.69:2.51:1.
  - Currencies insulate loads (aggregate ratio 1.01:1 before, 1.00:1 after another currency inflated).
  - Overhead comparable to Mach timesharing.
- **What failed / critiques:**
  - Randomized: accuracy only improves as √n, and the 10:1 run gave 13.42:1.
  - Waldspurger's own follow-up, stride scheduling (thesis 1995, cited in Banga et al. ref. 47), gives the deterministic version. I did not read it. **[INFERRED from citation]**
- **Lesson for Mini (fork 3):**
  - **Proportional share by funding fits resident resumes, but randomness does not fit re-execution.** A lottery must be seeded from consensus data (block hash) to be replayable, and even then its √n error is pointless when a deterministic virtual-time scheduler exists (Demers, below).
  - **Keep the structure, swap the mechanism:**
    - tickets → meter funding weights;
    - currencies → sub-meters with a fixed exchange to their parent (inflation contained);
    - **ticket transfer on call → a message to a resident carries the sender's funding**, so the callee's resume is scheduled at the caller's share (priority inheritance across Mini objects);
    - compensation → charge actual steps, not quanta.
  - **Cost:** a deterministic weighted-fair queue in the Host's turn selection. Small.

#### Spawn — a distributed computational economy (auctions, sponsors, conservation of funding)
- **Cite:** Waldspurger, C. A., Hogg, T., Huberman, B. A., Kephart, J. O. & Stornetta, W. S. (1992). *Spawn: A Distributed Computational Economy*. IEEE TSE 18(2):103–117. https://waldspurger.org/carl/papers/spawn-ieee-tse-feb92.pdf . Local: `~/paperbin/world-program-model/waldspurger-spawn-1992.pdf/.txt`. **[READ]** in full (figures as extracted text).
- **OS-level decisions:**
  - *Market.* Idle workstations sell CPU time slices by **sealed-bid second-price auction**. A resource manager kills tasks that overrun what they bought, and gives the running task right of first refusal on extensions.
  - *Sponsorship hierarchy.* A manager funds its children through "pipes". Managers can neither create nor destroy funds: **conservation of funding across forks**. Funding is a continuous *rate*.
  - *Priority is money.* Funding is an abstract, relative priority across heterogeneous machines.
- **Evidence:**
  - About 90% efficiency (10.3% overhead at 60 s slices).
  - Resource shares track funding ratios (simulated 3:2:1 gave 2.95:1.77:1 on 64 nodes).
  - Equilibrium price equals the money inflow rate ($0.06/s into 6 auctions gave $0.0098/s average price).
  - Heterogeneous machines priced within 20% of their relative worth (1.4×).
- **What failed / critiques, and why (the authors' own §V):**
  - **Iterated second-price auctions are volatile:** with funding $1/$2/$3, prices oscillate between $3 and $8 and are sensitive even to tie-breaking order.
  - Bidding overhead limits the system to coarse tasks.
  - Spatial price differentials persist under nearest-neighbour topologies.
  - No security: "no attempt … to protect the Spawn economy from … forging currency".
  - Their conclusion: **replace auctions with direct proportional sharing**, since "the average price in an iterated second-price auction converges to the sum of the funding rates", which led to the "priority flow" framework.
- **Lesson for Mini (fork 3, metering):**
  - **Don't run auctions per resume.** Allocate in proportion to funding rate (deterministically) and *derive* a price.
  - **Adopt "conservation of funding across forks" as a law:** when an activity forks sub-activities, it splits its meter and cannot mint. Phrased over meter cells, this is a sum invariant (`Σ children ≤ parent`), i.e. difference-logic territory. **[INFERRED]**
  - **Cost:** a law template on meter cells.

#### Markets and Computation: Agoric Open Systems
- **Cite:** Miller, M. S. & Drexler, K. E. (1988). *Markets and Computation: Agoric Open Systems*. In B. A. Huberman (ed.), *The Ecology of Computation*, North-Holland, 133–176. https://papers.agoric.com/assets/pdf/papers/markets-and-computation-agoric-open-systems.pdf . Local: `~/paperbin/world-program-model/miller-markets-computation-1988.pdf/.txt`. **[READ]** §1–2, §4 (Foundations, all), §5.1, §5.4, §7, §8, Appendix I start. **[SKIMMED]** §3, §5.2–5.3, §6, Appendix II.
- **OS-level decisions:**
  - *Foundations* = encapsulation and communication of **information, access (capabilities) and resources**. Capability security means access arrives only by birth, by message, or by creation. Security rests on *inabilities*, so an interpreter cannot add it on top of an insecure base.
  - *Round-robin is a commons.* A round-robin scheduler "is treated as a commons", and a spawner dilutes everyone else (§4.2).
  - *Performance modularity.* Prices are to performance what interfaces are to competence (§4.3).
  - *Currency between mutually distrustful machines* needs trusted bank objects; many local currencies (§4.4).
  - *Caching rule.* Cache a result when storage cost is below request rate × recompute cost (§5.1).
  - *Idle time* is evidence of a broken allocator (§5.4).
- **Evidence:** A position paper with no implementation.
- **What failed / critiques:**
  - §7 itself explains why agoric systems did not appear: accounting overhead is unjustified at small scale, and there was no compelling need.
  - 30+ years on, the vision lives mainly in blockchains (gas) and in Agoric's own ERTP work, not in OS schedulers. **[INFERRED]**
- **Lesson for Mini (metering):**
  - **The "round-robin is a commons" argument is decisive for fork 3.** Per-object or per-activity round-robin over residents lets anyone who spawns many residents dilute everyone else. Scheduling weight must come from *resources held*, not from the *count of entities*.
  - **Mini already has the paper's three foundations:**
    - laws + cells = encapsulation of information;
    - signed invocations + capabilities = access;
    - the missing third, encapsulation of **resources**, is what the meter cell supplies.
  - **Cost:** conceptual. It sets the invariant "no unmetered resource consumption reaches the Host".

#### Incentive Engineering for Computational Resource Management — escalators, expense accounts, rent, market-sweep GC
- **Cite:** Drexler, K. E. & Miller, M. S. (1988). *Incentive Engineering for Computational Resource Management*. In *The Ecology of Computation*, 231–266. https://papers.agoric.com/assets/pdf/papers/incentive-engineering-for-computational-resource-management.pdf . Local: `~/paperbin/world-program-model/drexler-incentive-engineering-1988.pdf/.txt`. **[READ]** §1, §2 (all), §3.1, §3.2.1, §3.2.3–3.3, §4–6. **[SKIMMED]** §3.2.2 and the FCP appendix.
- **OS-level decisions:**
  - **Escalator algorithm.** A process places a bid on an "escalator" rising at a fixed rate per time unit. Every slice goes to the highest current bid, paying the second-highest. A capped maximum initial bid guarantees **non-starvation**. Steady-state share ≈ R/P (escalation rate over price). With all bidders on the initial strategy it **reduces to round-robin**.
  - **Expense accounts.** "A client includes access to its current expense account in each outgoing request"; the consultant charges it, or substitutes its own account. Variations: a **limited new account** (a threshold) and a **shadow account** to monitor charges.
  - **Rent-based storage.** Landlords auction space. Consultants charge clients **retainer fees** to pay rent, and **objects that cannot pay are evicted = garbage-collected**. Unreferenced loops that cross trust boundaries "go broke and are evicted" without migrating them to one machine.
  - *Threshold pointers* generalize weak and strong pointers.
  - **Dividend algorithm.** Solves the public-goods/free-rider problem of shared retainers by turning retainers into investments repaid from per-use surcharges, with an incentive to report one's own future use truthfully.
  - **Alert and base-demand algorithms** propagate "need money" signals and demand-flux estimates. The authors flag a *race* that can wrongly evict.
  - **Probabilistic charging** (sample and charge T × price) cuts accounting overhead.
- **Evidence:** Analysis only. The code in the appendix "has not been run".
- **What failed / critiques, and why:**
  - The authors themselves say the storage algorithms are "substantially more expensive than typical garbage collection" and suitable only for large objects.
  - The alert algorithm can fail under unfavourable reserves, notice periods and path lengths.
  - Base-demand estimates create incentives to low-ball.
  - The public-goods problem they solve with dividends is exactly what later sank Ethereum state rent (see the state-rent entry: "bystander effect", "who would pay rent for a trustless non-owned contract?").
- **Lesson for Mini (metering, fork 3, fork 5):**
  - **Expense accounts are the right invocation shape.** A Mini invocation names the meter to charge. A callee may charge it or switch to its own meter (ICP's "reverse gas", below). Passing a *new limited meter* bounds the callee's spend. This is the capability-held meter. **[INFERRED]**
  - **The escalator is deterministic** and computable from block height: `priority = initialBid + rate·(h − h₀)`. Mini can use it for resident resumes when a resident wants "run soon, at higher price" versus "run cheaply when idle" (a stationary escalator = run only when the price drops).
  - **Rent-eviction as GC is attractive for fork 5 but dangerous as stated:** eviction races and public-goods problems are documented by the inventors. Mini's version should be **hibernate, not delete** (see the state-rent entry).
  - **Cost:** expense-account plumbing is small. Rent-sweep GC is not worth building as described.

#### KeyKOS meters and space banks — the capability-held meter
- **Cite:** Hardy, N. (1985; 8th ed. 1990). *The KeyKOS Architecture*. Operating Systems Review 19(4). Mirror: http://www.cap-lore.com/CapTheory/upenn/OSRpaper.html . Local: `~/paperbin/world-program-model/hardy-keykos-architecture-1985.html/.txt`. **[SKIMMED]** I read the "Meter service" and space-bank sections in full; the rest is covered by another lane.
- **OS-level decisions:**
  - *Meters.* A domain runs only if its meter slot holds a key to a valid meter, through a **chain of meters to the primitive meter**. Every meter in the chain records consumption.
  - *Two keys.* The *meter key* grants (bounded) consumption; the *meter service key* reads and replenishes. **"The meter key holder can build inferior meters."**
  - *Exhaustion.* When a counter hits zero, the **meter keeper** is called with a service key (to replenish) and a **resume key to the waiting domain**. The keeper is therefore the scheduler for everything under that meter.
  - *Space banks.* Banks sell nodes and pages. Inferior banks have their own limits, and destroying a bank reclaims everything ever bought from it.
- **Evidence:** A commercial OS (KeyKOS, then EROS/CapROS). Not measured here.
- **What failed / critiques:** Not covered in the sections read.
- **Lesson for Mini (metering, fork 3, fork 5):**
  - This is the cleanest model for "a meter is an object you hold and can subdivide", and it maps onto Mini almost literally:
    - **meter cell** = fuel counter + parent meter reference + keeper (an object to notify);
    - running out of fuel during a resident's resume does not kill it: the activity **suspends at the checkpoint with status "awaits funding"**, and the keeper (an owner's resident, a sponsor, a treasury object) receives a resume capability;
    - this is the KeyKOS keeper/resume-key protocol expressed in Mini's Activity vocabulary (yield with what it awaits).
  - **Space bank ↔ checkpoint storage.** A resident's checkpoints are bought from a bank meter, and destroying the bank reclaims them.
  - **This strongly favours capability-held meters over a single global fee market inside a domain** (see the synthesis).
  - **Cost:** meters as cells with a sum-invariant law; one Activity "awaits" variant (`AwaitsFuel`). Small to moderate.

#### Broken Metre — gas mispricing as a systematic DoS
- **Cite:** Perez, D. & Livshits, B. (2020). *Broken Metre: Attacking Resource Metering in EVM*. NDSS 2020. https://www.ndss-symposium.org/wp-content/uploads/2020/02/24267.pdf . Local: `~/paperbin/world-program-model/perez-broken-metre-2020.pdf/.txt`. **[READ]** in full.
- **OS-level decisions studied (EVM gas):**
  - a fixed per-opcode gas table (tiers 0/2/3/5/10, special);
  - a base cost of 21,000 per transaction;
  - fees non-refundable even if the transaction fails;
  - repricing hard forks (EIP-150 raised EXTCODESIZE 20 → 700, SUICIDE 0 → 5,000; EIP-2200 storage).
- **Evidence:**
  - Replaying 2.5 months of mainnet on an instrumented aleth client:
    - **CPU time is essentially uncorrelated with gas**; storage dominates (Pearson 0.907 post-EIP-150; storage+memory 0.938; adding CPU *lowers* the correlation);
    - MUL costs 65% more than ADD at equal speed; DIV is about 5× slower than MUL at equal gas;
    - BLOCKHASH, BALANCE and SLOAD show huge variance from I/O;
    - the page cache gives 24–33× speedups;
    - cached data is fully evicted after about 16 full blocks.
  - **A genetic algorithm** searching for programs minimizing gas/second reaches about 107k gas/s, **more than 100× slower** than typical contracts (about 20M gas/s). Generation 243 produces a 9.9M-gas block taking 93 s.
  - All major clients were affected (geth 75.6 s, Parity 47.1 s, Parity on bare metal 18.2 s per 10M gas).
  - Estimated cost: about $0.74 per block to keep commodity nodes from syncing. A fixed geth ran 20× faster.
  - $5,000 bug bounty.
- **What failed / critiques, and why:**
  - **A per-instruction price table cannot express costs that depend on hidden state** (cache, state size, I/O) or on argument size. Repricing is whack-a-mole: "increasing the cost of IO instructions … is often not sufficient … albeit it does increase their cost".
  - Long-term fixes named: stateless clients with **witness-carrying transactions**; dynamic penalties for instruction overuse (Chen et al.); sharding to bound state size.
- **Lesson for Mini (metering — the most important input in this lane):**
  1. **Exact Core4 step counting is necessary and not sufficient.** `runBounded`'s step count is exact and deterministic, so CPU-like metering is solved by construction. Broken Metre's point is that the attacks live *elsewhere*. In Mini those places are **store reads** (sparse-Merkle path walks; a cold cell costs I/O), **forcing large thunks / big Core4 data**, **checkpoint decode/encode proportional to heap size**, **law evaluation** (difference-logic satisfiability is polynomial: price it per constraint/edge, not per call), and **Plan application** (Merkle updates per touched cell). Each must be priced as a function of its *input size*. Wasmtime's newer `OperatorCost::variable` (per-byte, per-element, per-page) is the industry move in the same direction. **[INFERRED]**
  2. **Price as if cold.** Because the Host's cache state is not part of the turn's inputs, the price must not depend on it. On the n=4 BFT mesh, replicas differ in cache warmth, and only a cold-priced schedule keeps the "time per gas" bound uniform.
  3. **Witness/read-set declaration.** Adopt the stateless-client fix natively: an invocation **declares the cells it will read** (the read set), and the Host prefetches and charges per declared cell. An undeclared read is a deterministic refusal. Two side benefits: fork 3 gets read/write sets for free (Block-STM-style parallelism without speculation), and the admitter's I/O is bounded before execution starts. **[INFERRED]**
  4. **Refused turns are not free.** Ethereum charges fees on failure. Mini re-executes and *then* the law may refuse, so the re-execution was spent. If refusal is free, refusal is the DoS. The meter debit must sit *outside* the atomic turn (charged on refusal, up to the signer's declared limit), as EVM fees sit outside revert.
  5. **Make the attacker's tool a standing gate.** Broken Metre's genetic search for minimal gas/time is cheap to reproduce. Mini should run it as a calibration fuzzer against its cost table (per Core4 step rule, per law constraint, per byte of checkpoint) and fail the gate if any program's ns/gas exceeds a bound. Better still, state it as a **Lean theorem**: for every step rule, the modelled resource growth (heap cells allocated, store bytes read) ≤ k · gas charged. That turns "metering soundness" into a checked statement instead of a table.
  - **Cost:** cost function per step rule and per kernel operation (moderate), read-set declaration in the invocation format (moderate; greenfield, so just do it), fuzzer gate (small), metering-soundness theorem (moderate).

#### Transaction Fee Mechanism Design (EIP-1559) — what a global fee market can and can't do
- **Cite:** Roughgarden, T. (2020). *Transaction Fee Mechanism Design for the Ethereum Blockchain: An Economic Analysis of EIP-1559*. arXiv:2012.00854. https://arxiv.org/abs/2012.00854 . Local: `~/paperbin/world-program-model/roughgarden-tfm-eip1559-2020.pdf/.txt`. **[READ]** §1–6 and §8.6.5–8.6.6. §7, §8.1–8.5 and §9 not read.
- **OS-level decisions analysed:**
  - **Base fee** as a history-only posted price, burned. Update rule `r ← r·(1 + (s − s*)/(8 s*))`, i.e. ±12.5% per block.
  - Variable block size up to 2× target.
  - User **tips** to the block producer.
  - Formal properties defined:
    - **MMIC** (myopic miners follow the rule, no fake transactions);
    - **UIC** (an "obvious optimal bid" exists, a symmetric ex-post Nash equilibrium);
    - **OCA-proofness** (no gain from off-chain agreements).
- **Evidence (theorems):**
  - First-price auctions are MMIC and OCA-proof but **not UIC**.
  - Vickrey auctions are **not MMIC**: a miner gains by inserting fake bids (revenue 9 → 16 in the example).
  - 1559 is MMIC (Theorem 6.4), (r+μ)-costly against fake transactions, OCA-proof, and UIC except under an "excessively low base fee" (sudden demand spikes).
  - "**Persistently high transaction fees is a scalability problem, not a mechanism design problem**" (Takeaway 1).
  - The burn exists primarily to defeat off-chain agreements (Remark 5.28).
  - The 1/8 rate is a "magic number" priced against the cost of a double-full-block attack (≈1.9 ETH for 5 min, ≈275,000 ETH for 30 min).
- **What failed / critiques:** The update rule is "somewhat arbitrary". Variable block size opens a (costly) attack. UIC fails exactly when it matters most: demand spikes.
- **Lesson for Mini (metering — global fee market vs held meters):**
  - Mini's admitter is a single Host process (or a committee). The block producer is the operator, who chooses order and could insert its own invocations. Roughgarden's results say:
    - (a) if Mini ever prices by auction, use first-price or posted price, **never second-price** (the operator can shill);
    - (b) a **posted price** is the only UX-friendly option, i.e. a per-domain price per unit of metered work, adjusted by utilization with a 1559-style rule;
    - (c) if the payment goes to the operator, off-chain deals bypass the posted price. The base component should therefore go to a **domain treasury object or be burned**, not to whoever sequences.
  - **Where this matters:** only in multi-party domains with independent sequencers. In a single-operator domain, a held meter funded out of band is simpler and needs no mechanism-design guarantees. **[INFERRED]**
  - **Cost:** a posted-price parameter per domain plus a treasury object. Low. Defer the update rule's tuning; it is a parameter, not an architecture.

#### State rent in practice — Ethereum (abandoned), Solana (abandoned for deposits), ICP (freeze, then delete)
- **Cite:**
  - Akhunov, A. (2019). *EIP-2026: State Rent H — Fixed Prepayment for accounts* (status: Stagnant). https://eips.ethereum.org/EIPS/eip-2026 . Local: `~/paperbin/world-program-model/akhunov-eip2026-state-rent-prepayment-2019.txt`. **[READ]**
  - Akhunov, A. et al. (2019). *State Fees (formerly State rent) pre-EIP proposal version 3*, Ethereum Magicians thread. https://ethereum-magicians.org/t/state-fees-formerly-state-rent-pre-eip-proposal-version-3/2654 . Local: `…/akhunov-state-fees-v3-2019.txt`. **[SKIMMED]** the changelog and objections.
  - Yi, H. (2023). *SIMD-0084: Disable rent fees collection* (status: Implemented). https://github.com/solana-foundation/solana-improvement-documents/blob/main/proposals/0084-disable-rent-fees-collection.md . Local: `…/solana-simd0084-disable-rent-2023.md`. **[READ]**
  - DFINITY (accessed 2026-10-04). *Fee breakdown* and *Canister settings* (portal docs). https://internetcomputer.org/docs/building-apps/essentials/gas-cost . Local: `…/dfinity-icp-gas-cost-2026.mdx`, `…/dfinity-icp-canister-settings-2026.mdx`. **[READ]**
- **OS-level decisions:**
  - **Ethereum (proposed, never shipped).** Rent prepaid into a per-account `rentbalance` field at creation, non-recyclable via mining. "Lock-ups" were replaced with prepayments. Accounts are "hibernated so that users are forever able to restore them". `PAYRENT`/`CALLFEE` opcodes let others pay. "Linear cross-contract storage" makes the user who created the data own it.
  - **Solana.** Accounts must hold a rent-exempt minimum balance. Since about 2022 rent-paying accounts cannot be created, and SIMD-0084 removed rent collection entirely to "simplify the validator design … rent collection code is a non-trivial piece of code".
  - **ICP.**
    - "Reverse gas": canisters pay, users don't.
    - Storage costs about 127k cycles/GiB/s (≈ $5.35/GiB/yr).
    - **Storage reservation:** above 750 GiB of subnet use, new allocations move cycles into a non-transferable reserve, up to 10 years of payments at capacity.
    - **Freezing threshold** (default 30 days): a frozen canister executes nothing and pays only rent. When cycles run out it is **uninstalled** (code and data deleted, id kept).
    - Compute allocation buys guaranteed scheduling (1% gives a slot every 100 rounds).
    - Long messages run with *deterministic time slicing* (DTS) and reserve cycles for the maximum.
- **What failed / critiques, and why:**
  - Ethereum rent stalled on: **public goods / bystander** ("who would pay rent for a trustless decentralized non-owned contract?"); immutable legacy contracts that cannot add `CALLFEE`; **dust griefing** (an attacker adds storage that others must pay for); and migration complexity ("we're designing the migration from the legacy system").
  - Solana found periodic collection not worth its complexity once deposits existed.
  - ICP's deletion on exhaustion is a known operational hazard: the docs themselves recommend top-up automation (CycleOps).
- **Lesson for Mini (fork 5: "storage charged"):**
  - Mini is greenfield, so Ethereum's migration objections vanish. The public-goods and griefing problems do not. Recommended design:
    1. **Deposit, not periodic rent.** Each yield stores a checkpoint, and the resident's meter posts a **deposit proportional to checkpoint size** into the object cell's own `storage_deposit` field (EIP-2026's `rentbalance`, Solana's rent-exempt minimum). GC at yield shrinks the checkpoint, and the **delta is refunded**. That gives a direct, local incentive for small checkpoints and needs no rent-collection machinery.
    2. **Pressure pricing like ICP.** The deposit rate per byte rises with total store size (ICP's reservation curve), so the store's growth is priced where it happens.
    3. **Hibernate, never delete.** When a meter cannot fund a required deposit, the object is *frozen* (ICP's semantics): it accepts no resumes. Later it may be *evicted to its hash*: the sparse Merkle leaf keeps the content hash, and the bytes leave the hot store. **Anyone holding the bytes can restore it** by presenting the preimage (content addressing makes restoration self-verifying) and paying the deposit. This is Ethereum's "hibernation with restore" made trivial by Mini's Merkle store, and it converts IPFS's "who pins it?" problem into "anyone may re-pin, and the hash proves it". **[INFERRED]**
    4. **Who pays for shared objects.** Make the payer explicit per cell (the creator's meter by default, à la "linear cross-contract storage"). Avoid any rule where writes by A make B's deposit grow; that is dust griefing.
  - **Cost:** one deposit field and law, a freeze state, an evict-to-hash and restore path. Moderate. It replaces both GC policy and storage pricing.

#### Faasm — lightweight isolation, snapshots, and fairness delegated to the OS
- **Cite:** Shillaker, S. & Pietzuch, P. (2020). *FAASM: Lightweight Isolation for Efficient Stateful Serverless Computing*. USENIX ATC 2020. arXiv:2002.09344. https://arxiv.org/abs/2002.09344 . Local: `~/paperbin/world-program-model/shillaker-faasm-2020.pdf/.txt`. **[READ]** §1–5 in full, §6.1–6.3. §6.4–8 not read.
- **OS-level decisions:**
  - **Faaslets:** WebAssembly SFI memory isolation, with many tenants in one address space.
  - **CPU fairness via Linux cgroups** (one thread per Faaslet, equal CFS shares) and network via namespaces and `tc` shaping.
  - Shared memory regions remapped into a Wasm linear memory. Two-tier state: a local shared tier plus a global KVS with push/pull and global locks.
  - **Proto-Faaslets:** snapshots of initialized execution state (stack, heap, tables), restorable **across hosts** in hundreds of µs and used to **reset a Faaslet after every call** so no tenant data leaks.
  - The host interface is minimal and WASI capability-style.
- **Evidence:**
  - SGD training: 60% faster, 70% less network transfer, 90% less billable memory than Knative containers.
  - Inference: >200% more throughput, tail latency <150 ms versus >2 s.
  - Faaslet <200 KB versus containers at about 8 MB; cold start <10 ms; Proto-Faaslet restore in hundreds of µs.
- **What failed / critiques:** Fairness relies on the OS (non-deterministic, coarse). SFI alone gives no resource isolation (the paper's own Table 1). Wasm was 32-bit at the time.
- **Lesson for Mini (fork 5, metering):**
  - **Snapshot-as-template is directly reusable.** A package can publish, content-addressed, an **initialized checkpoint** (thunks already forced, mixins already resolved). Creating a resident = restoring that checkpoint, and per-turn reset is free because Mini already restores from checkpoint on every resume.
  - **Disagreement:** Faasm's cgroup/CFS fairness is unusable under re-execution consensus. Fairness in Mini must be computed from *counted* work, not wall time. Faasm is therefore the counter-example motivating in-language metering. **[INFERRED]**
  - **Cost:** "initialized checkpoint" is a package field. Low.

#### Wasmtime fuel vs epochs — deterministic metering with yield on exhaustion
- **Cite:** Bytecode Alliance (accessed 2026-10-04). *Interrupting Wasm Execution* (docs) and `wasmtime::Config::{consume_fuel, operator_cost, epoch_interruption}` (API docs). https://docs.wasmtime.dev/examples-interrupting-wasm.html ; https://docs.wasmtime.dev/api/wasmtime/struct.Config.html . Local: `~/paperbin/world-program-model/wasmtime-interrupting-wasm-2026.md`, `…/wasmtime-config-2026.html`. **[READ]** the two sections.
- **OS-level decisions:**
  - **Fuel** is "completely deterministic: the same program run with the same amount of fuel will always be interrupted at the same location", at higher overhead.
  - **Epochs** are cheap (about 10% slowdown) but **non-deterministic** (wall-clock based).
  - On interruption, either **trap** or **async-yield** to the host, which may resume later (`fuel_async_yield_interval`).
  - `operator_cost` sets per-operator costs, including variable per-byte, per-element and per-page costs.
  - Neither mechanism handles time blocked in host calls.
- **Evidence:** Product documentation; the "~10%" epoch overhead figure is the docs' own.
- **Lesson for Mini (metering, fork 3):**
  - **Mini's `runBounded` is fuel, by construction.** Keep it the only interruption mechanism inside admission; epochs are disqualified because replicas would diverge.
  - **Copy the async-yield option at the language level.** A long computation should not be one huge atomic turn. It should be an activity that yields *at fuel boundaries* and is resumed by further paid turns, each a deterministic slice. ICP's DTS does the same at the platform level.
  - **Design choice.** Either (i) out-of-fuel inside a turn = deterministic refusal (charged) and nothing persists, or (ii) an explicit `Activity` effect "checkpoint and continue" that the program places, making slices visible and atomic per slice. Recommend (i) as the default and (ii) as the opt-in idiom, so the atomicity of turns stays unconditional. **[INFERRED]**
  - **Cost:** small. The semantics already have a bound and a checkpoint codec.

#### Fair Queueing — deterministic weighted fairness, and the question "who is the user?"
- **Cite:** Demers, A., Keshav, S. & Shenker, S. (1989/1990). *Analysis and Simulation of a Fair Queueing Algorithm*. SIGCOMM '89; extended in Internetworking: Research and Experience 1:3–26 (1990). https://cseweb.ucsd.edu/classes/wi01/cse222/papers/demers-fq-ire90.pdf . Local: `~/paperbin/world-program-model/demers-fair-queueing-1989.pdf/.txt` (scanned PDF; I OCR'd pp. 1–8). **[SKIMMED]** pp. 1–8 (motivation, max-min fairness, algorithm definition, first analysis).
- **OS-level decisions:**
  - Emulate bit-by-bit round-robin: each packet gets a finish number `F = max(F_prev, R(t)) + P` and is sent in order of smallest F.
  - A promptness parameter δ via bids `B = P + max(F_prev, R(t) − δ)`.
  - On overflow, drop from the largest queue.
  - Fairness criterion: max-min.
  - **Who counts as a user?** Per source, per destination, per process and per source-destination pair are each gameable. Per-process "encourages … several processes" (the Sybil problem). They chose conversations.
- **Evidence:** Analytical delay bounds for Telnet against FTP sources, plus simulations (pages I did not OCR).
- **Lesson for Mini (fork 3):**
  - **Mechanism.** A deterministic virtual-finish-time scheduler is the replay-safe replacement for lotteries. For resident resumes: `F_i = max(F_i,prev, V(h)) + gas_i / weight_i`, admit in increasing F. It is computable from the turn log alone.
  - **Fairness unit.** Weight must come from **meter funding**, not from keys, objects or activities. Each of those is free to multiply (Miller–Drexler's "commons" point again). **[INFERRED]**
  - **Cost:** small.

---

### Cluster synthesis (§5)

Read together, these works describe one pattern for a multi-party, language-based OS: **resolve names and admit authority with small, decidable, prover-supplied derivations, and charge for every resource through objects the caller holds.** Six lessons carry the most weight for Mini.

**1. Use three kinds of name with a strict division of labour.**
- Global identity is a hash: content hashes for packages and code (IPFS, Unison), key hashes for principals (SPKI §2.7).
- Delegation and grouping use **SDSI linked local names**, stored in a namespace cell per principal.
- Humans see **petnames**: private and bidirectional, rendered by the projection. Edge names are just SDSI paths rendered for people (Spritely).
- Mutable "which version" names are **pointer cells governed by laws**, separate from immutable content (IPFS's IPNS/Merkle-DAG split; Git refs; Plan 9's Venti/Fossil split). Fork 4's governed upgrade is moving such a pointer.
- An object pinning an exact package hash is what makes its checkpoints interpretable forever (Unison's typed-durable-storage argument).

**2. Delegation should be checked, not searched.**
- SPKI/SDSI name resolution is a least fixed point of rewrite rules. Discovery costs O(n³l) (Clarke et al.), but checking a supplied compressed derivation is linear.
- Admission therefore receives the derivation from the signer; the client side does the search.
- Validity intervals over block heights are plain difference logic, so they belong in Mini's existing law fragment.
- Transitive membership is Datalog-shaped, not difference logic. It needs its own certified checker, whose verdict laws use as an atom.
- When a check fails, return the residual, partially evaluated requirement (SDSI's hint), and keep FAIL (missing evidence) distinct from FALSE (violates the law).

**3. Re-execution makes step metering exact, but steps are not where the attacks are.**
- Broken Metre's central measurement: EVM gas tracked storage and ignored CPU and I/O variance. An automated search then found programs over 100× slower per unit of gas than typical ones.
- Mini's dangerous costs are store reads, large-data forcing, checkpoint encode/decode, law satisfiability checks, and Merkle updates. Each must be charged as a function of its input size and priced as if the cache were cold.
- Invocations should declare their read sets. That bounds and prefetches I/O, and it gives fork 3 conflict detection for free.
- Refused turns must still be charged.
- The adversarial search itself should become a standing gate, and ideally a Lean theorem that charged gas bounds modelled resource growth.

**4. Use held meters inside a domain, and a posted price only between parties.**
- KeyKOS meters, Agoric expense accounts and Spawn's sponsorship all say the same thing: a meter is an object you hold, subdivide and pass along with requests, with funding conserved across forks.
- On exhaustion, a keeper receives a resume capability. In Mini this is an activity yielding with "awaits funding", not a kill.
- Banga's resource containers add that the payer is a different principal from the protection domain, and that kernel work done for a turn is charged to that turn.
- A global fee market matters only where independent sequencers exist. There, Roughgarden's results apply: use a posted price, never second-price auctions, and route the base fee away from the sequencer.

**5. Schedule residents in proportion to funding, deterministically.**
- Lottery scheduling's structure carries over: tickets become meter weights, currencies become sub-meters, and transfers on calls give priority inheritance. Its randomness does not carry over.
- Spawn's own conclusion: auctions are volatile, and direct proportional sharing gives a stable price.
- Use virtual-finish-time scheduling (Demers) or escalators (Drexler–Miller). Both can be replayed exactly from the turn log.
- The fairness unit is funding, never entity count, because a round-robin scheduler is a commons.

**6. Charge storage as refundable deposits, and hibernate rather than delete.**
- Periodic rent failed in practice: Ethereum's proposals stalled on public-goods and griefing objections, and Solana removed rent collection.
- Deposits proportional to checkpoint size, refunded when GC at yield shrinks the checkpoint, put the cost exactly where Mini's "GC at yield" happens.
- Freeze unfunded objects (as ICP does), then evict them to their Merkle hash. Anyone holding the preimage can restore one by paying again. This closes IPFS's "who pins it?" gap without Drexler–Miller's eviction races.

Where this lane disagrees with the proposed model: it says nothing about who pays, about refusal cost, or about names. Each of those has a well-tested answer above, and all of them are cheap to adopt in a greenfield system.

---

## §6. Live, inspectable, malleable systems; the UI as a projection; local-first (reading lane E)

Scope: what the live-object / malleable-software / local-first lineage teaches Mini's presentation
subsystem ("a card is an authorized view plus affordances; web/Discord/AI-resident render the same
projection"), "using is programming" (end-user mixins over an object's prototype, gated by law and
upgrade governance), local-first versus single-Host re-execution admission, why images failed at
collaboration and versioning, and liveness versus determinism.

All local copies are under `~/paperbin/world-program-model/`. Tags: READ = I read the text (for long
theses: the named chapters); SKIMMED = abstract/intro/selected sections; INFERRED = my connection.

---

### 6.A Local-first and malleable software (Ink & Switch)

#### Local-first software — seven ideals; CRDTs as the data layer; servers demoted to "cloud peers"
- **Cite:** Kleppmann, Wiggins, van Hardenberg, McGranaghan (2019). *Local-first software: you own
  your data, in spite of the cloud.* Onward! 2019, pp. 154–178, doi:10.1145/3359591.3359737.
  https://www.inkandswitch.com/essay/local-first/ . Local: `kleppmann-local-first-2019.pdf/.txt`
  (PDF) and `kleppmann-local-first-2019-web.txt` (the web essay, which I read end to end). **[READ]**
- **OS-level decisions:** *Persistence/authority:* swap the roles of server and client: "we treat the
  copy of the data on your local device ... as the primary copy. Servers still exist, but they hold
  secondary copies." *Communication:* CRDT changes can travel over any channel (server, P2P, Bluetooth,
  USB stick); a small edit or a batch "more like a pull request". *Conflicts:* the CRDT keeps
  concurrent values of the same property and leaves them to the application or user. *Naming/sharing:*
  URLs ("access permissions for documents beyond secret URLs remain an open research question").
  *Infrastructure role:* servers become "cloud peers" for discovery, backup, burst compute and bridging,
  "not on the critical path".
- **Evidence:** Three Electron/React prototypes (Trellis Kanban, Pixelpusher drawing, PushPin canvas),
  used by a five-person team plus about ten external usability testers, with no formal evaluation
  method. Findings: Automerge "works"; offline is "splendid"; FRP/reducer plus CRDT gives real-time
  collaboration "with little effort"; conflicts were rarer than feared and the default merge policies
  sufficed in every prototype ("we have so far not identified any case requiring customised semantics");
  history visualisation matters; URLs are a good sharing primitive.
- **What failed / critiques:** By their own account: CRDT history grows without bound and "can't easily
  be truncated" because a peer may reconnect after six months; P2P networking (NAT traversal) was
  "nowhere near production-ready"; peers are "never fully online or offline", which makes "kaleidoscopic"
  states hard to reason about; access control and "stop sharing" have no answer ("If we can't remove
  documents from others' computers, what does it mean to stop sharing?"); schema evolution has no
  authoritative "current" schema. The scope is explicit: "We are not talking about implementing things
  like banking services, e-commerce, social networking ... which are well served by centralized systems."
- **Lesson for Mini (fork 3, presentation, naming):** **Mini's authority-bearing state is exactly the
  category local-first excludes.** Balances, capabilities and law-guarded cells need a total order of
  admitted turns. The paper itself treats conflicts on one property as something for the application,
  and a law is precisely an application invariant that a blind merge does not preserve. So AGREE with
  the single-Host / BFT ordering for authority. Mini already gets some local-first ideals by
  construction: *Long Now* and *user control* follow from content-addressed packages plus signed
  receipts plus deterministic re-execution. A holder of (package bytes, receipt log) can re-derive and
  audit state without the Host, which no cloud app offers. What to build: (1) a **replay kit**, i.e.
  receipts plus packages being enough for any client to re-run admission in Lean and reach the same
  root. This makes the Host a sequencer rather than an oracle (cost: receipts must carry or reference
  every input; storage is charged). (2) A **non-consensus presentation tier** that *is* local-first:
  per-viewer card layouts, drafts and annotations live in a CRDT the viewer owns, never in cells
  (cost: a second store kind, but no law machinery). (3) **Offline drafts as speculative turns**: a
  client re-executes the method against its replica and shows the predicted Plan. On reconnection the
  draft is submitted and may be refused, and the law's refusal explanation is the UX. This is the
  "optimistic UI" the paper criticises, but Mini's refusal *explanations* answer the paper's complaint
  that optimistic UIs fail opaquely. DISAGREE with "servers in a supporting role" for authority cells.
  AGREE with it for everything a viewer owns.

#### Malleable software — gentle slope, tools-not-apps, communal creation; Patchwork/Farm/Cambria lessons
- **Cite:** Litt, Horowitz, van Hardenberg, Matthews (2025). *Malleable Software: Restoring User Agency
  in a World of Locked-Down Apps.* Ink & Switch essay, June 2025.
  https://www.inkandswitch.com/essay/malleable-software/ . Local: `litt-malleable-software-2025.txt`.
  **[READ]**
- **OS-level decisions:** *Gentle slope* (after MacLean et al. 1990 "Buttons"): each step up in tailoring
  power should need only a small step up in skill. HyperCard's five user levels were explicit modes,
  from read-only up to full scripting, that "served as guardrails". *Tools not apps:* shared data
  (filesystem, Airtable views, Smalltalk image objects, Webstrates DOM) plus a shared workspace
  (OpenDoc parts, Tchernavskij's "entanglers", Varv's additive trigger lists, Dynamicland's global
  database where new tools can "intercept messages between existing objects"). *Communal creation:*
  Nardi and Miller's "local developers" and Shirky's "situated software". *Infrastructure (Ink & Switch
  prototypes):* PushPin = "document FRP" (React component plus Automerge doc, with alternate editors
  registered for a doc type); **Cambria** = read/write schema decoupling via lenses, "ongoing live
  translations", not one-time migrations; **Farm** = code stored and synced in Automerge (Elm, "stricter
  compilation rules helped automate decisions for when to synchronize code"); **Patchwork** = data and
  tool code in Automerge with history and branching for everything ("universal version control").
- **Evidence:** Patchwork is used by the lab for its own work; the essay itself was written in it. A
  "Section Word Counter" tool was written with AI help mid-session, synced as a document "with no need
  to rebuild or redeploy", and shared by link. A "Request Tracker" tool went unused, which cost little.
- **What failed / critiques (their own):** PushPin's strong isolation between embedded components made
  shared context (hover, selection) impossible, and there was no way to reach into an existing
  component. Schema upgrades in PushPin "would frequently break compatibility with existing data".
  Cambria was never productionised ("may require deep integration with the underlying data engine").
  Farm: "How could you work on a tool without breaking it for other people as you edited it?"
  Patchwork: running branches of a tool side by side is unbuilt; the social question of "who makes
  product decisions for a given tool" is open; quality signalling ("as-is" versus maintained) is open.
  Out of scope and open: "Privacy and security: ... When untrusted strangers are sharing modifications
  ... that can access sensitive data, dangerous things can happen" (they work only within trusted
  groups).
- **Lesson for Mini (fork 4, presentation, security kernel):** The essay's own unsolved problem,
  *untrusted modifications over shared data*, is what Mini's "code proposes, law disposes" answers
  structurally. A stranger's mixin can only produce Plans, and every target cell's law judges them, so
  sharing behaviour is safe up to the law. That is a concrete selling point and a design constraint:
  **laws must be strong enough that mixins can be permissionless**. Build a **slope of five rungs**,
  each a distinct capability: (1) invoke affordances; (2) per-viewer card customisation (non-consensus,
  local-first; no governance); (3) a *personal mixin*, i.e. a Fare mixin over the object's prototype
  that runs only in the invoker's own turns (it changes which Plans *you* propose, never what the object
  does for others; gated only by the law); (4) a *proposed* mixin to the object's package through
  governed upgrade; (5) fork the package. Cost: (3) needs the method-resolution rule "viewer mixins
  apply to invocations signed by that viewer" to be part of the signed invocation (the mixin's hash is
  in the signed message), or re-execution is no longer deterministic. On Cambria: DISAGREE for authority
  state. Permanent bidirectional lenses are "two shapes that agree today" kept alive forever. Mini has
  a single admission point and free re-genesis, so a one-shot typed migration is the right default (see
  Dark below). Lenses are acceptable only at the *edge*, for old clients reading a newer card schema.

#### Potluck — gradual enrichment of text into tools; the shared-search propagation hazard
- **Cite:** Litt, Schoening, Shen, Sonnentag (2022). *Potluck: Dynamic documents as personal software.*
  Ink & Switch essay (companion to the Onward! 2022 paper). https://www.inkandswitch.com/potluck/ .
  Local: `litt-potluck-2022.txt`. **[READ]** (the essay; I did not read the Onward! PDF separately).
- **OS-level decisions:** State lives in the text ("There is no hidden metadata; searches are just a
  function of the text"). Computation is pure reactive formulas over extracted data. Annotations are a
  *view-time overlay* that never edits the text, to avoid "circular feedback loops". The one exception is
  explicit buttons whose writes are ordinary edits ("it's impossible to create runaway infinite loops").
  Searches are reusable and composable.
- **Evidence:** About a dozen informal testers, mostly JavaScript programmers; tools built for recipes,
  chores, a cash register, agendas, workouts and trips.
- **What failed:** "changes to a search automatically affect all the documents where it's used. This
  makes it ... very easy to break other documents when editing a search. We suspect a better approach
  would be to decouple the usage of a search in different documents." Parsing pasted text was hard.
  Non-programmers found the JavaScript formulas difficult. Even small tools were "time-consuming to
  understand and modify" for others.
- **Lesson for Mini (fork 4, presentation):** Two direct confirmations. (a) **Pin the package hash per
  object** (the proposed model): Potluck's live-shared searches are the failure that pinning prevents.
  AGREE. (b) **The projection must be a pure overlay; writes go only through explicit affordances that
  become admitted turns.** Potluck's overlay/button split is exactly "view = pure function of committed
  state; affordance = signed invocation". In Mini this can be *typed*: a card renderer is Core4 code
  with no `Activity` in its type, so it cannot perform. That is a checkable guarantee Potluck only
  enforced by convention. Cost: none beyond a typing rule on the projection entry point.

#### Patchwork notebook (2026) — tool heads recorded with document heads
- **Cite:** Ink & Switch (2026). *Patchwork Notebook: "grjte's Account History"* (2026-03-17).
  https://www.inkandswitch.com/patchwork/notebook/account-history/ . Local:
  `patchwork-notebook-account-history-2026.txt`. **[SKIMMED]**
- **Decision:** an "open document" log records the document URL, *the document heads at open time* and
  the tool used; a reviewer asks, "Might you also save the tool heads?"
- **Lesson for Mini (presentation, fork 4):** A card is a function of (cell state at root R, package
  hash P of the object, *renderer package hash Q*, viewer authority). Record all four in any persisted
  view (screenshots in Discord, AI-resident transcripts) so a past card can be re-rendered exactly. This
  is cheap, since all three hashes already exist. **[INFERRED]**

---

### 6.B Smalltalk, Morphic, and the image problem

#### Design Principles Behind Smalltalk — "Reactive Principle"; "an OS is a collection of things that don't fit into a language"
- **Cite:** Ingalls (1981). *Design Principles Behind Smalltalk.* BYTE 6(8), August 1981.
  https://www.cs.virginia.edu/~evans/cs655/readings/smalltalk.html . Local:
  `ingalls-design-principles-smalltalk-1981.txt`. **[READ]**
- **OS-level decisions:** *Personal Mastery*: "a system ... must be entirely comprehensible to a single
  individual". *Good Design*: "a minimum set of unchangeable parts". *Uniform metaphor* of communicating
  objects, with messages the only process outside objects. *Reactive Principle*: "Every component
  accessible to the user should be able to present itself in a meaningful way for observation and
  manipulation". *Operating System*: "a collection of things that don't fit into a language. There
  shouldn't be one." Storage, files, display, input and the debugger are all objects; "nearly the only
  run-time error ... is for a message not to be recognized". Future work names typed *protocol objects*.
- **Lesson for Mini (presentation, security kernel):** The Reactive Principle *is* Mini's card
  requirement: every cell must be able to present itself. Mini can make it total: a default card exists
  for every cell, derived by reflection over Core4 data plus the law, as Naked Objects did. Mini also
  completes Ingalls' unfinished item: Smalltalk protocols were "only a matter of style", while Mini's
  affordances are typed method signatures from a certified checker. DISAGREE with "minimum unchangeable
  parts" taken naively. Mini's unchangeable parts (the law decision procedure, admission) are
  deliberately *not* user-redefinable. Smalltalk's lesson (below) is that redefinable everything means
  any edit can break the editor.

#### Back to the Future: Squeak — VM written in itself; `become:` as in-place schema migration; bit-identical images
- **Cite:** Ingalls, Kaehler, Maloney, Wallace, Kay (1997). *Back to the Future: The Story of Squeak, a
  Practical Smalltalk Written in Itself.* OOPSLA '97. http://files.squeak.org/docs/OOPSLA.Squeak.html .
  Local: `ingalls-squeak-back-to-future-1997.txt`. **[READ]**
- **OS-level decisions:** The VM is written in a Smalltalk subset and translated to C (42 transformation
  rules; the simulated VM runs about 450x slower than the C one). The image is the unit of persistence
  and distribution and "runs bit-identical images across its wide portability base". *Schema change* is
  done by the `become:` primitive: "become operations are essential when adding an instance variable to
  a class with extant instances, as each instance must mutate into a larger object", restructured to
  "exchange the identity of many objects at once" in one memory pass. The GC is tuned for 5–8 ms
  incremental pauses.
- **Evidence:** Self-hosting after about 16 weeks; ports to Unix, Windows and Windows CE by outsiders
  within five weeks of release; a 968 KB image with the full development environment.
- **What failed / critiques:** The paper is a success story. The relevant weakness is structural:
  class-shape change is an untyped, in-place, whole-heap identity swap with no record of *why* or *from
  what*. See the practitioner critiques below.
- **Lesson for Mini (forks 4, 5):** `become:` is what Mini's typed migration replaces. In Squeak the
  migration is implicit (new slots are nil), global (every instance at once) and invisible (no log). In
  Mini, an upgrade turn should be explicit (a typed `migrate : S_old → S_new`), per object (each object
  pins its package, so instances migrate when *their* object is upgraded, not when a class is edited)
  and receipted. "Bit-identical images across platforms" is the property Mini's deterministic Core4
  re-execution guarantees for *turns*. Keep it for *checkpoints* too: the exact checkpoint codec must
  be platform-independent, or a resident cannot be resumed on another replica. **[INFERRED]**

#### Directness and Liveness in Morphic — structural reification; no run/edit mode; "which is the real object?"
- **Cite:** Maloney, Smith (1995). *Directness and Liveness in the Morphic User Interface Construction
  Environment.* UIST '95, pp. 21–28, doi:10.1145/215585.215636.
  https://worrydream.com/refs/Maloney_1995_-_Directness_and_Liveness_in_Morphic.pdf . Local:
  `maloney-morphic-directness-liveness-1995.pdf/.txt` (OCR of a scan, garbled in places). **[READ]**
- **OS-level decisions:** *Structural reification:* every part of a composite is a live, grabbable morph
  ("controls continue to work when they have been removed from their application"). *Layout
  reification:* row/column morphs are objects. *Ubiquitous animation:* `step` methods run
  synchronously in the display cycle, and "observing" polls other objects rather than requiring their
  cooperation. *Live editing:* no run/edit distinction. Their reason: "in a multi-user system, a
  run/edit distinction would require users to agree on the desirable mode at any given moment". A
  context "meta menu" on every morph includes an "Outliner" onto the implementing Self object, and any
  slot can be turned into a button.
- **Evidence:** The Self 4.0 environment itself is built from morphs; outliners have "thousands of
  submorphs nested over a dozen levels". Two users can work concurrently with separate cursors.
- **What failed / critiques (theirs):** Secondary tools (colour changer, property sheets) lose
  directness. The deep problem: "If both the morph and its outliner are on the screen, and the user can
  directly manipulate either, which is the 'real' object?"
- **Lesson for Mini (presentation):** Mini resolves Morphic's "which is the real object" by design: the
  **cell is the only real object**, and every card (use view, inspector or "meta-card" showing package,
  law, mixins and activities) is a pure projection of committed state. Build the meta-menu: every card
  carries an "inspect" affordance that opens the *meta-card* (source hash, law text, refusal history,
  pending activities). Adopt Morphic's modelessness: no global edit mode. Editing an object's behaviour
  is just another affordance ("propose mixin", "propose upgrade"), whose availability is set by
  authority, not by a mode the group must agree on. DISAGREE with Morphic's `step`/polling model for
  kernel state. Residents advance only by admitted, paid turns. Liveness of *display* (animation,
  polling for new roots) belongs in the client renderer.

#### The image problem — practitioner critique (Scry over Hacker News, 2011–2026)
- **Cite:** Hacker News comments retrieved via Scry, 2026-10-04 (items 4619221, 8497298, 15417160,
  21425264, 29221109, 30930810, 31555023, 34313804, 36572438, 45826078, 45826618, 47354288), with the
  quotations of Goldberg (1984) *Smalltalk-80: The Interactive Programming Environment* pp. 458 and 500
  as given by HN user igouy. Local: `scry-hn-smalltalk-image-critique-2026.txt`. **[SKIMMED]** (forum
  corpus; I did not read Goldberg 1984 itself).
- **The critique, by mechanism:**
  - *Merge is undefined:* "it is very difficult or impossible to 'merge' two or more images ... The
    ability to change anything in the image really means the ability to depend on any fact about the
    current image" (29221109, 2021). Users "extend stupid things like 'Object' and none of their code
    will run on your image without finding all the changes they made ... whack-a-mole with change sets"
    (31555023).
  - *Provenance lost:* "you basically got whatever state the developer ended up with, frozen in time,
    with no indication really of how they got there" (45826078). "Some data that was created using the
    old version of the function is still in the image" (8497298).
  - *Reproducibility:* "you would have an Image live on and on and maybe forget how to create it from
    scratch. Pharo has put a lot of effort into 'bootstrapping' the Image via CI to address this
    weakness" (15417160). "Pharo images are fully bootstrapped from a seed" (45826618).
  - *Self-breakage:* an incomplete `=` on a class broke the class browser that evaluated it (30930810);
    a bug "affected not only your target env it also affected your dev env" (36572438).
  - *The 1984 answer:* appoint a "version manager" who rebuilds the system image from submitted code
    files; "the image is a cache. For a reproducible process, version and archive source-code"
    (Goldberg 1984 via 34313804, 47354288).
- **Lesson for Mini (forks 4, 5):** Mini's split is the right one, and the Pharo trajectory (a
  bootstrap from a seed plus git) converges on it: **code is content-addressed and immutable
  (packages); data is per-cell with a declared type and law; the ledger records how every state came
  to be (receipts).** The image's three failures map to three Mini mechanisms: merge is replaced by a
  total order of turns; provenance is replaced by receipts; reproducibility is replaced by genesis plus
  replay. **But Mini reintroduces a small image: the resident checkpoint** (full machine state including
  thunks and closures over a package's code). "Data created using the old version of the function is
  still in the image" is exactly *a suspended activity whose closures belong to package P1 when the
  object is upgraded to P2*. Concrete rule to adopt: (a) a checkpoint pins the package hash it was
  created under, and that package is retained (GC by reachability from live checkpoints; storage
  charged, consistent with fork 5); (b) **typed migration applies to the object's data and to a
  *declared resume-state type* at yield points, never to raw continuations**; (c) an upgrade either
  waits for activities to reach a migratable yield, or lets them finish on old code (two versions live,
  as in Dark's "locked code in use" below). Also adopt the self-breakage lesson: the meta-card and
  inspector are rendered by a *fixed, kernel-pinned* renderer, never by the object's own (possibly
  broken) package code.

---

### 6.C Naked Objects — the closest prior art to "a card is an authorized view plus affordances"

#### Naked Objects (PhD thesis) — behaviourally complete objects, generic viewer, "about" methods
- **Cite:** Pawson (2004). *Naked Objects.* PhD thesis, Trinity College Dublin.
  https://metalup.org/phd_thesis/nakedobjects.pdf (TARA: tara.tcd.ie). Local:
  `pawson-naked-objects-thesis-2004.pdf/.txt` (cleaned: `.clean.txt`). **[READ]** chapters 1, 3, 4,
  5 (intro and 5.1), 8.3 and 9, plus Reenskaug's foreword; the rest **[SKIMMED]**.
- **OS-level decisions:** The application is written *only* as domain entity objects. A *generic*
  presentation layer (View plus Controller) is derived by reflection, with "an enforced correspondence
  between the two layers, so the illusion of manipulating the business objects is total". All user
  action is noun-verb: select an object, invoke one of its methods. Class methods (create, find) appear
  on class icons. **Selective viewing:** every action `actionX` may have an `aboutActionX` that controls
  availability per class, instance and member, "based upon the state ... or ... an authorization server",
  and "can also return a reason for the lack of availability, which the viewing mechanism can render as
  'balloon' help". *Multiple platforms:* "alternative generic viewing mechanisms, each tailored to the
  capabilities of a particular viewing platform", e.g. "each object as a web-page and with each
  behaviour as a hot button". *Process:* no use-case controllers; "purposeful objects" (a Transfer, a
  PriceAdjustment) reify processes as persistent entities with a state machine. *Multi-parameter
  actions:* the open-source framework could not render them, so the workaround was making the
  operation an object: "implement Transfer as a (purposeful) object in its own right ... then invokes
  the 'Execute' or 'Make it so' method".
- **Evidence:** The Irish DSFA Child Benefit Administration system went live in November 2002 (about 80
  users; COM+ objects, a Java applet viewer, XML messages naming viewable fields, associations and the
  method list). Survey of 15 users: 15/15 agreed it "contributes positively to my job satisfaction"
  (10 strongly); most did *not* want to be guided through steps; a backlog of over 20,000 claims was
  cleared (with overtime). An unplanned "once-and-done" reorganisation was possible because "nothing in
  the design of the system got in the way". Batch processing ran at up to twice the specified time, and
  association tables reached 95M rows. No development-time gain on the first project (21 months against
  12 planned, building the architecture in parallel). CarServ comparative experiment: the naked objects
  version needed less effort and was easier to change.
- **What failed / critiques:** Pawson's own limitations: no hand-crafted UI ("safety-critical user
  interfaces, disability access, highly graphical or spatial applications, ... typographical design");
  harder to learn for *infrequent* users (so "customer self-service applications ... are not typically
  good candidates"); batch processing. His proposed fixes: user customisation ("frequently-used options
  ... dragged into an object to appear as a button ... remembered in that user's profile"), viewers as
  first-class objects (Mugridge et al.), and alternative viewers per device. Reenskaug's foreword: the
  original MVC centred "the user's mind", which "was somehow forgotten".
- **Lesson for Mini (presentation):** This is Mini's card model, deployed and measured. It is both
  vindication and warning. Vindication: a generic projection of behaviourally complete objects *did*
  carry a real government transactional system, and the "reason for unavailability" channel already
  existed. **Mini's law refusal explanations are a strictly stronger "about" method**, because they come
  from the same decision procedure admission uses, so the card cannot disagree with the kernel. Build:
  `affordances(viewer, cell, root) = [(method, Visible | Disabled(reason) | Enabled)]`, where Disabled
  reasons come from (a) authority (no capability), (b) the *law's satisfiability check* on the method's
  possible Plans, and (c) the object's own state predicate. Cost: one bounded dry-run per affordance per
  render. Cache by (root, viewer, package). Warning: the generic card serves *frequent, expert* users. For
  infrequent users (most Discord users) Mini needs *task cards* (see Causeway view models). And the
  **multi-parameter workaround is a fork-3 insight**: a multi-party or multi-argument operation becomes
  a first-class *purposeful cell* (an Intent or Deal cell) that parties fill in turn and then "Make it
  so". That is a natural carrier for multi-party atomicity across domains, with each party's
  contribution an admitted turn and the final "execute" turn atomic. **[INFERRED]**

#### Naked objects: a technique for designing more expressive systems — the toolkit
- **Cite:** Pawson, Matthews (2001). *Naked objects: a technique for designing more expressive systems.*
  ACM SIGPLAN Notices 36(12), December 2001, pp. 61–67. (The lane brief dated it 2002; the printed issue
  is December 2001.) https://gwern.net/doc/cs/algorithm/2001-pawson.pdf . Local:
  `pawson-naked-objects-expressive-2001.pdf/.txt`. **[READ]**
- **OS-level decisions:** The Java reflection "Object Viewing Mechanism" (OVM) finds `get`/`set`
  (fields; drag-drop of typed associations, where "attempting to drag in the wrong type of object causes
  the field to flash red"), `action*` methods (menu items), `about*` (greyed out or hidden), `process`
  (meaning of drop-onto-object, also callable from code), `toString` (title) and `Status` (icon variant).
  Collections can be viewed as icon, list or table. At the time, "the system does not indicate to the
  user why a drop is not possible or why an action cannot take place. In the future an object will be
  returned by these methods ... containing the reason, very much like the 'Throwable'". Business rules
  sit "at the lowest level possible", on the objects.
- **Evidence:** The DSCFA prototype: users "within a few minutes ... were already asking questions about
  the system in those terms ('Could I have two Customer objects open at once?')". About 50 developers
  trained; they cited "flexibility" despite the "almost draconian" constraints. Answer to the "bloated
  objects" worry: role-filtered views plus delegating responsibilities to associated objects.
- **Lesson for Mini (presentation):** The 2001 toolkit's admitted gap, *no reason for refusal*, is what
  Mini's law language already supplies. Make refusal reasons a required part of every affordance
  (Disabled must carry a structured, renderable reason; "greyed out without why" is a bug). Also adopt
  "`process` is not UI-specific: it may be called within the program": **every card gesture must
  correspond to an ordinary signed invocation**, so a Discord command, a web button and an AI resident's
  tool call are the *same* method call with the same admission. **[INFERRED]**

#### The Emperor Has No Clothes: Naked Objects Meet the Interface — the usability critique
- **Cite:** Constantine (2002). *The Emperor Has No Clothes: Naked Objects Meet the Interface.*
  Constantine & Lockwood report #122, December 2002 (unpublished).
  http://web.archive.org/web/2006/http://foruse.com/articles/nakedobjects.pdf . Local:
  `constantine-emperor-naked-objects-2002.pdf/.txt`. **[READ]**
- **The critique:** "The greatest usability problem with Naked Objects is the one-size-fits-all premise
  ... one solution is presumed to fit all problems." Context menus are "hidden behavior whose contents
  change and must be perused on every use". Drag-drop and right-click are hard for many users. A forced
  object-then-action grammar ("selecting an object before an action or an action before an object is a
  matter of preference that varies"). Users must learn the jargon of objects. The appeal is to managers
  ("invest nothing at all in usability") and developers. He concedes the real lesson is empowerment:
  give users "better tools ... to achieve diverse ends by diverse means". Pawson replies (thesis §8.3)
  that Constantine had not seen the empirical data.
- **Lesson for Mini (presentation):** The critique targets the *rendering* (one fixed idiom), not the
  *projection* (one authoritative model of what can be seen and done). Mini should keep the projection
  generic and make **renderers plural and task-shaped**. A Discord renderer is verb-first (slash
  commands: action then object), the web renderer can be noun-first, and an AI resident gets a typed
  tool list. All consume the same `Card = {view, affordances with reasons, layout hints}` structure.
  This is the Naked Objects to Restful Objects move (below) and costs one schema for the card. AGREE
  that "web/Discord/AI render the same projection". DISAGREE with any reading where they must render the
  same *layout*.

#### Apache Causeway (ex-Isis, the open-source Naked Objects framework): what fixed "too generic"
- **Cite:** Apache Causeway project (2024–2026). *User Guide: Mixins; Business Rules; UI Layout & Hints;
  View Models; Background, Context and Theory.* https://causeway.apache.org/userguide/latest/ . Local:
  `causeway-{mixins,business-rules,ui-layout-and-hints,view-models,background-context-and-theory}.txt`.
  **[READ]** (documentation, not a paper).
- **OS-level decisions — the five fixes that accreted over 20 years:**
  1. **See it / use it / do it:** every member is checked in turn for visible (`hideX`), enabled
     (`disableX`, which returns a reason) and valid (`validateX(args)`, which returns a reason). "If all
     the members of the object are hidden, then a '404' style message ... is returned." Rules can live on
     the object, in a mixin, or in domain-event subscribers that can *veto*.
  2. **Mixins (contributed actions, collections and properties):** "allowing one module to contribute
     behaviour or derived state to another object ... the underlying domain class being contributed to
     does not 'know'"; bound "statically by way of the contributee type"; explicitly an instance of
     Reenskaug and Coplien's DCI. Crucially, contributed properties and collections "should have no
     side-effects; otherwise the very act of rendering the domain object would change state".
  3. **Layout out of the domain code:** `Xxx.layout.xml`, plus an object may *name an alternate layout*
     "changed according to the roles of the end-user that is viewing it", with fallbacks; title, icon and
     CSS hints come from the object.
  4. **View models = "desire lines":** non-persisted, task-specific objects "recreated dynamically by
     serializing their state ... into the URL itself", aggregating several entities. "You should add view
     models after having built up the domain layer, rather than before ... pave that commonly-trod path."
  5. **Escape hatches:** "custom controllers/views for specific use cases alongside the generic viewer ...
     for those specialised/high volume use cases", and the **Restful Objects** viewer exposing every
     object as JSON resources so custom UIs (React, Vue, ...) and integrations are built *against the
     projection*.
- **Lesson for Mini (presentation, fork 4):** This is the answer to "is Naked Objects a warning?". The
  generic projection survived; what was added is (1) three-stage availability with reasons, (2)
  contributed behaviour, (3) out-of-band, role-selected layout, (4) task projections, (5) the projection
  as a stable API. Mini's design should start with all five rather than rediscover them:
  - `Card` schema = {title, icon/state, fields (filtered by authority), affordances (Hidden | Disabled
    reason | Enabled + per-argument validators), layout key}. Renderers are clients of this schema; this
    is Mini's "Restful Objects".
  - **Mixins are Mini's native mechanism** (Fare-style, with one final self and super). Causeway shows
    contributed *actions* scale as a modularity tool, and that contributed *derived state* must be
    side-effect-free. In Mini that is enforceable by the `Activity` type: contributed fields are
    `Activity`-free. Concretely, an end user's mixin contributes affordances to cards of objects whose
    type matches. Its *actions* still produce Plans judged by law, so contribution is safe.
  - **Task cards = view models:** a pure Core4 function over several cells, unpersisted, whose state is
    carried in the card reference (like Causeway's URL). Build them after watching usage ("desire
    lines"); for Discord this is the main surface.
  - Cost: layout hints and task cards add a presentation package type. Keep them in packages (content
    addressed, pinned) rather than in cells, so presentation never touches law state.

---

### 6.D Boxer — naive realism and spatial scoping

#### Boxer: A Reconstructible Computational Medium
- **Cite:** diSessa, Abelson (1986). *Boxer: A Reconstructible Computational Medium.* CACM 29(9):
  859–868, doi:10.1145/6592.6595. Text via readkong transcription. Local:
  `disessa-boxer-1986-readkong.txt` (the two-column interleaving makes it hard to read but complete).
  **[READ]**
- **OS-level decisions:** *Naive realism*: "users should be able to pretend that what they see on the
  screen is their computational world in its entirety": any text on screen can be moved, edited or run;
  a variable is a box whose contents update when a program changes it. "There is no need to query the
  system to display its state, nor ... invoke a state-change operation to affect the system indirectly."
  *Spatial metaphor:* boxes are computational, not windows ("Windows ... have no computational semantics");
  scoping is containment, so a key binding like `FUNCTION-1-KEY` defined inside PHONE-BOOK "will be
  active only when the user enters" it. Sprites have a graphics form and a data form of the same box;
  `tell` sends messages. **Ports** fix containment's strict hierarchy: "a view of a box at some other
  place in the system ... any change in one will automatically cause the same change in the other",
  used for sharing, cross-reference and multiple views. Desiderata explicitly *not* prioritised:
  formal simplicity, efficiency, uniformity, and "Verifiability—rigor is not a primary requirement".
- **Evidence:** A prototype on Symbolics and TI Lisp machines; the paper is a design argument with
  examples (tutorial, phone book, sprite game, an imagined optics book).
- **Lesson for Mini (presentation):** Two transferable mechanisms. (1) **Affordance scoping by
  context**: Boxer binds keys by containment. Mini's affordances should be scoped by *where the card is
  shown* (inside a room or domain card, the affordances of contained objects are those the room's
  capability set grants), which is how a Discord channel, a web room and an AI resident's context differ
  without different code. (2) **Ports = cell references rendered as live embedded cards**: the same cell
  shown in two places is one cell, as transclusion in Webstrates. Mini gets this for free since cards
  are projections of a root; build "embed card by cell reference". DISAGREE with naive realism for
  writes: in Mini, editing the box a field is displayed in is an *invocation* that the law may refuse,
  so the card must show that editability is conditional (Disabled with reason). Boxer explicitly
  sacrificed rigor, and Mini cannot.

---

### 6.E Liveness with holes — Hazel

#### Live Functional Programming with Typed Holes (Hazelnut Live) — every editor state has meaning; fill-and-resume
- **Cite:** Omar, Voysey, Chugh, Hammer (2019). *Live Functional Programming with Typed Holes.* PACMPL
  3(POPL), 2019; extended version arXiv:1805.00155. https://arxiv.org/pdf/1805.00155 . Local:
  `omar-hazel-live-holes-2019.pdf/.txt` (also `~/paperbin/uweave/omar-hazel-live-functional-typed-holes.pdf`).
  **[READ]** §1, §3.5, §4 and §5; formal §3 **[SKIMMED]**.
- **OS-level decisions:** Empty holes for missing terms or types; non-empty holes as "membranes around
  static and dynamic type inconsistencies". Evaluation *proceeds around* holes, recording each hole's
  closure. Cast failures become holes, not errors. **Fill-and-resume**: hole environments are delayed
  substitutions (CMTT), so after an edit that fills a hole, evaluation resumes rather than restarts.
  **Theorem 4.2 (Commutativity):** filling commutes with reduction, *but* "only for languages where
  evaluation order 'does not matter', e.g. pure functional languages ... Languages with non-commutative
  effects do not enjoy this property." For external effects, "we do not want to continue past a hole ...
  and in so doing haphazardly trigger an unintended effect. In this setting, it is likely better to
  explicitly ask the programmer". DSU-based "edit-and-continue" (Visual Studio, Flutter) comes "without
  any guarantee that rerunning the program will produce the same result". Notebook cells read as let
  bindings ending in a hole, which gives "a reproducibility guarantee missing from Jupyter".
- **Evidence:** Metatheory mechanised in Agda; implemented in Hazel. Cites a study in which about 40%
  of Eclipse Java edits left the program malformed.
- **Lesson for Mini (liveness vs determinism, fork 5):** Mini is unusually well placed to have *sound*
  liveness, because effects are confined to `Activity<P,R,A>`. Pure Core4 segments enjoy Hazel-style
  commutativity; effects occur only at perform/yield boundaries the kernel already checkpoints. Concrete
  design: **"editing a running resident" = re-executing from its last checkpoint under the new package,
  never patching the live heap.** Between yields the code is pure, so the replay is the same as "fill and
  resume" up to the last effect boundary, and the exact checkpoint codec gives the resume point. Hazel's
  "ask before continuing past an effect" becomes "a resumed activity's next Plan is a new admitted turn",
  which is already Mini's model. A second build: **holes in packages under construction** (a draft
  package with typed holes renders cards whose affordances backed by holes are Disabled("unimplemented:
  hole u")), giving a gentle slope for authoring behaviour while every draft state stays meaningful.
  Publication requires completeness. Cost: hole support in the Core4 checker for draft mode only;
  admission never runs holed code.

#### Grove: A Bidirectionally Typed Collaborative Structure Editor Calculus — commuting edits, conflicts as holes
- **Cite:** Adams, Griffis, Porter, Satish, Zhao, Omar (2025). *Grove: A Bidirectionally Typed
  Collaborative Structure Editor Calculus.* PACMPL 9(POPL), Article 73, doi:10.1145/3704909.
  https://hazel.org/papers/grove-popl25.pdf . Local: `adams-grove-collab-structure-editor-2025.pdf/.txt`.
  **[SKIMMED]** (abstract and §1).
- **Decisions:** It removes diff and three-way merge: patches come from the log of edit actions, and
  "all edits commute, i.e. the repository state forms a commutative replicated data type (CmRDT)". The
  core is a labelled multigraph with unique vertex and edge ids; edits are edge insert/delete "with
  deletion being permanent". Conflicts (local, relocation, cyclic relocation) are "represented
  explicitly using holes", and type error localisation is total, so every merged state is statically
  meaningful. Agda-mechanised.
- **Lesson for Mini (fork 4, local-first boundary):** This is the correct shape for *collaborative
  authoring of .obend packages before publication*. Drafts are a commuting, local-first CmRDT where
  conflicts become typed holes, and **publication is one admitted turn that requires a hole-free,
  type-checked core** and yields a content-addressed package cell. Local-first where merging is sound
  (source drafts), consensus where it is not (which package an object runs). Cost: adopt or port a
  Grove-style editor model for Objective Bend syntax. That is non-trivial, and optional until communal
  authoring matters. **[INFERRED]**

---

### 6.F Practitioner retrospectives — Darklang and Eve

#### How Dark deploys code in 50ms — deployless, versioned functions and datastores, trace-driven upgrade
- **Cite:** Biggar (2019). *How Dark deploys code in 50ms.* Darklang blog, 9 July 2019.
  https://blog.darklang.com/how-dark-deploys-code-in-50ms/ . Local: `darklang-how-dark-deploys-50ms.txt`.
  **[READ]**
- **OS-level decisions:** "Dark runs interpreters in the cloud ... deployment is just a small write to a
  database, which is instant and atomic." A structured editor gives every incomplete state an execution
  semantics ("similar to typed holes in Hazel"). **Code in use is "locked"** and editable only through
  feature flags, function and type versioning, and migrations. **Function versioning:** editing makes a
  new version and callers switch per handler via flag ("If that function is deep in the callgraph, this
  makes a new version of every function along the way"). **Package upgrades do not propagate:** "all
  code continues using the exact same version ... you gain the option of upgrading uses ... case-by-case".
  **Language versions** are pinned per piece of code. **DB migration:** datastores are typed, and a
  migration is "a new type, and a rollback and rollforward function"; stores are accessed by versioned
  names (`Users-v0`, `Users-v1`); reads across versions apply the conversion; once no `v0` uses remain,
  "Dark will convert all remaining data in the background". **Trace-driven testing:** "We automatically
  save HTTP requests ... We test new code against those", and "because we run your production code, we
  can test the new versions for you, comparing their output for both new requests and past requests".
- **Lesson for Mini (fork 4, liveness):** Almost a blueprint for governed upgrade, and Mini can do it
  more soundly. Adopt: (a) **pin per object, upgrade per object, never propagate** (AGREE with the
  model); (b) **migration = typed `fwd : S1 → S2` (optional `bwd`)**, checked by the certifying checker,
  plus a law obligation: `law₂(fwd s)` must hold. Mini can discharge it either by re-checking every live
  cell in the upgrade turn (cost O(cells), charged) or, when `fwd` and both laws stay in the
  difference-logic fragment, by a decidable validity check `∀s. law₁(s) → law₂(fwd s)` done once. That
  is a concrete use of the law language's satisfiability machinery. (c) **Trace-driven upgrade
  governance:** Mini already holds every admitted invocation as a receipt and re-execution is
  deterministic, so an upgrade proposal can be accompanied by a **replay diff**: re-run the last N turns
  touching the object under P2 (after `fwd`) and list every turn whose Plan or refusal would differ.
  That is an exact, not sampled, version of Dark's request replay, and the right evidence for upgrade
  governance (fork 4). Cost: re-execution compute, charged to the proposer. DISAGREE with Dark's lazy
  dual-version reads (`Users-v0` read through `Users-v1`) for authority state, because it is a
  permanent two-shapes layer. Mini can migrate eagerly in the upgrade turn, since re-genesis is free and
  admission is single-point.

#### An overdue status update / Goodbye Dark Inc. — why the integrated live environment failed
- **Cite:** Korick (2024). *An overdue status update on Darklang.* Darklang blog, 12 March 2024.
  https://blog.darklang.com/an-overdue-status-update/ ; Biggar (2025). *Goodbye Dark Inc. – Hello Darklang
  Inc.* 16 June 2025. https://blog.darklang.com/goodbye-dark-inc-welcome-darklang-inc/ ; Biggar (2023).
  *Darklang is going all-in on AI.* 28 March 2023. https://blog.darklang.com/gpt/ . Local:
  `darklang-an-overdue-status-update.txt`, `darklang-goodbye-dark-inc-welcome-darklang-inc.txt`,
  `darklang-gpt.txt`. **[READ]** (the first two), **[SKIMMED]** (gpt).
- **What failed, in their words:** "our custom in-browser editor was bad, and disjointed from our users'
  'normal' development flows" (it was "~50% of our codebase", 50k lines of ReScript, a buggy structural
  editor: "Too fancy for our own good"). "Supporting backwards-compatibility was slowing everything down"
  ("it was a bit premature to advertise backwards-compatibility ... The OCaml -> F# rewrite ... would have
  gone by much quicker if we were more tolerant to breakages"). "We weren't writing much Darklang code"
  ourselves. "Users don't like vendor lock-in" (cloud-only runtime, source-available licence). After
  ChatGPT, "our product was not the right one for the era of coding agents. Our online structured editor
  didn't make sense when the LLM is generating the code". What they kept: "deployless, trace-driven
  development, no infra setup", immutability ("the secret sauce"; it makes it "easier to safely run code
  in an LLM or agent environment, and to replay code"). The company ran out of money in 2025 after 8
  years.
- **Lesson for Mini (presentation, fork 4):** (1) **Do not build a bespoke editor as the primary
  surface.** Mini's "AI resident renders the same projection" is correct; the projection must be a
  typed data structure an LLM agent can consume as tools (affordances with signatures and refusal
  reasons), not an editor. (2) The backward-compatibility lesson matches the repo's greenfield doctrine:
  Dark's cost came from *promising* migration of hosted user code early. (3) Dark's surviving core
  (immutability plus replay) is Mini's core, and lock-in was a top complaint. Mini's answer is the replay
  kit (local-first section): an object's history must be re-executable off-Host. **[INFERRED]**

#### Against the Current: What We Learned From Eve — 30+ prototypes; "you give us the model, we give you the interface"
- **Cite:** Granger (2018). *Against the Current: What We Learned From Eve.* Talk at LIVE 2018;
  transcript by J. Ashkenas. https://observablehq.com/@jashkenas/against-the-current-what-we-learned-from-eve-transcript .
  Local: `granger-against-the-current-eve-2018.txt` (auto-transcript, error-prone). **[READ]**. Also
  Granger (2016) *Two years of Eve*, https://chris-granger.com/2016/07/21/two-years-of-eve/ , local
  `granger-two-years-of-eve-2016.txt` **[READ]**; and the HN wind-down thread (story 16227130) via Scry,
  in `scry-hn-smalltalk-image-critique-2026.txt` **[SKIMMED]**.
- **Decisions and evidence:** Light Table made career programmers "about twice as fast" but "did not
  make programming more accessible at all". "We learned with Light Table that we can't just slap a UI
  onto Javascript ...; the platform has to allow for the representation" (2016). Eve's core became a
  Datalog-family temporal relational language and database (BOOM lab lineage). Over the project's life:
  "34 environments and 24 compilers and 9 interpreters". Spreadsheet field research found the crux:
  "every action you take in this environment gives you value", unlike a script that gives "literally
  nothing ... until I've written the entire thing". Eve 0.2 let you ask "why isn't this what I expected
  ... debugging took seconds because ... the system told you exactly what was wrong". Natural-language
  syntax lost "the naturalness" once formalised. The final unreleased version: "you give us the model,
  we give you the interface", building a family business's software on a phone "in 50 seconds", but
  "nobody was interested in trying to productize something like this". Internal lessons: "we must
  understand the whole system" (after two failures where nobody did), and skepticism of dependencies
  ("free as in a puppy").
- **What failed:** commercial (no revenue path for programming tools; big-company copies such as Swift
  Playgrounds), an accessibility goal never reached, and a research scope ("cutting-edge PL, database and
  HCI research as three guys") on a startup timeline.
- **Lesson for Mini (presentation, laws):** Eve converged independently on Naked Objects' thesis
  ("model in, interface out"), which is evidence the card model is a recurring attractor. Two concrete
  pushes. (1) **"Why" is the killer feature of a live system, and Mini can make it exact:** every cell
  value is the result of admitted turns with receipts, and every refusal carries a law explanation.
  Build a kernel query `why(cell, field)` (the turns and Plans that last wrote it) and `whynot(viewer,
  method)` (the authority or law clause that disables it), and render both on every card. (2) "The
  platform has to allow for the representation": the projection's needs (purity of view code, reasons,
  provenance) must be properties of Core4 and the kernel, not of a UI layer added later. That AGREES with
  putting the card in the semantics. **[INFERRED]**

---

### 6.G Shared live documents — Webstrates

#### Webstrates: Shareable Dynamic Media — the DOM as the shared object; transclusion; instruments
- **Cite:** Klokmose, Eagan, Baader, Mackay, Beaudouin-Lafon (2015). *Webstrates: Shareable Dynamic Media.*
  UIST '15, doi:10.1145/2807442.2807446.
  https://www.klokmose.net/clemens/wp-content/uploads/2015/08/webstrates.pdf . Local:
  `klokmose-webstrates-2015.pdf/.txt`. **[READ]**
- **OS-level decisions:** Each page's whole DOM, including embedded JS and CSS, is persisted and
  synchronised through OT (ShareJS) on a central server ("the medium is the model"). **Composition by
  transclusion** (iframes); tools are separate "instrument" webstrates with a per-host "instantiation
  element"; per-user presentation by *container* webstrates and by injecting styles without touching
  the shared DOM. Access rights are "an attribute of its html tag", with external OAuth. Same-origin
  iframes "can access and modify the other".
- **Evidence:** The paper itself was written in Webstrates; the to-do benchmark took 53 logical lines
  against 110 (Meteor) and 90 (Firebase); a 75-tile wall display ran a shared window manager.
- **What failed / limits (theirs):** "a webstrate shares the DOM, the whole DOM and nothing but the DOM";
  problems come "from either wanting to share information that is not represented in the DOM or not
  wanting to share information that is in the DOM". "A webstrate is identical for all users, and cannot
  directly contain different tools for different users"; personal comments needed injected local styles
  to hide them. OT has no move operation. Communication was unencrypted and auth "overly simple"; script
  changes need a reload; libraries like CodeMirror "do not play well with our persistent DOM".
- **Lesson for Mini (presentation):** Webstrates is the cleanest demonstration that *conflating
  presentation state with shared state* is the core pain. Mini should separate three layers explicitly:
  **(i) consensus state (cells, law-judged), (ii) the projection (a pure function, never stored), (iii)
  per-viewer presentation state (layout choices, collapsed panels, private annotations), which is
  local-first and never a cell.** The Webstrates container pattern is Mini's "renderer package plus
  viewer prefs". Transclusion = embedding a card by cell reference (AGREE). Its security model (shared
  code runs with full access to everything same-origin) is the counter-example Mini's capability and
  law split exists to avoid. **[INFERRED]**

#### MyWebstrates: Webstrates as Local-first Software — sovereignty, and the access-control wall
- **Cite:** Klokmose, Eagan, van Hardenberg (2024). *MyWebstrates: Webstrates as Local-first Software.*
  UIST '24, doi:10.1145/3654777.3676445. https://cs.au.dk/~clemens/files/MyWebstrates-UIST2024.pdf .
  Local: `klokmose-mywebstrates-local-first-2024.pdf/.txt`. **[READ]** §1–2 and §6–7; §4–5 **[SKIMMED]**.
- **OS-level decisions:** Webstrates rebased on Automerge "data substrates": local by default
  (IndexedDB), opt-in sync servers or P2P (WebRTC signalled by QR codes), branch and merge by shared
  history, globally unique document ids independent of servers ("collectively owned").
- **What failed / open (theirs):** No global version order ("the order of these versions is not globally
  stable"). Asynchronous *semantic* conflicts "may happen unexpectedly and in distant parts of a
  document"; conflict tooling was deferred. **Authorisation:** the document id is a bearer capability,
  and "there is no mechanism for revoking access ... nothing short of forking the document to a new ID".
  Worse, "anyone can contribute code that everyone will execute in their browser". **Group membership
  under concurrency:** "Alice is a group administrator and removes Eve. Before Bob receives that message,
  he receives updates from Eve and takes actions based on it ... how should Eve's updates be handled?",
  plus mutual concurrent removal of two admins, with "no solution ... currently available for Automerge".
  History cannot be redacted ("passwords ... will thus be accessible"). Federated copies are "extremely
  difficult to delete". Peering two clients shares all open webstrates by accident.
- **Lesson for Mini (fork 3, security kernel):** This is the strongest evidence in the cluster *for*
  Mini's ordered admission of authority. Revocation, membership change and "remove Eve before or after
  her edit" are ordering problems, which a total order of admitted turns (Host or BFT mesh) answers by
  construction: Eve's turn either precedes the removal turn or is refused by the law afterwards. Keep
  capabilities, membership and revocation in consensus cells. Let the local-first layer hold only data
  whose authority is the viewer's own. Also note *unredactable history*: Mini receipts are similar, so
  secrets must never enter cell state or invocation payloads in the clear (a custody-boundary rule for
  the Rust side). **[INFERRED]**

---

### Cluster synthesis (§6)

Read together, these works describe one recurring dream (the system is made of live objects you can
see, touch and reshape, and the UI is just their showing) and two recurring failure points: **shared
mutable state without an order** and **presentation without a model**. Mini's proposed design sits on
the right side of both, but only if a few specific mechanisms are built, not assumed.

1. **The projection is a proven pattern; the warning is about renderers, not projections.** Naked
   Objects carried a production government system on a generic, reflection-derived UI (15/15 users
   positive on job satisfaction), and Eve's last prototype independently reinvented "you give us the
   model, we give you the interface". Constantine's critique and Pawson's own limitations hit the
   *single fixed rendering idiom* and infrequent users. Causeway's twenty-year answer is a checklist
   Mini should adopt on day one: see-it/use-it/do-it with reasons, contributed behaviour (mixins),
   role-selected layout out of domain code, task-shaped view models ("desire lines"), and the projection
   as a stable API (Restful Objects). Mini's law refusal explanations are a stronger version of Pawson's
   "about" methods, because the card and admission share one decision procedure.

2. **Separate three layers: consensus cells, a pure projection, local-first viewer state.** Webstrates
   ("the whole DOM and nothing but the DOM") and Potluck (pure overlays, explicit write buttons) show the
   pain of conflating them. Mini can *type* the separation: projection code is `Activity`-free Core4 and
   so cannot perform. Per-viewer layout, drafts and annotations can be a CRDT the viewer owns.

3. **Local-first is right for what you alone own, and wrong for authority.** Kleppmann et al. explicitly
   exclude banking-like systems. MyWebstrates hits the wall exactly there: no revocation, membership
   races, unredactable history, code from anyone running everywhere. Those are ordering problems that
   Mini's admitted-turn order solves. Mini can still deliver the *Long Now* and *user control* ideals
   through a replay kit (content-addressed packages plus receipts plus deterministic re-execution), so
   the Host is a sequencer, not an oracle.

4. **Images failed because code, data and history were fused in one mutable heap.** Merges are
   undefined, provenance is lost, rebuilds are irreproducible, and `become:` migrations go unrecorded.
   Pharo's escape (bootstrap from a seed plus git) converges on Mini's split of content-addressed
   packages, typed per-cell data and receipts. **Mini's residual image is the activity checkpoint.** Pin
   each checkpoint to its package hash, keep old packages reachable, and migrate data and declared
   resume-state types at yield points, never raw continuations.

5. **Governed upgrade needs evidence, and Mini can produce exact evidence.** Dark showed per-caller
   pinning, typed roll-forward/roll-back migrations and replaying recorded requests against new code.
   Mini can turn the last into a *replay diff* over real receipts, and turn migration safety into a law
   obligation `law₂(fwd s)`, decidable when both laws and `fwd` stay in the difference-logic fragment.

6. **Liveness must be replay, not patching.** Hazel proves fill-and-resume commutes only for pure code,
   and DSU edit-and-continue carries no guarantee. Because Mini confines effects to `Activity`, "editing
   a running resident" can be sound: re-execute from the last checkpoint under the new package, with
   every effect boundary an admitted turn. Grove adds that collaborative *drafts* of packages can be a
   commuting CRDT with conflicts as typed holes, while *publication* is one admitted, hole-free turn.

Underneath all six: "using is programming" is safe in Mini where it was dangerous elsewhere (Ink &
Switch name untrusted modification as unsolved), because a mixin can only *propose* Plans that laws
dispose of. That makes law strength the real limit on how malleable Mini can afford to be.

---

## §H. Evolution of live code: dynamic software updating (read by SCHOLAR-OS directly)

#### H1. Erlang/OTP code replacement and `code_change/3`
- **Cite:** Ericsson (2025). *Erlang System Documentation: Compilation and Code Loading — Code Replacement*; *Appup Cookbook*. https://www.erlang.org/doc/system/code_loading.html ; https://www.erlang.org/doc/system/appup_cookbook.html . Local: `~/paperbin/world-program-model/erlang-code-loading-docs.txt`, `erlang-appup-cookbook-docs.txt`. **[READ]**
- **Content:** "The code of a module can exist in two variants in a system: current and old ... Both old and current code are valid, and can be evaluated concurrently. Fully qualified function calls always refer to current code"; a third load purges old code and kills lingering processes. Processes holding state upgrade by *synchronized code replacement*: suspend, call `code_change(OldVsn | {down, Vsn}, State, Extra)` to transform state, resume; module dependency ordering (`DepMods`) for multi-module upgrades; downgrade functions are first-class. Faré (ch. 5) calls Erlang "far better than anything else" at live upgrade.
- **Lesson for Mini (fork 4):** Adopt the Erlang *shape* precisely: (1) an object has at most two live package versions, `current` and `old`; (2) a checkpointed activity keeps running on the package it was started with until its next yield, and the switch happens at a *resume* (Erlang's "fully qualified call" = Mini's resume boundary); (3) the migration is `code_change`: `(fromVersion, State, Extra) → State'` plus an explicit **downgrade** inverse when the governance wants rollback; (4) multi-object upgrades declare dependency order. Erlang's weakness (types are absent; `code_change` is unchecked) is precisely where Lean helps: Mini can *type-check* `code_change` against both packages' state types and check the post-state against the cell's law.

#### H2. Kitsune: whole-program DSU with explicit update points and generated state transformers
- **Cite:** Hayden, C. M., Saur, K., Smith, E. K., Hicks, M., Foster, J. S. (2014). *Kitsune: Efficient, General-purpose Dynamic Software Updating for C*. ACM TOPLAS 36(4) (OOPSLA 2012 conference version). https://www.cs.umd.edu/~mwh/papers/kitsune-journal.pdf . Local: `~/paperbin/world-program-model/hayden-kitsune-2014.pdf` (.txt beside). **[READ: abstract, §1-2; rest SKIMMED]**
- **Content:** Updates the *whole program* at once, only at explicit `kitsune_update` *update points*; the programmer writes *data migration* and *control migration* (redirect to the corresponding update point in the new version); `xfgen` generates state-transformation code from per-type/per-variable *transformer* specs and traverses the heap "analogously to a tracing garbage collector". Evidence: six programs (vsftpd, redis, Tor, memcached, icecast, Snort) over 3 months-3 years of releases; 57-529 LoC of changes; overhead -2.2% to +2.35%; pause typically <40 ms, <400 ms worst case; multi-threaded programs need all threads to reach an update point.
- **Lesson for Mini (fork 4, fork 5):** Mini's checkpoint at yield *is* a Kitsune update point, and Mini's "GC at yield" traversal is exactly where xfgen's GC-like transformer runs: migrate the heap of a parked activity by traversing its checkpoint and applying per-type transformers. The piece the root has not named is **control migration**: a parked activity's continuation refers to *old package code*. Three honest options, cheapest first: (a) let it finish on old code (Erlang); (b) require the new package to export, per yield site of the old one, a typed *resume adapter* `OldYieldState → NewYieldState` (Kitsune's control migration, typed); (c) refuse the upgrade while such activities exist (quiescence). Ship (a)+(c) first, (b) as the typed general case.

#### H3. Specifying and Verifying the Correctness of Dynamic Software Updates
- **Cite:** Hayden, C. M., Magill, S., Hicks, M., Foster, N., Foster, J. S. (2012). *Specifying and Verifying the Correctness of Dynamic Software Updates*. VSTTE 2012, LNCS 7152. https://www.cs.cornell.edu/~jnfoster/papers/dsu-correct-vstte12.pdf . Local: `~/paperbin/world-program-model/hayden-dsu-correct-2012.pdf` (.txt beside; downloaded by another lane). **[READ: §1-2]**
- **Content:** Observational equivalence is too strong (bug fixes change behaviour); "reachability" is both too weak and too strong (vsftpd example). Proposes *client-oriented specifications*: *backward-compatible* (same in old and new), *post-update* (new behaviour after update), *conformable* (same modulo a uniform interface change); verified by *merging* old program + update into one program that simulates updating at any update point; ~4x verification slowdown.
- **Lesson for Mini (fork 2 × fork 4 — the most important single connection in this section):** Mini's **laws are CO-specs.** A cell's law is a client-visible property that must hold before and after every write, including the write performed by an upgrade's migration. So the upgrade-correctness criterion can be stated in Mini's own terms: *an upgrade is admissible iff the migrated state satisfies the cell's law, and the new package's methods preserve the law* (backward-compatible CO-spec), with *law changes* themselves being a separately governed act (a post-update CO-spec, requiring a higher authority than a code change). This splits fork 4 cleanly: code may change under the owner's authority as long as laws are preserved; laws change only under the law's own governance. INFERRED.

#### H4. Cambria: schema evolution with bidirectional lenses, translated on read
- **Cite:** Litt, G., van Hardenberg, P., Henry, O. (2020). *Project Cambria: Translate your data with lenses*. Ink & Switch. https://www.inkandswitch.com/cambria/ ; paper version: Litt, van Hardenberg, Henry (2021), *Cambria: Schema Evolution in Distributed Systems with Edit Lenses*, PaPoC '21, https://doi.org/10.1145/3447865.3457963 . Local: `~/paperbin/world-program-model/litt-cambria-2020.txt`. **[READ the essay in full; PaPoC paper not read]**
- **Content:** Schema versions form a *graph* whose edges are bidirectional lenses (built on Hofmann-Pierce-Wagner edit lenses); data is stored in the *writer's* schema and "translations in decentralized systems should be performed on read, not on write"; lenses are kept "where even old versions of the program can retrieve them, such as ... as part of the document itself"; one lens spec generates types, runtime JSON Schema and translation. Limits found: perfect compatibility is impossible (single vs multiple assignee: consistency, conservation, predictability cannot all hold); one-directional/partial lenses (firstName+lastName→fullName) and lenses needing external data are unsolved; Stripe's API middleware (a linear stack of per-version translators) is the industrial precedent.
- **Lesson for Mini (fork 4, fork 1):** Mini's upgrade-by-migration is "translate on write" (rewrite the cell's state to the new schema). For *state* that is right — a cell has one owner and one law. But for *calls across objects and across versions* Cambria is the better model: a caller compiled against interface version v3 invoking an object now at v5 should have its arguments and the returned Plan/response translated through a lens chain registered *in the package graph*. Build: package cells carry their `lens` edges to predecessor interfaces; the Host translates invocations at the boundary (Stripe-style); partial lenses refuse with an explanation (the same refusal machinery laws use). This turns a flag-day upgrade into one where old clients (web, Discord, residents compiled earlier) keep working.

---

# Appendix — index of works and reading depth

| § | Work | Tag |
|---|---|---|
| F | F1. Houyhnhnm Computing, ch. 5 "Non-Stop Change" | [READ, in full] |
| F | F2. Houyhnhnm Computing, ch. 10 "Houyhnhnms vs Martians" | [READ, in full] |
| F | F3. Houyhnhnm Computing, ch. 8 "Inter-process Communication" | [READ, in full] |
| F | F4. Orthogonal Persistence, The Model (2024 reframing; LambdaConf 2025) | [READ, in full] |
| F | F5. Climbing Up the Semantic Tower | [READ climbing in full; fci via FAREOO §8 quotes — SKIMMED] |
| F | F6. PCLSRing: Keeping Process State Modular | [READ, §§1-5] |
| 2 | Singularity (system) | [READ] |
| 2 | Sing# channels and the exchange heap | [READ] |
| 2 | Sealed processes | [READ] |
| 2 | Midori | [READ for the four posts named; SKIMMED for the rest] |
| 2 | Theseus | [READ] |
| 2 | RedLeaf | [READ] |
| 2 | Tock | [READ] |
| 2 | House | [SKIMMED: intro, P-Logic, H-monad sections] |
| 2 | JX | [SKIMMED: architecture, portals, performance] |
| 2 | Project Oberon | [SKIMMED: ch. 2–3 (commands, tasks, central loop) read; ch. 6 loader and ch. 8 storage in parts] |
| 2 | Symbolics Genera | [SKIMMED: OCR damaged in places] |
| 2 | Self | [SKIMMED: §4.4 mirrors, §5.5 transporter] |
| 2 | MirageOS / unikernels | [SKIMMED: §1–2 and design sections] |
| 2 | Asterinas | [SKIMMED: abstract, §1–2, §4.4] |
| 2 | Atmosphere | [READ: §1–4 and §5 TCB; eval skimmed] |
| 2 | "Spectre is here to stay" | [SKIMMED: abstract, §1, conclusion] |
| 3 | KeyKOS Architecture | [READ] |
| 3 | KeyKOS checkpoint mechanism | [READ] |
| 3 | KeyKOS Nanokernel | [READ] |
| 3 | EROS: a fast capability system | [READ] |
| 3 | Design Evolution of the EROS Single-Level Store | [READ] |
| 3 | seL4: Formal Verification of an OS Kernel | [READ] |
| 3 | L4 Microkernels: The Lessons from 20 Years | [READ] |
| 3 | Scheduling-Context Capabilities | [READ] |
| 3 | Zircon / Fuchsia component framework | READ (8 concept pages); SKIMMED (Fuchsia as a whole) |
| 3 | The Use of Name Spaces in Plan 9 | [READ] |
| 3 | Plan 9 from Bell Labs | [READ] |
| 3 | The Inferno Operating System | [READ] |
| 3 | Orthogonally Persistent Object Systems | [READ] |
| 3 | PJama review | [READ] |
| 3 | Grasshopper | [READ] |
| 3 | Morningstar (2006): Electric Communities' orthogonal persistence post-mortem | READ |
| 3 | Twizzler | [READ] |
| 3 | Aurora | [READ] |
| 3 | Motoko enhanced orthogonal persistence on the Internet Computer | [READ] |
| G | G1. Orthogonal Persistence Revisited (2010) | [READ, in full] |
| G | G2. A Persistent System in Real Use | [READ, in full] |
| G | G3. TreeSLS: whole-system persistence on a capability tree (2023) | [SKIMMED: abstract, §1-2 read; design/eval skimmed] |
| G | G4. Orthogonal persistence as an anti-pattern (practitioner critique) | [READ] |
| 4 | Urbit whitepaper | [READ] |
| 4 | Urbit today (Gall, threads, Azimuth L2 docs) | READ |
| 4 | Urbit retrospectives and practitioner critiques | [READ] |
| 4 | The Internet Computer for Geeks | [READ] |
| 4 | ICP message execution, inter-canister calls, upgrades (docs + spec) | READ (spec: named sections) |
| 4 | Motoko enhanced orthogonal persistence and migrations | [READ] |
| 4 | Breitner, "How to audit an Internet Computer canister" | [READ] |
| 4 | SwingSet kernel: vats, c-lists, cranks, transcripts, snapshots, metering, upgrade | [READ] |
| 4 | Agoric `asyncFlow` and `vow` | [READ] |
| 4 | Miller & Drexler, "Markets and Computation: Agoric Open Systems" | [READ] |
| 4 | Ethereum Yellow Paper (Shanghai version) | [READ] |
| 4 | Salehi, Clark, Mannan | [READ] |
| 4 | Spritely, "The Heart of Spritely" | [READ] |
| 4 | Holochain whitepaper (2018) and current DNA model | [READ] |
| 4 | Reed (1978), "Naming and Synchronization in a Decentralized Computer System" (NAMOS) | [READ] |
| 4 | Croquet: A Collaboration System Architecture (TeaTime, 2003) | [READ] |
| 4 | Croquet OS / Multisynq (2020s) | [READ] |
| 5 | SDSI 1.1 | [READ] |
| 5 | Certificate chain discovery in SPKI/SDSI | [READ] |
| 5 | SPKI Certificate Theory (RFC 2693) | [READ] |
| 5 | Petname systems (Stiegler) | [READ] |
| 5 | Petnames: a humane approach (Spritely) | [READ] |
| 5 | IPFS | [READ] |
| 5 | Unison | [READ] |
| 5 | Resource Containers | [READ] |
| 5 | Lottery Scheduling | [READ] |
| 5 | Spawn | [READ] |
| 5 | Markets and Computation: Agoric Open Systems | [READ] |
| 5 | Incentive Engineering for Computational Resource Management | [READ] |
| 5 | KeyKOS meters and space banks | [SKIMMED] |
| 5 | Broken Metre | [READ] |
| 5 | Transaction Fee Mechanism Design (EIP-1559) | [READ] |
| 5 | State rent in practice | [READ] |
| 5 | Faasm | [READ] |
| 5 | Wasmtime fuel vs epochs | [READ] |
| 5 | Fair Queueing | [SKIMMED] |
| 6 | Local-first software | [READ] |
| 6 | Malleable software | [READ] |
| 6 | Potluck | [READ] |
| 6 | Patchwork notebook (2026) | [SKIMMED] |
| 6 | Design Principles Behind Smalltalk | [READ] |
| 6 | Back to the Future: Squeak | [READ] |
| 6 | Directness and Liveness in Morphic | [READ] |
| 6 | The image problem | [SKIMMED] |
| 6 | Naked Objects (PhD thesis) | [READ] |
| 6 | Naked objects: a technique for designing more expressive systems | [READ] |
| 6 | The Emperor Has No Clothes: Naked Objects Meet the Interface | [READ] |
| 6 | Apache Causeway (ex-Isis, the open-source Naked Objects framework): what fixed "too generic" | [READ] |
| 6 | Boxer: A Reconstructible Computational Medium | [READ] |
| 6 | Live Functional Programming with Typed Holes (Hazelnut Live) | [READ] |
| 6 | Grove: A Bidirectionally Typed Collaborative Structure Editor Calculus | [SKIMMED] |
| 6 | How Dark deploys code in 50ms | [READ] |
| 6 | Darklang: An overdue status update / Goodbye Dark Inc. / going all-in on AI | READ (two posts); SKIMMED (gpt post) |
| 6 | Against the Current: What We Learned From Eve | [READ] |
| 6 | Webstrates: Shareable Dynamic Media | [READ] |
| 6 | MyWebstrates: Webstrates as Local-first Software | [READ] |
| H | H1. Erlang/OTP code replacement and `code_change/3` | [READ] |
| H | H2. Kitsune: whole-program DSU with explicit update points and generated state transformers | [READ: abstract, §1-2; rest SKIMMED] |
| H | H3. Specifying and Verifying the Correctness of Dynamic Software Updates | [READ: §1-2] |
| H | H4. Cambria: schema evolution with bidirectional lenses, translated on read | [READ the essay in full; PaPoC paper not read] |
