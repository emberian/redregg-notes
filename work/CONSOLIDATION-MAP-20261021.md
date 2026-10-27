# CONSOLIDATION-MAP-20261021: folding nano's contextual program into one module per concept

Architect: Opus (read-only, launched by ROOT at real 10-21 on Ember's "maybe we need to spend some time refactoring and
restructuring and tidying up"). I wrote this file and nothing else. Tree read: nanodregg `origin/main` = **d7989d9**
(`lang!: deploy substituted contextual holes …`, P7 landed), extracted with `git archive` into my scratchpad
`/private/tmp/claude-501/-Users-ember-dev-breadstuffs/7c10f132-0e99-4487-aaaa-62ea34c9f1c0/scratchpad/cm/tip`. I also
read the unlanded PE1 worktree `hbox:/tank/dregg-build/nanodregg/wt/CX-PE1` (HEAD d7989d9 plus untracked files).
Nothing was built.

Every claim carries a tag:
- **READ** `<path[:line]>`: I read it.
- **MEASURED**: a script ran over the tree (`graph.py`, `disp.py`, `table.py` in the scratchpad `cm/`). It parses
  `^import` lines, counts lines, counts `theorem|lemma` declarations, and computes import closures from the
  `lean_exe` roots in `lakefile.lean`.
- **INFERRED**: my judgment. Disagree with these first.

The doctrine I hold the program to: `breadstuffs/CLAUDE.md` (greenfield; prefer deleting the old thing to keeping
both; never keep a no-op; say what you broke). CHARTER law 1 ("A second shape of an existing thing is a defect, not a
transition") and law 8 (small modules, split proofs) [READ `CHARTER.md`:44, :93]. The memory rule
`feedback-iterate-inside-the-substrate-not-beside-it.md`: a prototype beside the substrate is a twin.

---

## 0. Bottom line

1. **P7 changed the problem.** `Lang/Contextual` is no longer a leaf library. Since d7989d9 the Host executable
   closure (91 modules) contains five contextual modules: `Closure`, `Core`, `HoleDecl`, `LangCalculus`,
   `LangSubstitution` [MEASURED closure of `host` = `Host.Main`]. Two of them are there by accident.
   - `LangCalculus` bundles the deployed term operations (`fillRefs`, `usesVar`, `decEq`) with the theory instance
     `langData : CalculusData`. Its strengthening uses CMTT-core's `liftIdx`/`lowerIdx`. So the deployed host links
     the whole simply-typed CMTT core (393 lines) and the abstract closure (573 lines). That closure includes
     experiment 4's `Rule`/`lfpIter`/`countRun` [READ `Lang/Contextual/LangCalculus.lean`:8,15–17,589–601;
     `Closure.lean`:548–566].
   - The same coupling puts `Lang/Proofs/Contextual/Core.lean` (1,201 lines of CMTT metatheory) inside the proof
     closures of `Kernel/Proofs/InvokeWitness`, `Kernel/Proofs/Logic/History` and `Ledger/Proofs/EscrowRun`. The
     path is `LangRenaming`'s use of `upR_upR`/`upR_id` [MEASURED; READ `LangRenaming` uses: 22× `upR`, 6× `liftIdx`,
     5× `lowerIdx`]. **The first structural move is to cut that coupling. Deletion comes second.**
2. **The program is 92 modules, 17,389 lines, 908 theorems** [MEASURED]. The review counted 73 / 15,011 / ~700
   before P7. 24 modules are REACHED by a deployed object. 8 more are leaf theorems whose subject is deployed. **60
   are BESIDE**: nothing but other contextual modules imports them, and their subject is a toy or a second shape
   (§1).
3. **Law-1 twins inside the program, by name:**
   - two `provenance` definitions and two `provenance_iff` theorems. One is env-specialized, and its own tooth
     `ProvenanceTeeth.provenance_env_specialized` proves it wrong.
   - two `Outcome` types (`Closure.Outcome`, `RepairObjects.Outcome`).
   - at least six status/verdict types.
   - four "is this filling good" judges.
   - a fifth `CalculusData` instance *inside the journey*: `p8Data` (Ty := Bool, Tm := Nat × Bool). The journey's P8
     rows run `Contextual.judge`, `Trace` and `TransportKinds` over it, while the same rows invoke the real live ROM
     [READ `Lang/Journey.lean`:2206–2245, 2334–2366].
4. **Nothing connects the deployed live runtime to the closure's judge.** `selectHole`/`resolveHole`
   (`Lang/LiveHoles.lean`:66–134) speak in strings (`holeSupportMoved`, `holeDerivationMoved`, `holeGuardBlocked`).
   `Contextual.judge` speaks `Status`. The only bridge, `HoleBridge.hole_judgment_admission_bridge`, covers the
   *closed* fragment of `Std.hole` (`hctx : I.ctx = []`, `hhyps : I.hyps = []`) [READ
   `Lang/Proofs/Contextual/HoleBridge.lean`:113–123; MEASURED: `judge` appears in no Live*/Deployed*/Closed* proof
   module]. So the spine itself is still beside nano at the live boundary. The fold must either land that bridge or
   take the closure judge out of Lang (§7 R2).
5. **The fold, by default:**
   - delete 45 modules (6,075 lines, 359 theorems) in four pure-deletion landings;
   - rehome 19 deployed-subject modules out of `Contextual` into `Lang/` and `Lang/Proofs/` (17 proof modules into
     9, with statements byte-identical);
   - split three modules (`LangCalculus`, `Trace` ×2);
   - move the P6 certificate reader to `Census`;
   - put three questions to Ember (Protocol: 5 modules / 2,397 lines; the live bridge; the CMTT core: 5 modules /
     1,796 lines).

   End state: `Lang/Contextual` + `Lang/Proofs/Contextual` go from **92 modules to 12** (17 if the CMTT core stays),
   and the Host closure goes from **91 to 89** [MEASURED for the inputs; INFERRED for the end-state arithmetic].
   **No landed public theorem gains a hypothesis.** Every step deletes, moves (statement-identical, by census
   digest), or replaces one definition whose only consumers are deleted (§3).

---

## 1. THE INVENTORY

### 1.1 Who imports the program from outside it [MEASURED `grep ^import` over Lang Kernel Ledger Protocol Host Hosting Census Codec Emit Bench Ops]

