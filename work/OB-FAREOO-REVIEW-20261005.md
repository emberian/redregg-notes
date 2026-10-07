# Objective Bend vs *Lambda: the Ultimate Object*: calculus review (OB-FAREOO-REVIEW, 2026-10-05)

## Scope

**Book.** Faré's *Lambda: the Ultimate Object* (LTUO), offline mirror
`~/dev/fareoo/raw/mirrors/ltuo/2026-10-03/ltuo-readable.txt` (sha256 0644ab39...). I read these sections
in the book itself:

- §5.4–5.5: mix and fix, argument order, the top value, the interaction of modularity and extensibility.
- §6.1.2–6.1.4: conflation. Both issues, recursive conflation, R(Y M) vs Y(R∘M), records.
- §7.3.5–7.4.6: the constraints, C4 and suffixes.
- §9.2.3–9.2.6: effective methods, sub-methods, standard and simple method combination.

From the Scheme sources I read `c4-linearize` in `~/workbox/fareoo-primary-scholar-20261003/pommette.scm`. For the
other sections I relied on the 10-03 scholar synthesis (`sources/ltuo-objective-bend-20261003.txt`):

- §8: typing. Cross-checked against `docs/objective-bend/MODULAR-TYPING.md`.
- §9.1: optics. §9.3: multiple dispatch. §10.4 and §10.6 (MOP): headings and outline only.

**Calculus, as reviewed.** Main 5d0b452d, plus these ranges replayed on hbox lane
`/tank/dregg-build/claude-lanes/ob-review/src`:

- the ob-ltuo stack e16f281e..ed3e9f58, LT0 through LT2 step 4
- ob-lt2-parser 291875da
- for OB7 call, gate tree mk-gate-n3 09833f2d, read only

**Not repeated.** GPT-6's audit at 259a2fb, summarized in OB-LTUO-20261005.md and recovered from root session
ce776c01 prompt 113. It covered:

- typing modularity (LT1, LT2)
- surface semantics (LT3)
- the C4 proof package
- the reflection-contract split (LT4)
- ecosystem (LT5)
- laws, requires and guardedness (LT6)

Nothing below re-derives those. It covers what the audit did not examine: **method
combination, the composition of qualified specs, reflection's observers, argument
conventions, and the unbuilt LTUO feature surface.**

**Evidence base.**

- Every DEFECT was measured through the real Lean front end before it was fixed. The probe cohort
  is `tests/objective-bend-source/fareoo/probe-cohort.json`, gate row `fareoo-probes`.
- Logs are under `/tank/dregg-build/claude-lanes/ob-review/logs/`:
  - `probes-pin1`: before the fix
  - `probes-fix4`: after the fix
  - `plants.log`: one planted fault per fix

Line numbers marked *pre* are at the pre-fix tree (gate n3 + s4 + parser). Lines marked *lane* are at the fix lane.

## Verdict

The kernel agrees with LTUO where it matters most:

- one final self
- the whole super
- `fix` as a computation with a real knot
- lazy records of suspensions
- C4 as a faithful port of pommette, step for step, including the ancestor-count detail

The discrepancies were concentrated in **method combination**, which no audit had read against §9.2:

- Three of them were outright wrong:
  - `and` was strict.
  - `compose` erased combined contributions.
  - Open specs silently dropped qualifiers.
- One let a combined method double-count.
- One leaked source positions into reflection.

All five are fixed on lane/ob-review (below). The rest is either a stated deliberate deviation or unbuilt.

## Discrepancies

### DEFECTS (fixed on lane/ob-review)

