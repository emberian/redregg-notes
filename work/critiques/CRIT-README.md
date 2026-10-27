# CRIT-README

2026-10-27. Outside review by Codex.

I reviewed `origin/main` at `6faa984839c13dff10e29f53bdd658d806104001`.
The README at that revision has 304 lines and 2,537 words.
Line numbers below refer to that revision.
Repository inspection used Git objects on hbox.
I ran no project executable, build, test, journey or benchmark.
I changed no repository file.

I read the README, `docs/OVERVIEW.md`, `docs/JUDGE.md`, `Spec/README.md` and `CHARTER.md`.
I checked all 48 distinct Markdown link targets with `git show`.
Every target exists.
I inspected the command definitions, build declarations, landing scripts and relevant theorem statements.
I inspected selected implementation paths for followers, heads, foreign receipts, contextual preparation, execution, value and resident effects.
I read excerpts of the runbook and the older layer designs.
This is a documentation review against source, not a proof audit.

## Verdict

The README inventories the repository before explaining its use.
It introduces a World through another undefined concept, a “verified single-writer World.”
It gives heads and generators more introductory space than documents or escrow.
It never walks through one member action.
It gives a contributor more help landing a patch than it gives a newcomer running an application.

The main defect is the order of explanation.
The next defect is the scope of assurance claims.
The literature list names relationships without specifying their limits.
The reading map sends a newcomer to at least one obsolete account of the running system.

The remedy is not a status confessional.
Describe a member action first.
Explain the components through that action.
Attach each assurance claim to its subject and premises.
Put the contributor workflow behind its existing documentation link.

## Three readers after ten minutes

### The strong engineer

The engineer knows that one writer orders calls.
They know that each member has a follower that checks execution.
They know that Lean implements decisions.
They know that Rust handles transport, custody and confinement.
They know that packages supply methods and laws.
They know that a Turn commits its effects together.
They know that the operator can read the data.

They still cannot explain the application in ordinary terms.
The README does not show what a document contains or how two people edit it.
It does not define the difference between an object method and an object law with an example.
It does not show which process owns each Store.
It does not explain the relationship between `nd`, `host follow`, `host serve` and `nd-supervise` in one place.
It leaves “resident,” “Bell,” “activity,” “floor,” “pin” and “head” to context.

They have to guess whether this is primarily a language, a database, a ledger or an application platform.
They have to guess whether followers retain separate durable copies.
They have to guess whether membership restricts access to individual objects or grants access to the World's bytes.
They have to guess why this system is useful when everyone already trusts the operator with plaintext.
The missing answer is concrete: members check the authorized state transitions themselves.

`docs/OVERVIEW.md` supplies a better first description in its first paragraph.
`docs/OBJECTS.md` supplies the missing distinction between methods and laws.
Neither requires the reader to start with a 1,975-line `Kernel/World.lean`.

### The verification researcher

The researcher knows that the implementation has executable Lean definitions and proofs.
They know that `Spec.System` abstracts selected deployed entry points.
They know that `deployed` instantiates those fields with named implementation functions.
They know that selected claims reject trivial replacement systems.
They know that hash-binding statements expose collision alternatives.
They can find the TCB table.

They still do not know what the opening word “verified” quantifies over.
The README groups model theorems, component theorems, runtime behavior and composed system claims under one promise section.
It does not identify the theorem for its signing sentence.
It does not state the common-start premise beside the equal-head claim.
It states law-history preservation more broadly than `Integrity.law` states it.
The late reference to `Spec/README.md` makes the researcher repair these interpretations after reading them.

They have to guess whether “one lawful history” means agreement among members.
They have to guess whether the compiler is verified.
They have to guess whether the resident's retry behavior has a composed crash theorem.
They have to guess whether a trivial countermodel establishes non-vacuity of every conjunct.
`Spec/README.md` explicitly distinguishes these cases.
The README should preserve those distinctions at the claim, without reproducing the backlog.

### The person who wants to run it

This reader knows the Lean version.
They know the names of two native build commands.
They know where the host and client binaries appear.
They know that a browser demonstration exists.
They know that native operation involves a Store, a follower and a supervisor.