| outside importer | imports | what for |
|---|---|---|
| `Lang/Check.lean`:18 | `Lang.Contextual.HoleDecl` | `abbrev HoleSignature := List (Contextual.HoleDecl (List Ty) Ty)` (:22) — **deployed** |
| `Lang/HoleROM.lean`:3, `Lang/HoleBudget.lean`:3 | `Lang.Contextual.LangCalculus` | `fillRefs`, `HoleDecl`; `HoleBudget` is itself in namespace `Nanodregg.Lang.Contextual` (:5) — **deployed** |
| `Lang/LiveHoles.lean` (via HoleBudget) | — | `open Contextual` (:10); `Term.usesVar`, `Term.renameVar (lowerIdx x)` (:73, :94) — **deployed** |
| `Lang/Program.lean`:216 | (via LiveHoles) | `Contextual.Term.nodes` inside `Package.preparationCost` — **deployed** |
| `Lang/StdHoleModel.lean`:4,63 | `Lang.Contextual.Trace` | only `Contextual.Trace.collect` (an 8-line list fold, `Trace.lean`:54–61) |
| `Lang/Journey.lean`:108–110 | `Trace`, `Provenance`, `TransportKinds` | only the P8 toy rows `p8Data…p8Available` and their checks (:2206–2245, :2334–2366) |
| `Lang/Journey/Certificate.lean`, `Census/{Certificate,CertificateData}.lean` | `Lang.Contextual.Certificate` | the P6 reader; exe `certificate-tests` (root `Lang.Journey.CertificateMain`) |
| `Lang/Proofs/StdHoleCoverage.lean`:3 | `Lang.Proofs.Contextual.Trace` | `collect` lemmas (:32) |
| `Lang/Proofs/Provenance.lean`:36–37 | `…Contextual.LiveInvoke`, `…ClosedDeployment` | `invoke_live_never_stuck`, `program_run_closed` |
| `Kernel/Proofs/InvokeWitness.lean`:38 | `…Contextual.ClosedLeaf` | `judgeOneContextual_leaf_closed`, `runMeasuredLive_leaf_closed` (:258, :318) |
| `Ledger/Proofs/EscrowRun.lean`:59–60 | `…ClosedLeaf`, `…LawReceiver` | `judgeContextual_mem`, `judgeOneContextual_leaf_closed`, `runMeasuredLive_leaf_closed` (:401–402) |
| `Kernel/Proofs/Logic/History.lean`:51 | `…Contextual.LawReceiver` | `judgeContextual_mem`, `judgeOneContextual_ok`, `judgeOneContextual_admits_relib`, `loadContextual_top` (:383–450) |
| `Census/Proofs/Certificate.lean` | `…Contextual.Certificate` | `read_faithful`, `accepted_reachable_definition` |
| Host, Hosting, Protocol, Codec, Emit, Bench, Ops, gates/*.py, gates/*.tsv | **nothing** | (MEASURED: no import; `grep Contextual gates/` empty) |

All of the Live/Closed/Law proof theorems that Kernel and Ledger consume are already in namespace `Nanodregg.Lang`,
not `Contextual` [READ `namespace` lines of ClosedLeaf, LawReceiver, LiveInvoke, ClosedDeployment, LiveHoles]. So
rehoming them changes **import lines only** in Kernel/Ledger.

### 1.2 Reach legend

- **REACHED·host**: in the import closure of the `host` exe (the deployed Host). The other deployed exes (`resident`,
  `hosting-*`, `ob`, `rows`) contain the same five, through `Lang.Check` [MEASURED].
- **REACHED·journey**: in `lang-journey`'s closure only.
- **REACHED·cert-exe**: in `certificate-tests`' closure.
- **REACHED·proof**: transitively imported by a non-contextual module (a Kernel/Ledger/Lang/Census proof).
- **LEAF·deployed subject**: imported by nothing, but its theorems are about a deployed object (the live loader,
  the ROM generator, Std.hole). A leaf theorem over a real object needs no importer.
- **BESIDE**: reached only by other contextual modules or by nothing, and its subject is a toy calculus, a private
  language, a second shape of a spine concept, or a paper's definitions restated.

Disposition column: DELETE / REHOME (move out of `Contextual` to `Lang/` or `Lang/Proofs/`, statements identical) /
SPLIT / KEEP (theory spine, stays in `Lang/Contextual`) / CENSUS (move to `Census/`) / RULING (§7, default DELETE).

`C/` = `Lang/Contextual/`, `P/` = `Lang/Proofs/Contextual/`. In the importer column, names before "within:" are
outside the program and names after it are inside.

### 1.3 The table: 92 modules [MEASURED lines, theorems, importers, reach; READ for "defines"]

| module | lines | thms | defines | imported by | reach | disposition |
|---|---:|---:|---|---|---|---|
| C/Acyclic | 65 | 0 | P12 rank-witnessed hole unrolling adapter: own Expr, Graph, Refusal | within: C/AcyclicExamples; P/Acyclic | BESIDE | DELETE |
| C/AcyclicExamples | 36 | 0 | P12 fixture graphs (chain, cycles, bad witness) | within: P/AcyclicExamples | BESIDE | DELETE |
| C/Boundary | 179 | 0 | P2 boundary declarations + private 4-constructor search Term (binary/linear/var/hole) | within: C/ModalBoundary; P/Boundary | BESIDE | DELETE |
| C/Certificate | 119 | 0 | P6 logic-certificate reader (Checker, Entry, Reader, Refusal) — tooling data, 'not nano admission' | Census.CertificateData; Lang.Journey.Certificate ‖ within: P/Certificate | REACHED·cert-exe | CENSUS |
| C/Closure | 573 | 0 | LANG-66 abstract CalculusData, World/Token/Edit, Iface, Status, Candidate, Slot, judge, provenance (env-specialized), ops, Session, Consumer, + experiment-4 Rule/lfpIter/countRun | within: C/Acyclic; C/Boundary; C/CoreCalculus; C/LangCalculus; C/NogoodGames; C/P1; C/Provenance; C/RepairObjects; C/Trace; C/Worlds; P/ClosureStatements | REACHED·host | KEEP |
| C/ContextMorphisms | 36 | 0 | P11b context-morphism values (Cave–Pientka) over CMTT Core | within: P/ContextMorphisms | BESIDE | DELETE |
| C/Core | 393 | 0 | LANG-66 simply-typed CMTT: Ty/Tm, renaming, substitution, msubst, checker; ALSO upR/liftIdx/lowerIdx used by deployed Lang | within: C/ContextMorphisms; C/CoreCalculus; C/LangCalculus; C/LangSubstitution; P/Typing | REACHED·host | KEEP |
| C/CoreCalculus | 34 | 0 | CMTT data as a CalculusData (cmttData, holeEnv) | within: C/ModalBoundary; C/TraceExamples; P/CoreInstance; P/ProvenanceTeeth; P/RepairExperiments | BESIDE | KEEP |
| C/Games | 36 | 0 | P11a provenance-game draws (OutsideReason, checkDraw) | within: C/NogoodGames; P/Games | BESIDE | DELETE |
| C/HoleDecl | 10 | 0 | shared HoleDecl structure (10 lines) — imported by Lang.Check | Lang.Check ‖ within: C/Closure | REACHED·host | REHOME |
| C/HoleModel | 47 | 0 | two-support/one-blocker fragment of langData for the Std.hole bridge | within: P/HoleBridge | BESIDE | KEEP |
| C/Interfaces | 21 | 0 | P11a interface-automata witnesses (sevenPeer, twiceReceiver) | within: P/Interfaces | BESIDE | DELETE |
| C/LangCalculus | 604 | 0 | deployed-term ops (Term.decEq, usesVar, usesRef, fillRefs, tyOf) + legacy ΔOf/holeBound + langData : CalculusData | Lang.HoleBudget; Lang.HoleROM ‖ within: C/HoleModel; P/LangRenaming | REACHED·host | SPLIT |
| C/LangSubstitution | 95 | 0 | capture-avoiding renameVar/substVar/substList over deployed Lang.Term | within: C/LangCalculus; P/LangSubstitution | REACHED·host | REHOME |
| C/Material | 101 | 0 | P11b finite ludics 'material' guards (own Verdict type) | within: P/Material | BESIDE | DELETE |
| C/ModalBoundary | 86 | 0 | P11b typed syntax-reading guards over CMTT (own Var/Code/Guard) | within: P/ModalBoundary | BESIDE | DELETE |
| C/NanoBridge | 66 | 0 | LANG-67 embedding of Hosting.Resident.Prog into Protocol.Prot | within: P/Protocol | BESIDE | RULING |
| C/NogoodGames | 58 | 0 | P11a completion games with nogood certificates | within: P/NogoodGames | BESIDE | DELETE |
| C/Nogoods | 76 | 0 | P9 RecordedClosure with nogood database (second judgment judgeRecorded) | within: P/Nogoods | BESIDE | DELETE |
| C/P1 | 155 | 0 | P1 finite interaction guards (own Design/Report/Handler, toy session) | within: C/Material; P/P1 | BESIDE | DELETE |
| C/P5 | 136 | 0 | P5 stand-alone finite-domain judge: LogicalStatus, Problem, Refutation, Formula, Machine, priceReceiver | within: C/Games; C/Interfaces; C/Nogoods; C/P1; P/P5 | BESIDE | DELETE |
| C/Protocol | 757 | 0 | LANG-67 open protocols: Prot, holes with polarity, linear tokens, Hist, View, interpret | within: C/NanoBridge; C/P5; P/ProtocolTyping | BESIDE | RULING |
| C/Provenance | 73 | 0 | P9 all-environment provenance (EnvLit, Monomial, label) — a second provenance beside Closure.provenance | Lang.Journey ‖ within: C/ProvenanceRepairs; P/Provenance | REACHED·journey | KEEP |
| C/ProvenanceRepairs | 40 | 0 | P9 reverse provenance: repair plans over RepairObjects | within: C/Nogoods; P/ProvenanceRepairs | BESIDE | DELETE |
| C/RepairChanges | 35 | 0 | P11b change structures (Cai et al.) over repair objects | within: P/RepairChanges | BESIDE | DELETE |
| C/RepairObjects | 188 | 0 | P4 first-class repairs + a SECOND Outcome type (sixth case 'transport'), Policy, Registry | within: C/ProvenanceRepairs; C/RepairChanges; C/TransportKinds; P/RepairObjects | REACHED·journey | DELETE |
| C/Trace | 130 | 0 | P10 per-candidate traces: Guard/Snapshot/Cached/refresh/early cutoff; collect (8 lines) used by StdHoleModel | Lang.Journey; Lang.StdHoleModel ‖ within: C/TraceExamples; P/Trace | REACHED·journey | SPLIT |
| C/TraceExamples | 43 | 0 | P10 CMTT trace sessions | within: P/TraceExamples | BESIDE | DELETE |
| C/TransportKinds | 48 | 0 | P11b translation validation vs internal transport (Claim, recheck) | Lang.Journey ‖ within: P/TransportKinds | REACHED·journey | DELETE |
| C/Worlds | 123 | 0 | P3 alternative worlds / stable-model rule programs (own Report) | within: P/Worlds | BESIDE | DELETE |
| P/Acyclic | 219 | 18 | P12 adapter soundness/completeness | within: P/AcyclicExamples | BESIDE | DELETE |
| P/AcyclicExamples | 68 | 13 | P12 decide-instances over fixture graphs | — | BESIDE | DELETE |
| P/Boundary | 272 | 29 | P2 lattice facts, reuse_* congruences, dependent_inhabitants_change_types (Fin 1/Fin 0) | within: P/ModalBoundary | BESIDE | DELETE |
| P/Certificate | 150 | 8 | P6 reader faithfulness; contexts_distinguish/checkers_distinguish (congrArg) | Census.Proofs.Certificate | REACHED·proof | CENSUS |
| P/ClosedDeployment | 188 | 11 | P7 closed specialization: live loader = closed loader when holes=[] (program_run_closed, runMeasuredLive_closed …) | Lang.Proofs.Provenance ‖ within: P/ClosedLeaf; P/LawMeaning | REACHED·proof | REHOME |
| P/ClosedLeaf | 68 | 4 | P7 leaf-closed forms consumed by Kernel/Ledger witnesses | Kernel.Proofs.InvokeWitness; Ledger.Proofs.EscrowRun | REACHED·proof | REHOME |
| P/ClosureStatements | 89 | 0 | CalculusLaws (Prop structure) + closure statements | within: P/CoreInstance; P/Judge; P/LangInstance | BESIDE | KEEP |
| P/ContextMorphisms | 79 | 9 | P11b morphism validity | within: P/P11bExperiments | BESIDE | DELETE |
| P/ContractTeeth | 87 | 9 | P7 counterexample teeth for the superseded fillRefs contracts | — | LEAF·deployed subject | REHOME |
| P/Core | 1201 | 101 | CMTT metatheory: substitution lemmas, subject reduction, checker sound+complete, *_toy instances | within: P/ContextMorphisms; P/CoreInstance; P/LangRenaming; P/ModalBoundary | REACHED·proof | KEEP |
| P/CoreInstance | 114 | 6 | cmttLaws : CalculusLaws cmttData …; bell_template_toy | — | BESIDE | KEEP |
| P/Deployed | 90 | 9 | P7 closed facts over the deployed contextual ROM generator (selected_uses_context …) | — | LEAF·deployed subject | REHOME |
| P/DeployedCycle | 31 | 3 | P7 grounded cycle compiled into a deployed filling (rfl/BigStep) | — | LEAF·deployed subject | REHOME |
| P/Experiments | 689 | 40 | ToyCalc (lit/var/hole/add) + toyLaws + the eight experiments by decide | — | BESIDE | DELETE |
| P/Games | 114 | 8 | P11a draw soundness | within: P/NogoodGames | BESIDE | DELETE |
| P/History | 142 | 8 | closure session invariants (consumer_boundary, session_preserves_*) | within: P/Experiments; P/RepairObjects | BESIDE | KEEP |
| P/HoleBridge | 236 | 11 | Std.hole (68e704d) judgment = Closure.judge on HoleModel — closed fragment (hctx=[], hhyps=[]) | — | LEAF·deployed subject | KEEP |
| P/HoleBudget | 168 | 16 | node-count bounds for renaming/substitution/fill (deployed HoleBudget) | within: P/LiveHoles | REACHED·proof | REHOME |
| P/Integration | 267 | 15 | P8 theorems over journey's toy p8Data + wrappers of Kernel/Ledger/Host facts | — | BESIDE | DELETE |
| P/Interfaces | 202 | 7 | P11a de Alfaro–Henzinger definitions restated | — | BESIDE | DELETE |
| P/Judge | 227 | 20 | judge_verified_iff/conflict_iff/frame, provenance_iff (env-specialized), reissue_never_reenables | within: P/Acyclic; P/Boundary; P/HoleBridge; P/Material; P/P1; P/Provenance; P/ProvenanceTeeth; P/Repair; P/Stability | BESIDE | KEEP |
| P/LangFilling | 212 | 13 | fillHoles_typed family: live filling typed in declaration context | within: P/HoleBudget; P/LangOccurrences | REACHED·proof | REHOME |
| P/LangInstance | 138 | 12 | langLaws : deployed Lang is a lawful CalculusData; ΔOf lemmas; lang_*_toy | within: P/ContractTeeth; P/HoleBridge | BESIDE | KEEP |
| P/LangOccurrences | 312 | 20 | hasType_declaresHole family; usesRef through renaming/substitution/fill | within: P/LangInstance | LEAF·deployed subject | REHOME |
| P/LangRenaming | 418 | 31 | renameVar algebra + typing (closed names byte-identical, _live generalizations) | within: P/LangSubstitution | REACHED·proof | REHOME |
| P/LangSubstitution | 142 | 13 | substVar/substList typing, capture teeth | within: P/LangFilling | REACHED·proof | REHOME |
| P/LawMeaning | 418 | 21 | Law* relational semantics of contextual law bodies (moved from Extract) | within: P/LawReceiver | REACHED·proof | REHOME |
| P/LawReceiver | 177 | 6 | judgeContextual_mem/ok/admits_relib, loadContextual_top — consumed by Kernel Logic/History + Ledger EscrowRun | Kernel.Proofs.Logic.History; Ledger.Proofs.EscrowRun ‖ within: P/LawReceiverTeeth | REACHED·proof | REHOME |
| P/LawReceiverTeeth | 107 | 7 | contextual law teeth (dormant/demanded hole) | — | LEAF·deployed subject | REHOME |
| P/LiveCost | 102 | 8 | preparation-cost bounds for instantiateHoles | — | LEAF·deployed subject | REHOME |
| P/LiveHoles | 274 | 14 | selectHole_origin, holeRow_authenticated, instantiateHoles_typed, loadLive_* invariants | within: P/ClosedDeployment; P/Deployed; P/LiveCost; P/LiveInvoke | REACHED·proof | REHOME |
| P/LiveInvoke | 49 | 2 | method_live_run_sound, invoke_live_never_stuck — consumed by Lang/Proofs/Provenance | Lang.Proofs.Provenance | REACHED·proof | REHOME |
| P/LiveNeed | 80 | 4 | requiredOfLive_* need bounds for runMeasuredLive | — | LEAF·deployed subject | REHOME |
| P/Material | 101 | 9 | P11b material guard facts | within: P/P11bExperiments | BESIDE | DELETE |
| P/ModalBoundary | 66 | 8 | P11b extensional/intensional boundary facts | within: P/P11bExperiments | BESIDE | DELETE |
| P/Negotiation | 474 | 36 | LANG-67 two-cell one-use negotiation over Protocol (36 thms) | within: P/Integration | BESIDE | RULING |
| P/NogoodGameBridge | 42 | 2 | P11a/P9 bridge between two toys | — | BESIDE | DELETE |
| P/NogoodGames | 136 | 11 | P11a certificate soundness | within: P/NogoodGameBridge | BESIDE | DELETE |
| P/Nogoods | 105 | 9 | P9 nogood database soundness | within: P/NogoodGameBridge; P/ProvenanceExperiments | BESIDE | DELETE |
| P/Operations | 227 | 13 | closure ops ok/grows lemmas | within: P/Soundness | BESIDE | KEEP |
| P/Outcomes | 258 | 12 | five-outcome soundness (alternative/replacement/strengthening/suspended) | within: P/Soundness | BESIDE | KEEP |
| P/P1 | 201 | 22 | P1 interaction-guard facts | — | BESIDE | DELETE |
| P/P11bExperiments | 127 | 9 | P11b decide sessions | — | BESIDE | DELETE |
| P/P5 | 255 | 23 | P5 judge facts incl. refuted_ne_outside (no-confusion), not_unfilled_suspends (unfold) | within: P/Interfaces; P/NogoodGames; P/P1 | BESIDE | DELETE |
| P/Protocol | 968 | 65 | LANG-67 metatheory (65 thms) + nano_runs_iff/nano_interp_agrees/nano_interp_runs | within: P/Negotiation; P/P5 | BESIDE | RULING |
| P/ProtocolTyping | 132 | 0 | HasProt typing relation (Prop defs) | within: P/Protocol | BESIDE | RULING |
| P/Provenance | 197 | 15 | P9 all-env provenance_iff, minimality | within: P/Integration; P/ProvenanceRepairs | BESIDE | KEEP |
| P/ProvenanceExperiments | 111 | 13 | P9 decide sessions | — | BESIDE | DELETE |
| P/ProvenanceRepairs | 189 | 14 | P9 repair-plan soundness/minimality | within: P/Nogoods | BESIDE | DELETE |
| P/ProvenanceTeeth | 20 | 1 | tooth: Closure.provenance is env-specialized (proves the twin is wrong) | within: P/ProvenanceExperiments | BESIDE | DELETE |
| P/Repair | 252 | 16 | repair_agrees_from_scratch, locality, repair_rejudged_eq_touched | within: P/Operations; P/Outcomes | BESIDE | KEEP |
| P/RepairChanges | 84 | 10 | P11b change laws | within: P/P11bExperiments | BESIDE | DELETE |
| P/RepairExperiments | 200 | 10 | P4 decide sessions | — | BESIDE | DELETE |
| P/RepairObjects | 331 | 23 | P4 repair-object soundness | within: P/RepairChanges; P/RepairExperiments; P/TransportKinds | BESIDE | DELETE |
| P/Soundness | 325 | 14 | conditional_soundness, *_wellFilled preservation | within: P/History | BESIDE | KEEP |
| P/Stability | 86 | 6 | valueGuard/stability class, lfpIter_sound (experiment 4) | within: P/Experiments; P/TransportKinds; P/Worlds | BESIDE | DELETE |
| P/Trace | 306 | 20 | P10 collect_sound/total/missing (used by StdHoleCoverage) + cache/early-cutoff facts | Lang.Proofs.StdHoleCoverage ‖ within: P/Integration; P/TraceExamples | REACHED·proof | SPLIT |
| P/TraceExamples | 87 | 14 | P10 decide sessions over CMTT | — | BESIDE | DELETE |
| P/TransportKinds | 114 | 9 | P11b recheck soundness | within: P/Integration; P/P11bExperiments | BESIDE | DELETE |
| P/Typing | 54 | 1 | CMTT HasTy/HasSubst/Step inductives | within: P/Core; P/CoreInstance | REACHED·proof | KEEP |
| P/Worlds | 326 | 21 | P3 stable-world facts | within: P/WorldsField | BESIDE | DELETE |
| P/WorldsField | 122 | 6 | P3 stable = labelling correspondences | — | BESIDE | DELETE |

Totals [MEASURED]:

| disposition | modules | lines | theorems |
|---|---:|---:|---:|
| DELETE | 45 (18 def + 27 proof) | 6,075 | 359 |
| RULING (Protocol, default delete) | 5 | 2,397 | 101 |
| REHOME (deployed subject) | 19 (2 def + 17 proof) | 3,028 | 191 |
| SPLIT (`LangCalculus`, `Trace` def+proof) | 3 | 1,040 | 20 |
| KEEP (spine theory, includes CMTT core) | 18 | 4,580 | 229 |
| CENSUS (P6 certificate reader) | 2 | 269 | 8 |
| **all** | **92** | **17,389** | **908** |

Lang grew from 71 files (744d00c) to 193 at d7989d9 [MEASURED `find Lang -name '*.lean'`].

### 1.4 The unlanded PE1 journal (hbox `wt/CX-PE1`, untracked) [READ; MEASURED `wc -l`]

| file | lines | thms | defines | imports | reach if landed | disposition |
|---|---:|---:|---|---|---|---|
| `Census/JournalExpr.lean` | 136 | 0 | shared-DAG export of elaborated declarations (types, proof values, axioms, premise applications) | `Lean` | tooling | LAND (§6) |
| `Census/Journal.lean` | 204 | 0 | the obligation journal exporter over the census | `Census.JournalExpr`, `Census.Statements` | tooling | LAND (§6) |
| `Census/JournalRun.lean` | 94 | 0 | `#journal_judge` (runs `Closure.judge` on receipts), `#journal_worlds` (runs P3's `Worlds` toy) | `Census.Journal`, `Lang.Contextual.Journal`, **`Lang.Contextual.Worlds`** | tooling | SPLIT: keep the judge command re-homed on plain receipt data; delete `#journal_worlds` |
| `Lang/Contextual/Journal.lean` | 99 | 0 | **a fourth `CalculusData` instance**: `Ty := Revision`, `Tm := Receipt`, `check := receiptCheck`, `uses := false`, `drop/strengthen/weaken := id` | `Closure`, `Protocol` | BESIDE | DO NOT LAND in Lang; the receipt structure moves to Census |
| `Lang/Proofs/Contextual/Journal.lean` | 118 | 11 | `admitted_receipt`, `exhausted_unavailable`, `repair_composes`, … over that instance | `Judge`, `Protocol` | BESIDE | DO NOT LAND as is (§6) |
| `Lang/Proofs/Contextual/JournalTeeth.lean` | 37 | 10 | `*_tooth` over the receipt instance | | BESIDE | as above |
| `gates/journal*.py` (6 files) | 1,124 | — | pilot, plants, compose, finish, coverage plants | | tooling | LAND with the exporter |

`Kernel/Proofs/Journal.lean` and `Kernel/Proofs/JournalHead.lean` on main are KERNEL's journal (the World's
replay journal), not PE1. My glob caught them, and they are out of scope [READ importers: Host/Protocol/Codec
proofs].

### 1.5 Structural findings the table does not show

- **F1 · the deployed host links theory.** `Lang.HoleROM`/`Lang.HoleBudget` → `LangCalculus` → `Core` + `Closure`
  [MEASURED]. What the deployed code actually uses from them:
  - `CalculusData` (only as `langData`'s type);
  - `liftIdx`/`lowerIdx`, two one-line `if`s, `Core.lean`:357–360;
  - `upR`, 3 lines, `Core.lean`:72–74.

  Everything else in those 966 lines is dead weight in the Host closure, including experiment 4's `Rule`,
  `lfpIter`, `supportCount`, `countRun` (`Closure.lean`:546–566). [READ]
- **F2 · a no-op in the deployed path.** `ΔOf` ("Legacy name-indexed type projection retained for its lookup API",
  `LangCalculus.lean`:580–587) and `holeBound` have no caller outside `LangInstance`'s own `ΔOf_getElem?`,
  `ΔOf_nil`, `lt_holeBound` [MEASURED `grep ΔOf`]. CLAUDE.md: "Never keep a no-op for compatibility."
- **F3 · twins inside the program.**
  - `Contextual.provenance` (`Closure.lean`:236, specialized to one `env`) and `Contextual.P9.provenance`
    (`Provenance.lean`:42, all-env).
  - `Contextual.provenance_iff` (`Judge.lean`:112) and `Contextual.P9.provenance_iff` (`Provenance.lean`:18).
  - `ProvenanceTeeth.provenance_env_specialized` is a theorem that the first one loses answers.
  - `Closure.Outcome` (:179) and `RepairObjects.Outcome` (:37, "the old five outcomes embed unchanged; transport
    adds the sixth case").
  - Status/verdict types: `Closure.Status`, `P5.LogicalStatus`, `Material.Verdict`, `Worlds.Report`, `P1.Report`,
    `Games.OutsideReason`.
  - Judges: `Contextual.judge`, `P5.judge`, `NogoodGames.judge`, `Nogoods.judgeRecorded`, `P1.judgeAt`,
    `Games.judgeDraw`, plus the deployed `Std.hole` judgment and the live `selectHole`. [READ `grep ^inductive|^def judge`]
- **F4 · the journey's toy calculus.** `Lang/Journey.lean`:2206 defines `p8Data : Contextual.CalculusData` with
  `msubst _ t := t`, `uses _ _ := false`, `strengthen _ t := t`. That is an identity calculus. The P8 rows then
  report "trace rejudged", "live provenance", "conflict guardFails" and "checked representation false → true"
  computed on it. Meanwhile the same session invokes the real contextual ROM (`chooseCode`, :2328–2331). So the
  P8 rows are half real and half mirror. [READ]
- **F5 · no live bridge** (§0 item 4). `langLaws` (`LangInstance`) makes `langData` lawful. It has no consumer
  except `HoleBridge` and `ContractTeeth` [MEASURED importers of `P/LangInstance` = 2], and no theorem relates a
  `HoleResolution` to a `Status`.
- **F6 · deployed code in the `Contextual` namespace.** `Lang/HoleBudget.lean` is `namespace
  Nanodregg.Lang.Contextual` (:5). `Lang/Program.lean`:216 calls `Contextual.Term.nodes`. `Lang/LiveHoles.lean`:10
  opens `Contextual`. [READ] The namespace says "theory" over code the Host runs.
- **F7 · P7's conformance debts landed as-is** (review M5). They are still there at d7989d9:
  - formatted-string refusals: `throw s!"holeType {h.name}"`, `"holeSignatureBound"`, `"holeGuardBlocked …"`
    (`LiveHoles.lean`:15–33, :86–108);
  - inline bounds: `≤ 64`, `≤ 16`, fuel `256`, `256 * rs.length` (:17, :29, :83, :163);
  - the preparation charge written twice (`LiveHoles.lean`:163 and `Program.lean`:212–216);
  - `(Ω : HoleSignature := [])` defaults on `inferE`, `inferFields`, `inferArms`, `inferSubst`, `infer`, `checkE`,
    `check` (`Check.lean`:90–234).

  [READ]
- **F8 · decision ids.**
  - `decisions/lang.md` has two `## LANG-72` headings (:3035 P2, :3120 P3), then LANG-73 (:3208), then LANG-70
    (:3287). There is no LANG-71.
  - Ten card-named ids follow: LANG-P10, P12, P11b, P9, P11a, P6, P8, ACT, P13, and two LANG-P7 entries (:4449,
    :4512).

  [READ `grep '^## ' decisions/lang.md`]

---

## 2. THE TARGET STRUCTURE: one module per concept

Principle [INFERRED, from law 1 and the substrate rule]. A module stays in Lang only if:
- (a) a deployed object reaches it; or
- (b) its theorems are about a deployed object; or
- (c) it is the abstract spine (calculus laws, closure, judge, provenance, repair, soundness) and the deployed
  language is a proved instance of it.

Everything whose subject is a toy, a private language, or a paper's definitions restated is deleted. Git keeps the
history, and the docstrings' literature lineage stays readable at d7989d9.

**I disagree with the review on one point.** The review proposed a `Research` lean_lib (B4 P9) and a status type
"extended with P5's `refuted`/`outside` and P1's `partial`" (§A2). Both keep the toy vocabularies alive. Under the
substrate rule a research library inside the product repo is the same twin with a different lakefile line, and no
deployed object needs `refuted`/`outside`/`partial`. One status type is reached by deleting the others, not by
merging them in. [INFERRED]

### 2.1 Final module list

**Deployed language (`Lang/`, in the Host closure)**: three modules, replacing four contextual ones

| module | absorbs | content |
|---|---|---|
| `Lang/Index.lean` (new, ~15 lines, no imports) | `upR`, `liftIdx`, `lowerIdx` out of `C/Core` | the de Bruijn index maps both calculi use. CMTT (if kept) imports it, and so does Lang. One of each. |
| `Lang/Subst.lean` | `C/LangSubstitution` (95) + the term half of `C/LangCalculus` (`Term.decEq*`, `usesVar*`, `usesRef*`, `fillRefs*`, `tyOf`) + `Term.nodes` from `Lang/HoleBudget` | the deployed term operations. Namespace `Nanodregg.Lang`. **Deletes** `ΔOf`, `holeBound` (F2). |
| `Lang/HoleDecl.lean` | `C/HoleDecl` (10) | the shared declaration. `Lang.Check` imports it. |

`Lang/HoleBudget.lean`, `HoleROM.lean`, `HoleWire.lean`, `LiveHoles.lean`, `Program.lean` and `StdContextualHole.lean`
keep their files. They change their imports and leave namespace `Contextual`. Host closure: −`Core`, −`Closure`,
−`LangCalculus`, `LangSubstitution`→`Subst`, `HoleDecl` moved, +`Index` = **91 → 89** [INFERRED arithmetic].

**Deployed-subject proofs (`Lang/Proofs/`)**: 17 modules become 9, plus one new

| module | absorbs | key theorems (consumer) |
|---|---|---|
| `Lang/Proofs/Index.lean` (new) | `upR_upR`, `upR_id` and the `liftIdx`/`lowerIdx` facts out of `P/Core` | consumed by `Subst` and (if kept) CMTT |
| `Lang/Proofs/Subst.lean` | `P/LangRenaming` (418) + `P/LangSubstitution` (142) | `hasType_renameVar(_live)`, `hasType_unshiftAt(_live)`, `substList_typed`, `substList_*_capture` → the deployed `factorHole`/`Term.renameVar (lowerIdx x)` in `selectHole` (`LiveHoles.lean`:94, :113) |
| `Lang/Proofs/Fill.lean` | `P/LangFilling` (212) + `P/LangOccurrences` (312) | `fillHoles_typed`, `fillHolesFields_typed`, `fillHolesArms_typed`, `hasType_declaresHole` family → `instantiateHoles_typed` |
| `Lang/Proofs/HoleBudget.lean` | `P/HoleBudget` (168) | `fillRefs_nodes`, `substList_nodes`, `fillBounded_bounds` → `instantiateHoles_cost` |
| `Lang/Proofs/LiveHoles.lean` | `P/LiveHoles` (274) + `P/LiveCost` (102) + `P/LiveNeed` (80) + `P/LiveInvoke` (49) | `selectHole_origin`, `holeRow_authenticated`, `instantiateHoles_typed`, `loadLive_checked`, `instantiateHoles_cost`, `requiredOfLive_spec`, `invoke_live_never_stuck` → `Lang/Proofs/Provenance.lean` |
| `Lang/Proofs/LiveClosed.lean` | `P/ClosedDeployment` (188) + `P/ClosedLeaf` (68) | `program_run_closed` → `Lang/Proofs/Provenance.lean`; `judgeOneContextual_leaf_closed`, `runMeasuredLive_leaf_closed` → `Kernel/Proofs/InvokeWitness.lean`:258,318, `Ledger/Proofs/EscrowRun.lean`:402 |
| `Lang/Proofs/LawMeaning.lean` | `P/LawMeaning` (418) | `law_bigStep_back`, `lawTerm_fill` → LawReceiver |
| `Lang/Proofs/LawReceiver.lean` | `P/LawReceiver` (177) | `judgeContextual_mem`, `judgeOneContextual_ok`, `judgeOneContextual_admits_relib`, `loadContextual_top` → `Kernel/Proofs/Logic/History.lean`:383–450, `Ledger/Proofs/EscrowRun.lean`:401 |
| `Lang/Proofs/LiveTeeth.lean` | `P/ContractTeeth` (87) + `P/LawReceiverTeeth` (107) | the counterexample teeth of the superseded `fillRefs_*` contracts and the dormant/demanded-hole law teeth (leaf; subject: the deployed checker and loader) |
| `Lang/Proofs/LiveJourney.lean` | `P/Deployed` (90) + `P/DeployedCycle` (31) | `generated_signature`, `linked_signature`, `used_hypothesis_suspends`, `deployed_cycle_*` (leaf; subject: `Std.contextualHole`, the ROM generator the signed journey installs) |

**Spine theory (`Lang/Contextual/`, not in any exe closure)**: 2 def + 10 proof modules (+1 if R2 lands the bridge)

| module | absorbs | keeps | consumer / why it stays |
|---|---|---|---|
| `C/Closure.lean` | `C/Provenance` (73, P9) | `CalculusData`, `World`, `Token`, `Edit`, `Iface`, `Status`, `Candidate`, `Slot`, `Closure`, `judge`, **the all-env `provenance`** (P9's, replacing the env-specialized one), ops, `Session`, `Consumer` | the one closure. **Deletes** `Rule`, `lfpIter`, `supportCount`, `countRun` (experiment 4) and the old `provenance`. |
| `C/LangInstance.lean` | `langData` (the tail of `C/LangCalculus`) + `C/HoleModel` (47) | `langData : CalculusData` over `Lang.Subst`'s operations; the Std.hole fragment | the deployed language as an instance |
| `P/ClosureStatements.lean` | — | `CalculusLaws` (Prop structure with the anchors `weaken_avoids`, `uses_var`) | the laws every instance proves |
| `P/Judge.lean` | — | `judge_verified_iff`, `judge_conflict_iff`, `judge_frame`, `judge_pruned`, `reissue_never_reenables`, `withdraw_never_refutes`, `hyp_var_cites`, `drop_removes`. **Deletes** the env-specialized `provenance_iff`. | used by HoleBridge, Repair, Provenance |
| `P/Provenance.lean` | — | `provenance_iff` (renamed from `P9.provenance_iff`; statement unchanged), `minimal_*`, `label_iff` | the label of why a hole is available |
| `P/Repair.lean`, `P/Operations.lean`, `P/Outcomes.lean`, `P/Soundness.lean`, `P/History.lean` | — (LANG-69's split by responsibility is right; keep it) | `repair_agrees_from_scratch`, `locality`, `repair_rejudged_eq_touched`; `*_ok`/`*_grows`; the five outcomes (`alternative_sound`, `replacement_sound`, `strengthening_sound`, `suspended_sound`); `conditional_soundness`, `op_preserves_wellFilled`; `consumer_boundary`, `session_preserves_*` | the closure's metatheory |
| `P/LangInstance.lean` | — | `langLaws`, `langHasTy_*`. **Deletes** `ΔOf_getElem?`, `ΔOf_nil`, `lt_holeBound`. | the deployed language is lawful |
| `P/HoleBridge.lean` | — | `hole_judgment_admission_bridge`, `holeAdmission_judge_iff`, `hole_select_iff`, `hole_fill_iff` | subject: the deployed `Std.hole` generator (68e704d), closed fragment |
| `P/LiveBridge.lean` (R2, new) | — | `selectHole … = .ok s ↔ judge (romIface h) (rowWorld rv self) (romCandidate h s.index) = .verified` with the strengthening outcome, and each named refusal ↦ a `Status` | **the condition for keeping `judge` in Lang** (§7 R2) |

**CMTT core** (R3, default DELETE after R2): `C/Core`, `C/CoreCalculus`, `P/Core`, `P/Typing`, `P/CoreInstance`
(5 modules, 1,796 lines, 108 theorems). If kept, it stays under `Lang/Contextual/` as the reference model. It
imports `Lang.Index`, and no deployed module imports it.

**Census**: `Census/CertificateReader.lean` + `Census/Proofs/CertificateReader.lean` (from `C/Certificate`,
`P/Certificate`). Its own docstring says it is "a data/reader interface, not nano admission" [READ
`Certificate.lean`:3–7]. Census already holds its only consumers, and `certificate-tests` moves with it.

**End count** [INFERRED from the table]:
- Contextual dirs: 92 → 12 (or 13 with the live bridge, 17–18 with the CMTT core).
- Lang/Proofs: +10.
- Lang: +3 / −0 net files moved.
- Census: +2.

### 2.2 What is DELETED, by name, with the reason

Group **D-TOY**: experiments as `decide` over a toy, superseded by the deployed experiments (P7 put "all eight
experiments" on the live ROM: `P/Deployed`, `P/DeployedCycle`, `Lang/Journey/Contextual*`).
- `P/Experiments` (689 lines, 40 thms): `ToyCalc` (`lit/var/hole/add`) and `toyLaws`, plus
  `withdraw_one_of_two_supports`, `withdraw_last_support`, `withdraw_pruning_reason`, `cycle_loses_grounding`,
  `counting_keeps_cycle`, `dependent_context_change`, `replace_filling_preserving_contract`,
  `correct_but_cost_lost`, `reapply_earlier_filling`, … Every one is `decide` on a toy session next to the general
  theorem it instances [READ docstring :1–25]. The general theorems stay in Judge/Outcomes/History.
- `P/ProvenanceExperiments`, `P/RepairExperiments`, `P/P11bExperiments`, `P/TraceExamples` + `C/TraceExamples`,
  `P/AcyclicExamples` + `C/AcyclicExamples`: decide-sessions of the same kind.

Group **D-JUDGE**: second, third and fourth judges and their status types (law 1).
- `C/P5` + `P/P5`: `P5.judge`, `LogicalStatus`, `Problem`, `Refutation`, `Formula`, `Machine`, `priceReceiver`.
  Trivial deliverables: `refuted_ne_outside` (constructor no-confusion), `not_unfilled_suspends` and
  `negation_preserves_suspension` (`simp [evaluate]`) [review H2, READ P5 proofs :57–68].
- `C/Games` + `P/Games`, `C/NogoodGames` + `P/NogoodGames`, `P/NogoodGameBridge`: game statuses over P5.
- `C/Nogoods` + `P/Nogoods`: `RecordedClosure`, `judgeRecorded`. This is a second judgment that "erasing
  toClosure loses" [READ docstring].
- `C/P1` + `P/P1`, `C/Material` + `P/Material`: interaction/material guards with their own `Report`/`Verdict`.
- `C/Interfaces` + `P/Interfaces`: de Alfaro–Henzinger Definition 14 restated (`refines_iff_definition14`).

Group **D-PRIVATE**: private languages and second shapes of spine concepts.
- `C/Boundary` + `P/Boundary`: the four-constructor search `Term` (`binary/linear/var/hole`, "not an encoding of
  deployed Lang terms"). Trivial deliverables: `dependent_inhabitants_change_types : Nonempty (Fin 1) ∧ ¬ Nonempty
  (Fin 0)`; `Boundary.reuse_cost_bound` (adds `overhead` to both sides); `Boundary.reuse_cached_observation`
  (`congrArg`) [review H2].
- `C/ModalBoundary` + `P/ModalBoundary`: a third syntax (`Var`, `Code`, `Guard`) over CMTT.
- `C/RepairObjects` + `P/RepairObjects`: **the second `Outcome` type**, plus `Policy`, `Registry`, transport.
- `C/RepairChanges` + `P/RepairChanges`, `C/TransportKinds` + `P/TransportKinds`, `C/ContextMorphisms` +
  `P/ContextMorphisms`: P11b paper structures over the above.
- `C/ProvenanceRepairs` + `P/ProvenanceRepairs`: repair plans over `RepairObjects`.

Group **D-RULES**: a second rule semantics beside the closure.
- `C/Worlds` + `P/Worlds` + `P/WorldsField`: stable worlds ("not a second kernel World or an admission path",
  which is exactly what it is beside).
- `C/Acyclic` + `P/Acyclic`: the P12 adapter. `DeployedCycle` compiles a grounded cycle into a deployed filling,
  which is the substrate version.
- `P/Stability`: `lfpIter_sound`, `stability_class`; its consumers are Experiments, Worlds, TransportKinds.
- The `Rule`/`lfpIter`/`supportCount`/`countRun` definitions in `C/Closure`.

Group **D-WRAP**: card deliverables that wrap landed facts or the toy.
- `P/Integration` (267, 15 thms). Ten statements are over `p8Data`/`p8Iface`/`p8World`/`p8Registry` [READ :1–120].
- The other five restate landed Kernel/Ledger/Host facts at the journey's program:
  - `reexecute_committed_effect` is `submit_replayed hj`;
  - `one_use_consumption` is `grant_moves_le_cap` at cap 1;
  - `progress_under_ready_writer` is the four branches of `submit` read back (review H2, READ);
  - `commitment_binds_receipt` and `recovery_preserves_consumption`: same kind.

  The kernel path stays exercised by the journey rows themselves (commit, revoke, cancel through `Receive`).
- `Lang/Journey.lean`: `p8Data`, `p8Guard`, `p8Iface`, `p8Candidate`, `p8Swap`, `p8Correspondence`, `p8Registry`,
  `p8World`, `p8Available`, and the checks built on them in `p8Rows` (:2334–2366).

Group **D-TWIN**: the env-specialized provenance.
- `Contextual.provenance` (old def).
- `Contextual.provenance_iff` (`Judge.lean`:112).
- `P/ProvenanceTeeth` (its tooth; it has no subject once the twin is gone).

Group **D-NOOP**: `ΔOf`, `holeBound`, `ΔOf_getElem?`, `ΔOf_nil`, `lt_holeBound`.

Group **D-TRACE**: everything in `C/Trace` + `P/Trace` except `collect` and `collect_sound`/`collect_total`/
`collect_missing`. That is `Guard.install`, `Snapshot`, `Cached`, `seed`, `refresh`, `repair`, `dirtyReaders`,
`early_cutoff`, `refresh_consistent`, …. Reason: the live runtime selects "fresh on each invocation" [READ
`LiveHoles.lean`:97–99; d7989d9 message]. A cache-validity theory has no deployed subject. Its only consumers are
the p8 toy rows, Integration and TraceExamples. `collect` moves to `Lang/StdHoleModel.lean` (its one user) and the
three lemmas to `Lang/Proofs/StdHoleCoverage.lean`. [INFERRED; the review counted P10's trace as spine. Its
deployed half *is* kept, and the cache half is not reached.]

**Not deleted, on purpose:** the `_toy` theorems in `P/Core` (15), `P/CoreInstance` (2) and `P/LangInstance` (2).
They pair a positive and a refuting conjunct next to the general theorem they instance (e.g. `box_cannot_capture_toy`:
`∀ T, ¬ HasTy … (.box [] (.var 0)) T ∧ … HasTy … (.box [.base] (.var 0)) …`). They are teeth, not guards
[READ :636–895]. One conjunct is vacuous: `tm_decEq_toy`'s `Tm.mvar 3 [...] = Tm.mvar 3 [...]` (:894). Drop that
conjunct in S10.

### 2.3 What is KEPT as a genuine theorem over nano's real objects, and who consumes it

| theorem(s) | nano object | consumer today | after the fold |
|---|---|---|---|
| `judgeOneContextual_leaf_closed`, `runMeasuredLive_leaf_closed` | the live loader on closed leaves | `Kernel/Proofs/InvokeWitness.lean`:258,318; `Ledger/Proofs/EscrowRun.lean`:402 | `Lang/Proofs/LiveClosed` |
| `judgeContextual_mem`, `judgeOneContextual_ok`, `judgeOneContextual_admits_relib`, `loadContextual_top` | the contextual law receiver | `Kernel/Proofs/Logic/History.lean`:383–450; `EscrowRun`:401 | `Lang/Proofs/LawReceiver` |
| `program_run_closed`, `invoke_live_never_stuck`, `method_live_run_sound` | `Program.run`, live invoke | `Lang/Proofs/Provenance.lean` (`program_run_past_extraction`) | `LiveClosed`, `LiveHoles` |
| `selectHole_origin`, `holeRow_authenticated`, `blocked_has_no_receipt`, `resolveHole_refusal`, `instantiateHoles_typed`, `instantiateHoles_sources`, `instantiateHoles_cost`, `loadLive_checked` | `Lang.LiveHoles` (Host closure) | ClosedDeployment, LiveInvoke | `Lang/Proofs/LiveHoles` |
| `fillHoles_typed` (+Fields/Arms), `hasType_declaresHole` (+fields/arms), `substList_typed`, `hasType_renameVar(_live)` | `fillRefs`, `substList`, `renameVar` (deployed) | LiveHoles | `Fill`, `Subst` |
| `fillRefs_nodes` … `fillBounded_bounds` | `HoleBudget` | LiveCost | `Lang/Proofs/HoleBudget` |
| `collect_sound`, `collect_total`, `collect_missing` | `StdHoleModel`'s collector | `Lang/Proofs/StdHoleCoverage.lean`:32 | moved into StdHoleCoverage |
| `hole_judgment_admission_bridge` + 10 | `Std.hole` (deployed generator) | none (leaf) | `P/HoleBridge` |
| `generated_signature`, `linked_signature`, `selected_uses_context`, `used_hypothesis_suspends`, `deployed_cycle_*` | `Std.contextualHole` ROM | none (leaf) | `LiveJourney` |
| `langLaws` | `langData` over the deployed ops | HoleBridge, ContractTeeth | consumed by `LiveBridge` (R2) |
| `read_faithful`, `accepted_reachable_definition` | the census certificate | `Census/Proofs/Certificate.lean` | `Census/Proofs/CertificateReader` |
| `nano_runs_iff`, `nano_interp_agrees`, `nano_interp_runs` | `Hosting.Resident.Prog` | **none**; `nano_interp_runs` re-derives the landed `Hosting/Proofs/ResidentRun.lean`:700 `interp_runs` through the embedding | R1 |

The brief named "the kernel integration P8" as a keep candidate. It is not one: see D-WRAP. Every statement in it
either has a toy subject or restates a landed Kernel/Ledger/Host theorem. [READ; INFERRED]

---

## 3. THE PREMISE AND STATEMENT PRICE

### 3.1 Statements that disappear (by module; the full name lists are in `cm/thms.txt`)

| step | statements removed | why none of them is load-bearing |
|---|---|---|
| S1 | 151 (Experiments 40, P11bExperiments 9, ProvenanceExperiments 13, RepairExperiments 10, TraceExamples 14, AcyclicExamples 13, WorldsField 6, NogoodGameBridge 2, Interfaces 7, P1 22, Integration 15) | zero importers each [MEASURED] |
| S3 | 60 (P5 23, Games 8, NogoodGames 11, Nogoods 9, Material 9) | importers only inside the group after S1 [MEASURED] |
| S4 | 102 (Boundary 29, ModalBoundary 8, ContextMorphisms 9, RepairChanges 10, TransportKinds 9, RepairObjects 23, ProvenanceRepairs 14) | after S2 the journey no longer imports TransportKinds; no other outside importer [MEASURED] |
| S5 | 45 (Worlds 21, Acyclic 18, Stability 6) | as above |
| S6 | `ΔOf_getElem?`, `ΔOf_nil`, `lt_holeBound` | they are about the no-op only |
| S10 | `Contextual.provenance_iff` (env-specialized), `P9.provenance_env_specialized`; `tm_decEq_toy` loses a reflexive conjunct (a statement change; nothing consumes it) | the surviving `provenance_iff` has the same left side, and its right side quantifies over every env, so it is the stronger statement; `Closure.provenance`'s only other consumers are deleted [MEASURED grep] |
| S11 | 17 Trace theorems (`seed_valid`, `refresh_valid`, `refresh_consistent`, `repair_entries`, `from_scratch_consistency`, `repair_minimal`, `repair_once`, `early_cutoff`, `repair_valid`, `capture_sound`, `checkedJudge_sound`, `checkedJudge_total`, `changed_iff`, `tagged_filter`, `evaluate_observe`, `guard_reads_only`, `observation_complete`) | consumers only Integration (S1), TraceExamples (S1) and the p8 rows (S2) |
| R1 | 101 (Protocol 65, Negotiation 36) | consumers: P5 (S3), Integration (S1) |
| R3 | 108 (Core 101, Typing 1, CoreInstance 6) | consumers after S7: none |

### 3.2 Statements that move (names change, elaborated statements identical)

- **Namespace `Nanodregg.Lang.Contextual` → `Nanodregg.Lang`.** This covers every theorem in today's `P/LangRenaming`,
  `P/LangSubstitution`, `P/LangOccurrences`, `P/LangFilling`, `P/HoleBudget` and `P/ContractTeeth`, and every
  def in `C/LangSubstitution`, the term half of `C/LangCalculus`, and `Lang/HoleBudget.lean` [READ namespace lines].
  Consumers: only modules inside the rehome set, plus `Lang/Program.lean`:216 (`Contextual.Term.nodes` →
  `Term.nodes`) and `Lang/LiveHoles.lean`:10 (`open Contextual`).
- `upR_upR`, `upR_id` (+ index lemmas): `Nanodregg.Lang.Contextual` → `Nanodregg.Lang` (`Lang/Proofs/Index`).
- `Contextual.P9.provenance_iff` → `Contextual.provenance_iff`. The statement text is unchanged, and `P9.provenance` →
  `provenance`.
- `Contextual.Trace.collect` and its three lemmas → `Nanodregg.Lang.Std` (beside `StdHoleModel`). Consumers:
  `Lang/StdHoleModel.lean`:63 and `Lang/Proofs/StdHoleCoverage.lean`:32.
- `Contextual.Certificate.*` → `Census.CertificateReader.*`. Consumers: `Census/{Certificate,CertificateData}`,
  `Census/Proofs/Certificate`, `Lang/Journey/Certificate` (moves to Census), and the lakefile `certificate-tests` root.
- **Kernel/Ledger consumers change import lines only**: `Kernel/Proofs/InvokeWitness.lean`:38,
  `Kernel/Proofs/Logic/History.lean`:51, `Ledger/Proofs/EscrowRun.lean`:59–60 and `Lang/Proofs/Provenance.lean`:36–37.
  The theorems they use are already in `Nanodregg.Lang` [READ]. That makes each one a CROSS-LAYER line (KERNEL,
  LEDGER) with a one-line diff per file.

### 3.3 Statements that change: S9 (the P7 conformance card), and only there

- Removing the `(Ω : HoleSignature := [])` defaults (F7) changes the *source text* of every statement that writes
  `inferE Δ Γ t` or `check Δ t T`. It does not change their *elaborated* statements: the default already elaborates
  to `[]`. The gate is the census digest, not the text [INFERRED; this is exactly the review's B4 P6 option B].
  If the fix is "two named entry points" (`checkClosed := checkE · · · []`), the 13 closed checker theorems that
  P7 kept byte-identical keep their names and gain nothing.
- Refusal constructors (`HoleRefusal.supportMoved n i` for `s!"holeSupportMoved {n} {i}"`) change
  `used_hypothesis_suspends` (`P/Deployed`:83–86, `= .error "holeSupportMoved 0 1"`), `resolveHole_refusal`, and the
  journey string checks (`Lang/Journey/ContextualChecks.lean`:60–92 compare `"holeType 0"` etc.). The conclusions
  become constructor equalities, and no premise is added. This is a **change of meaning in the refusal type**
  (`Except String` → `Except HoleRefusal`), so it is a `lang!`. Re-emit: none on the wire if the refusal bytes are
  `HoleRefusal.name`, else the journey rows. Say it in the commit.

### 3.4 Consumers that must change (complete list) [MEASURED import grep + READ name uses]

- **Lang (deployed):** `Check.lean` (import), `HoleROM.lean`, `HoleBudget.lean`, `LiveHoles.lean`, `Program.lean`:216,
  `StdHoleModel.lean`, `StdContextualHole.lean` (transitively, through LiveHoles; import path only).
- **Lang (journey):** `Journey.lean` (imports :108–110; p8 rows :2206–2245, :2334–2366), `Journey/Certificate.lean`,
  `Journey/CertificateMain.lean`.
- **Lang (proofs):** `Proofs/Provenance.lean`:36–37, `Proofs/StdHoleCoverage.lean`:3,32.
- **Kernel:** `Proofs/InvokeWitness.lean`:38, `Proofs/Logic/History.lean`:51 (import lines).
- **Ledger:** `Proofs/EscrowRun.lean`:59–60 (import lines).
- **Census:** `Certificate.lean`, `CertificateData.lean`, `Proofs/Certificate.lean`.
- **lakefile:** `certificate-tests` root.
- **Records:** `SIZE.md` every step; `decisions/lang.md` every step.
- **Unaffected:** Host, Hosting, Protocol, Codec, Emit, Bench, Ops, `gates/*.tsv`, `rows/` [MEASURED: no import, no
  `Contextual` string]. No generated file, wire vector or codec table changes in S1–S8 and S10–S12.

**Journey rows that vanish in S2** (say them in the commit) [READ `Lang/Journey.lean`:2334–2366]:
- "trace rejudged …" (the trace half of the "P8.1 old signed plan after unrelated update" note);
- "live provenance …" (in the P8.2 withdraw note);
- "P8.2 re-pinned tombstone: conflict guardFails";
- "P8.2 mismatched live authority pin: conflict guardFails";
- "P8.3 checked representation false -> true; unknownCertificate refused".

The kernel halves (the plan is still admitted, the withdrawn instantiation is "rejected stale", the cancel) stay.
The `chosen` index that P8.3 took from the toy transport becomes the live ROM's own selection (`chooseCode r 1`),
which the session already invokes. The successor check is that the second provider's code is selected and the
commit admitted. That is a real ROM row instead of a mirror.

### 3.5 Confirmation: no public landed theorem gains a hypothesis

- S1, S3, S4, S5, S11, R1 and R3 only delete.
- S6, S7, S8 and S12 only move, by namespace and by file.
- S10 replaces a def. The old one's consumers are deleted in the same step, and the surviving `provenance_iff` is
  the stronger one.
- S9 changes the refusal type and drops a default. No `→` is added to any conclusion.

**The mechanical check, per step:** diff the census `statements.tsv` of main against the candidate, keyed by name,
under the step's declared rename map. The rows are names plus elaborated-statement digests, and
`Census/Statements.lean` already elaborates everything.
- Every surviving name's digest must be equal.
- Every vanished name must be in the step's declared deletion list.
- Every new name must be in the rename map's image, or be S13's bridge.

That replaces "PRICE PREMISES: none" prose with an artifact [INFERRED; the review's B4 P6 option B, applied to the
fold]. If the census statements export does not yet carry digests, adding them is S0's tooling item, and it is the
same export PE1's `Census/JournalExpr` already walks (§6).

---

## 4. THE ORDER

### 4.1 Dependency drawing

```
S0  ledger + IMPACT + statement review + decision-id erratum      (no Lean)
 │
 ├─ S1  DEL leaves (14 mods)  ── pure deletion, fast path
 │    │
 │    └─ S3  DEL P5/P1/games/nogoods/material (11)  ── pure deletion
 │
 ├─ S2  JOURNEY: drop p8 toy rows (consumer first)
 │    │
 │    └─ S4  DEL boundary/repair-objects/transport/morphisms/changes/prov-repairs (14)  ── pure deletion
 │         │
 │         └─ S5  DEL worlds/acyclic/stability (5)  ── pure deletion
 │
 ├─ S6  Lang/Index + Lang/Subst + Lang/HoleDecl  (deployed; Host closure 91→89; ΔOf deleted)
 │    │
 │    └─ S7  Lang/Proofs/{Index,Subst,Fill,HoleBudget}  (Kernel/Ledger proof closures lose CMTT)
 │         │
 │         └─ S8  Lang/Proofs/{LiveHoles,LiveClosed,LawMeaning,LawReceiver,LiveTeeth,LiveJourney}
 │              │      CROSS-LAYER: KERNEL, LEDGER (import lines)
 │              └─ S9  P7 conformance (refusal constructors, Bounds, one charge, named entry points)  lang!
 │
 ├─ S10 Closure tidy: P9 provenance replaces the twin; exp-4 Rule/lfpIter out   (after S5, S6)
 ├─ S11 Trace split: collect → StdHoleModel/StdHoleCoverage; rest deleted       (after S1, S2)
 ├─ S12 Certificate → Census                                                     (independent)
 │
 └─ S13 R2 LiveBridge (or take judge out of Lang)   (after S8, S9, S10)
      ├─ S14 R1 Protocol (default delete)           (after S3; independent of S13)
      └─ S15 R3 CMTT core (default delete)          (after S7, S13)
```

S1, S2, S6 and S12 have no predecessors and could start in any order. They are **sequential by method** (one Lang
worker at a time, §5), not by dependency.

### 4.2 Steps [lines/modules MEASURED for deletion groups; INFERRED estimates for edits]

| step | kind | modules removed | lines removed | theorems removed | judge path | notes |
|---|---|---:|---:|---:|---|---|
| S0 | records/tooling | 0 | 0 | 0 | — | rulings ledger rows; IMPACT.md for S1–S12; the census statement-digest diff; erratum for LANG-72×2/71/70 |
| **S1** | **pure deletion** | 14 | 2,216 | 151 | fast | Experiments, P11bExperiments, ProvenanceExperiments, RepairExperiments, TraceExamples×2, AcyclicExamples×2, WorldsField, NogoodGameBridge, Interfaces×2, P/P1, Integration |
| S2 | consumer edit | 0 | ~70 | 0 | fast (journey) | Journey p8 toy rows; drop 3 imports |
| **S3** | **pure deletion** | 11 | 1,273 | 60 | fast | P5×2, Games×2, NogoodGames×2, Nogoods×2, Material×2, C/P1 |
| **S4** | **pure deletion** | 14 | 1,747 | 102 | fast | Boundary, ModalBoundary, ContextMorphisms, RepairChanges, TransportKinds, RepairObjects, ProvenanceRepairs (def+proof each) |
| **S5** | **pure deletion** | 5 | 819 | 45 | fast | Worlds×2, Acyclic×2, Stability |
| S6 | move (deployed) | 2→3 (net +1) | ~15 (ΔOf/holeBound + lemmas) | 3 | fast (reached targets; Host rebuilds) | not `!`: no wire byte changes [INFERRED: Package/Term encodings untouched] |
| S7 | move (proofs) | 6→5 (net −1) | ~0 | 0 | fast | Kernel/Ledger proof closures drop `P/Core`, `P/Typing` |
| S8 | move (proofs) | 11→6 (net −5) | ~0 | 0 | fast; CROSS-LAYER | import lines in 4 foreign files |
| S9 | conformance | 0 | ~ +40/−40 | 0 | full (`lang!`) | the only statement-text change; journey checks compare constructors |
| S10 | spine edit | 3 (Provenance def merged, P/ProvenanceTeeth, Provenance proof stays) → net −2 | ~70 | 2 | fast | Closure.lean leaves the Host closure in S6, so this no longer rebuilds Host |
| S11 | split + delete | 2 | ~380 | 17 | fast | collect + 3 lemmas re-homed |
| S12 | move | 2→2 | 0 | 0 | fast | plus the `certificate-tests` root; the 12 MB golden is the GATES card from review H3, not this step |
| S13 | new theorem | +1 | — | +n | fast | R2 |
| S14 | deletion (R1) | 5 | 2,397 | 101 | fast | default |
| S15 | deletion (R3) | 5 | 1,796 + `Lang/Index` users rewired | 108 | fast | default after S13 |

**Pure deletion first:** S1 → S3 → (S2) → S4 → S5 removes **44 modules, 6,055 lines, 358 theorems** before any file
that survives is edited, except the journey [MEASURED sums]. The 45th deleted module is `P/ProvenanceTeeth`; it
goes with its twin in S10.

**Totals at the default rulings:**
- **removed:** ~57 modules deleted outright plus ~8 eliminated by merges (65 fewer modules tree-wide), ~10,700
  lines and ~590 theorems, of 92 modules / 17,389 lines / 908 theorems;
- **moved out of `Contextual`:** ~3,600 lines (deployed and deployed-subject);
- **left in `Lang/Contextual`:** ~2,800 lines of spine theory [INFERRED from the sums above].

Why this order:
- Deletions first because they are cheap, cannot change a surviving statement, and shrink every later step's
  build.
- S2 before S4 because the journey is S4's only outside consumer (consumers first, review B2(c)).
- S6–S8 before S10 so that the Closure edit no longer rebuilds the Host.
- S9 after S8 so the conformance card edits files in their final homes, once.
- S13 last among code because it is the only step that adds a theorem, and its statement is reviewed against the
  folded spine, not the pile.

---

## 5. THE METHOD (from REVIEW-20261021 Part B, applied to this fold)

1. **One Lang worker at a time.** No parallel Lang workers: every step touches `Lang/` and most touch the Journey or
   Closure. Parallel Lang lanes are how the day produced "a textually clean, semantically broken merge" (review B1.1).
   A worker that finishes a step continues with the next one (veterans back to the front). A fresh worker starts
   only past ~400K tokens, and from the predecessor's own continuation file.
2. **Before any build: IMPACT.md per step.** It is written by the worker and contains:
   - the definitions the step deletes or moves;
   - `grep -rln` of every one of those names across `Lang Kernel Ledger Host Hosting Protocol Census Codec Emit Bench
     Ops gates rows`;
   - reverse dependencies from the elaborated environment (census, or PE1's exporter, §6);
   - every gates table or fixture whose subject moves;
   - the step's **theorem list as statements**, each tagged with its nano object or marked DELETE with the group
     reason from §2.2.

   The P7 grep took one second and named all six foreign consumers (review A5). §3.4 above is that grep for the
   whole fold. Each step's IMPACT.md should reproduce its slice of it, measured again on the current tip.
3. **Pre-build statement review by a CROSS-FAMILY reader**: Claude when Codex builds, and the reverse. It reads
   IMPACT.md, not the diff, and is asked three questions per surviving or new theorem:
   1. "What nano object is this about?"
   2. "Which landed theorem or consumer would be weaker without it?"
   3. The disjunct check.

   "No answer to (1) and (2)" means DELETE, not "LAND". For the pure-deletion steps the question is inverted:
   "name any surviving module or row that is weaker after this deletion." The answer must be grounded in the census
   diff, not prose. Same-family reading is what let `Nonempty (Fin 1) ∧ ¬ Nonempty (Fin 0)` land (review H2, B3).
4. **A rulings ledger, mechanical.** `RULINGS.tsv` (id, time, target worker or `*`, kind ∈ {GRANT, RULE, HOLD,
   RELEASE}, scope paths, text path) in the coordination repo.
   - `scripts/commit` refuses while a HOLD applies, and refuses a CROSS-LAYER path no GRANT covers.
   - The worker writes `ACK <id>` in its report.
   - Seed rows for this fold:
     - GRANT KERNEL+LEDGER import-line edits for S8 (the four files of §3.2);
     - GRANT CENSUS for S12;
     - RULE "deletions in S1–S5 are authorized by path list". GATES-20b's stale-path guard refuses deliberate
       deletions; it refused 14 of 150 historical landings, each deliberate (review M6). Each deletion step's
       landing record must carry its path list as the explicit deletion authorization (the LANG-P7 precedent:
       "deletion authorization must be explicit in the machine-checked landing record") [READ d7989d9 decision tail];
     - HOLD on any new `Lang/Contextual/*` file that is not in §2.1 until the fold closes.
5. **No exit with an open ASK.** A worker whose last report line is `ASK:` without a later `ACK` of a ruling sleeps
   the full deadline and re-reads, up to 2 h. Then it writes `PARKED` with its continuation. `launch.sh` treats an
   exit without DONE/PARKED as a crash and relaunches from the WORKLOG (review B4 P4). R1–R3 are asked in S0, so no
   step waits on Ember mid-build. Each ruling's step is last in its chain.
6. **Per step, the gates that can refute it:**
   - the census statement-digest diff under the declared rename/delete map (§3.5);
   - the whole-tree `lake build` after S6–S8 and S12 (shared modules move; per-file green hides a red umbrella);
   - the journey (`lang-journey`) after S2 and S9;
   - `certificate-tests` after S12;
   - `gates/check.py` (closure C3: no def in a Proofs module; `CalculusLaws` is a Prop structure, which C3 allows
     [READ LANE-RULES rule 11]).

   No unfiltered suite. Each deletion step asserts that its deleted paths are gone (`git ls-tree`) before it reads
   any verdict; that is the "falsifier that stopped falsifying" rule.
7. **Decisions.** S0 writes one `## LANG-74 Consolidation of the contextual program` entry. It holds §2.1's module
   list, the rename map, the deletion groups with reasons, and the three rulings. Each step appends a `### LANG-74.n`
   subsection with its own critique and meta-critique. The meta-critique names a bias, not a rejected strawman
   (review M9).

   S0's erratum fixes the ids in place: the second LANG-72 (P3, :3120) becomes LANG-71, and each card-named entry
   (LANG-P10 … LANG-P13, LANG-ACT, both LANG-P7) gets a one-line "superseded by LANG-74.n" pointer under its
   heading. Do not renumber the P-ids, because commit messages cite them.
8. **SIZE.** Every step's SIZE lines carry numbers and a *why*, not just a *what* (review L11). S6 should also fix
   `gates/size.py`'s "deployed" count to mean "in an exe closure". After S6, `Lang/Contextual` is in none.

---

## 6. The unlanded PE1 journal

What it is [READ the decision tail and the files on hbox]:
- **(a)** a real environment exporter, `Census/JournalExpr.lean` + `Census/Journal.lean`, 340 lines. It walks
  elaborated types, proof values, axiom sets and premise applications as shared DAGs, and is measured on eight
  Kernel obligations.
- **(b)** a fourth `CalculusData` instance, `Lang/Contextual/Journal.lean`, in which a receipt is a term, a
  revision is a type, and `strengthen`/`weaken`/`msubst` are identities. It has 21 theorems over that instance.
- **(c)** `Census/JournalRun.lean`'s `#journal_worlds`, which runs P3's `Worlds` toy. S5 deletes that toy.

**Recommendation: fold PE1 directly into the target structure.** Do not land its Lang modules first and fold them
later.
1. **Land (a) now, as Census tooling**, with `gates/journal*.py`, independent of the fold.
   - It touches no Lang file and imports no contextual module.
   - It is the tool §5.2 and §3.5 need: reverse dependencies and statement digests from the elaborated environment.
   - The review's B4 P1 said "dogfood PE1 as the front end of the judge, not beside it". The fold is its first
     customer: S0's IMPACT.md files and the per-step digest diff come from it.
2. **Do not land (b).** The receipt judgment is a finite check over strings with its own result type `CheckResult
   {checked, rejected, exhausted, incomplete}`. Routing it through `Closure.judge` by an identity calculus is the
   same move as `p8Data` (F4): a second shape that reads as reuse.
   - Keep the receipt record and its result as plain Census data (`Census/JournalReceipt.lean`), with refusals by
     name.
   - Keep only the theorems with a non-toy subject: `receiptCheck_iff`, `matches_iff`, `revision_mismatch` and
     `append_history`, restated over the Census record, plus the teeth `revision_tooth`, `success_tooth`,
     `coverage_tooth`, `input_tooth`.
   - Delete `admitted_receipt`, `exhausted_unavailable`, `incomplete_unavailable`, `repair_receipts`,
     `repair_composes` and `repair_batch`. They are `Closure.judge`/`Protocol` facts instanced at the identity
     calculus. [INFERRED from the instance definition `Lang/Contextual/Journal.lean`:42–55 READ]
3. **Delete (c).** `#journal_judge` becomes a Census command over the Census receipt and needs no
   `Lang.Contextual` import. Census tooling may then stay out of Lang entirely.
4. **Order:** PE1(a) lands before S0, because S0 uses it. PE1(b,c) never land. The LANG-PE1 decision text in the
   worktree says "the dependent-context bridge … remain the next card". That bridge belongs to S13 (R2) and to the
   live ROM, not to a receipt calculus.

---

## 7. Rulings needed from Ember (asked in S0; each default stated; none blocks S1–S12)

- **R1 · the open-protocol calculus (LANG-67).** `C/Protocol` (757), `C/NanoBridge` (66), `P/Protocol` (968),
  `P/ProtocolTyping` (132) and `P/Negotiation` (474): 2,397 lines, 101 theorems.
  - Its one tie to nano is `NanoBridge`, an embedding of `Hosting.Resident.Prog` with a trivial index and no holes
    (`Empty`) [READ `NanoBridge.lean` docstring].
  - Through it, `nano_interp_runs` re-derives the landed `Hosting/Proofs/ResidentRun.lean`:700 `interp_runs`.
  - Nothing consumes any of it after S1/S3.
  - This is a genuine fork: (A) the resident's `Prog` gains holes and *becomes* `Prot`'s one shape (a HOSTING+LANG
    card, a real redesign), or (B) delete it.
  - **Default (B)**: two protocol languages are the law-1 defect, and (A) is a design to write when activities
    need it, not a reason to carry 2,397 lines now. [INFERRED]
- **R2 · keep the closure's judge in Lang only with a live bridge.** S13 states and proves that the deployed
  `selectHole`/`resolveHole` is `Contextual.judge` over `langData`:
  - `.ok s` ↦ `.verified` with `s.strengthened` as the strengthening outcome;
  - `holeSupportMoved` ↦ `suspended`;
  - `holeDerivationMoved` ↦ `conflict .guardFails`;
  - `holeGuardBlocked` ↦ `conflict .guardFails`;
  - `holeSelectionAbsent`/`holeUnpinned` ↦ `uncovered`.

  That runs at a `World` read from the `RowView` (`live t := holePinHolds rv self t`). The mapping is my reading of
  `LiveHoles.lean`:66–134 against `Closure.Status` [INFERRED; the statement review in S0 must check it]. If the
  statement cannot be made true without new premises on landed theorems, **take `judge`/`Status`/`provenance` out
  of Lang**, keep `CalculusLaws` + `langLaws` (the substitution theory the deployed operations satisfy), and delete
  the rest of the spine. **Default: build S13**, because P7 made the live ROM rich enough to be the instance.
- **R3 · the CMTT core.** Its job was to give the closure a lawful instance before Lang had contextual holes
  (LANG-66/68: `langTemplate_no_hyps` proved deployed holes closed). P7 replaced that boundary, and `langLaws` is
  now the non-degenerate instance. The core's remaining unique content is first-class contextual values
  (`box`/`letbox`), which nano's `Term` does not have.
  - **Default: delete after S13**, because a second calculus kept as a reference model is a twin.
  - Keep it only if Ember wants `box` in nano's `Term`. Then the card is "add `box`/`letbox` to `Lang.Term`" and
    the core is its specification, retired when that lands.

  The review called LANG-66's core "genuine theory", and it is. This ruling is about where it lives, not whether it
  is good. [INFERRED]

---

## Appendix · How I measured

- Tree: `git -C ~/dev/nanodregg fetch origin` → `origin/main` = d7989d9; `git archive origin/main` into
  `cm/tip`.
- `cm/graph.py`: parses `^import` across Lang/Kernel/Ledger/Protocol/Host/Hosting/Census/Codec/Emit/Bench/Ops. It
  reads the `lean_exe … root := \`M\`` pairs from `lakefile.lean` and computes import closures per exe. It counts
  `theorem|lemma` with optional attribute and `private`/`protected`, which gives 908 contextual theorems. It does
  not count `structure … : Prop` fields (`CalculusLaws` shows 0).
- `cm/disp.py`: my disposition of each module, with sums. `cm/table.py` → `cm/table2.md` is the §1.3 table.
  `cm/thms.txt` holds every theorem name per proof module.
- PE1: `ssh hbox` reads of `wt/CX-PE1` (`git status`, `wc -l`, `grep ^import`, the LANG-PE1 decision diff, and
  `Lang/Contextual/Journal.lean`, `Census/JournalRun.lean` whole).
- Not done: no build; no census run; no statement digests (§3.5 is a proposal). I read the Closure, LangCalculus,
  LiveHoles, StdContextualHole and Journey P8 sources in the ranges cited. For the deleted groups I read headers,
  definitions and theorem names, not every proof.