| # | Discrepancy | LTUO | Evidence (pre) | Measured | Fix |
|---|---|---|---|---|---|
| D1 | `combine and` lowered to the strict `conjunction` primitive, so it did not short-circuit. A more specific `false` still forced every less specific method, and one diverging method suspended the whole effective method. | §9.2.6: simple combinations run most specific first. `and` stops at the first false (`stop? = not`), like CL `AND`. | `Compiler/ObjectiveBendElaborate.lean:1128` (`"and" => ("conjunction", ...)`), `:1605-1611` (`.binary primitive own next`); strict operands, `Theory/ObjectiveBendOpenRecursion.lean` `binaryRight` needs `Value left` and then steps `right`. | F03: `suspended` (tick budget), target `false`. | `combination` returns a combiner. `and` becomes `ifBool own next false`, and `or` (new, the dual) becomes `ifBool own true next`. Theorems `and_lowering_short_circuits` and `strict_conjunction_waits_for_next` (the tooth) are in `Compiler/ObjectiveBendCombination.lean`. |
| D2 | `compose(A, B)` of specs that both contribute to a `combine` member erased A's contributions. Each declared spec's extension carried its own identity layer (`weight := 0`), which reset the member halfway up a mixin chain. The tutorial documented the symptom ("The 20 from `Left` is gone") but gave no reason. It is inconsistent with OB's own stated rule that "compose copies each spec as written". | §9.2.4–9.2.6: sub-methods accumulate through inheritance. The method-init spec is idempotent: it computes the effective method from self, and op0 is applied once. §5.4.4: the top value belongs to `fix`. | `Compiler/ObjectiveBendElaborate.lean:1700-1712` (pre: the per-spec `init` layers); `docs/OBJECTIVE-BEND-TUTORIAL.md:846`. | F01: 301 (1+300); target 322 (1+20+1+300, with Root twice because compose applies each spec as written). | **The combination is the protocol's.** The record declares it (`record Doc: combine + weight() -> Nat`). Specs contribute with `combine +`. `fix` extends the seed with the identity for each combined member of the target protocol, so the seed's own value is never a contribution (F07). The per-spec identity layers are deleted. New refusals are `combine-undeclared` (F09), `combine-qualifier` (F08) and `protocol-ambiguous`. |
| D3 | A `combine` method's body could read `super.m`, which already holds the partial combination of the less specific methods, so they were counted twice. | §9.2.6: a simple-combination method receives `abort` as call-next-method. It has no next method. | `:1131-1137` (no check), `:1605-1611`. | F04: 12; target refused. | `refused (combine-next)` when a combined body mentions `super` (`checkSpecMethods`, new `exprMentions`/`bodyMentions`). |
| D4 | The interface label read by `metadata(S)` carried every method's and requirement's source **span**, and the parents as the import alias the source wrote. Moving code, adding a comment line, renaming a file or renaming an import alias therefore changed what a program computes. The span had already reached the published typed packets: EvenOddTen and TwiceReview re-emit only those bytes. | §7.3.5.7, shape determinism: "renaming ..., moving code around, ... changing filenames and line numbers ... will not change" behaviour. REFLECTION.md lists the interface as an observer but never mentions positions. | `:1635-1639` (`s.methods.map (·.signature)` with `span`, `s.parents` as written); tutorial `:827` output. | F05: `false`; target `true`. | `withoutSpans` and qualified parent keys in `interfaceLabel`. Theorem `interface_label_span_free`. |
| D5 | An open spec (`spec S[Self has .., Super has ..]`) accepted `combine`/`around` methods and **silently ran them as primaries**, because `layerAt` ignores qualifiers. | §9.2.3: the qualifier selects the sub-method group, so dropping it changes meaning. | `:1389-1398` (`layerAt` iterates all methods with no qualifier). | F10: accepted (0); target refused. | `refused (open-qualifier)`. Open specs' methods are primary until a protocol-carrying open form exists (task below). |
| D6 | Doc defect: the overview cited ltuo §8.2.1–4 for typing against a future self. §8.2.1 is the *trivial non-modular* case; the reference for that typing is §8.4.1.3. | — | `docs/OBJECTIVE-BEND.md:73`. | — | Citation corrected. |

**Planted faults.** Each fix was reverted alone, in a private overlay copy of the
elaborator. In every run the promoted cohort turned red on exactly the row that fix owns
(`logs/plants.log`):