They still lack a first successful interaction.
The code block builds binaries and invokes verification harnesses.
It does not start a writer or connect a member.
It does not install a document or exercise escrow.
It gives no expected output.
It gives no short prerequisite list for native confinement.
It gives no complete browser build-and-serve command sequence.
The link to `testground/index.html` opens source on GitHub.

They have to choose between the 782-line runbook and a build script.
They have to infer Emscripten's version requirement from the script.
They have to infer that the browser page must be served over HTTP rather than opened as a file.
They have to infer that a local browser World does not require the hosted resident deployment.
The README should offer that smallest complete route first.

## Claims checked against the tree

### “Verified” has no subject precise enough to check

The first sentence calls the World verified.
`Spec/System.lean` varies selected decision functions.
It does not model every instruction executed by Rust, C, the compiler, the filesystem or the operating system.
`gates/tcb.tsv` records trusted implementation components.
The README later acknowledges those dependencies.
That does not make the opening adjective an exact claim.

Write “The admission and follower decisions are implemented in Lean.”
Then identify the composed history, value and settlement properties.
State the trusted implementation boundary beside the proof map.

### Equal heads require a common start

The promise says: “Matching step counts and chains identify the same World, up to a collision among the named link inputs.”
`OneHistory.pair` in `Spec/Proofs/Claims.lean:98` quantifies over two folds from the same `g`.
The sentence omits that premise.

Write “Two logs folded from the same starting World produce the same World when their step counts and chains match, unless the hash collides among their link inputs.”
A second sentence should explain that this binds a comparison.
It does not make disconnected members agree.

The adjacent phrase “one lawful history” also invites a consensus interpretation.
The implementation checks a member's accepted history.
The charter permits fork detection and refuses history merging.
Use “a checked history for each member” before introducing the comparison property.

### The law-history sentence exceeds its theorem

“An object's history follows its laws” drops the restrictions of `Integrity.law`.
The claim requires an audited log and canonical cells.
It requires `IsLaw t` and `NoRef t`.
Its chain conclusion applies to a law present throughout the relevant history.
The README mentions `NoRef` in the component inventory, but omits it from the promise.

Write “For a law in force throughout an object's history, the law-history theorem relates the object's transitions to that law's reference semantics under `IsLaw` and `NoRef`.”
Link directly to the claim.
Explain runtime admission separately.

There is a further reading-map defect in `Spec/README.md`.
Its premises section describes `NoRef` as “laws without holes.”
`Lang/Proofs/Receiver.lean:129` rejects `.ref` and recursively permits `.hole` when its substitutions satisfy `NoRef`.
The top-level README's description as absence of package references is closer to the definition.
Do not copy the Spec page's gloss into the rewrite.

### Signing behavior is not one of the listed composed claims

“It signs calls its own copy admits” describes the intended command path.
`docs/MEMBER.md` describes re-derivation before requesting a signature.
`Spec/README.md` lists signing, C(i), under “Not yet claims.”
The README must distinguish an implementation account from a composed theorem.

Write “The follower derives a call against its own World before requesting its signature.”
Put `Consent.okCommitted` beside the separate settlement statement.
Do not infer a signing theorem from the existence of the settlement theorem.

### Durability and the Bell need an explicit kind of claim

The durability sentence names the Store contract.
That qualification is necessary.
The following Bell sentence does not identify the crash model or the correspondence to the running processes.
`Spec/README.md` does not list DURABILITY or THE BELL among its composed claims.
The README's final paragraph acknowledges this distinction only after making the promises.

`Hosting/Resident/Run.lean` keeps intent before a provider request.
It keeps an answer before submitting it.
`Hosting/Proofs/ResidentRun.lean` proves effect ordering over paths through `tickP`.
Those facts support a precise component description.
They do not make “a second answer” an adequate description of every provider, delivery and crash event.

Write the persistence order as behavior.
Name the Bell guard's object-level rejection separately.
Identify durability models as models at their link.
Remove “Safety is a theorem under stated assumptions” as a catch-all conclusion.

### A certifier authority is not necessarily enabled

The opening mentions an authority fixed at genesis.
That representation exists.
`Host/Cli.lean:477` accepts `--certifier` and `--threshold` options.
Omitting both selects `Authority.none`.
`Protocol.Head.certifiesWorld` accepts without a certificate when the threshold is zero.

