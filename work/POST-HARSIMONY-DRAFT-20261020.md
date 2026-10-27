# Welcome post for Sam Harsimony: draft section

> Note for Ember: this was written WITHOUT Sam's recent thread (it wasn't given to the drafting agent). The prompts in part 2 are deliberately general; tune them once you've reread his thread.

Before posting, check two things: (a) which of the github repos named below are actually public (only degg-research's URL came from you; the others are local `origin` remotes and their visibility wasn't checked), and (b) the nano contextual-holes work. It's on the hbox nanodregg main, but the Mac checkout at `704af55` doesn't have those commits yet, so links to those files may 404 for a reader until it's pushed.

---

## 1. Paste-able section (~800 words)

welcome sam! here's a longer map of what i've been doing, since you'll see bits of it all over the delve.

the short version is one question: can a competitive swarm (people, firms, agents, all with their own interests) coordinate on real industrial problems without someone ending up in the middle holding all the information and all the power? i call the cryptographic half of that "dark coordination". the idea is that you don't need an arbitrary encrypted computer. you need a small set of exact relations that markets and operating plans are already made of: aggregation, a uniform-price crossing, physical feasibility, a canonical optimum, pro-rata allocation, conservation, net settlement, selective release. each one gets a precise leakage contract, and each one can be compiled to a clear, shielded, or dark backend (MPC, FHE, or a proof over public data) without changing what it means. "dark" has a strict definition in the repo. nobody learns anything past a declared leakage function and their own authorized output, under a named corruption model. threshold encryption with one decryptor isn't dark, and a design with a regulator master key isn't dark either. that second rule is the anti-oppression constraint, and it is the point of the whole thing.

what actually exists there is pretty small, and that's on purpose. there's a padded four-slot frequent batch auction with two independently written oracles (300 million enumerated batches, zero final divergences), a typed relation IR whose clear lowering agrees with both, an inclusion and abort model, a leakage lab, a settlement model, and a confidential energy-dispatch relation (three providers, three periods, two buses) that picks the true optimum and rejects a conserving but suboptimal plan. the dark backends deliberately refuse to run. nothing private is implemented yet. the next real step is a bakeoff of TFHE, BFV plus MPC, discrete CKKS and proof-carrying clear on identical vectors, with full trust and leakage ledgers next to the timings.

the other half is authority. if a swarm is going to coordinate, every actor needs to be able to delegate a narrow slice of power to someone else, revoke it, and later prove what happened. that's the capability platform i spent most of the year building, breadstuffs (the system is called dregg). everything is a cell: value, state, a capability tree, and append-only evidence. a turn is one authorized step, and a receipt binds the whole post-state. the through-line is macaroons and biscuits: a turn is the exercise of an attenuable proof-carrying token over owned state, and it leaves a receipt behind. the kernel is written and proved in lean, the circuits are emitted from lean, and the idea is that a light client holding one root can tell the history was authorized and conserved without re-executing it. it isn't running right now. it's waiting to be picked back up or composted into the next robigalia.

mini (minidregg) and nano (nanodregg) are side explorations next to it. mini is a programmable shared world for people and agents: lean owns semantics and admission, rust owns the physical boundary, and it has its own language, objective bend, which follows faré's account of objects as lazy open recursion over partial specifications. nano rebuilds mini from its spec rather than its code, as an object of study. it has a tiny verified kernel where one function admits every turn, and a follower re-derives each turn and refuses the log by name if the host lied. this week nano landed a contextual modal type theory with a "guarded contextual closure". a hole is a persistent place where a decision gets made, and it carries what it may depend on and the reason each alternative was set aside. when a fact is withdrawn, repair re-judges only what touched it and provably agrees with judging from scratch. that matters for dark coordination too. degg-research already has "guarded holes", late-filled positions whose whole transition shape and authority are fixed before the value arrives, which is how you keep a late fill from becoming a free option. and we want the same machinery for our own proofs, so a library can explain and repair its obligations through a redesign.

then the dragon's egg. the thesis behind dreggnet is that distributed capability infrastructure is climate infrastructure. copper is the binding constraint on electrification, and asteroid return is the escape valve. i sometimes call the asteroid we'll mine the dragon's egg. space industry needs exactly what this stack is shaped for: authority that works across light-minutes of latency, orthogonal persistence, live upgrade, structural multi-tenant isolation, and very little overhead. a mining consortium is a competitive swarm with a coordination problem, which brings us back to the start.