| Plant | Red row |
|---|---|
| strict-and | F03 |
| super-allowed | F04 |
| spans-kept | F05 |
| no-seed-base | F07 |
| open-qualifier-dropped | F10 |
| combine-drops-next | F01 |

The whole cohort on the unfixed front end is all red (`logs/probes-planted-unfixed.log`).

### DELIBERATE DEVIATIONS (with the stated reason)

| # | Deviation | LTUO | Where the reason is stated |
|---|---|---|---|
| V1 | The extension takes self first (`C → V → W`), and `fix(spec, seed)` takes spec first. | §5.4.2: `(mix c p t s)`, super before self. `(fix t m)`: seed first. "The order of arguments is immaterial ... up to a simple isomorphism." | `sources/ltuo-objective-bend-20261003.txt` §1 (PROPOSED self-first). GPT-6 §2 ("not a semantic defect"). |
| V2 | `compose(a, b, c)` is least specific first: the **rightmost wins**, as in Nix `composeManyExtensions`. `spec S extends A, B` and the precedence list are most specific first: **A wins**. | §5.4.2: the flow "should match ... the order of the parents in the class definition syntax, and/or the order in which you store the precedence list" (a usability criterion, not a semantic one). | Only the convention is stated (`docs/OBJECTIVE-BEND-TUTORIAL.md:563,707`; `OBJECTIVE-BEND.md` mix formula). **No reason is given for the mismatch with `extends`.** This is a taste fork for Ember: flipping `compose` to most-specific-first is a re-emit of every compose site. Task 01a10afe-eda1. |
| V3 | Under `compose`, an `around` of the lower operand wraps only its own chain (F02 = 12). LTUO's sub-methods would make it wrap the whole composed effective method (50012). | §9.2.4: sub-methods live in a record next to the method. The effective method is computed from self. | `docs/OBJECTIVE-BEND-TUTORIAL.md` §5, "Composing specs by hand" (rewritten in this lane to state it). FRONTEND guide: "the extension is the mix chain". F02 is pinned as a control (12). The LTUO-faithful design (hidden sub-method fields carried by the protocol) is task 01a10afe-ec03. |
| V4 | Templates, not polymorphic Core4 terms: an open extension is second class. | §8.4.3: first-class OO typing. | `docs/objective-bend/MODULAR-TYPING.md` §2 D1 (keeps every machine proof unchanged). |
| V5 | No subtyping. Rows are compared canonically and bounds are lower bounds (`supports`). | §8.1.3: partial record knowledge as subtyping. | `docs/OBJECTIVE-BEND.md` "Types and quantities"; MODULAR-TYPING D2. |
| V6 | Declared ancestry requires one target type across all ancestors. | §7.3.8: an MI spec must be a *strict* extension. Same-type is the conservative sufficient condition. | Elaborate `:1690-1693` refusal text ("declared ancestry composes one target type"). |
| V7 | `before`/`after` are refused in pure code. | §9.2.5: before and after methods exist for their effects. | `checkSpecMethods` message; FRONTEND guide (a pure one would be silently discarded). Existing task 01a1056f-00a4. |
| V8 | An effect inside a forced shared thunk is refused. | Scholar note §4: an effect while forcing a shared field needs a sharing-sensitive semantics. | `docs/OBJECTIVE-BEND.md` no-refusal row; OBJECTIVE-BEND-EVENTS. |
| V9 | Identity in the DAG is the qualified declaration key (static, generative per declaration). `compose(E, E)` applies E twice. | §7.3.3: specs are DAG nodes with identity; equal code is not equal identity. | FRONTEND guide, "Declared ancestry". |

### UNBUILT FEATURES

Each item lists its LTUO reference, its evidence of absence, and its task. "New" means a task opened in this review,
under `cv task list --repo ~/dev/minidregg`.

