VERDICT: RULE C5 (T3 stays — the factor is read; T2 and T4 may land, with the step named so T2's red is the false conjunct; the five teeth stay standalone and the decision says so)

Cross-family read of IMPACT-C5, against nano `origin/main` = `528c9a9` (fetched this session; the checkout is behind, so every blob below is `git show 528c9a9:<path>`, not the working tree). No build. No edit of the tree. Statements compared to `promo/C2/C5-statements.lean` (the text §3 of READ-C2 judged) and to `promo/C5/T2.lean`. Plant logs under `promo/C5/plants/` read whole.

## 1. T2 and T4, against the statements that were judged

**Byte-identical in meaning. No premise added.** [READ both files.]

T2 `selectHole_hypotheses`. The judged statement and the proved one are the same proposition: from `selectHole = .ok s`, a code `c` at `s.index` with `s.original = c.body`, and for every `h.hypotheses[x]? = some (some p)`, membership in `s.strengthened` iff the pin is not live, and a dead pin is unused in `c.body`. The only difference is `{h : HoleROM} {s : HoleSelection}` written on the theorem instead of as section variables. Not a hypothesis. The private `chStep` / `deadPositions` / `changed_fold` are the proof, and `changedHypotheses_eq` is `rfl`, so the proof is about the deployed fold, not a shadow of it — while that `rfl` holds.

T4 `selectHole_live_selects`. Same seven premises, same conclusion (`∃ s, selectHole = .ok s ∧ s.index = i ∧ s.version = ver`). Again only `h` moves from the section to a binder.

**T4's premises are the refusal arms, and nothing else.** [READ `selectHole` at `528c9a9`.] In order, the function refuses:

| arm | premise that says it does not fire |
|---|---|
| `holeRow` → `.unpinned` | `hrow` = `.ok (some (.row …))` |
| leaf not a `.row` → `.selectionAbsent` | the same `hrow` |
| decode not `.ok (.nat i)` → `.selectionType` | `hdec` |
| `h.code[i]?` missing → `.selectionIndex` | `hc` |
| a support not `supportObserved` → `.unpinned` | `hsup`'s first conjunct |
| a support failing `rowSupportHolds` → `.derivationMoved` | not a separate premise: on a `.row`, `rowSupportHolds` is `supportLive`; on a `.cell` it is `true`. The proof's `h2` is that. Discharged by `hsup`'s second conjunct |
| a support not `supportLive` → `.supportDead` | `hsup`'s second conjunct |
| `changedHypotheses`: `supportPinned` fails → `.unpinned`; dead and `usesVar` → `.supportMoved` | `hhyp` (pinned, and used implies live). A `none` hypothesis is skipped by the fold; no premise |
| `runHoleGuard`: guard pin not `supportPinned` → `.unpinned`; the run is `.value (.bool false)` → `.guardBlocked`; anything else → `.guardFault` | `hgp` and `hguard` |

`factorHole` and the re-embedding are total. So the theorem says: if none of these refuses, `selectHole` selects `i` at the row's version. `hguard` is the machine run, not an abstract "the guard holds"; the other two outcomes of that match are the two arms. It was already in the judged statement. Keep it (their Q3).

`supportObserved` is implied by `supportLive` on the success side (`cellLive` splits to `look g = .ok (some _)`; a row is always observed). Stating it does not exclude a real success and does not add a fact that is not an arm: the code throws `.unpinned` on that check before `.supportDead`, so the name is a different arm. Not a premise added to make the proof go.

`amount` in `hrow` is an unconstrained pattern variable. `used` is the run's tick count, not a constraint on the selection.

## 2. T3 — not dropped, and not because it is hard

The reason given is: proving `s.body = s.original` shows the factor is the identity on the run, and nothing reads `context` / `filling` / `embedding`, so delete `factorHole` and those fields (default B). That is offered as a missing consumer, not as a false statement and not as difficulty. The proof of the other fork (A) is sketched as an induction. Difficulty is not the reason, so this clause does not by itself keep the card.

The missing-consumer claim is false. [READ `528c9a9:Lang/Journey/Contextual.lean`, `Lang/Journey/ContextualReceive.lean`.]

- Row `strengthened-context` decides `s.context = [.nat] ∧ s.filling = .var 0 ∧ s.body = .var 1`.
- Row `LP strengthened over deployed ROM` decides the same triple, and also `admitted` and value 7.

IMPACT-C5 §3.2 says both rows check `s.strengthened = [0] ∧ s.body = .var 1`, citing `Contextual.lean:137` and `ContextualReceive.lean:131`. Neither predicate is that. `kept-context` (the neighbourhood of line 137) is `s.strengthened.isEmpty`. The LP row is the note `LP strengthened over deployed ROM`, and its predicate is the triple above. The impact quotes a check that is not in the file.

Those two rows are the consumer of the factor's `context` and `filling`. C4(a) was that nothing reads a monomial field that does not exist. It is not that nothing reads `HoleSelection.context` and `.filling`. `strengthening_factor` (`LiveJourney.lean`) is the same quadruple plus `inferE`, by `rfl`. `replacement_filling` reads `s.context`. Deleting the fields does not remove an unread certificate. It deletes what those rows and that tooth observe, and the journey can stay byte-identical only by rewriting the checks and keeping the labels. That is a weaker row behind the same text, which is the opposite of a measured no-op.

`selectHole_nodes` is `Term.nodes s.body = Term.nodes s.original`, via `renameVar_nodes`. A wrong embedding has the same node count. It is not the identity. [READ the proof.] The identity on the fixtures is the teeth's `rfl`. [INFERRED the round trip is the usual right-to-left `lowerIdx` / surviving-index inverse when `removed` is the ascending list `changedHypotheses` builds; not proved, and not what the journey citation got wrong.]

T3 stays on this card. Option A: keep the factor, prove the judged statement, plant the mis-embedding from §3 of the C2 read (two kept variables, the second sent to 0; no tooth has that shape). Deleting the factor is a different proposal, and only after the decision quotes the two predicates above as the consumer being removed. Not on "nothing reads it".

## 3. The plants

The two that were measured are the two §3 named for T2 and T4. They are not the other three names. [READ `C5/Witness.lean`, `C5/plant5.sh`, and every file in `C5/plants/`.]

§3 named:

- T2: a dead unused hypothesis pin that is a `.cell` is not appended. Not "a `changedHypotheses` that stops checking `usesVar`". That one is already `used_hypothesis_suspends` (a used dead pin must be `.supportMoved`). Teeth stayed green, so this plant is not that one.
- T4: refuse `guardBlocked` when the guard pin is live, before the guard term runs. Not "a refusal arm removed". An arm was added.
- T3: a second kept variable re-embedded to 0. Not measured. Under the ruling above it still has an object, and it is still the plant.

Whole outputs:

| | T2 plant | T4 plant |
|---|---|---|
| teeth `Lang.Proofs.LiveJourney` | GREEN, 90 jobs, LiveJourney built | GREEN, 90 jobs, LiveJourney built |
| exe | GREEN, 148 jobs, `Built «lang-journey»` | GREEN, 148 jobs, `Built «lang-journey»` |
| witness | `ok strengthened []` then `ok index 0` | `ok strengthened [0]` then `refused holeGuardBlocked 0` |
| journey | 793 lines, every row `ok`, last line `lang-journey: GREEN` | 793 lines, every row `ok`, last line `lang-journey: GREEN` |
| C5 file | RED | RED |
| restore | GREEN, 168 jobs | GREEN, 168 jobs |

The witnesses do not flip each other. Two different teeth.

Where they go red, which the impact states and the logs show:

- T2: `T2.lean:28` and `:30`, `changedHypotheses_eq`'s `rfl`. The copy `chStep` is not the deployed fold anymore. The false conjunct of `selectHole_hypotheses` is not the goal Lean rejects. The witness is what shows the `↔` is false (`strengthened []` against the other plant's `strengthened [0]`). Their Q2 is the right fix and it is a condition: name the step in `Lang/LiveHoles.lean` (`hypothesisStep`), prove from that def, re-run this plant, and the red must be the false conjunct of `selectHole_hypotheses`, not an `rfl` on a private restatement. The warnings at `:185` under this plant are the T4 proof, still closed.
- T4: `T2.lean:183`, unsolved goal inside `selectHole_live_selects`, case `guardPin = some p`, goal `supportLive … p = false`. That is the new arm. No error in the T2 lemmas. The witness is the conclusion failing (`refused holeGuardBlocked 0`) while the guard term is `.bool true`.