honest caveats: this is very early. the dark backends are refusals, not implementations. the shielded baseline still trusts its executor (out of 1,125 alternate published results we tried, 377 pass every modeled check). breadstuffs' own statement audit found several soundness results vacuous at the field we deploy on, and we keep that list in the open. none of it is deployed.

places to poke:

- https://github.com/emberian/degg-research : start at `docs/VERDICTS.md`, then `docs/RESEARCH_STANCE.md`, `docs/PRIVACY_MODES.md`, `docs/GUARDED_HOLES_DOSSIER.md`
- `degg-research/docs/research/CONFIDENTIAL_ENERGY_DISPATCH_RELATION.md` : the energy relation and its counterexamples
- `degg-research/docs/FHE_FRONTIER.md` : what we know about FHE and verifiable FHE costs
- https://emberian.github.io/zkml-research/ : the sibling program on verifiable ML inference (hash-based, no trusted setup)
- dregg/breadstuffs `docs/OVERVIEW.md` and `metatheory/CLAIMS.md` : what is proved and what isn't
- minidregg `docs/OBJECTIVE-BEND.md` : the language
- nanodregg `README.md` and `CHARTER.md` : the rebuild and its twelve laws; `Lang/Contextual/` for the holes

---

## 2. Things agents could talk about

1. What is the smallest exact relation in Sam's domain that a competitive group would actually want computed darkly, and what leakage function would its participants accept?
2. Where does the anti-oppression constraint (no master key, no omniscient operator) collide with real-world observability needs, and is there a named, thresholded, due-process modality both sides could live with?
3. MPC vs FHE vs proof-carrying-clear: for a given coordination problem, which trust model is honest, and what does each cost per participant per round?
4. Aborts and availability: when a participant withholds or goes offline mid-protocol, who pays, and can attribution be made cryptographic rather than social?
5. Attenuable capabilities as the coordination primitive: what would delegating a narrow, revocable, auditable slice of authority look like for the agents or institutions Sam thinks about?
6. Guarded holes and late information: how do you let a decision wait for a value without turning the wait into a free option, and does that generalize beyond markets?
7. High-latency coordination: what protocols survive minutes or hours of round-trip delay (the asteroid-mining case), and what does that rule out?
8. Verifiable computation as public good: should verifiable inference and verifiable coordination be enterprise features, or commons, and what would make them cheap enough to be the latter?

---

## 3. SOURCES

Tags: READ means read at source in this pass, INFERRED means it's my synthesis, and EMBER means it came from your own framing in the brief.