The README does not explain this distinction.
A reader cannot tell whether a normal genesis requires certified heads.
Write “Genesis can name the keys and threshold used to certify heads.”
Keep the policy representation separate from the mechanism that produces certificates.

### A foreign receipt proves a narrower fact than “a claim”

The Certificate Transparency comparison says a member can check “a claim against a held head.”
`Protocol/Foreign.lean` checks a decoded receipt for a committed transaction.
It rejects absent and refused settlements as `notCommitted`.
Its soundness account assumes that the held head belongs to a fold of the cited foreign World.
It does not establish arbitrary outside content, freshness or cross-World atomicity.

Write “A foreign receipt proves transaction admission relative to a held head.”
State the held-head premise immediately afterward.
`docs/OBJECTS.md` already makes this distinction.

### Convergence reports candidate causes

The README says convergence reports “which landing it came from.”
`gates/converge.py` attributes a failure to commits in the range since the last green report whose changes intersect its inputs.
Its fallback rules over-attribute.
This is not a determination of the introducing commit.

Write “The report lists failures and the landings that changed their inputs.”
`scripts/standing.sh` also carries successful results for unchanged inputs within its daily limit.
“Runs every row” describes coverage over the report's policy, not fresh execution of every row on each invocation.
Write “The report covers every registered row and identifies reused results.”

### The landing summary is broader than its selector

`scripts/commit` exists and accepts the documented forms.
`gates/touched.py` selects affected Lean and Cargo rows.
It explicitly leaves `standing:` and `script:` rows to convergence.
Its Lean target selection builds reached libraries whole.
The README's “runs the rows the change touches” omits those categories.
Its “builds the changed modules and their importers” omits the library granularity.

These details belong in `docs/JUDGE.md`.
The README needs one contributor link.
Do not use an onboarding page to restate an evolving selector algorithm.

### The memory advice and script defaults disagree

The README gives 6G for a module and 24G for a tree.
`scripts/commit` defaults `SWARM_MEM_MAX` to 24G.
`scripts/converge` uses a measured memory floor.
Its unset cap is documented as 96G.
The README does not explain how its fixed budgets interact with that refusal.

Move host-specific resource policy out of the general build instructions.
Link to the current shared-host policy from the contributor page.
This is a documentation contradiction.
It is not a request to weaken the resource controls.

### Some named destinations are historically wrong

The README introduces `Host/DESIGN.md` as the process-boundary starting point.
That file says the follower opens a Store read-only, takes no lock and never appends.
`Host/Follow.lean:1` describes durable appends to the follower's separate Store.
`docs/OPERATING.md` describes the follower as owning a writable Store.
The old design also places the writer lock on the segment handle.
The current operating guide places it on the key-file handle.

Use `docs/OPERATING.md` for the process introduction.
Label the old design as historical if it remains linked.
`client/DESIGN.md` also starts from an October 16 design and directs readers to frozen decisions.
Use `docs/MEMBER.md` before it.

### Historical and environmental assertions are not established by this tree

“Main (origin/main on GitHub) is the only branch” is literally false.
`git ls-remote --heads origin` returned `main` and `gh-pages` during this review.
Write “Land source changes on main.”
That states the contribution rule without misdescribing deployment refs.

The external redregg memos are not nanodregg paths.
Their contents cannot be checked with `git show origin/main:<path>` in this repository.
The reading map gives no usable link or access condition for them.
Keep them under historical background after the self-contained documentation.

The minidregg and breadstuffs ancestry is repeated in the charter.
That repetition does not independently establish the stated reconstruction history.
Present it as project history.
Remove “meaningful” from “meaningful theorem statements.”

“Build with stable Rust” is not reproducible toolchain information.
The manifests identify edition 2024 and workspace resolver 3.
The lockfile fixes dependencies.
They do not pin a tested Rust release.
I did not compile the tree, so this review does not verify compatibility with an installed stable compiler.

### What the command check established

The commands below are source-supported forms.
Their successful execution was not tested.

