# SCHOLAR-FRONTIER — Agoric in depth, the 2022–2026 frontier, and corrections to the four sibling scholars

Scholar: SCHOLAR-FRONTIER. Date: 2026-10-04. Brief: `/Users/ember/dev/redregg/work/PROGRAM-MODEL-BRIEF-20261004.md`.
Siblings read first: SCHOLAR-BREAD, SCHOLAR-LAWS-CONTRACTS, SCHOLAR-CALLS-CONCURRENCY, SCHOLAR-OS-LINEAGE (Part I
synthesis + "where the sources disagree" + its §4.3 Agoric), and ROOT-READING-NOTES. Nothing was built, run or
committed; no repository was edited. This file is the only deliverable.

**How it was produced.**
- **Part 1 (Agoric) was read by me**, at source: the SwingSet docs already in paperbin (re-read where I cite them),
  plus new downloads: Endo READMEs (SES, exo, patterns, pass-style, eventual-send, captp), the Agoric documentation
  guides (ERTP ×5, Zoe ×10, hardened JS, governance, orchestration ×5), the Zoe *source* that enforces offer
  safety (`offerSafety.js`, `rightsConservation.js`, `zcfSeat.js`, `zoeSeat.js`, `evalContractCode.js`,
  `docs/zoe-zcf.md`), 13 agoric-sdk GitHub issues (10 read) that record production failures, one Agoric forum
  post-mortem, Miller–Morningstar–Frantz 2000, and Drossopoulou–Noble–Miller–Murray 2015. I also read Mini's own
  `Theory/CanonicalResourceKernel.lean` (the kernel Book) because the Agoric mapping depends on it.
- **Part 2 (frontier)** was read by two reading lanes I briefed (Opus), plus my own reading. Each entry says who
  read it: `[me]`, `[lane A]` (effects, capability types, resource bounds, certified checking) or `[lane B]`
  (choreographies, local-first, verified distributed systems, deterministic actors, durable workflows, IFC,
  world-computer OSes). I spot-checked one verbatim quote per lane entry I rely on in Part 3.
- **Tags.** READ = core sections read in the text; SKIMMED = abstract/introduction/located passages; INFERRED = my
  conclusion or background knowledge, not the source's claim. Every new download is in
  `~/paperbin/world-program-model/` (PDF + `pdftotext -layout` `.txt`, or `.md/.txt/.js` for web/source files).
- **Searches.** Kagi: 5 queries by me (POST helper `scratchpad/scholar-os/kagi.sh`); lanes used their own budgets
  (stated in Part 2). GitHub API issue search (free) for Agoric production history.

**Mini facts used (READ in `~/dev/minidregg`).** `Theory/CanonicalResourceKernel.lean`: a kernel `Book` of
accounts with signed balances `Π₀ (AccountId × AssetId) → Int`; an asset *is* its issuer-well account; every
`Operation` (`transfer | mint | burn | fee | lease`) is exactly one `Posting` (one debit, one equal credit), and
`Operation.apply_conserves` proves the per-asset total is preserved; admission forbids non-minting overdrafts. The
law language (`Pred`) and Core4 facts are as summarised by SCHOLAR-LAWS and the brief.

---

# Part 1 — Agoric, mechanism by mechanism

## 1.0 The stack, and the one-line verdict

Agoric's stack, bottom up: a Cosmos-SDK chain (consensus, `vbank`, `vstorage`) → the **SwingSet kernel** (run-queue,
c-lists, kernel promise table, metering, run policy, swing-store) → **vats** (each an `xsnap` XS-engine worker with
heap snapshots and a transcript) → **liveslots** (the vat's "libc": marshalling, virtual/durable objects, GC
reporting) → **Endo / Hardened JS** (lockdown, `harden`, Compartments, pass-styles, patterns, exos) → **ERTP**
(issuers, mints, brands, purses, payments) → **Zoe** (escrow, invitations, seats, offer safety) → contracts written
with **zones, vows and asyncFlow**, **orchestration** across IBC chains, and **governance** (electorates,
ContractGovernor) on top, with chain-level `CoreEval` proposals as the actual root of upgrade authority.

Mini's stack lines up almost layer for layer: Simplex mesh / Host → Lean admission kernel → cells under one Merkle
root → the Core4 machine with its checkpoint codec → packages + laws → the kernel **Book** → offers/objects →
residents → governance. **The verdict:** Agoric is the closest existing system to Mini and its *object-level design*
(c-lists, linear promise resolution, offer safety, rights as objects, exos with guards, legible governance) is the
best prior art there is. Its *production failures* cluster almost entirely in the one place Mini differs by
construction: Agoric runs **untrusted, engine-defined, non-deterministic-GC JavaScript with replay-based
persistence**, so every hard problem (upgrade, GC, metering, engine change, promise survival) became a problem of
reconstructing state the platform could not name. Mini names its whole machine state with a specified codec and
re-executes under a proved semantics. Most Agoric lessons therefore arrive as *"adopt the interface, replace the
mechanism"*.

---

## 1.1 Vats, cranks, blocks, and the kernel boundary

**How it works [me, READ `agoric-swingset-delivery-2025.md` §intro, run-queue; `agoric-vat-data-2025.md`].** Vats
talk only to the kernel through `syscall.*` and receive `dispatch.deliver/notify`; arguments are pure data
(`CapData` body + slots) "to build a deterministic transcript". A **turn** is empty-stack to empty-stack; a
**crank** is one delivery processed until the vat's promise queue is empty; all syscall state changes sit in a
"crank buffer" that is committed or discarded; a **block** is the durable commit and outbound messages are embargoed
until it commits. The kernel keeps a **c-list per vat** mapping vat refs (`o+N` exports, `o-N` imports, `p±N`) to
kernel refs (`koN`, `kpN`); a vat can only cite refs in its c-list, so capabilities cannot be forged across vats.

**What broke.** Nothing structural here; the turn/crank/block tiering is sound (SCHOLAR-OS and SCHOLAR-CALLS
already adopt it). The cost showed up in *size*: by Dec 2024 two mainnet vats had JS heaps of 712 MB
(`v43-walletFactory`, growing ~9.5 MB/day) and 604 MB (`v7-board`); large heaps slowed GC, snapshotting and
state-sync and "sufficiently-large heap snapshots will break state-sync" (issue #10743 "Slow Block Saturdays",
`agoric-issue-10743.txt`, READ). Long END_BLOCK executions (>20–30 s) then broke CometBFT keepalives, so slowness
amplified itself.