- **U1. Recursive conflation and a prototype that establishes its own provenance (LT4).**
  - LTUO: §6.1.3, Y(R∘M); §6.1.4.
  - Absent: `prototype` is a raw pair. Its typing `Ty.prototype spec target` relates nothing (`Theory/ObjectiveBendTypes.lean:23`). REFLECTION.md "Prototypes and provenance (LT4, open)".
  - Task: 01a10afe-eb86 (new).
- **U2. Behavioural associativity of `Term.mix` in the reference semantics.**
  - LTUO: §5.5.3, exercise 5.19.
  - Absent: `composition_associative` is list concatenation in a separate model (`Theory/ObjectiveBendExtensions.lean:76`), and nothing ties it to `Term.mix`. REFLECTION.md states the claim as a DRAFT.
  - Task: 01a10afe-ebb1 (new).
- **U3. The C4 proof package and `OrderedPresentationInvariant`.**
  - LTUO: §7.3.5, §7.4.4.
  - Absent: `Compiler/ObjectiveBendC4.lean:150` is a `Prop` that nothing proves.
  - Task: 01a10500-6ea2 (existing). GPT-6 already covered this.
- **U4. The remaining simple combinations and user-defined method combinations.**
  - LTUO: §9.2.6 (`progn`, `min`, `max`, `list`, `append`), §9.2.7.
  - Absent: the `combination` table covers `+ * and or` only.
  - Task: 01a10afe-ebda (new).
- **U5. Qualified methods under mixin `compose`, via sub-methods** (the LTUO-faithful version of V3).
  - LTUO: §9.2.4.
  - Task: 01a10afe-ec03 (new).
- **U6. First-class multiple inheritance**: parents as values, runtime C4 over generative node identities (`make-poi`).
  - LTUO: §7.4.6.
  - Absent: a parent must be a declaration (Elaborate `:1100`, "is not a spec declaration").
  - Task: 01a10afe-ec2c (new).
- **U7. Local order as a partial order** (a list of lists of parents).
  - LTUO: §7.3.5.4.
  - Absent: `precedence` passes `[parents]`, one total chain (`:1115`).
  - Task: 01a10afe-ec56 (new).
- **U8. Sealing / `final`, and static dispatch derived from suffix and sealing.**
  - LTUO: §5.5.4, §9.4.4, §10.4.2.
  - Absent: overview "Further gaps".
  - Task: 01a10afe-ec7f (new).
- **U9. Optics and focused, nested specifications.**
  - LTUO: §9.1.4–9.1.6.
  - Absent: no field-spec / focus combinators; nesting is by hand with `extend`.
  - Task: 01a10afe-eca7 (new).
- **U10. Multiple dispatch (multimethods).**
  - LTUO: §9.3.
  - Absent: no construct.
  - Task: 01a10afe-ecd0 (new).
- **U11. Class OO: prototypes for first-class type descriptors.**
  - LTUO: §6.2.
  - Absent: types are static only.
  - Task: 01a10afe-ecf9 (new) (decision).
- **U12. Surface semantics and lowering preservation (LT3 / OB1).**
  - LTUO: §5 (the meaning of mix and fix in source).
  - Absent: OBJECTIVE-BEND.md "Front-end adequacy" is open.
  - Task: 01a10afe-ed23 (new) (LT3 row). GPT-6 covered this.
- **U13. Ecosystem extension (LT5) and dynamic `get` by label.**
  - LTUO: §9.2.9, §9.3.7.
  - Absent: overview roadmap item 5.
  - Task: 01a10afe-ed4d (new).
- **U14. Laws checked or discharged (LT6) and checked `requires`.**
  - LTUO: §8.4.2.
  - Absent: law status is always `unchecked`.
  - Task: 01a10500-6f6f (existing).
- **U15. Ancestry specs in partial-seed or open chains (LT2 item 7), and `instance_accepted` (LT2 step 5).**
  - LTUO: §8.4.1.3.
  - Absent: chainFix takes plain specs only.
  - Tasks: 01a10a62-36f9 and 01a10a62-36cb (existing).