| README command or path | Source check |
|---|---|
| `export CARGO_TARGET_DIR="$PWD/target"` | Sets the stated per-worktree Cargo output location. |
| `lake build host` | `lakefile.lean` declares `host` with root `Host.Main`. |
| `cargo build --locked --release -p nanodregg-client` | The workspace contains the package. Its manifest declares `nd` and `nd-supervise`. |
| `lake exe kernel-sim --seeds 64` | `Kernel/Sim/Main.lean` accepts the seed-count form. The same invocation appears in `gates/runs.tsv`. |
| `lake exe host-sim 1` | The executable delegates to the simulation runner. Seed 1 appears in `gates/runs.tsv`. |
| `lake exe host-file-sim 1` | `Host/Sim/File.lean:1182` accepts a seed and optional directory. The default scratch path is `.lake/host-file-sim`. |
| `lake exe lang-journey --contextual` | `Lang/Journey.lean:2934` filters registered contextual sessions. |
| `lake exe rows --deployed receipt` | `Protocol/Rows/Run.lean` parses the deployed flag and row names. `Protocol/Rows.lean` contains the receipt row. |
| `cargo test --locked -p nanodregg-client --test frame` | `client/tests/frame.rs` exists. The manifest uses Cargo's normal integration-test layout. |
| `lake build` | The listed libraries and executables have default-target attributes. This builds substantially more than the native host. |
| `scripts/commit -F MESSAGE_FILE PATH...` | The parser accepts a message file with named paths. |
| `testground/build/build.sh` | The script requires `c`, `wasm` or `all`, followed by `WORK`. Its header requires Emscripten 6 or later. |

The toolchain pin, absence of external Lean packages, warnings-as-errors option and binary declarations agree with the README.
The browser script emits the Wasm module and copies package texts.
These source checks found no invented executable in the build block.
They do not turn the block into a runnable application tutorial.

## Sentences to replace

These are the sentences whose framing decorates, inflates or obscures their facts.
The table also includes sentences whose compression violates the one-fact rule.
Ellipses identify long sentences without reproducing their entire link markup.
The replacements retain technical nouns that name actual structures.