**Mini.** *Adopt as is:* the crank-buffer discipline (Mini's atomic turn) and outbound embargo to commit. *Better by
construction:* there is no opaque per-object heap; an object's state is cells under the Merkle root, so "how big is
this object" is a query, and storage is charged (brief fork 5). *Must add (INFERRED):* a **per-block admission budget
in Core4 steps** with a hard wall-clock-independent cap, because Agoric's evidence is that one heavy block degrades
the *consensus network*, not just the block.

## 1.2 Kernel promises: the decider, linear resolution authority, and pipelining

**How it works [me, READ `delivery.md` §Result Promise Management, §Pipelining, §Kernel Run-Queue].** Each kernel
promise has at most one **decider**. "Allocating a new Promise in `CapData` creates resolution authority, sending the
Promise in `.result` gives it away, getting a Promise in `.result` acquires it, and using the Promise in
`resolve()` consumes it"; while the message sits on the run-queue the decider is *cleared*, so authority lives in the
queued message. A send to an unresolved promise is queued *in the kernel promise table* unless the decider vat opted
into pipelining — and only the comms vat does ("In SwingSet, pipelining is most (only?) useful on the Comms
Vat"). Sends to a promise fulfilled to data reject with `CannotSendToData`; to a rejected promise, with the
rejection. Three-party handoff is "deferred … our main use case doesn't strictly need it".

**What broke / was redesigned.** The resolver-vs-promise type confusion was debated and left implicit ("I'm inclined
to stick to `Object` and `Promise`", open questions). Promise *redirection* (forwarding without settling) is still a
design note. The deep break is upgrade: a vat's promises are rejected at upgrade (§1.11), which drove the whole vow
redesign (§1.12).

**Mini.** *Adopt:* linear resolution authority as a **kernel rule**: an answer slot has exactly one decider; the
decider role moves only with the message; resolving consumes it. This is exactly SCHOLAR-BREAD's "await id spent like
a nullifier" and SCHOLAR-CALLS idea 2; Agoric is the production precedent that it is implementable and sufficient.
*Adopt:* queue-at-the-slot pipelining as the default; early delivery to the decider only across domains (SCHOLAR-CALLS
Part II.2 resolves this correctly). *Better:* in Mini the decider is a cell, not a vat process, so a promise can
survive the decider's *upgrade* (Agoric's cannot); make "upgrade of the decider" a typed disposition, not a
rejection (§1.11).

## 1.3 Transcripts, heap snapshots and engine upgrades

**How it works [me, READ `agoric-swingset-transcript-2025.md`, `persistence.md` (via SCHOLAR-OS, spot-checked),
`agoric-xsnap-readme-2026.md`, issue #8955].** Orthogonal persistence by replay: every delivery and every syscall
result is logged; a worker restarts from the last XS heap snapshot and replays the current span, and the kernel
checks that the replay emits the same syscalls. Snapshots are engine-specific binary images.

**What broke.** **Engine upgrades.** Moving to a new `xsnap` invalidates every heap snapshot and transcript, so the
"chain-halting upgrade invokes the swingset/controller API that says 'I want to restart all vats'"; and a restart
that fails *cannot roll back* ("that old heap snapshot and transcript are unusable without the old xsnap"); "this
restart-all-vats plan might be practical for now, when we have 87 vats on chain, but not when we have a thousand".
The proposed fix is a new lifecycle state, **suspended vats** (no worker, no snapshot, no transcript), revived
in-consensus on demand (issue #8955, open since Feb 2024, READ).

**Mini.** *Better by construction, and say so loudly:* Mini's checkpoint is a **specified codec of the Core4
machine**, not an engine image, so an evaluator change (C machine ↔ `@[csimp]` fast machine) does not invalidate
suspended activities provided both refine the Lean semantics. *Adapt:* the codec itself becomes the thing whose
version must be governed (SCHOLAR-OS §4 "the codec is a versioned wire format" is right); a codec change needs a
checked `decode_old → encode_new` *or* a typed `Upgraded` disposition per activity — never "restart everything".
*Adopt the idea of suspension* for objects with no funding or no traffic (SCHOLAR-OS's hibernation): it is the same
state machine Agoric is now designing, and Mini can make revival a pure function of the root.

## 1.4 Metering, run policy, and why Agoric could not meter its own kernel work

**How it works [me, READ `agoric-swingset-metering-2025.md`, `run-policy-2025.md`, `liveslots-2025.md` §GC vs
Metering].** "Computrons" are counted by the XS engine; a per-crank limit (100 M) and an optional refillable
`Meter`; "any vat which exceeds its limit is terminated, and any messages it sent before the limit was reached are
cancelled"; the host run policy ends a block by cumulative computrons (≈65 M per 5 s by their measurement).

**What broke.** (1) **Kernel work is unmetered on purpose.** Because XS GC timing can differ after a snapshot reload,
"we run most of the 'inbound' side of liveslots without metering", including argument deserialisation and the whole
post-crank GC phase — otherwise metering would diverge between validators and cause a consensus failure. (2)
**Terminate-on-exhaustion is catastrophic** for a contract: the vat and its state are gone; the metering doc keeps
the rule, but production contracts run with unlimited meters plus the per-crank cap (INFERRED from the docs'
`createUnlimitedMeter` guidance). (3) Computrons are engine-defined, so an engine upgrade is a consensus event.

**Mini.** *Better by construction:* Mini's GC is at yield, inside the Lean semantics, deterministic; so the
SCHOLAR-OS demand to "meter kernel work" (decode, GC, law checks, Merkle updates) is *achievable in Mini where Agoric
proved it is not achievable in a JS engine*. Treat that as a requirement with a theorem ("metering is a function of
the pre-state and the invocation"), not an aspiration. *Adapt:* exhaustion must **abort the turn and park the
activity** (refundable, resumable with more budget), never terminate the object — Agoric's own `delivery.md` already
anticipates "interrupted by an out-of-gas error (in which case it could be replayed or restarted after a Keeper
supplies more funds)", but the shipped rule is termination. *Adopt:* the two-level meter (per-turn cap + refillable
meter object with a threshold notifier) — already in SCHOLAR-OS §6.

## 1.5 Garbage collection: reachable vs recognizable, refcounts, and the cycles nobody can collect

**How it works [me, READ `agoric-swingset-garbage-collection-2025.md` §Reachability–§Post-Decref].** User code gets
no `WeakRef`/`FinalizationRegistry` (determinism); liveslots forces `gc()` after each delivery and emits
`dropImports` / `retireImports` / `retireExports`. The kernel keeps two refcounts per object, **reachable** and
**recognizable** (a `WeakMap` key can *recognise* an object it cannot *reach*), and processes zero-crossings only at
end of crank (`maybeFreeKrefs`), because delivery is "break-before-make".

**What broke.** (1) **Cross-vat cycles are never collected**: a Zoe↔price-feed cycle (Zoe holds an `ExitObject`
presence; the contract vat holds the `SeatHandle` presence; each held by durable state on its own side) had **~50k
instances, 37 kv entries each, ≈310 MB**, growing ~3 MB/day; "performing distributed GC among mutually-suspicious
parties is … a 'purple box'" (issue #8401, READ). (2) **A safety feature became the biggest leak**: ERTP's *recovery
set* (every withdrawn payment kept strongly by its purse so lost payments can be swept back) held old price-quote
payments that subscribers never deposited — "about 60% of our kvstore entries", +10 rows per quote (issue #8400,
READ); the same objects then pinned RAM in `v7-board` (#10743). (3) **Termination of a large vat is O(N²) kernel
work** that "would probably crash the chain", so `terminateVat` was split into mark-now / clean-up-slowly under a
per-block budget ("terminate vats slowly", #8928; run-policy §Terminated-Vat Cleanup); and the old bloated vats
still could not be terminated *in-band* because the authority (`adminNode`) was held by Zoe and not reachable by
governance, so the plan uses a host-level `controller.terminateVat()` "superpower" outside the kernel (#9483,
open since Jun 2024, READ).

**Mini.** *Better by construction (INFERRED, but strong):* within one domain all references between objects are
kernel-held capabilities in one Merkle store, so **cross-object cycles are collectable by an ordinary deterministic
tracing pass** over the cap graph — the "purple box" exists only *across* trust domains, which Mini keeps narrow.
*Adopt as a design rule:* **every retention structure has a payer** (recovery sets, watcher tables, inboxes,
pending-await indexes): Agoric's leak came from a retention structure nobody paid for and nobody owned. *Adopt:*
O(1) termination — make an object's state a Merkle *subtree*, so terminating detaches one root and reclamation runs
off the consensus path; and give every object, at creation, an *in-band* termination authority (law-governed), so no
host superpower is ever needed (Agoric's #9483 is the counterexample).

## 1.6 Virtual and durable objects, kinds, zones, baggage

**How it works [me, READ `agoric-swingset-virtual-objects-2025.md`, `agoric-vat-data-2025.md`,
`agoric-doc-zoe-contract-details-2026.md`, `agoric-zone-readme-2026.md`].** Three storage tiers: heap (RAM, lost at
upgrade), virtual (paged to the vatstore DB, lost at upgrade), durable (paged, survives upgrade). A **kind** is
`(tag/kindHandle, init, behavior | facets, {finish, stateShape})`; each instance's state is a record fixed by
`init`: "State properties cannot thereafter be added or removed"; values are hardened and serialised on assignment
("you cannot do `state.zot.push`"). The **zone** API makes library code storage-agnostic. All durable state must be
reachable from one durable map, the **baggage**.

**What broke / was redesigned.** (1) The three-tier split forced every long-lived contract to be *rewritten* for
durability (`define*`→`prepare*`, `Far`→exo, promises→vows). (2) **State shape is frozen across upgrades**: "These
cannot currently be changed on upgrade, though we're considering relaxing that restriction"
(`contract-details`, READ) — Agoric has *no typed state migration for durable objects*; v2 must keep v1's fields and
put new state in side stores. (3) "When a vat is restarted, all previous Kinds must be defined in the first crank" —
the reason given is that a suspended half-started vat "would expose other vats to side effects, so the
restart/upgrade could never be fully unwound if it fails".

**Mini.** *Better by construction:* Mini has no heap/virtual/durable split; the object's state *is* its cells. Keep
it that way and **do not import the zone taxonomy**. *Adopt:* `stateShape` — a declared, checked predicate on every
state write — which is exactly a Mini law (§1.8). *Better:* typed migration of object state at upgrade (SCHOLAR-OS §8,
SCHOLAR-CALLS idea 8) is precisely what Agoric lacks; it is a real advance, not a reinvention. *Adopt:* the
"first-crank" rule in Mini form: an upgrade is one atomic turn that must rebind every exported obligation or be
refused — which Mini gets for free because the turn either commits or does not.

## 1.7 Hardened JavaScript: lockdown, harden, Compartments

**How it works [me, READ `endo-ses-readme-2026.md` §Lockdown, §Compartment, §Security claims and caveats, §TCB;
`agoric-doc-js-programming-hardened-js-2026.md`].** `lockdown()` freezes all undeniable intrinsics; `harden`
deep-freezes; a **Compartment** gives a guest its own `globalThis` and module graph with *no* I/O and no clock unless
endowed. The stated claims: a guest "cannot initially perform any I/O" and "cannot measure the passage of time"; but
it "can execute for an indefinite amount of time, allocate arbitrary amounts of memory", and "the ses shim does not
in itself isolate the stack of guest programs", so synchronous interaction risks "a reentrancy attack"; "A host object
can defend itself from reentrancy attacks by ensuring that it interacts with guest objects on a clean stack through
the use of promises." TCB includes the JS engine and "any JavaScript that has executed in the same realm before …
`lockdown`".

**What broke.** No public break of SES isolation that I found; the cost is the TCB (an ES-2021-conformant engine plus
the shim) and ecosystem compatibility (frozen primordials break npm packages; dynamic `import` banned in vats).

**Mini.** Core4 has no ambient authority at all (no clock, no I/O; "Time is an admitted input", SCHOLAR-OS §7), so
Mini *starts* where lockdown ends, with a **proved** semantics instead of a shim over an engine. The transferable
lesson is the caveat: **synchronous cross-principal interaction is where re-entrancy lives, and Agoric's answer was
"never synchronous across trust boundaries"**. Mini is choosing to allow synchronous in-turn calls across principals
(Ember's "very rich" calls); Agoric's evidence says that choice must come with the kernel guard SCHOLAR-CALLS idea 1
proposes (refuse re-entry into an object already on the stack) — not as an option.

## 1.8 Exos, interface guards, patterns and pass-styles — Agoric's "laws at the call boundary"

**How it works [me, READ `endo-exo-readme-2026.md`, `endo-patterns-readme-2026.md`, `endo-pass-style-readme-2026.md`,
`contract-details` §Guards].** An **exo** is a remotable object plus an `InterfaceGuard`:
`M.interface('name', { m: M.call(argShapes).returns(retShape), n: M.callWhen(M.await(s)).returns(r) })`. "If a caller
provides a parameter that doesn't match the template specified in the guard, SwingSet returns an exception to the
caller without notifying the receiver. If the return value doesn't match, the function returns an exception to the
caller." Patterns are a small decidable language over passable data: `M.nat()`, `M.gte(5)`, `M.lte(100)`,
`M.and/or/not`, `M.splitRecord(required, optional, rest)`, `M.arrayOf`, size bounds, `M.remotable()`, etc.;
`stateShape` applies a pattern to an exo's state on write; `zcf.makeInvitation(handler, desc, details,
proposalShape)` applies one to proposals. **Pass-styles** fix what may cross a boundary (copyRecord, copyArray,
tagged, remotable, promise, error, primitives); "passStyleOf({ x: 1 }) // Error: not frozen".

**What broke / was redesigned.** `Far` objects (no validation) were superseded by exos; validation moved from
hand-written checks in method bodies to declared guards at the boundary. (`offerArgs` still carry a docs warning:
"These values need input validation before being used".)

**Mini.** This is the most under-appreciated Agoric lesson for fork 2, and none of the four siblings names it.
**Agoric converged on decidable predicates at three points: method arguments/returns, object state writes, and
offer proposals.** Mini's `Pred` is the same idea with a satisfiability checker and refusal explanations. *Adapt:*
give every package method a **guard** in the law language — preconditions over arguments *and the request*
(SCHOLAR-LAWS idea 1's request atoms) and a postcondition over the returned value — checked by the kernel *before*
the method runs (args) and before the Plan applies (returns). A guard failure is a refusal with an explanation that
costs no Core4 execution. *Adopt:* pass-styles as Mini's "exchangeable payloads" (SCHOLAR-OS §2: forced data,
capabilities, linear assets, never thunks) — Agoric's table is the worked example. *Better:* Mini can *decide*
guard satisfiability and implication at publish time (dead methods, upgrade compatibility "new guard accepts
everything old accepted" = `old ∧ ¬new` unsat), which Agoric only checks at runtime.

## 1.9 ERTP: issuers, mints, brands, purses, payments — and the rights taxonomy beneath them

**How it works [me, READ `agoric-doc-ertp-{index,amounts,issuers-and-mints,purses-and-payments}-2026.md`;
`miller-capability-financial-instruments-2000.txt` §3.3–3.4, §6.1–6.4].** One-to-one-to-one **mint / issuer /
brand**; the issuer is "the source of truth of how many digital assets each purse and payment holds"; an **amount**
(`{brand, value}`) is a *description*, never an asset; `AssetKind.NAT` (fungible bigint) and `SET` (non-fungible
records); a **payment** is consumed whole on deposit; a **deposit facet** lets anyone deposit and no one withdraw;
`brand.isMyIssuer` because "the issuer is authoritative and the brand is not". The 2000 paper gives the taxonomy that
explains the whole design: rights are *shareable vs exclusive, specific vs fungible, opaque vs assayable, exercisable
vs symbolic*, and "exclusive rights can only be reliably assayed by actually obtaining exclusive access to them …
Trade of exclusives may therefore require a trusted third party who can hold them in escrow." Its 30-line mint
proves six properties, the first being "Only someone with the mint of a given currency can violate conservation".

**What broke / was redesigned.** `split`, `combine`, `claim` and `withdraw` are now marked **DEPRECATED** in the
guides (READ; the docs do not give the reason — INFERRED: payments-in-flight as first-class objects proved costly to
track, cf. recovery sets). Recovery sets (§1.5) leaked 60% of chain storage. Zoe "does not verify that the assets were
made using the latest ERTP implementation" and its liveness is conditional on issuers behaving (§1.10).

**Mini.** *Already better by construction (READ in Mini):* the kernel **Book** *is* ERTP-in-the-kernel — asset id =
issuer-well account (brand ≡ issuer identity), `mint` debits the well (only the well's authority can create supply,
exactly property 1), `transfer` is one conserved posting, `Book.applyPosting_conserves` is the conservation theorem
ERTP only asserts. *Adopt:* the vocabulary and the taxonomy. Mini should expose **deposit-facet capabilities**
(credit-only authority on an account) and **amounts as descriptions** (an offer names amounts, never moves them).
*Adopt the escrow argument but notice where Mini escapes it:* assaying-then-transferring an exclusive needs escrow
only because the two steps are separated in time. **Inside one Mini turn, assay and transfer are atomic, so
single-domain trades need no escrow at all**; escrow is needed only across a yield or across domains. *Do not adopt*
user-coded issuers: keep every asset Book-native, so conservation and payout liveness are kernel theorems, not
assumptions about third-party code.

## 1.10 Zoe: invitations, proposals, seats, reallocation, offer safety, payout liveness

**How it works [me, READ `agoric-doc-zoe-{index,proposal,offer-enforcement,contract-requirements,contract-details}`,
`agoric-zoe-zcf-doc-2026.md`, and the source `agoric-src-{offerSafety,rightsConservation,zcfSeat,zoeSeat,
evalContractCode}-2026.js`].**
- A party calls `E(zoe).offer(invitation, proposal, payments, offerArgs)`. An **invitation** is an ERTP payment of
  Zoe's invitation issuer, describing instance, installation, handler description and custom terms; Zoe *burns* it
  on use, so the right to play is exclusive and assayable (Miller 2013's contract-host token, made an ERTP asset).
- The **proposal** is `{give, want, exit}` with contract-defined keywords; `exit` is `onDemand` (default),
  `waived`, or `afterDeadline {timer, deadline}`.
- Zoe escrows the payments in its own purses; the contract sees only **allocations** on **seats**.
- The contract changes allocations only through `zcf.atomicRearrange(transfers)`, which checks, in order: all
  seats live; **rights conserved** per brand over the touched seats (`assertRightsConserved`); **offer safety** for
  every touched seat; then a single commit point. Offer safety is exactly:
  `isOfferSafe(p, a) = (∀k∈p.give. a[k] ≥ p.give[k]) ∨ (∀k∈p.want. a[k] ≥ p.want[k])` (READ, `offerSafety.js`).
  Because the initial allocation equals `give`, "allocations are always in an offer safe state for every offer" —
  an **invariant checked on every write**, not a property checked at exit.
- **Payout liveness:** "once the exit of an offer is triggered, Zoe ensures that the payout … will be made promptly,
  no matter what the contract code does".

**What the docs and code admit (READ — the corrections the siblings miss).**
1. **The check runs inside the contract's own vat.** "ZCF in the contract vat enforces offer safety and rights
   conservation on every reallocation", and the Zoe service accepts the result unchecked: `replaceAllocation`
   just does `state.currentAllocation = replacementAllocation` ("Merging happens in ZCF"). The contract is
   separated from ZCF only by a SES Compartment (`importBundle(bundle, {endowments})`). Agoric's own hindsight: "this
   file probably should have been part of a larger division that also included checks of offer safety and rights
   conservation during reallocations, as Zoe 2.0 does in the Escrow Service" (`zoe-zcf.md`), and a 2023 spike
   "toward correct-by-construction Zoe2 escrow" cites the 2000 and 2013 papers and Necessity specs (#8184).
2. **Payout liveness is conditional on issuers.** "The full payout liveness guaranteed by Zoe is conditional on
   well-behaved issuers"; a hanging deposit leaves funds "no longer accessible to the user" (tracked as #1271).
3. **Minting bypasses conservation:** `zcfMintReallocator.reallocate` "does not check conservation".
4. **One vat holds every escrow on the chain**: "all of the assets that Zoe escrows … are escrowed in the single Zoe
   Service vat".
5. **Offer safety ends at the Zoe boundary.** Orchestration flows move assets out of the seat into chain accounts
   (`zoeTools.localTransfer`) and on failure the *contract author* writes the compensation
   ("withdrawToSeat(...); seat.exit(errorMsg)", `send-anywhere` walkthrough, READ).

**Mini.** This is the strongest single mapping in this report, and it is concrete:
- **A seat is a Book account plus a law.** The offer-safety predicate is, for fungible (`NAT`) amounts, an `anyL` of
  two `allL`s of lower-bound atoms — **already inside Mini's `Pred` fragment**. READ in `Pred/Core.lean:161–194`:
  `le slot v` means `new[slot] ≤ v`, and `not`, `allL`, `anyL` exist, so `amount_k ≥ c` is `not (le slot_k (c−1))`
  over integer slots. One care point: `le` on a *missing* slot is `false`, so its negation is `true`; Agoric treats
  a missing keyword as *unsatisfied* (`offerSafety.js`), so the seat's slots must be total (initialised to 0). So "offer safety" in Mini is not a framework: it is a law on the seat account,
  judged on every write by the kernel, *outside* any contract code. Non-fungible `SET` amounts need set-inclusion
  atoms (`memberOf` over a finite set covers the bounded case — INFERRED, to be checked against `Pred`).
- **Conservation is not a law atom** (a sum over n slots is not difference logic) — it is the Book's posting
  invariant, already a theorem. Offer safety (a law) and conservation (the Book) are two separate kernel
  obligations, exactly Zoe's two checks, but both run in the kernel.
- **Payout liveness becomes a kernel theorem for Book assets:** `exit` is a kernel action on the seat whose
  admissibility for the offerer is a law clause the contract cannot override; `afterDeadline` is a height-indexed
  clause (`valid_until` is already a height); `waived` drops the clause. No issuer can hang it because no issuer is
  user code.
- **Invitation = an exclusive, assayable capability** naming (package hash, instance cell, role, terms); redeeming it
  is a nullifier-style spend in the same turn as escrow. The 2013 contract host is literally Mini's kernel.
- **Better by construction:** Zoe 2.0's "correct-by-construction escrow service" is what Mini has on day one: the
  enforcing code is the Lean kernel, the checks are decidable laws plus a proved posting algebra, and the contract
  only *proposes* the reallocation (a Plan). *Must extend:* offer safety must also govern **assets that leave the
  seat across a yield or a domain** (Agoric's orchestration gap): an escrow across a yield is a seat that stays open
  with its law; a cross-domain leg is the SCHOLAR-CALLS deal cell with offer safety as its decision rule.

## 1.11 Dynamic vats and vat upgrade

**How it works [me, READ `agoric-swingset-vat-upgrade-2025.md`, `dynamic-vats-2025.md`, `contract-upgrade-doc`].**
`createVat(bundlecap, {meter, vatParameters, critical, …})` via the non-ambient vatAdminService; upgrade is
`E(adminNode).upgrade(bundlecap, {vatParameters})`: shut down worker, reject outstanding promises, abandon
non-durable exports, delete snapshot and transcript, start v2, run `buildRootObject(vatPowers, vatParameters,
baggage)` as one **upgrade-phase crank** which must redefine every durable kind "with the same facets and methods or
a superset thereof"; on any failure v1 is reinstated. "Upgrade is Semi-Traumatic … preserve long-term state, but
abandon any work that was in-progress." "Promises Are Broken". "The ability to upgrade a vat is also the ability to
control it." For contracts, `adminFacet.upgradeContract(bundleId)`; on mainnet the adminFacet "is stored in the
bootstrap vat, allowing the BLD stakers to upgrade such a contract in a later swingset.CoreEval" (READ).

**What broke.** (1) **The rollback path itself halted the chain.** Oct 2025: an upgrade's `startVat` failed
("defineDurableKind not called for tags: [asyncFlow]"); the kernel's refcount processing "was not prepared for
kpids absent from the database because of rollback, leading to a kernel panic" → `CONSENSUS FAILURE!!!` (issue
#12138, READ). (2) Engine upgrades force restart-all-vats without rollback (§1.3). (3) In-flight work is lost, which
created vows, retry-send and asyncFlow (§1.12).

**Mini.** *Adopt:* (a) the superset-of-obligations rule as a kernel check; (b) upgrade authority as a capability
whose holder is effectively the author, *made legible on the card* (SCHOLAR-OS §8). *Better by construction:* in
Mini an upgrade is one admitted turn; refusal is "the turn did not commit", so there is no rollback code path to get
wrong — Agoric's #12138 is a bug class Mini does not have, *provided* the upgrade, the migration and every activity
disposition are decided inside that one turn. *Correct the default:* Agoric's "abandon in-flight work" was forced by
engine-opaque heaps, not chosen on merit; Mini can type its continuations, so "abort everything in flight" should
be one disposition among four, not the platform rule.

## 1.12 Vows, retry-send and asyncFlow: rebuilding durable async after the fact

**How it works [me, READ `agoric-vow-2025.md`, `agoric-async-flow-2025.md`, `agoric-async-flow-states-2025.md`,
issues #9608, #12315].**
- **Vows** are durable promise-like objects: "Native promises are not compatible with Agoric's durable stores …
  such promises disconnect their clients when their creator vat is upgraded." `watch` survives upgrade of both ends;
  `when` "cannot survive the upgrade of the calling vat"; internally `shorten()` steps the chain and *retries on
  disconnection*.
- **Retry-send** (#9608): resend a message while its result is rejected with `UpgradeDisconnection`; "Assumes
  idempotence … we cannot automagically turn unmarked eventual-sends into retry-send … APIs intended to be reliably
  usable across upgrade of either side should often be designed to be idempotent."
- **asyncFlow**: a *closed* async function whose interactions with the host are logged through a membrane; at
  upgrade the activation is **Sleeping**, then **Replaying** the new code against the log ("must exactly produce its
  previously logged behavior"), then **Running**; on divergence **Failed** "so it can be repaired by another future
  upgrade"; **Done** drops the log.

**What broke.** Jan 2026 (#12315, open, READ): "if a flow fails replay, it is marked as panicked in the hope that
future upgrade can handle the situation. This can often be wishful thinking because the incompatible flow can now
have new activations, resulting in replay logs of both incompatible behaviors. A contract should be able to chose
failing its upgrade if flows fail to replay." The asyncFlow durable kind also appears in the #12138 chain halt.

**Mini.** This is the decisive production evidence for fork 4, and it settles the SCHOLAR-OS vs SCHOLAR-CALLS
disagreement (Part 3, item 6): after three layers of machinery (vows, retry-send, asyncFlow) Agoric arrived at *long-lived
continuations reconstructed by replay*, and its open problem is that replay compatibility is discovered *after* the
upgrade commits. *Adopt:* the activation state machine. *Better by construction:* Mini's activity log is exactly
the typed `(Plan_i, Response_i)` sequence (SCHOLAR-OS §4.3), so the replay check is decidable *inside the upgrade
turn* — make "every live activity gets an explicit disposition, and a Replay disposition is admitted only if replay
succeeds now" a precondition of the upgrade turn. That is #12315's proposed fix, made mandatory and atomic. *Better
by construction:* Mini's eventual sends can carry deterministic ids (`H(turn, call-site)`, SCHOLAR-CALLS idea 2) and
the kernel can dedupe, so retries are exactly-once without asking application authors for idempotence.

## 1.13 Orchestration: cross-chain programs as capabilities

**How it works [me, READ `agoric-doc-orchestration-{how-orch-works,key-concepts,txvsportfolio,
contract-walkthroughs-send-anywhere}-2026.md`, `agoric-orchestration-readme-2026.md`].** Chains and remote accounts
are reified as objects: `orch.getChain('osmosis')`, `chain.makeAccount()` (an IBC Interchain Account the Agoric chain
controls); "Whoever has access to the JavaScript object can control the account"; ICQ for cross-chain reads; flows
are asyncFlow guests so they survive upgrade. Contracts are "transactional" (one-shot) or "portfolio" (long-lived
per-user state).

**What broke / limits.** There is no cross-chain atomicity: failure handling is author-written compensation
(withdraw back to the seat, exit with error). Offer safety does not extend past the seat (§1.10.5).

**Mini.** *Adopt:* **remote domains as capabilities**: a remote account is a cap whose methods are sends with
typed, height-bounded replies (IBC timeouts), and light-client verification is how a remote reply becomes an
admitted input. *Better:* Mini can carry offer safety across the boundary by making the cross-domain leg a deal cell
whose law is offer safety (SCHOLAR-CALLS idea 7), rather than leaving compensation to authors.

## 1.14 Governance: electorates, vote counters, ContractGovernor, legibility, CoreEval

**How it works [me, READ `agoric-governance-readme-2026.md`, `agoric-doc-governance-index-2026.md` (skimmed)].**
Electorates (committees, stakeholders) and VoteCounters are separate contracts; a QuestionSpec `{method, issue,
positions, electionType, maxChoices}` with a closing rule; a governed contract holds its mutable parameters in a
**ParamManager** whose setting facet only the **ContractGovernor** holds; governance can change declared
parameters, invoke declared methods, and **filter offers** (block invitations). The design goal is **legibility**:
"observers (clients and voters) are able to see who has control, and what actions can be taken". In production,
contract upgrade authority sits at the chain root (BLD-staker `CoreEval`, which evaluates privileged scripts).

**What broke.** The authority to terminate the bloated price-feed vats was not reachable by in-band governance, so
the fix needs a host-level call (§1.5, #9483). INFERRED: `CoreEval` is effectively root, so per-contract governance
is a convention layered on a superuser.

**Mini.** *Adopt:* legibility as a card requirement: the projection of every object shows its governed parameters,
its upgrade policy, who holds each governing capability, and the vote-counting package (SCHOLAR-BREAD's "display ≤
evidence" rule extends naturally). *Adopt:* governed parameters as cells whose law names the governor; offer
filters as a law clause on invitation redemption. *Better:* no `CoreEval`-style superuser: every privileged act
(terminate, upgrade, re-key) is a law-governed capability created with the object, so nothing ever needs a host
superpower.

## 1.15 Mapping table

| Agoric mechanism | Mini equivalent | Verdict | Concrete build in Mini |
|---|---|---|---|
| crank buffer + block commit + outbound embargo | atomic turn; block = admitted batch; embargo off-domain effects | **adopt** | name the block tier; outbox ids `H(turn, i)` |
| c-lists (vref↔kref) | kernel-held caps in cells | **adopt** (Mini already) | laws judge krefs, never object-chosen names |
| kernel promise with one decider; linear resolution authority | answer slot = nullifier-spent await id | **adopt** | one kernel module; decider moves only with the message |
| queue-at-promise pipelining; comms-only early delivery | queue at slot, forward in resolving turn; early delivery cross-domain only | **adopt** | as SCHOLAR-CALLS idea 2 |
| transcript + XS heap snapshot | specified Core4 checkpoint codec | **better** | version the codec; checked `decode_old→encode_new` |
| restart-all-vats on engine change; suspended vats | evaluator swap is invisible if it refines Lean; hibernation from the root | **better / adopt state** | refinement theorem for each executor |
| computrons (engine-defined), unmetered liveslots + GC | Core4 steps + priced kernel work, deterministic GC | **better** | metering-is-a-function theorem |
| terminate vat on meter exhaustion | abort turn, park activity, refundable | **adapt** | `AwaitsFunding` disposition |
| reachable/recognizable refcounts; uncollectable cross-vat cycles | tracing GC over the in-domain cap graph | **better** | deterministic, metered collector pass |
| recovery sets (leaked 60% of storage) | every retention structure has a payer | **adapt (rule)** | storage deposits on watchers, inboxes, awaits |
| slow vat termination under run policy | O(1) detach of an object subtree | **better** | object = Merkle subtree |
| heap / virtual / durable zones + baggage | cells only | **do not import** | — |
| kind state frozen across upgrade | typed linear migration | **better** | migration checker in the upgrade turn |
| SES lockdown + Compartments | Core4 with no ambient authority, proved semantics | **better** | — |
| "clean stack via promises" against re-entrancy | kernel re-entry guard on in-turn calls | **adopt the lesson** | mandatory, not opt-in |
| exo InterfaceGuard / patterns / stateShape / proposalShape | method guards + laws in `Pred` | **adopt + better** | guard field on every package method; publish-time sat/implication |
| pass-styles | exchangeable payload types | **adopt** | forced data, caps, Book amounts; never thunks |
| ERTP mint/issuer/brand/purse/payment | kernel Book (issuer wells, postings) | **better (exists)** | deposit-facet caps; amounts as descriptions |
| invitation = burnable ERTP payment | exclusive cap (package, instance, role, terms), spent like a nullifier | **adopt** | invitation kind in the kernel |
| Zoe seat + atomicRearrange + offer safety + conservation | seat = Book account + offer-safety law; Book conservation | **better** | offer-safety law template; `exit` kernel action |
| payout liveness (issuer-conditional) | kernel theorem for Book assets | **better** | liveness lemma over `exit` |
| vows + retry-send (idempotence required) | deterministic message ids, kernel dedupe | **better** | exactly-once sends |
| asyncFlow (replay; Failed discovered late) | typed `(Plan,Response)` log; replay checked inside the upgrade turn | **adopt + better** | disposition precondition on upgrade |
| orchestration (chains as objects; author compensation) | remote domains as caps; deal cell with offer-safety law | **adopt + better** | light-client inputs; deal-cell law |
| ContractGovernor / ParamManager / legibility / offer filters | governed-parameter cells; card shows control | **adopt** | legibility fields in the projection |
| CoreEval superuser; host `terminateVat` | none: every privileged act is an in-band law-governed cap | **better** | termination + upgrade caps minted at creation |

## 1.16 What Agoric got right that Mini could still lose

1. **Interfaces are guarded at the boundary, always.** If Mini lets method bodies validate their own inputs, it will
   repeat the pre-exo era. Make guards part of the package's checked core.
2. **Rights are objects you can hold, attenuate and pass** (deposit facets, invitations, creator vs public facets).
   A cell-and-law design can drift into "permissions are fields in a table"; keep facets as distinct capabilities
   over shared state (exoClassKit is the model: several facets, one state record).
3. **Legibility is a security property.** Voters and users can see *who can change what*. Mini's projection should
   make this a required field, not a nice-to-have.
4. **The caller's terms travel with the call** (offers). This is SCHOLAR-LAWS idea 2; Agoric is the proof it works
   for real users and real contracts (AMM, vaults, auctions, PSM on mainnet).
5. **Semi-traumatic honesty.** Agoric documents exactly what an upgrade breaks. Whatever dispositions Mini chooses,
   each live activity's fate must be visible to whoever awaits it (`Upgraded` reaches the awaiting party).


---

# Part 2 — The frontier, 2022–2026: annotated bibliography

Organised by the question each cluster answers for Mini. Readers: `[me]`, `[lane A]`, `[lane B]`. Lane A used 11
Kagi queries (arXiv API rate-limited it; PDFs were fetched directly), lane B used 4. I spot-checked the verbatim
quote behind every lane entry that Part 3 relies on (all found in the saved `.txt`; Lean4Lean's quote is split by
two-column extraction but present). Entries the lanes could not obtain are marked INFERRED.

## 2.A Effects, continuations and what may cross a yield (forks 1, 3, 5)

**A1. Ahman, Pretnar. "Asynchronous Effects." POPL 2021 (PACMPL 5:24), arXiv:2003.02110.** —
`ahman-asynchronous-effects-2021.pdf`. READ (§1–2.5) [lane A; quote spot-checked].
- **New.** An operation splits into a non-blocking outgoing *signal* `↑op`, an incoming *interrupt* `↓op`, and a
  *promise handler* installed for it; the continuation keeps running and blocks only at `await p`. They "surrender
  … access to the continuation that captures the rest of the computation" in exchange for "a natural and robust
  formalism for asynchronous programming". Type safety mechanised in Agda.
- **Mini.** The cleanest formal reading of a resident: between turns its state is a term with interrupt handlers
  installed, not a captured stack; B's reply to A is an interrupt whose delivery is A's next paid turn, and **no
  continuation ever crosses an object boundary**. Worth checking that `Activity<P,R,A>` reads as "signals of type P,
  interrupts of type R". Caveat (lane): λæ broadcasts interrupts; Mini needs capabilities on the interrupt channel
  (the answer-slot decider of §1.2 is exactly that).

**A2. Ahman, Sobolev. "Strong Normalisation for Asynchronous Effects." arXiv:2602.05528, 2026.** —
`sn-asynchronous-effects-2026.pdf`. SKIMMED [lane A]. Without general recursion λæ is strongly normalising even with
reinstallable interrupt handlers. **Mini:** a possible *total residents* tier (no `fix` inside a turn): "lives
forever, every reaction terminates" by typing. Low priority; SN gives no step bound, so metering stays.

**A3. Phipps-Costin, Rossberg, Guha, Leijen, Hillerström, Sivaramakrishnan, Pretnar, Lindley. "Continuing
WebAssembly with Effect Handlers" (WasmFX). OOPSLA 2023, arXiv:2308.08347.** — `phippscostin-wasmfx-2023.pdf`. READ
(§1–3, 5–6) [lane A; quote spot-checked]. `cont.new / suspend / resume`; "we only support single-shot continuations";
>3× slower than native in the prototype, much smaller than Asyncify; now Wasm stack switching. **Sivaramakrishnan et
al., "Retrofitting Effect Handlers onto OCaml", PLDI 2021** (SKIMMED [lane A]): one-shot fibers, ~1% overhead.
**Mini:** both production effect systems chose one-shot, **non-serialisable** stack continuations. Mini's exact
checkpoint codec is the unusual choice; its nearest precedent is Unison, not the effects literature, so Mini must
own codec adequacy itself. One-shot is enforced in Mini *by the store* (resume compare-and-swaps the checkpoint
hash), not by linear types. Do not adopt Wasm stack switching as a resident substrate: it cannot be checkpointed.

**A4. Legoupil, Pederson, Birkedal, Lindley, Pichon-Pharabod. "Iris-WasmFX: Modular Reasoning for Wasm Stack
Switching." Draft, Nov 2025.** — `iris-wasmfx-stack-switching-2025.pdf`. SKIMMED [lane A]. Mechanising WasmFX had to
type the *administrative* (runtime-only) forms, where the spec gaps sat. **Mini (a concrete check):** preservation
must cover *decoded machine states*, not only source terms; if Core4 lacks a typing judgment for mid-execution
states, "decode then resume" is outside the adequacy proof.

**A5. Ma, Ge, Lee, Zhang. "Lexical Effect Handlers, Directly" (Lexa). OOPSLA 2024.** —
`ma-lexa-lexical-handlers-directly-2024.pdf`. READ (§1–2, theorems, evaluation) [lane A; quote spot-checked].
Handlers as capabilities compiled to direct stack switching; dynamic handler search makes a scheduler benchmark
"𝑂(𝑛²)" in Effekt/Koka/OCaml, Lexa linear. **Mini (conditional, INFERRED):** if Core4 ever lets user code install
handlers that `perform` *searches*, a step meter that counts `perform` as one step under-counts by the handler depth
(a DoS). If, as the brief describes, `perform` always yields to the kernel, the concern reduces to charging the
yield (codec + checkpoint) by size. Either way: define metering as a **Lean cost semantics** with "meter ≥ machine
transitions" as a theorem.

**A6. Unison: "Visualizing remote computations" (2023) and Labella, "Volturno" (Nov 2025); Unison Cloud concepts.** —
`unison-visualizing-remote-2025.txt`, `unison-volturno-design-2025.txt`, `unison-cloud-core-concepts-2025.txt`. READ
(practitioner sources) [lanes A, B]. Distribution is an ability; content-addressed code ships by hash; one program
interpreted by a *blueprint* handler and a *run* handler; "typed persistence". **Mini:** run the *same* method under
a dry-run/plan handler (quote, preview, law pre-check, card affordance "would this be admitted now?") and under
admission — previews for free. Content-addressed code makes "activities pinned to old code" well defined, so
pinning is a real disposition (sides with SCHOLAR-CALLS Part II.4).

**A7. Koka line: Perceus (PLDI 2021), generalized evidence passing (ICFP 2021), first-class handler names (OOPSLA
2022).** INFERRED [lane A] (reports not retrieved). Evidence passing indexes rather than searches; Perceus is the RC
scheme Lean 4's runtime shares. **Mini:** deterministic deallocation makes "bytes live after the turn" a function of
the program, hence chargeable — the storage half of metering is well defined in Mini in a way it was not in Agoric
(§1.4).

## 2.B Capability and capture types (forks 1, 3, 5)

**B1. Odersky, Zhao, Xu, Bračevac, Pham. "Tracking Capabilities for Safer Agents." arXiv:2603.00991 (CAIS '26),
2026.** — `odersky-tracking-capabilities-safer-agents-2026.pdf`. READ (§1–4.1) [lane A; quote spot-checked].
- **New.** Untrusted generators (LLM agents) submit *code* in a capability-safe Scala 3 subset; it is capture-checked
  then run; pure function types (`T -> U`) cannot invoke anything; scoped capabilities die at block exit; in
  multi-turn sessions "capabilities granted … in turn 𝑛 are invalid in turn 𝑛 + 1"; "Capability completeness:
  capabilities regulate all safety-relevant effects, except those that can be contained at runtime."
- **Evidence.** 131 trials per model/mode; classified mode 100% security for both models tested, utility 99.2% and
  90.0%.
- **Mini.** This is Mini's admission with a REPL where Mini has a Host, applied to *AI residents*. Transfers:
  (1) law and plan-producing code typed pure; (2) **turn-scoped capabilities (the signer's authority, the fee meter)
  may never enter a checkpoint**; (3) a warning the siblings miss — **law refusal explanations are an information
  channel**: a caller can probe a cell it cannot read by proposing writes and reading the refusal. Fork 2 needs a
  redaction policy (who may see which leaf).

**B2. Pham, Bračevac, Xu, Zhao, Odersky. "Classifying Capabilities." arXiv:2607.24504, Jul 2026.** —
`classifying-capabilities-2026.pdf`. READ (§1–2.1, 3.6, 4.1–4.3) [lane A; quote spot-checked].
- **New.** An open hierarchy of capability *classifiers* (Control, ThreadLocal, Shared, Exclusive, user-defined);
  capture-set projections `c.only[C]`, `c.except[C]`; soundness via a **checked big-step semantics** where evaluation
  carries an allowance and gets stuck on an unauthorised use; "Given a well-typed term … and a label allowance of at
  least the runtime labels of the use set, evaluation never gets stuck"; mechanised **in Lean 4**.
- **Mini.** (a) The right *shape* for Mini's admission theorem: re-execution is a checked semantics whose allowance
  is the invocation's granted authority; theorem: "a certified-typed invocation is never refused for authority, only
  by laws". (b) Classifiers answer "what may cross a yield" in one line: the resume body captures
  `any.except[TurnScoped]`. (c) A ReadOnly classifier gives static read-only signals for parallel scheduling.
  Cost: capture sets in Core4 types are a real extension with re-proofs; the Lean mechanisation is a template.

**B3. Xu, Bračevac, Pham, Odersky. "What's in the Box" (reach capabilities, System Capless). OOPSLA 2025,
arXiv:2509.07609;** **"System Capybara", arXiv:2607.09383, 2026;** **Boruch-Gruszecki et al., "Capturing Types",
TOPLAS 2023;** **Brachthäuser et al., "Effects, Capabilities, and Boxes" (System C), OOPSLA 2022.** —
`xu-whats-in-the-box-2025.pdf`, `boruchgruszecki-capturing-types-2023.pdf`, `brachthauser-effects-capabilities-
boxes-2022.pdf`. SKIMMED [lane A]. Reach capabilities name the authority hidden inside generic data (Lean-mechanised);
Capybara adds separation/freshness/read-only (Lean 4 soundness); System C makes capabilities **second-class by
default** (passed down, never returned or stored) unless boxed with a tracked capture set. **Mini (cheap and
decisive):** (1) **keep Plans first-order** (no closures), so the Host never has to find authority "in the box";
(2) adopt System C's rule as v1's checkpoint discipline: handlers and turn-scoped caps are second-class; only durable
caps may be stored in cells or checkpoints. This is the type-level form of SCHOLAR-CALLS idea 4's val/iso/tag rule.

**B4. Classics revisited [lane A, INFERRED]: Wyvern (Melicher et al., ECOOP 2017), Pony (Clebsch et al., 2015, in
paperbin), Austral (2023).** Wyvern: module authority as a static query — Mini should *show* an object's reachable
authority on its card. Pony `tag` (send-only, no read/write) is the right capability tier for "may invoke B, may not
read B". Austral's linear capabilities are not needed: Mini enforces one-shot in the store.

## 2.C Resource bounds and gas (forks 1, 3)

**C1. Grosen, Kahn, Hoffmann. "Automatic Amortized Resource Analysis with Regular Recursive Types." LICS 2023,
arXiv:2304.13627;** **Hoffmann, Jost. "Two Decades of AARA." MSCS 32(6), 2022 (INFERRED, paywalled);** **Lian, Wang.
"RaRust: prophecy potentials", arXiv:2502.19810, 2025.** — `grosen-aara-regular-recursive-types-2023.pdf`,
`lian-aara-2025.pdf`. SKIMMED [lane A]. Bounds for every regular recursive type by LP; RaRust layers potentials on an
already-checked ownership discipline. **Mini (decides "not now"):** Core4 is lazy call-by-need with general `fix`,
reflection and mixin dispatch, which defeat standard AARA (lazy AARA is much weaker). Build the *target* instead: a
Lean cost semantics. RaRust's idea of potential carried *on a cell* is a sketch for prepaid resident fees.

**C2. Das, Balzer, Hoffmann, Pfenning, Santurkar. "Resource-Aware Session Types for Digital Contracts" (Nomos). CSF
2021.** — `das-nomos-2019.pdf`. SKIMMED [lane A]; **Cai et al., "Asparagus" (OOPSLA 2023)** INFERRED. Potential in the
session type; well-typed contracts cannot run out of gas. **Mini:** the cheap version is a **declared, kernel-enforced
per-resume step cap in the `Activity` type**: a response delivered to a resident must carry the declared budget or
is refused before execution — "the fee is part of the interface", without inference.

## 2.D Certified admission, checker diversity, robust safety (fork 2, assurance)

**D1. Bosamiya, Lim, Parno. "Provably-Safe Multilingual Software Sandboxing using WebAssembly" (vWasm/rWasm). USENIX
Security 2022.** — `bosamiya-vwasm-rwasm-2022.pdf`. READ (§1, §4) [lane A; quote spot-checked]. "we do not have the
semantics of the input language in our TCB, while traditional compiler correctness would necessarily need it."
**Mini (decisive, cheap):** split assurance into two theorems with different TCBs. (1) **Sandboxing**: every Host
transition applies a signed, paid, law-accepted Plan — a theorem about the Host step function that holds *even if the
Core4 evaluator or the Objective Bend front-end is wrong*. (2) **Agreement**: re-execution is deterministic, which is
where the evaluator and the Lean compiler sit in the TCB. This keeps "no proof system in admission" honest.

**D2. Carneiro. "Lean4Lean: Verifying a Typechecker for Lean, in Lean." arXiv:2403.14064 (v3 Sep 2025).** —
`carneiro-lean4lean-2024.pdf`. READ (§1–2.4, 7) [lane A; quote spot-checked]. An independent Lean 4 kernel in Lean,
"between 20% and 50% slower", checks all of Mathlib; found and fixed one kernel soundness bug. **Mini:** run
Lean4Lean (and nanoda) over Mini's environment in CI — minutes of cost. It covers the *kernel*, not the **compiler**
that runs the Core4 evaluator in the Host; diversity for execution needs a second evaluator framed as a *checker*.

**D3. Abate, Blanco, Garg, Hriţcu, Patrignani, Thibault. "Journey Beyond Full Abstraction." CSF 2019,
arXiv:1807.04603;** (Mück et al., POPL 2026, already in paperbin). — `abate-journey-beyond-full-abstraction-2019.pdf`.
READ (§1–2.1) [lane A; quote spot-checked]. Robust *safety* preservation is cheaper than full abstraction. **Mini:**
laws as a reference monitor give robust safety of *per-cell* invariants against any code by construction; but
**cross-cell invariants proved only at the Objective Bend level do not hold against arbitrary signed Core4
invocations**. So fork 2 needs multi-cell (relational) laws — the same conclusion lane B reached from Anoma's action
scope (G1) by a different road.

**D4. Rao, Georges, Legoupil, Watt, Pichon-Pharabod, Gardner, Birkedal. "Iris-Wasm." PLDI 2023.** —
`rao-iris-wasm-2023.pdf`. SKIMMED [lane A]. Robust safety: "unknown, adversarial code can only affect other modules
through the functions that they explicitly export." **Mini:** use it as the *statement* template ("an object's cells
change only via its methods' Plans under its laws"); prove it as a plain trace invariant of the Host step function,
not with Iris.

**D5. Stoyle, Hicks, Bierman, Sewell, Neamtiu. "Mutatis Mutandis: Safe and Predictable Dynamic Software Updating"
(Proteus). POPL 2005 [foundational].** — `stoyle-proteus-dsu-2005.pdf`. READ (abstract, §1) [lane A; quote
spot-checked]. An update to type t is safe iff the program is *con-t-free*: "no updated values v′ of type t will ever
be manipulated concretely by code that relies on the old representation". **Mini (fork 4):** with an exact codec,
con-freeness is a literal scan of each suspended activity's machine state — **including inside unevaluated thunks**,
which hide concrete uses of old code in a lazy machine. This is the decidable check behind a Map/Replay disposition,
and it needs the machine-state typing A4 already asks for.

## 2.E Rich calls: pipelines, gates and caller-side authority (fork 1)

**E1. Varda. "Cap'n Web: a new RPC system for browsers and web servers." Cloudflare blog, 2025-09-22.**
https://blog.cloudflare.com/capnweb-javascript-rpc-library/ — `cloudflare-capnweb-2025.txt`. READ [lane B; quote
spot-checked by me].
- **New.** Schemaless ocap RPC with import/export tables on both sides; each `push` gets a predictable id, so a
  caller can address a result before it exists; `.map()` is executed once on a placeholder to *record* the
  pipelined calls, which ship as a non-Turing-complete program — "the 'DSL' used to represent 'instructions' for the
  map function is just the RPC protocol itself."
- **Evidence.** Design post; in production for Wrangler remote bindings; no benchmarks.
- **Mini.** The signed invocation should be a **pipeline** (pushes on capabilities or prior results), not one
  method call. In one domain the Host re-executes the whole pipeline as one turn, so the chain is atomic and the
  laws judge the composed Plan; across domains it splits into eventual sends to answer slots. Keep the pipeline
  language non-Turing-complete so metering stays a function of its length.

**E2. Varda. "Durable Objects: Easy, Fast, Correct — Choose Three." Cloudflare blog, 2021.**
https://blog.cloudflare.com/durable-objects-easy-fast-correct-choose-three/ —
`cloudflare-durable-objects-easy-fast-correct-2021.txt`. READ [lane B].
- **New.** Input gates (no new event while storage I/O is pending), **output gates** ("any new outgoing network
  messages will be held back until the write has completed"), write coalescing between awaits.
- **Mini.** Mini's atomic turn is the input gate. The output gate must be a *runtime rule* for every eventual send
  and every external reply: nothing leaves until the turn is committed (and Simplex-final in committee domains).
  The post's admitted residual hole — interleaving of replies to an object's own outgoing calls — is Mini's
  several-activities-per-object hazard (fork 3); deterministic, but still a correctness hazard.

**E3. Cloudflare. "We've added JavaScript-native RPC to Cloudflare Workers." 2024.**
`cloudflare-workers-rpc-2024.txt`. SKIMMED [lane B]. Same-domain RPC "usually runs in the very same thread as the
caller"; class instances cross as stubs. **Mini:** supports "same domain = in-turn call, other domain = stub +
eventual send" as the default split.

**E4. Labella. Unison Forall 2024 talk notes; Unison Cloud core concepts (2024–25).**
`systemfw-unison-klogs-forall-2024.md`, `unison-cloud-core-concepts-2025.txt`. READ (talk notes) [lane B].
- **New.** `Location g` is typed by the abilities it supports; `Storage.transact : Database -> '{Transaction,
  Exception} a -> {Storage, Exception} a` — **a transaction body cannot perform `Remote` effects, by typing.**
- **Mini.** The type-level rule fork 1 needs: code inside a turn has a `Transaction`-like effect row (reads,
  in-domain calls, Plan construction); eventual sends and yields are a different effect, legal only in the returned
  Plan. Core4's `Activity<P,R,A>` can carry exactly this split.

**E5. Kadena. "Capability theory in Pact" (pact wiki, Stuart Popejoy et al., c. 2020–2023) and "Capabilities"
(Pact 5 docs, 2025–26).** https://github.com/kadena-io/pact/wiki/Capability-theory-in-Pact ,
https://docs.kadena.io/smart-contracts/capabilities — `kadena-pact-capability-theory-wiki.md`,
`kadena-docs-capabilities-2026.md`. READ (definitions, operational semantics of install/acquire/compose; docs
§signature-based scope) [me].
- **New mechanism.** A signer attaches *capability references with parameters* to its signature (e.g.
  `coin.TRANSFER alice bob 10.0`); the signature then authorises **only** acquisition of those capabilities.
  *Managed* capabilities carry a pure manager function `m :: P_M → P_S → Either Error P'_M` that decrements the
  installed budget each time code requests a matching capability; acquisition is scoped to a `with-capability`
  block on the call stack; `compose-capability` imports sub-capabilities only from inside a guard.
- **Evidence.** In production on Kadena mainnet since Pact 3 (2019–); the docs' own claim: "Scoped capabilities
  provide a transparent way for transaction signers to safely call untrusted code … Regardless of the code that
  runs during the transaction, scoped capabilities ensure that only authorized actions can be performed on the
  user's behalf."
- **Mini (fork 1 × fork 2).** This is the missing *authority* half of Zoe's offers. An offer bounds the *outcome*;
  a scoped/managed capability bounds what any code *in the turn* may do with the signer's authority while it runs.
  For rich synchronous calls across principals (Ember's fork 1), the signed invocation should carry a list of
  scoped grants — `Transfer(from = me, asset = A, ≤ 10)`, `Call(target, method)` — each a decreasing counter judged
  by a `le` atom, so nested callees can spend the caller's authority only within the signed envelope. Cost: one
  invocation field, one kernel table per turn, and the guard check at every authority use. This is strictly
  simpler than ECF or call-tree authorization rules and composes with both (SCHOLAR-LAWS idea 3).

**E6. Mysten Labs. "Programmable Transaction Blocks" (Sui docs, 2023–2026).**
https://docs.sui.io/concepts/transactions/prog-txn-blocks — `sui-ptb-docs-2026.txt`. SKIMMED [me].
- **Mechanism.** A transaction is a vector of inputs and up to 1,024 commands (`MoveCall`, `SplitCoins`,
  `MergeCoins`, `TransferObjects`, …) that "execute in order. You can use the results from one … command in any
  subsequent … command"; effects apply atomically at the end; "If any command fails, the entire block fails".
- **Mini (fork 1).** The *caller-composed* form of rich cross-object calls: a signed invocation that is itself a
  tiny straight-line Plan program over several objects' methods with result passing. It needs no callee to trust
  another callee, and it gives the wallet/AI resident a way to compose without writing a package. Mini can admit it
  as a restricted Core4 term (no recursion, results by index), re-executed like any method. Cost: an invocation
  form; every command is an ordinary call under the same guards and laws.

## 2.F Re-entrancy, confused deputies and information flow (fork 1 × fork 2)

**F1. Cecchetti, Yao, Ni, Myers. "Compositional Security for Reentrant Applications" (SeRIF). IEEE S&P 2021.**
arXiv:2103.08577 — `cecchetti-serif-reentrant-2021.pdf`. READ (§4 definitions) [lane B; quote spot-checked].
- **New.** A *semantic* definition: "A program is ℓ-reentrancy-secure if every ℓ-integrity property, such as a
  program invariant, that holds for all non-ℓ-reentrant executions holds for all executions." Enforced by integrity
  labels plus static/dynamic locks; tail re-entrancy is secure by construction.
- **Mini.** The correctness criterion for in-turn synchronous calls. End-of-turn law checks stop only damage a law
  can express; a stale-read-derived but law-valid write (the DAO shape) passes. So the Lean theorem to prove is
  "every admitted re-entrant turn is equivalent to some non-re-entrant turn" — which the SCHOLAR-CALLS re-entry
  guard makes true by refusing re-entry, and which an opt-in ECF check would make true by search.

**F2. Yao, Ni, Ma, Schiff, Myers, Cecchetti. "SCIF: A Language for Smart Contracts with Secure Control Flow."
OOPSLA 2025 (arXiv:2407.01204v2).** — `yao-scif-secure-control-flow-2024.pdf`. READ (§1–3) [lane B].
- **New.** Confused-deputy prevention by checking whose authority a call carries; after an untrusted call "the pc
  label is modified, restricting future operations to only those that cannot violate high-integrity invariants";
  declared *exceptions* (state kept) vs *failures* (rolled back), `atomic { } rescue`.
- **Mini.** (a) exception vs failure = typed Plan alternative vs law refusal (whole turn rolls back); (b) `atomic …
  rescue` = sub-turn rollback for an in-turn call, cheap with Mini's checkpoint codec; (c) pc-lowering is a
  *finer* alternative to refusing re-entry, worth it only if refusal proves too strict.

## 2.G Laws over actions: resource machines (fork 2 × fork 3)

**G1. Khalniyazova, Goes. "Anoma Resource Machine Specification." Heliax, 2024-06-25, doi:10.5281/zenodo.10689620;
plus the 2025 online spec (actions, resource logics).** — `khalniyazova-anoma-resource-machine-2024.pdf`,
`anoma-specs-action-2025.txt`, `anoma-specs-resource-logic-2025.txt`. READ [lane B; quote spot-checked by me].
- **New.** State = immutable resources; each carries a *resource logic* checked on create and consume; validity =
  per-resource logic + a transaction-wide **delta (balance) check** (Σ kind-homomorphic deltas = balancing value)
  + compliance (existence, nullifier freshness). Transactions compose by disjoint union; an unbalanced partial
  transaction is an *intent*; a solver composes intents into a balanced transaction — multi-party atomic
  settlement without 2PC. 2025: "Actions partition the state change induced by a transaction and limit the
  evaluation context of resource logics."
- **Evidence.** Specification with worked examples (swap, 3-party NFT cycle); no theorems, no measurements.
- **Mini (with my correction to the lane).** The lane says a Mini per-cell law "cannot state conservation"; that is
  true of `Pred`, but Mini *already has* ARM's delta check for kernel assets: the Book's posting algebra with
  `Operation.apply_conserves` (READ). What Mini lacks is the **action scope**: a law that may read the *other cells
  touched by the same Plan* (beyond `LawComposition`'s declared dependency DAG). Adopt it — it is what lets a seat's
  law, an escrow's law or a deal cell's law say "only together with that matching leg". And adopt **composition of
  signed partial invocations** (each party signs an unbalanced Plan; anyone composes; admission checks laws +
  Book balance) as Mini's in-domain multi-party atomicity. Do not adopt ARM's solver/preference machinery.

## 2.H Choreographies, 2025–2026 (fork 1 × fork 3)

**H1. Kløvedal, Plyukhin, Peressotti, Montesi. "Accompanist: A Runtime for Resilient Choreographic Programming."
arXiv:2603.20942, Mar 2026.** — `klovedal-accompanist-2026.pdf`. READ (§1, 4.4–5, 6) [lane B; quote spot-checked;
proofs in a supplement, not checked].
- **New.** Choral programs compiled to sidecars; fault tolerance by replay; durable inbox/outbox; idempotent local
  transactions; sagas with compensation; theorems: deadlock-freedom and **weak atomicity** (all succeed, or all run
  compensations in reverse), EPP bisimulation, and restart elimination. "Our key assumptions are that choreographic
  programs should be deterministic, transactions within a saga should be idempotent, and messages should be written
  to a durable message queue."
- **Evidence.** Median latency 32 ms vs 190 ms for Temporal; p99 6.7× better.
- **Mini.** Mini supplies all three assumptions by construction (re-execution, once-only admission, outbox cells).
  This is the buildable answer for cross-domain workflows that are *not* pure asset exchange (where the deal cell of
  SCHOLAR-CALLS idea 7 applies): typed compensating Plans + a weak-atomicity theorem in Lean. Weak atomicity is not
  isolation; laws must tolerate visible intermediate states.

**H2. Wiersdorf, Greenman. "Chorex: Restartable, Language-Integrated Choreographies." Programming 10(3), 2025,
arXiv:2511.15820.** — `wiersdorf-chorex-2025.pdf`. READ (§1–2, 5, 7) [lane B]. `checkpoint … rescue` per actor,
supervisor restart, an "all clear" barrier; overhead 1.01×–6.76×, dominated by checkpointing deep stacks. **Mini:**
evidence for the exact machine codec, and a warning that per-resume checkpoints must be incremental/structurally
shared, not full re-serialisations.

**H3. Daniel, Böhler, Richter, Weisenburger, Mezini. "On Eliminating the Impossible with Dependent Types:
Choreographic Libraries with Proof-Carrying Located Values" (ChorLean). arXiv:2608.23237, Aug 2026.** —
`daniel-chorlean-proof-carrying-located-values-2026.pdf`. SKIMMED [lane B]. A **Lean 4** choreography library with
total endpoint projection via proof-carrying located values and census polymorphism. **Mini:** Lean-native prior art
if Mini writes multi-domain protocols as choreographies.

**H4. Samuelson, Hirsch, Cecchetti. "Choreographic Quick Changes: First-Class Location (Set) Polymorphism" (λqc).
arXiv:2506.10913, 2025;** follow-on "Step in Tine", arXiv:2605.23031. — `samuelson-quick-changes-2025.pdf`. SKIMMED
[lane B]. First typed choreographic language with first-class process names (deadlock freedom mechanised in Rocq);
the follow-on adds forking. **Mini:** object/domain references are first-class names, so this is the feature a Mini
choreography layer needs; typed deadlock freedom survives it.

**H5. Gopinathan, Feser, Naim, Tavares, Bingham. "Pact: A Choreographic Language for Agentic Ecosystems." CP'26
workshop, arXiv:2605.03143.** — `gopinathan-pact-2026.pdf`. SKIMMED [lane B]. Choreographies as games with
`agent.choose` and declared utilities. **Mini:** a reminder that projection assumes cooperation; each domain's laws
must stand alone against self-interested parties.

**H6. Laddad, Cheung, Hellerstein, Milano. "Flo: a Semantic Foundation for Progressive Stream Processing." POPL
2025.** — `laddad-flo-2025.pdf`. SKIMMED [lane B]. Streaming progress, eager execution, and a bounded/unbounded
stream distinction (only bounded streams may be blocked on). **Mini (INFERRED):** a boundedness tag on an activity's
typed response channel makes "waits forever on an unbounded source" a static error.

## 2.I Local-first and consensus-free multi-party state

**I1. Kleppmann. "Making CRDTs Byzantine Fault Tolerant." PaPoC 2022.** — `kleppmann-bft-crdt-2022.pdf`. READ
[lane B]. Hash-DAG of updates; validity decided only from `before(u)` ("we can safely decide whether update u is
valid by basing the decision only on the updates in before(u)"); tolerates any number of Byzantine replicas; the
general claim is explicitly a conjecture. **Mini:** this decides fork 3's "genuinely multi-party" question:
consensus-free multi-party domains are possible *only if* laws are judged on the causal past the invocation names,
not on current state. Committee domains (Simplex) do not need it.

**I2. Good, Mumm, Zelenka (+Yen). Keyhive lab notebook, Ink & Switch, 2024-08 → 2026-07.** —
`inkandswitch-keyhive-notebook-2025.txt`. READ (entries 00, 01, 05, 06) [lane B]. Convergent capabilities: a document
is a public key that delegates over itself; the delegation graph is CRDT state; BeeKEM group keys; Beelay sync. Open:
concurrent mutual revocation and backdating — revocation under concurrency "needs consensus or it is unsound".
**Mini:** keep fail-stop ocaps in committee domains; steal "documents are groups" (objects as principals in the
delegation graph).

**I3. Gentle, Kleppmann. "Collaborative Text Editing with Eg-walker: Better, Faster, Smaller." EuroSys 2025.** —
`gentle-egwalker-2025.pdf`. READ (§1–3) [lane B]. Persist the event graph; build CRDT state only transiently around
concurrency; "critical versions" allow discarding it; 1–2 orders of magnitude less steady-state memory. **Mini:**
the log-as-truth shape Mini already has; "critical version" names when per-branch bookkeeping can be compacted.

## 2.J Verified distributed systems, Lean-adjacent

**J1. Pîrlea, Gladshtein, Kinsbruner, Zhao, Sergey. "Veil: A Framework for Automated and Interactive Verification
of Transition Systems." CAV 2025.** — `pirlea-veil-2025.pdf`. READ (§1–4) [lane B; quote spot-checked]. Ivy-style
DSL embedded in **Lean 4**; "its verification condition (VC) generator is proven sound"; SMT discharge (cvc5/Z3) with
interactive fallback; `sat trace` non-vacuity checks; 16 case studies incl. non-EPR protocols, 87.5% verify in <15 s.
**Mini:** the tool for protocol-level invariants (Simplex, sagas, the resume protocol) in Mini's own language;
`sat trace` is a built-in guard against vacuous specs. Caveat: results are kernel-checked only with proof
reconstruction (Lean-SMT), not with a trusted solver.

**J2. Sun, Ma, Gu, Ma, Chajed, Howell, Lattuada, Padon, Suresh, Szekeres, Xu. "Anvil: Verifying Liveness of Cluster
Management Controllers." OSDI 2024 (Best Paper).** — `sun-anvil-2024.pdf`. READ (§1–3) [lane B; quote spot-checked].
`step(desired, response, local) → (local', request)` with "no more than one external request per step()"; spec
*Eventually Stable Reconciliation* ∀d. □(□desire(d) ⇒ ◇□match(d)); three verified Kubernetes controllers, proof:code
4.5–7.4. **Mini:** Anvil's step *is* a Core4 activity (one Plan action per yield is already Core4's shape). ESR is
the ready-made **liveness spec for residents**, which safety-only laws cannot state.

**J3. Zhang, Hance, Kapritsos, Chajed, Parno. "Inductive Invariants That Spark Joy" (Kondo). OSDI 2024.** —
`zhang-kondo-2024.pdf`. READ (§1, 3, 6) [lane B]. Prove protocol invariants on a **synchronous** version; generate
the asynchronous protocol plus message/ownership invariants; zero user invariants for three of ten protocols.
**Mini:** the method for fork 1 — specify with in-turn calls, lift to eventual sends mechanically; capability
transfer is an ownership invariant (the fully automated class).

**J4. Howard, Kuppe, Ashton, Chamayou, Crooks. "Smart Casual Verification of the Confidential Consortium
Framework." NSDI 2025.** — `howard-smart-casual-ccf-2025.pdf`. READ (§1, 6) [lane B]. Trace validation of a 63 kLoC
C++ system against TLA+; six bugs prevented. **Mini:** the right bar for the non-Lean parts (Simplex mesh, Rust
custody, networking): log events, validate against a Veil/Lean model in CI.

**J5. Lattuada et al. "Verus: A Practical Foundation for Systems Verification." SOSP 2024.** —
`lattuada-verus-sys-2024.pdf`. SKIMMED [lane B]. Linear ghost resources, an EPR mode inside a general verifier.
**Mini:** only for Rust that stays in the TCB.

## 2.K Durable execution and deterministic transactions, 2022–2026

**K1. Li, Chandramouli, Bernstein, Madden. "Distributed Speculative Execution for Resilient Cloud Applications"
(libDSE). arXiv:2412.13314, 2024.** — `li-distributed-speculative-execution-2024.pdf`. READ (§1–2) [lane B]. Write as
if every step persists; track recovery dependencies; "Externally visible results are delayed until persistence";
cascading rollback to a consistent cut; up to 10× lower latency. **Mini:** a *later* optimisation (speculative
cross-domain consumption); v1 should use the plain output gate.

**K2. Kraft, Li, Kaffes, Skiadopoulos, Kumar, … Stonebraker, Suresh, Yu, Zaharia. "Apiary: A DBMS-Integrated
Transactional Function-as-a-Service Framework." arXiv:2208.13068.** — `kraft-apiary-2023.pdf`. READ (§4) [lane B].
Outputs recorded under workflow-derived invocation ids; *selective function recording* (record writers and fan-out
reads only) cuts overhead from 2.2× to <5%. **Mini:** the question it raises is sharp: at a resume, only the
*response* is non-recomputable; the machine can be re-derived by replay from the last full checkpoint. A measured
size-vs-replay-time trade, not a semantic change.

**K3. Liu, Levy, Noghabi, Burckhardt. "Doing More with Less: Orchestrating Serverless Applications without an
Orchestrator" (Unum). NSDI 2023.** — `liu-unum-2023.pdf`. READ (§1, 3.3) [lane B]. First-writer-wins checkpoint per
invocation name gives exactly-once despite non-deterministic duplicates; 2× faster, 9× cheaper than Step Functions.
**Mini:** first-writer-wins on (activity, step) for externally driven resumes — one law on the activity cell.

**K4. Psarakis, Christodoulou, Fragkoulis, Katsifodimos. "Transactional Cloud Applications Go with the (Data)Flow."
CIDR 2025.** — `psarakis-dataflow-transactional-cloud-2025.pdf`. SKIMMED [lane B]. Deterministic protocols are
"forward-only" (no rollback once order or read/write sets are fixed); 180K tpmC sub-second. **Mini:** supports
deterministic parallel admission (SCHOLAR-CALLS idea 5); reply-before-snapshot conflicts with the output gate.

**K5. Skiadopoulos et al. "DBOS: A DBMS-oriented Operating System." PVLDB 15(1), 2022.** — `skiadopoulos-dbos-2022.pdf`.
SKIMMED [lane B]. OS state in a distributed transactional DBMS. **Mini:** shares the thesis (everything is cells under
one root); Apiary is the useful descendant.

**K6. Maraschi, Collina. "State Without a Landlord." arXiv:2609.17645, Sep 2026.** —
`maraschi-state-without-landlord-2026.pdf`. SKIMMED [lane B]. Replicated authenticated journals among a workflow's
parties; "signatures establish (authorship and order)" but not "truth of recorded effects". **Mini:** re-execution
establishes effect truth; that is the differentiator to state in comparisons.

## 2.L Agoric-adjacent formal work

**L1. Drossopoulou, Noble, Miller, Murray. "Reasoning about Risk and Trust in an Open World." VUW tech report
ECSTR15-08, 2015.** http://ecs.victoria.ac.nz/foswiki/pub/Main/TechnicalReportSeries/ECSTR15-08.pdf —
`drossopoulou-risk-trust-open-world-2015.txt`. SKIMMED (abstract, §1) [me].
- **Mechanism.** Hypothetical predicates `o obeys Spec`, `MayAccess(o,p)`, `MayAffect(o,p)` and a Hoare logic of
  four-tuples (pre, invariant, post) used to prove the key steps of the 2013 escrow exchange.
- **Mini.** It is the formal ancestor of Agoric's "Zoe2 correct-by-construction escrow" spike (#8184) and of
  SCHOLAR-LAWS's necessity specs (B14). For Mini, the point is negative: Mini does not need trust reasoning about
  issuers or escrow agents, because both are kernel code; the logic is needed only for *user* packages that hold
  others' capabilities across yields.

---

# Part 3 — Synthesis: what the four siblings' recommendations should be upgraded or corrected to

The four reports agree on Mini's spine. Agoric's record and the 2022–2026 work change twelve of their
recommendations; each item names whose and why.

**1. Offers are persistent seats, not one-shot caller checks (corrects LAWS idea 2, CALLS A13, ROOT's Zoe note).**
The siblings describe Zoe as "the contract proposes a reallocation; Zoe commits it only if offer-safe". The code says
something stronger and something weaker:
- *Stronger:* offer safety is checked on **every** reallocation of a seat, for as long as the seat lives, so it is an
  invariant, not an admission-time check.
- *Weaker:* the check runs in ZCF *inside the contract's own vat*, separated from the contract only by a SES
  Compartment. Payout liveness is "conditional on well-behaved issuers", minting skips conservation, and Agoric's own
  docs say the check belonged in a separate escrow service (§1.10).

Mini can have the strong version without the weaknesses:
- an offer creates a **seat**, which is a Book account plus a law;
- the offer-safety predicate is already expressible in `Pred` (`anyL` of two `allL`s of lower bounds over total
  slots);
- conservation is the Book's proved posting algebra;
- `exit` is a kernel action whose admissibility for the offerer no contract can override.

Payout liveness then becomes a kernel theorem for Book assets. So: no user-coded issuers, and LAWS' per-invocation
"caller law" is the single-turn special case of a seat. And **inside one turn, assay and transfer are atomic, so single-domain trades need no escrow at all.** Escrow
is needed only across a yield or a domain (Miller 2000's argument for escrow assumes those two steps are separated in
time).

**2. Bound authority as well as outcome (fills a gap in LAWS ideas 2–3 and CALLS idea 1).** Offers bound what the
caller *ends up with*. They do not bound what nested callees do with the caller's authority during a rich synchronous
call tree. Pact's scoped and managed capabilities solve this in production: the signer attaches parameterised
capabilities to the signature (`TRANSFER me * A ≤ 10`), and a pure manager decrements them as code acquires them.
The Pact docs say this lets signers "safely call untrusted code". In Mini: an invocation field of scoped grants, each a
decreasing counter judged by a `le` atom. Together with CALLS' re-entry refusal, it makes Ember's
"very rich" calls safe without ECF search.

- **The spec for re-entrancy should be semantic.** SeRIF's definition, "every invariant of non-re-entrant executions
  holds of all executions", becomes the Lean theorem that the re-entry guard discharges.
- **Make the re-entry guard mandatory, not opt-in.** SES documents the synchronous-call re-entry hazard, and Agoric's
  own answer was never to call synchronously across trust boundaries.

**3. Laws apply at three points, not one (upgrades LAWS and BREAD fork 2).** Agoric independently converged on
decidable predicates at three points:
- method arguments and returns (exo `InterfaceGuard`), checked *before* the method runs;
- object state writes (`stateShape`);
- proposals (`proposalShape`).

Give every package method a guard in the law language; a guard refusal costs no Core4 execution. Mini can also *decide* guard implication at publish time, which Agoric cannot:
an upgrade is compatible iff `old ∧ ¬new` is unsatisfiable.

**4. Add an action scope for laws and multi-cell laws (upgrades LAWS idea 1 and BREAD 3.2).** Two independent routes
reach the same conclusion:
- Anoma's resource machine bounds each resource logic to an *action*, meaning the resources co-touched by one
  transaction.
- The secure-compilation lattice (Abate et al.) shows that cross-cell invariants proved only at the Objective Bend
  level do not hold against adversarial Core4 invocations.

So a law must be able to read the *other cells its Plan touches*. That reach goes beyond `LawComposition`'s declared
dependency DAG. Lane B's further claim that a Mini law "cannot state conservation" needs correcting: conservation is
already the Book's posting theorem (`Operation.apply_conserves`), which plays the role of Anoma's delta check. The gap
is only relational laws over non-Book state.

**5. The invocation is a pipeline (adds a third call form to CALLS idea 1).** CALLS proposes two forms: depth-first
`call` and breadth-first `send`. Production adds a third, caller-composed form:
- Sui's Programmable Transaction Blocks: up to 1,024 commands with result passing, all-or-nothing.
- Cap'n Web: a record-and-replay pipeline whose DSL "is just the RPC protocol itself".

In Mini, a signed invocation is a straight-line, non-recursive pipeline of calls on capabilities and on prior
results. It is re-executed as one turn, and the laws judge the composed Plan. Composing *partially signed* pipelines
from several parties gives in-domain multi-party atomicity with no two-phase commit (Anoma's composed intents). This
narrows BREAD's "2PC with escrow" and CALLS idea 7 to the cross-domain case only.

**6. Continuations: settle OS vs CALLS in CALLS' favour, with Agoric's open bug as the decider (corrects OS Part I.1).**
OS wants continuation checkpoints kept "short-lived by policy". Agoric's history argues the other way:
- Abandoning in-flight work at upgrade was forced by engine-opaque heaps.
- It then had to be rebuilt in three layers: vows, retry-send, and asyncFlow replay. That rebuild amounts to
  long-lived continuations reconstructed by replay.
- Its open problem (#12315, January 2026) is that replay failure is discovered *after* the upgrade commits. Flows are
  marked Failed "in the hope that future upgrade can handle the situation … often … wishful thinking".
- Its rollback path halted mainnet (#12138, October 2025).

Upgrade to this rule:
- Checkpoints live as long as their awaits. They are pinned to their package hash and storage-charged.
- Every live activity must receive a disposition **inside the upgrade turn**, and the upgrade is refused otherwise.
- **Replay** is admitted only if replay succeeds in that turn. **Map** is admitted only if the activity is
  con-T-free (Proteus), where the scan reaches *inside thunks*, because laziness hides old-code uses.

Keep OS's requirement that *durable* state be stable-typed first-order data. Do not import Agoric's
heap/virtual/durable zones. Agoric's freeze of durable object state shape across upgrades shows that typed migration
(OS §8, CALLS idea 8) is a real advance and not a reinvention.

**7. What crosses a yield, typed (sharpens CALLS idea 4).** System C makes capabilities second-class by default, and
the 2026 capability classifiers (mechanised in Lean 4) and Odersky's agent harness ("caps from turn n are invalid in
turn n+1") support it. Together they give the type-level form of CALLS' val/iso/tag rule:
- turn-scoped authority (signer grants, the fee meter, handlers) may never enter a checkpoint or a cell;
- Plans stay first-order, so the Host never has to find authority hidden inside closures;
- Ahman–Pretnar asynchronous effects give the matching reading of a resident: no continuation ever crosses an
  object, and each interrupt delivery is one paid turn.

**8. Metering kernel work is achievable in Mini and impossible in Agoric (raises OS §6 from aspiration to theorem).**
Agoric runs liveslots deserialisation and all post-crank GC *unmetered* on purpose, because XS GC timing differs
after snapshot reload and metered GC would fork consensus. Mini's GC runs at yield, inside the semantics, so it is
deterministic. Mini can therefore state "metering is a function of pre-state and invocation, and meter ≥ machine
transitions" as a Lean cost-semantics theorem, covering codec, GC, law and Merkle work.

- Replace Agoric's terminate-on-exhaustion with *park and refund*.
- Defer AARA-style static gas: Core4's laziness, `fix` and reflection defeat it. A declared per-resume step cap in
  the `Activity` type (Nomos-lite) is the cheap typed budget.

**9. Every retention structure has a payer, and in-domain GC is ordinary (sharpens OS §4).** Agoric's two largest
storage failures:
- ERTP recovery sets, a *safety* feature, held about 60% of mainnet kv entries (#8400).
- A Zoe↔contract reference cycle (about 50k instances, about 310 MB) was uncollectable because cross-vat GC among
  suspicious parties is a "purple box" (#8401).

- Every watcher table, recovery list, inbox and await index is a cell with a payer.
- Within one domain all references are kernel-held caps in one Merkle store, so a deterministic tracing pass collects
  cycles.
- Termination is O(1): the object is a subtree root, detaching it ends the object, and reclamation happens off the
  consensus path. A law-governed termination capability is minted at creation, so no host "superpower" is ever needed
  (#8928, #9483).

**10. Cross-domain: output gate, deal cell for rights, sagas for the rest (refines CALLS idea 7 and OS §2).** 
- **The output gate is a runtime rule, not program discipline** (Durable Objects). Nothing leaves a domain until its
  turn is committed and final.
- **Exclusive rights use CALLS' deal cell**, with offer safety as its decision law (item 1).
- **Everything else uses choreographed sagas.** Accompanist proves weak atomicity under exactly the three
  assumptions Mini supplies by construction: determinism, idempotent admission, and a durable outbox. Laws must
  tolerate visible intermediate states.

On the fork 3 goal: genuinely multi-party domains *without* consensus require laws judged on the causal past the
invocation names (Kleppmann's `before(u)`). Keyhive shows the price is that revocation under concurrency becomes
unsound. Keep fail-stop ocaps in committee domains.

**11. Residents need a liveness spec, and there is a Lean tool (fills a gap; every sibling stops at safety plus
justness).**
- Anvil's controller step, with at most one external request per step, *is* a Core4 activity. Its *Eventually Stable
  Reconciliation*, □(□desire ⇒ ◇□match), is the resident liveness property that laws cannot express.
- **Veil** (Lean 4, with a VC generator proven sound and `sat trace` non-vacuity checks) plus **Kondo's** method
  (prove the synchronous protocol, lift it to the asynchronous one mechanically) is the verification path for the
  resume protocol, the deal cell and Simplex.
- Non-Lean parts get CCF-style trace validation.

**12. Assurance architecture and legibility (adds to OS §7 and BREAD's display ≤ evidence).** Split Mini's claims, as
vWasm does:
- **Sandboxing**: every transition is a signed, paid, law-accepted Plan. This holds even if the evaluator or the
  Objective Bend front-end is wrong.
- **Agreement**: re-execution is deterministic. This is the only claim that trusts the evaluator and the Lean
  compiler.

Lean4Lean in CI checks the kernel, not the compiler. - **Refusal explanations are an information channel** (lane A, from Odersky et al.'s threat model), so fork 2 needs
  a redaction policy.
- **Legibility is a security property** (Agoric governance). The card must show who holds each upgrade, termination
  and parameter capability, and which package counts the votes. Mini should have no `CoreEval`-style superuser.

**What does not change:** code proposes, law disposes; the turn as the unit of admission; linear answer slots;
law-derived coordination grades; Block-STM-style parallel admission; upgrade as one governed turn.

Agoric is the strongest evidence *for* it: its failures sit where it had to reconstruct state it could not name,
which is exactly what Mini's codec names.

---

# Appendix — what I read, what I relied on, and what I did not read

**Read by me (READ unless noted).** Agoric: `agoric-swingset-{delivery (intro, result promises, pipelining,
run-queue, three-party handoff, open questions), kernel-promises, garbage-collection (§Reachability–§Post-Decref),
virtual-objects, dynamic-vats, metering, run-policy, vat-upgrade}`, `agoric-liveslots-2025.md` (§GC vs Metering),
`agoric-vat-data-2025.md`, `agoric-vow-2025.md`, `agoric-async-flow{,-states}-2025.md`, `agoric-contract-upgrade-doc.txt`,
`agoric-zoe-offer-safety-docs.txt`; new downloads `agoric-doc-*-2026.md` (ERTP ×5, Zoe ×10, hardened JS, governance,
orchestration ×5; governance index SKIMMED), `agoric-zoe-zcf-doc-2026.md`, `agoric-src-{offerSafety,rightsConservation,
zcfSeat,zoeSeat,evalContractCode}-2026.js`, `agoric-{governance,orchestration,zone,xsnap,ertp,zoe}-readme-2026.md`,
`endo-{ses,exo,patterns,pass-style}-readme-2026.md` (eventual-send, captp, daemon READMEs SKIMMED),
`agoric-issue-{8400,8401,8928,8955,9483,10743,12138,12315,8184,9608}.txt`, `agoric-forum-patched-vuln-2023.txt`;
`miller-capability-financial-instruments-2000.txt` (§3.3–3.4, §6.1–6.4), `miller-distributed-electronic-rights-js-2013.txt`
(§2.5, §5, §6), `drossopoulou-risk-trust-open-world-2015.txt` (SKIMMED), `kadena-pact-capability-theory-wiki.md`,
`kadena-docs-capabilities-2026.md` (signature scope), `sui-ptb-docs-2026.txt` (SKIMMED). Mini:
`Theory/CanonicalResourceKernel.lean` (Book, Posting, Operation, `apply_conserves`), `Pred/Core.lean:161–270`
(constructors, `le` semantics). Siblings: all four reports' syntheses and disagreement sections, plus their Agoric
entries in full.

**Relied on from lanes (spot-checked by quote, not re-read in full):** every `[lane A]` and `[lane B]` entry in
Part 2. Lane caveats carried forward: Accompanist's proofs (supplement) unchecked; Veil's kernel-checked status
depends on the SMT backend; Kleppmann 2022's general claim is a conjecture; Hoffmann–Jost 2022, Asparagus and the
Koka reports were not obtained (INFERRED).

**Claims about Mini that are mine and unverified (INFERRED):** that Core4's `perform` always yields to the kernel
(Part 2 A5 is conditional on it); that an object's state can be laid out as a Merkle subtree for O(1) termination
(§1.5); that `memberOf` suffices for bounded non-fungible offer safety (§1.10); that in-domain cap-graph tracing GC is
cheap enough to run per block (§1.5). Each should be checked against `~/dev/minidregg` before it is briefed as fact.

**Not read.** Agoric's `comms` vat internals and `vstorage`/state-sync code; the Zoe 2 design (no public design doc
found beyond spike #8184); Agoric `smart-wallet` and `vbank` docs; the Inter Protocol vault contracts; talk videos
(no transcripts found); Waterken beyond what SCHOLAR-CALLS read.