- **U16. Open specs that carry a protocol** (combine and around over `Self`, follow-up of D5).
  - LTUO: §9.2.4 with §8.4.
  - Absent: D5 now refuses this.
  - Task: 01a10afe-ed78 (new).
- **U17. Meta-object protocol: introspection and intercession beyond `metadata`/`reflect`/`targetOf`.**
  - LTUO: §10.6, which is only an outline in the book.
  - Absent: REFLECTION.md observers table.
  - Task: none. The book has no content to build against yet. Tracked by LT4.

### OB7 call and OB8 send (queued, read at 65b022e2 and lane/ob8 65064ab9)

Neither adds a Core4 constructor, a machine frame or a typing rule. Neither range touches
`Theory/`; OB8's diff is in `Kernel/`, `Host/`, docs and a journey. A cross-object
`call` or `send` is a Plan label that a method yields and the kernel answers in the
same turn:

- `call` is answered with `returned`.
- `send` is answered with `queued {slot}`.

So the OO calculus stays the pure lazy mix/fix core. Messaging is the kernel's, outside
the calculus. This **agrees** with LTUO §3.1.6, "OO isn't Message Passing": message
sends are one way to invoke a method, not what makes something object-oriented, and
the message-passing picture leaves no room for multimethods.

For the calculus, the lesson goes to U10: if multiple dispatch is ever built, it belongs
to the calculus, not to `send`. Neither range has an LTUO discrepancy.

## What the fix breaks (flag day)

- **Source.** A `combine q m` contribution now requires the target record to declare `combine q m`.
  The packages in this repo that used one are re-authored in the lane:
  - `tests/objective-bend-source/Ancestry.obend`
  - `docs/tutorial/ch5-ancestry.obend`
  - `world/collective/CollectiveAdoption.obend` (record `Rule`)
- **Refusals that are new:**
  - `combine-undeclared`
  - `combine-qualifier`
  - `combine-next`
  - `open-qualifier`
  - `protocol-ambiguous`
- **Meaning:**
  - `combine and` and `combine or` short-circuit.
  - `compose` of combined specs keeps every contribution.
  - A seed's value for a combined member is ignored.
- **Front-end identity changes.** Re-genesis for published Objective packages. The interface label changes for every
  declared spec: no spans, qualified parents. The re-emitted packets are EvenOddTen.typed.json and
  TwiceReview.typed.json, plus three tutorial outputs.
- **Elaborator API.** `interfaceLabel` takes the parent keys. `Signature` gains `qualifier`.

## Lane, evidence and status

**Lane.** hbox `/tank/dregg-build/claude-lanes/ob-review/src`, branch lane/ob-review. The base is main 5d0b452d with
the ob-ltuo stack (to ed3e9f58) and parser 291875da cherry-picked onto it. The fix is one commit on top.

**Executed** with the edited Parse and Elaborate compiled into a private overlay over gate n3's oleans:

| Check | Result | Note |
|---|---|---|
| fareoo probes | 10/10 at target | |
| check-elaborate | EVERY OBEND ELABORATES: 36 | |
| check-parser | 36 | |
| preview cohort | passed | |
| world cohorts | all 12 world cohorts pass (ballot bounty collective commons drex dues market play station story workshop + market-cohort) | |
| tutorial | 71/71 after re-pinning the 3 intended outputs | |
| LTUO probes | 26/27 at their pins | S4a differs only because the overlay's FrontEnd olean predates s4's `checkTemplates` |

**Not yet run.** hbox build-slot-2 is paused for fn's release image, per HBOX-HOLD. Still to do:

1. The real `lake build` of the front-end targets and `ObjectiveProofs`, including the new `Compiler/ObjectiveBendCombination.lean`.
2. `check-objective-proofs.sh proofs --update` (new statements).
3. The example drivers.
4. The full `check-objective-frontend.sh`.

These run in slot-2 when the root reopens it. The queue line follows the build.