| Location and original wording | Plain replacement |
|---|---|
| 3: “nanodregg is a verified single-writer World: a shared state whose members check its history by re-executing the log.” | “nanodregg is a research system for shared objects.” “One writer orders changes.” “Each member checks changes by re-executing the log.” |
| 4: “Its metered ledger language, Objective Bend, gives objects methods and laws, with programs whose meaning depends on justified facts in the World.” | “Objective Bend defines object methods and laws.” “Methods compute proposed changes.” “Laws accept or reject changes.” “Contextual slots select code using checked observations.” |
| 6: “A World's position is itself a kernel object: members can hold heads, compare histories, and check receipts against them, with an authority fixed at genesis naming who may certify a head.” | “A head records a World's position.” “Objects can store heads.” “Members use heads to compare histories and check receipts.” “Genesis can name certifying keys and a threshold.” |
| 18: “Programs can also construct programs.” | “A method can return an install call containing a generated package.” Merge this with the following generator explanation. |
| 23: “Membership and follow grants define access; this is a trusted vat with independently checked execution.” | “A follow grant authorizes access to the World's bytes.” “Followers check execution.” Delete “trusted vat” here. |
| 50: “The design assumes that every fact an invocation needs is in its pinned view; the program cannot read an ambient World behind the signer's back.” | “An invocation reads through its pinned view.” “Missing required observations cause refusal.” |
| 93: “The ledger assumes the denomination's issuer and the escrow's named parties and arbiter have the roles the members intend; conservation does not decide the economic meaning of an asset.” | “Members choose the denomination's issuer and the escrow's parties.” “Conservation does not establish an issuer's ability to redeem a balance.” |
| 105: “Its guarantees assume the member socket and durable volume contracts, while provider availability and the usefulness of a model's answer remain external facts.” | “Resident proofs assume the member-socket and durable-volume contracts.” “They establish neither provider availability nor answer quality.” |
| 113: “These programs carry frames, keep keys and attempts, and perform process and filesystem operations, refusing unsafe custody paths and confinement failures; law 2 assigns semantic decisions to Lean and gives Rust generated protocol tables.” | “Rust carries frames and performs operating-system effects.” “It stores keys and signed attempts.” “It checks custody paths and confinement.” “Lean supplies protocol decisions and generated tables.” |
| 120: “a desktop of member terminals, object windows, demos and a wire inspector makes the system explorable.” | “The page contains member terminals, object windows, demonstrations and a wire inspector.” |
| 134: “The claim's named premises are part of its meaning…” | “The member-history claim assumes a trusted adoption key.” “Value conservation requires canonical tries.” State the law claim's `NoRef` restriction beside that claim. |
| 147: “These checks assume Lean's kernel and the explicitly listed trusted components, and keep the distinction between a failed check and a check that could not run.” | “The report distinguishes failed checks from checks that did not run.” Put proof dependencies beside the proof claims. |
| 154: “exercise the concrete Store and client paths, refuse invalid measurements, and measure THE BAR: two friends and a hosted resident using one World.” | “The benchmark runs two members and one hosted resident against one World.” Put workload size and measured quantities at the benchmark link. |
| 157: “Operational guarantees assume the runbook's filesystem and identity setup; performance limits are judged in the conditions the benchmark names.” | “The runbook specifies required filesystem and identity settings.” “Each benchmark records its measurement conditions.” |
| 162: “These are the lines of work behind the design, and the choices that give nano its particular shape.” | “The design draws on the following work.” |
| 166: “Nano makes the same receiver the source of the writer's Turn and the follower's check, and makes consent before signing a property of that command path.” | “The writer and follower use the same receiver.” “The follower checks a planned call before requesting its signature.” |
| 170: “Nano puts heads and their governing authority into the World's vocabulary, so an object can use a foreign receipt as an input to its own law.” | “Objects can store foreign heads.” “A law can check a transaction receipt against a stored head.” |
| 185: “Its relationship to the reference meaning and the fuel it requires is proved, so ticks have a specified meaning across re-executions.” | “`run_bigStep` relates successful runs to the reference semantics.” “`bigStep_run` proves that a reference result is reachable with sufficient fuel and stack.” |
| 190: “Nano checks that justification against the caller's pinned World and names the failed support when it withdraws a choice; the document makes that behavior visible as a suspended section.” | “Invocation checks each selection's support against pinned observations.” “A refusal identifies failed support.” “The document demonstration displays the resulting suspension.” |
| 206: “Nano makes the verdict readers' ability to recognize failure a standing check, and `Spec/` gives the top claims explicit trivial countermodels.” | “Harness controls test whether verdict readers reject known failures.” “The top claims have trivial countermodels.” |
| 211: “The organizing promise is one lawful history…” | “A member accepts a history checked from its trusted starting state.” State preservation and head comparison separately. |
| 223: “The Bell carries this through a running application…” | “The resident persists request intent before asking the provider.” “It persists the answer before submitting it.” “The Bell rejects a repeated answer to an answered ring.” |
| 231: “Safety is a theorem under stated assumptions; progress is measured on the running system.” | Delete. The named claims and named measurements already say what is established. |
| 298: “nanodregg is rebuilt from minidregg's specification and battleground: its journeys, simulations, workload and meaningful theorem statements.” | “nanodregg draws its requirements from minidregg's scenarios, simulations, workload and theorem statements.” |
| 300: “It is a focused research demonstration that minidregg can draw from, within the Dragon's Egg lineage whose earlier whole-system exploration is dregg (breadstuffs).” | “nanodregg is a research demonstration in the Dragon's Egg project.” “Earlier systems include minidregg and dregg, also called breadstuffs.” |

“The running instance,” “the concrete instance” and “the concrete wiring” repeatedly ask adjectives to explain instantiation.
Name what is bound instead.
`Host.Deployed.X` binds the kernel to the deployed codecs and language.
That sentence needs no second label.

“Start at” is functional navigation when the destination is suitable.
Its repetition adds little when each component already has an entry-point link.
Put the entry points in a table.
Keep each component's prose for its role and inputs.

“Turn,” “head,” “pin,” “canonical” and “CEK” are not decorative words.
They need definitions or links.
Deleting them would reduce precision.

## Literature comparisons

The README names no paper title, author list, date or link in this section.
A reader cannot distinguish a borrowed construction from an analogy.
Each entry needs the common mechanism, the material difference and a source.
The following corrections cover every named group.

