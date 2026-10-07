# 07 — Native admission by re-execution

Code: minidregg main `4ef4e808`, read only. Tags as in the index. Block-STM and CALM primary-text checks:
`lit/LIT-W3-calls-sends-contracts.md` §8–§9.

## 1. Current design

There is **no proof system in admission**: a receiver admits an Objective invocation by re-running the
front end and re-executing the method (`docs/OBJECTIVE-BEND.md:495-543`; `docs/ZK.md` is the empty proof
carrier).

- **Publish** (`Host/ObjectivePackageAuthor.lean`): the Host's own front end runs on the package; exactly
  `publishedCore` (`Compiler/ObjectiveBendPublication.lean`) is published; package edition 3 names one
  front-end identity.
- **Quote** (`Host/ObjectiveInvocationQuote.lean`): the local Host derives the final command from the
  member's retained request; it never accepts a remote command, output or input.
- **Admit** (`Kernel/ObjectiveBendNativeAdmission.lean`, `prepareCore` then `admit`): the registered
  policy re-encodes exactly; the declared envelope ≤ the policy maximum; `proofWork` equals the tariff's
  price of the declared envelope; funding checked before execution; sources and inputs only as current
  authenticated reads with exact guards; the receiver **re-runs the named front end** and admits only a
  byte-identical typed core; the applied term is type-checked; `executeWith` runs under the declared
  limits; the result is lowered to a Plan whose effects must equal the command's (`Output.exact`); measured
  usage must fit the declared envelope.
- **What it proves** (`Kernel/ObjectiveBendAdmissionSemantics.lean`): `admitted_source_semantics` (`:26`):
  the admitted run is a finished `runBounded` and its Data is *the* deep reference evaluation of the
  applied term; `admitted_data_unique` (`:44`): two admissions of the same applied term extract the same Data
  under any deployments, capacities and codecs ("a capacity envelope admits or refuses a run; it never
  changes what the run means"); `admitted_front_end` (`:97`): the typed core is byte-for-byte this front
  end's lowering of the package sources and is never refused by the machine.
- **Fees are priced on declared envelopes, never measured work** (`refund_measurement_free`,
  `Kernel/ObjectiveActivity.lean:2927`; `exhaustion_charges_declared`, `:3084`). Exhaustion is a paid,
  committed turn.
- **The front end is trusted.** "Source semantics" in these theorems is Core4's reference semantics, not
  `.obend`'s (GPT-6 §6; topic 00 row LT3). A replaying receiver reproduces the compiler's bytes, wrong or
  right.

## 2. What it commits us to

1. **Determinism is the whole security argument.** Every node must compute bit-identical results from the
   same inputs: no measured quantity may reach state or fees. Our theorems state determinism of the
   reference semantics (`source_evaluates_unique`) and resource independence (`runBounded_resource_independent`,
   `Theory/ObjectiveBendDemandAdequacy.lean:3636`). The C backend is differential-tested only
   (`docs/OBJECTIVE-BEND.md:644-647`), so a second executor is not covered by these theorems.
2. **Re-execution costs every validator the full work**, so the tariff must price the worst case it
   admits (declared envelope), and the envelope must also bound the front end's own re-run. Read: the
   checker's `typeFuel` is a priced lane of the tariff (`Kernel/ObjectiveTariff.lean:50`) and is passed to
   the replay (`Kernel/ObjectiveBendNativeAdmission.lean:395,418-419`, run "last, after every cheap
   refusal"); the policy bounds `sourceBytes` (`:79`). Not found: any bound or price on the parser,
   the elaborator, C4 linearization or template instantiation as such. INFERRED: their cost is bounded only
   indirectly, by source size, and no theorem states that bound.
3. **Admission is sequential per turn**; parallel admission would need a Block-STM-like guarantee that the
   parallel result equals a preset sequential order (the root's "root = sequential fold";
   VIA-SCHOLAR REVIEW-SCHOLAR-CALLS scope line).
4. **Privacy is out of scope**: laziness leaks through access patterns and timing; a private backend
   needs a both-arms `case` and a public resource bound (`docs/OBJECTIVE-BEND.md:642-652`).

## 3. Literature

- **State machine replication** (Schneider 1990, "Implementing fault-tolerant services using the state
  machine approach", ACM Computing Surveys): replicas agree if commands are deterministic and applied in
  the same order. Re-execution admission is SMR with the program as part of the command. INFERRED (classic;
  not re-read for this packet).
- **Execute-order-validate** (Androulaki et al. 2018, "Hyperledger Fabric: A Distributed Operating System
  for Permissioned Blockchains", EuroSys; paperbin `androulaki-hyperledger-fabric-2018.pdf`): Fabric does not
  re-execute at validators; it validates endorsed read/write sets, because chaincode may be nondeterministic.
  Our choice is the opposite and depends on Core4 determinism being total. INFERRED from my knowledge of the
  paper; not re-read for this packet.
- **Block-STM** (Gelashvili et al., PPoPP 2023; paperbin `gelashvili-block-stm-2022.pdf`): parallel
  optimistic execution; Corollary 2: the snapshot after join "returns the exact same values at exact same
  paths as would be persisted at the end of a sequential run"; termination (Thm 2) rests on `VM.execute` being
  wait-free; and "a single location for gas updates could make any block inherently sequential". READ
  (LIT-W3 §8). Our deferred-write frames are Block-STM's per-transaction write set, and no intra-turn
  read-your-writes across frames keeps validation per location — **provided** read sets are recorded per
  (object, field, version) and fee/escrow credits are commutative deltas rather than read-modify-write on one
  sink.
- **CALM** (Hellerstein & Alvaro, "Keeping CALM: When Distributed Consistency Is Easy", CACM 2020;
  paperbin `hellerstein-keeping-calm-2019.pdf`), Theorem 1: "A program has a consistent, coordination-free
  distributed implementation if and only if it is monotonic." READ. LIT-W3 §9 grades our operations: only
  unbounded appends and write-once slot decisions are monotone; the inbox bound, postage escrow, consume-once,
  deadline expiry and view reads all need the log (with Bailis et al. 2014 Claims 11–14 for the counter cases).
- **Durable functions** (Burckhardt et al. 2021, OOPSLA, Lemma 6.5 "Deterministic Replay", Thm 6.4): replay
  and stored-state models are bisimilar given determinism of the step, which "in a mainstream programming
  language … is not implicitly guaranteed" (§6.3). READ (LIT-W2 §E2). Our re-execution admission puts the
  determinism obligation on the *machine* (provable in Lean) rather than on user code — the stronger position.

## 4. Questions for GPT-6

- **Q7-1.** Is "admit by byte-identical front-end re-run + deterministic re-execution" a sound basis for a
  multi-party ledger when the front end itself is trusted and unverified against a surface semantics
  (LT3)? Concretely: what does a receiver actually guarantee a *source author* today, and what would LT3 add?
- **Q7-2.** Fees on declared envelopes: type-checking fuel is priced, elaboration is not (as read). Is there
  a package engineered to be cheap to execute and expensive to *elaborate* within the policy's source-size
  bound (C4 on a wide DAG, template instantiation blow-up — MODULAR-TYPING D1 admits "code grows with the
  number of distinct instances")? Should elaboration be a metered lane with a theorem bounding it by
  declared fuel?
- **Q7-3.** What determinism obligations does call-by-need impose that call-by-name would not (heap
  addresses in checkpoints, GC order), and are they all covered by `admitted_data_unique` + the checkpoint
  codec, or is there a nondeterminism channel through checkpoint *bytes* (topic 04)?