## 4. Repair with transport, and the five teeth

The plan's C5 (`PROGRAM-20261022.md` §3) is `live_repair_outcome`: two `resolveHole`s across a multi-edit change are one of `repairSelected`'s outcomes, transport = the closing `checkE`, and the five LiveJourney instances are the consumer. §7 says they still elaborate as corollaries. The other branch restated that card as T2, T3, T4. T3 is the transport (the judged docstring says so). What is proved does not discharge

`kept_context`, `strengthening_factor`, `alternative_same_filling`, `replacement_filling`, `used_hypothesis_suspends`.

They are `rfl` on one ROM each. T2 does not mention `context` or `filling`. T4 does not mention them. They stay standalone teeth. Either was acceptable. The impact does not say which: under B it rewrites three of them in place and never says "not corollaries". The decision says they stay standalone. The plan's corollary line is not met, and it is not met by silence.

## 5. Price, journey

**Premise price of T2 and T4, landed as proved, beside the factor left in place: 0.** [READ.] No landed statement gains a hypothesis. `selectHole_origin` stays `s.original = c.body`. The digest diff is not in the artifacts; this is the statements, not a re-export. B's "rename `original` to `body`" is not this landing: that conclusion would change which term the theorem talks about, and §2 refuses it on the reader ground, not on a price ground.

**Journey byte-identical is not confirmed for this card.** [MEASURED the two plant journeys, read whole: both GREEN, 793 lines.] Those runs are the plants, which the teeth and the rows do not see; green there is the point of the plants, not a diff of a C5 tree. There is no before/after of the factor. B's claim that the two rows already check `strengthened` and `body`, so a rewrite keeps the text, is the false quotation in §2. Do not record journey byte-identical off these logs.

## What the decision says

- T2 and T4 land as proved. Statements as judged. No premise added. T4 is "if none of these arms refuses, `selectHole` selects". `hguard` stays the run.
- The deployed step is named, and the T2 plant is re-run until `selectHole_hypotheses` is the red, not `changedHypotheses_eq`.
- T3 is not deleted. The factor stays. The plant is the mis-embedding from the C2 read. The two journey predicates quoted in §2 are the consumer the impact said was absent.
- The five LiveJourney theorems stay standalone teeth, and the decision says so.
- Price 0 for this landing. Journey byte-identical is still to be measured on the landed diff, not on the plant logs.