**PeerReview, SUNDR and SPORC.** PeerReview audits recorded behavior through replay and uses witnesses to support accountability.
SUNDR's central result is fork consistency.
SPORC combines fork consistency with operational transformation and encrypted collaborative state.
The three do not implement one generic technique called “accountability by re-execution.”
Nano's shared receiver is a specific implementation choice.
Name that choice without borrowing the other systems' full guarantees.
The README already rules out host secrecy and merging.
Repeat those differences only at the SPORC comparison.
[PeerReview](https://www.mpi-sws.org/tr/2007-003.pdf), [SUNDR](https://www.usenix.org/conference/osdi-04/secure-untrusted-data-repository-sundr), [SPORC](https://www.cs.princeton.edu/courses/archive/fall15/cos518/papers/sporc.pdf).

**Certificate Transparency.** The common mechanism is authentication relative to a signed commitment.
CT distinguishes inclusion from append-only consistency.
Nano's foreign-receipt path checks transaction admission against stored roots.
Calling that simply “a claim” hides the strongest useful fact it establishes.
The comparison also needs to distinguish a certificate on a head from proof that the head represents a lawful history.
A signature identifies an attester under a policy.
It does not replace re-execution or the held-head premise.
[RFC 9162](https://www.rfc-editor.org/rfc/rfc9162.html).

**Kung–Robinson, Sui and Fabric.** Read validation before commitment is the precise Kung–Robinson connection.
Fabric's versioned read sets provide a closer implementation comparison than a generic list of three systems.
Sui's transaction inputs include versioned object references.
That similarity does not identify Nano's ordering architecture with Sui's.
The useful Nano-specific point is its behind/ahead distinction and diagnostics for missing observations.
Explain what those diagnostics let a client do.
Do not imply that version pins themselves are novel.
[Kung–Robinson](https://www.eecs.harvard.edu/~htk/publication/1981-tods-kung-robinson.pdf), [Fabric read sets](https://hyperledger-fabric.readthedocs.io/en/release-2.5/readwrite.html), [Sui objects](https://docs.sui.io/develop/sui-architecture/object-model).

**KeyKOS, SPKI and macaroons.** The connection is delegated authority with restricted rights.
KeyKOS supplies protected object capabilities.
SPKI describes authorization certificates and delegation.
Macaroons use bearer credentials with attenuating caveats.
Nano instead checks grant records in authenticated mutable state.
That choice makes revocation and counted consumption part of the same ordered transition as an object operation.
The current sentence names this state placement but does not explain its consequence.
It also erases the distinction between a protected reference and a signed or MAC-authenticated credential.
[Security in KeyKOS](https://css.csail.mit.edu/6.858/2014/readings/keykos-sec.pdf), [SPKI](https://www.rfc-editor.org/rfc/rfc2693.html), [macaroons](https://research.google.com/pubs/archive/41892.pdf).

**EUTXO, Cardano validators, XRPL trust lines and Move.** EUTXO and Cardano validators belong in one comparison.
Their connection is validation of a proposed transaction against explicit inputs and context.
Nano uses mutable objects and kernel balance cells rather than an unspent-output state model.
XRPL belongs beside credit: Nano permits negative balances down to a floor.
Move belongs beside resource representation: its resource discipline prevents unauthorized copying or discarding of protected values.
Nano's conservation rule applies to kernel balances rather than ordinary language values.
The README states that last distinction but hides the credit model behind “floors.”
It also says floors are conserved without the well-creation exception in `Integrity.value`.
Spell out that exception when making the conservation comparison.
[EUTXO](https://developers.cardano.org/docs/get-started/technical-concepts/eutxo/), [XRPL trust lines](https://xrpl.org/docs/concepts/tokens/fungible-tokens/trust-line-tokens), [Move resource safety](https://arxiv.org/abs/2004.05106).

**CEK machines and CakeML.** CEK identifies the evaluator's machine structure.
CakeML is a separate comparison about relating executable evaluation to semantics.
The tree supports that narrow comparison through `Lang/Proofs/Agree.lean` and `Complete.lean`.
`Cost.lean` adds a bound on primitive operand bytes per charged tick.
None of these statements verifies the Lean-to-native compilation chain.
CakeML's verified compiler must not be implied by the adjacency of its name to “verified.”
Name the semantic agreement result and its resource quantifiers.
[CakeML](https://github.com/CakeML/cakeml), [CakeML evaluation semantics](https://github.com/CakeML/cakeml/blob/master/semantics/evaluateScript.sml).

**Contextual modal type theory, de Kleer's ATMS, Doyle's truth maintenance and why-not provenance.** These are four different connections.
Contextual modal type theory gives typed open code an explicit context.
Doyle tracks reasons for beliefs.
An ATMS tracks assumption sets supporting conclusions.
Why-not provenance explains missing query results.
Nano's deployed mechanism selects typed candidates and checks recorded support at invocation.
Its refusal data names failed observations.
That is a useful connection to explanation and retraction.
It does not establish equivalence to an ATMS or implement contextual modal type theory merely by using typed slots.
`docs/OBJECTS.md` explicitly distinguishes the contextual research model from deployed preparation.
The literature paragraph should preserve that distinction.
[Contextual modal type theory](https://www.cs.cmu.edu/afs/cs.cmu.edu/user/fp/www/papers/cmtt05.pdf), [Doyle](https://www.ijcai.org/Proceedings/77-1/Papers/035.pdf), [de Kleer](https://www.sciencedirect.com/science/article/pii/0004370286900809), [Why Not?](https://citeseerx.ist.psu.edu/document?doi=1aa60b5ae893cd93a221bf71b6b264f5aa5ca6b8&repid=rep1&type=pdf).

**Interaction Trees and sans-I/O.** The resident represents effects as an inductive `Prog` with a handler.
Its trace theorems inspect paths through that representation.
Interaction Trees also address potentially nonterminating computations through coinduction and equivalence up to weak bisimulation.
The README's shared idea is reified effects with interpreters.
It should claim that idea, not leave the reader to infer the full ITree theory.
Sans-I/O describes a different separation: protocol logic consumes data without performing network I/O.
Give it its own sentence.
[Interaction Trees](https://arxiv.org/abs/1906.00046), [sans-I/O](https://sans-io.readthedocs.io/).

**EverParse and Narcissus.** The round-trip and canonical-representation comparison is substantive.
EverParse also verifies low-level memory safety and generates zero-copy parsers.
Narcissus derives encoders and decoders from format descriptions.
Nano's Lean codec proofs and emitted Rust layouts are a different implementation boundary.
The README should identify that boundary.
The structural-tag caveat is precise but belongs after the principal codec property.
Fixed vectors detect specified changes of byte meaning.
They do not replace parser correctness or establish complete interoperability.
[EverParse](https://www.microsoft.com/en-us/research/publication/everparse/), [Narcissus](https://www.cs.purdue.edu/homes/bendy/papers/Narcissus/index.html).

**Schneier–Kelsey and KERI.** This pairing conflates two kinds of key.
Schneier–Kelsey addresses protection of earlier log entries after compromise through evolving cryptographic state.
`Host/Keys.lean` describes a single Store key used for integrity at rest.
Its header explicitly disclaims protection against a party that can write the Store.
KERI's relevant connection is precommitting future identity-control keys.
Nano's member-key rotation does not turn the Store MAC into a forward-secure audit log.
Split the comparison into log integrity and identity rotation.
[Schneier–Kelsey](https://www.schneier.com/academic/archives/1999/05/secure_audit_logs_to.html), [KERI](https://keri.one/).

**Mutation testing and Kupferman–Vardi vacuity.** Known-bad controls test whether checks reject chosen defects.
Trivial replacement systems test whether selected claims distinguish those systems.
Kupferman–Vardi vacuity examines whether parts of a specification affect its truth in a model.
One countermodel does not establish that every premise or conjunct matters.
`Spec/README.md` says the law floor refutes package preservation and does not independently refute the law-chain clause.
Call the floors countermodel checks.
Keep the broader vacuity connection as motivation.
[Kupferman–Vardi](https://cris.huji.ac.il/en/publications/vacuity-detection-in-temporal-model-checking-13/).

## Three README models

[ripgrep](https://github.com/BurntSushi/ripgrep/blob/master/README.md) names its operation in the first sentence.
It states default behavior and supported platforms before its implementation details.
Its navigation gives installation and a user guide immediate prominence.
Nano needs the same clarity about the member's operation and the first usable route.

[restic](https://github.com/restic/restic/blob/master/README.md) shows repository creation and one backup with expected output.
That gives the reader a completed task before discussing design principles.
Nano needs one comparably complete document or escrow interaction.
A sequence ending in a test verdict does not serve that purpose.

[CakeML](https://github.com/CakeML/cakeml/blob/master/README.md) identifies what is implemented and which prover checks it.
It provides build instructions and built compiler links before its directory map.
Its map explains what each directory contains.
Nano needs that ordering and that specificity about verification.
These are structural models, not prose to imitate wholesale.

## The reading map

The current map begins with project rules and decision history.
Those answer a maintainer's questions before a newcomer's.
The component inventory also treats source modules as introductory explanations.
`Protocol/Command/Machine.lean` has 1,584 lines.
`Lang/Package.lean` has 844 lines.
A filename is not an explanation of what to look for inside it.

Use this order:

1. State the purpose and show one document interaction.
2. Offer the local browser demonstration with prerequisites and expected result.
3. Explain the process path from member command to follower, writer, log and settlement.
4. Link `docs/OVERVIEW.md` for the complete system map.
5. Link `docs/OBJECTS.md` for packages, laws, relations and contextual support.
6. Link `docs/MEMBER.md` for commands and their outcomes.
7. Link `Spec/README.md` and `docs/TRUST.md` for precise claims and trust assumptions.
8. Link `docs/OPERATING.md` before `deploy/RUNBOOK.md` for native deployment.
9. Give the literature map with exact sources and limited comparisons.
10. Link `docs/JUDGE.md`, `CHARTER.md` and `decisions/README.md` for contributors.
11. Put proposals, historical designs and external research records last.

Keep the whole-system component inventory.
Reduce it to roles, boundaries and links.
Separate runtime components from proof modules and test tooling.
Do not give a census the same explanatory weight as the member's follower.

The README should directly link the existing OBJECTS, MEMBER, TRUST, OPERATING and TESTGROUND guides.
At present it reaches them indirectly through OVERVIEW.
Those guides are the missing middle between introductory prose and source code.

## Five changes with the highest value per hour

These are editing estimates.
They exclude implementing new functionality.

1. **Replace the opening and add one action trace. Estimate: 30–45 minutes.** Define the system as shared objects with independently checked updates. Use a document edit to introduce the member, follower, writer, Turn and law. This removes the largest burden of inference for all three readers.

2. **Fix the reading map and remove obsolete starting points. Estimate: 20–30 minutes.** Link the current guides directly. Put `Host/DESIGN.md` under historical design. Move landing instructions to `docs/JUDGE.md`. This prevents a reader from learning the wrong process model.

3. **Scope the five central assurance sentences. Estimate: 45–60 minutes.** Specify the common start for head equality. Specify the law-history restriction. Separate signing behavior from settlement theorems. Label durability and Bell models. Explain optional certifier authority. This makes the claims defensible without adding a status section.

4. **Add one complete local browser route. Estimate: 45–90 minutes.** State Lean, Emscripten and HTTP-server prerequisites. Show the build invocation with a private scratch directory. Name the demonstration to open and the visible result. Have the docs lane execute that route under its build authorization. This gives an arriving user a task they can finish.

5. **Rewrite the eleven literature entries around mechanisms. Estimate: 60–90 minutes.** Add primary links. Separate the conflated systems identified above. Give one material difference per comparison. This converts a list of names into a research reading map.

DONE 2026-10-27. Review complete at `6faa984839c13dff10e29f53bdd658d806104001`.
No landings.
No project runs.

## The paragraph I would put first

nanodregg is a research system for shared objects whose updates each member checks independently. One writer orders signed calls. Each member's follower re-executes the log from a trusted starting state. Objective Bend defines the objects' methods and laws. Methods propose changes. Laws decide whether changes are allowed. The kernel commits an accepted call's effects together. The system includes document and escrow demonstrations, a native host and client, a hosted model resident, and a browser testground. Lean proofs cover specified properties of admission, history and settlement. The operator can read every byte in a World.