- Dark coordination is about swarms coordinating on industrial problems without centralizing dynamics. EMBER.
- "does not need an arbitrary encrypted virtual machine", plus the list of relations (aggregation, crossing, feasibility, optimization, allocation, conservation, net settlement, selective release). READ `/Users/ember/dev/degg-research/README.md`.
- The Clear/Shielded/Dark compile targets. READ `degg-research/README.md` (compiler picture), `docs/ARCHITECTURE.md` via `/Users/ember/dev/redregg/work/DEGG-RESEARCH-STATE-20261020.md`.
- The Dark definition, and the rule that one-decryptor threshold encryption isn't dark. READ `/Users/ember/dev/degg-research/AGENTS.md` (Privacy modes).
- The master-key / omniscient-operator anti-oppression constraint. READ `/Users/ember/dev/degg-research/docs/RESEARCH_STANCE.md`.
- "it is the point of the whole thing". INFERRED (my emphasis).
- The four-slot FBA, two oracles, 300,436,169 batches with zero final divergences. READ via DEGG-RESEARCH-STATE (cites `experiments/dark-fba-independent/README.md`). Not re-run.
- The IR clear lowering agreeing with both oracles (2,116,916 cases). READ via DEGG-RESEARCH-STATE (`experiments/relation-ir/README.md`).
- The inclusion/abort model, leakage lab, and settlement model exist. READ via DEGG-RESEARCH-STATE (`experiments/{inclusion-availability,leakage-lab,settlement-model}/README.md`); `ls experiments/` READ directly.
- Energy dispatch with 3 providers, 3 periods, 2 buses, optimum chosen, a conserving but suboptimal plan rejected (cost 56 vs 60). READ via DEGG-RESEARCH-STATE (`docs/VERDICTS.md` V11, `research/confidential-energy-dispatch/README.md`).
- The dark backends refuse and no private backend is implemented. READ `degg-research/README.md` ("Current truth"), DEGG-RESEARCH-STATE.
- The TFHE / BFV+MPC / discrete CKKS / proof-carrying-clear bakeoff as the next step. READ via DEGG-RESEARCH-STATE (`docs/ROADMAP.md` R4). Calling it "the next real step" is INFERRED.
- The shielded baseline trusts its executor, with 377 of 1,125 passing. READ via DEGG-RESEARCH-STATE (`docs/VERDICTS.md` V3).
- Breadstuffs' cell / capability / turn / receipt model, and the light client holding one root. READ `/Users/ember/dev/breadstuffs/docs/OVERVIEW.md`.
- The macaroons/biscuits through-line, "attenuable proof-carrying token ... leaving a receipt". READ (memory index header, `~/.claude/projects/-Users-ember-dev-breadstuffs/memory/MEMORY.md`).
- The kernel proved in Lean, with circuits emitted from Lean. READ `breadstuffs/docs/OVERVIEW.md` (CIRCUITS-FROM-PROOFS, `metatheory/Dregg2/`).
- "the system is called dregg". READ (OVERVIEW title "dregg / deos"; origin remote `github.com/emberian/dregg`). Public visibility NOT checked.
- Breadstuffs isn't running, waiting to be resumed or composted into the next robigalia. READ `/Users/ember/dev/nanodregg/README.md` ("Where this sits").
- Mini: a programmable shared world, Lean owns semantics and admission while Rust owns the physical boundary. READ `/Users/ember/dev/minidregg/README.md`.
- Objective Bend as Faré's lazy open recursion over partial specs. READ `/Users/ember/dev/minidregg/docs/OBJECTIVE-BEND.md`.
- Nano rebuilt from spec not code, an object of study, `World.admit` admitting every turn, the follower refusing by name. READ `/Users/ember/dev/nanodregg/README.md`.
- Nano landed CMTT plus the guarded contextual closure. READ `memory/project-nano-contextual-theory-landed.md` and `/Users/ember/dev/redregg/work/HOLES-FOR-PROOF-ENGINEERING-20261020.md` (which read the hbox nano main at `b5f880bc`). NOT in the Mac checkout (`704af55`); LANG-66..69 are not in its `decisions/lang.md`. The memory file is dated 10-22, which may be a typo; the brief says "today", 10-20.
- The "persistent place where a decision is made ..." wording. EMBER (your phrasing), consistent with READ HOLES memo (candidates retain supports and blockers; provenance is a support/blocker list).
- Repair re-judges only touched candidates and agrees with from-scratch. READ HOLES memo (`repair_agrees_from_scratch` under `Coherent`; `repair_rejudged_eq_touched`). Caveat from the memo: it isn't a complexity bound, and from-scratch agreement needs the `Coherent` premise.
- Guarded holes in degg-research: late-filled, shape and authority fixed before the value. READ `/Users/ember/dev/degg-research/docs/GUARDED_HOLES_DOSSIER.md` and DEGG-RESEARCH-STATE (`GUARDED_EVENT_FOUNDATIONS.md`).
- "how you keep a late fill from becoming a free option". INFERRED (the dossier frames it as when a hole becomes an event-contingent claim; the "free option" wording is mine).
- Using the same machinery for proof obligations through a redesign. READ HOLES memo (recommendation section, itself tagged INFERRED there).
- The Dragon's Egg, copper, asteroid return, and the space-industry requirements list. EMBER. I found no copy of the copper thesis in `/Users/ember/dev/DreggNet` or `DreggNet-pub` in this pass (a grep for "copper" came up empty there).
- A mining consortium as a competitive swarm. INFERRED.
- Breadstuffs' statement audit found soundness results vacuous at the deployed field. READ (memory index: STATEMENT AUDIT 07-27, Soundness Apex HUB "vacuous at BabyBear"). Underlying files not re-read.
- Nothing deployed. READ: nanodregg README ("no deployment exists"), minidregg OBJECTIVE-BEND ("deployed (nothing here is)"), degg-research AGENTS.md (no venue).
- zkml-research is verifiable ML, hash-based, no trusted setup, with a public website. READ `/Users/ember/dev/zkml-research/README.md`. (Its `docs/VERDICTS.md` is dated 08-13; the repo is mainly STARK/field/prover measurements plus "encrypted learning" reading paths. I didn't summarize its results in the post.)
- degg-research filings: deliberately left out of the post. DEGG-RESEARCH-STATE notes there's no submission receipt for the CFTC comment builds.
