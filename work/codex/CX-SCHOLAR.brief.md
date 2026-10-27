Name: CX-SCHOLAR (run 3: a REVISION pass). READ-ONLY scholar: no worktree, no landing. A first run wrote
/Users/ember/dev/redregg/work/HOLES-FOR-PROOF-ENGINEERING-20261020.md (40K chars) from a CONDENSED copy of the GPT documents; your job
is to REVISE that memo IN PLACE against the RAW documents (below), keeping what survives and adding what the condensation lost; mark
every revised or new section `(rev 3)`. Append your REPORT lines to codex/CX-SCHOLAR.report.md (do not rewrite it).

EMBER'S ASK (real 2026-10-20): "regarding the deployed language and its holes we need to think about using these techniques for
the verification / proof engineering, because somewhat soon we'd be applying them to minidregg and then someday ~/dev/breadstuffs
proper. We should figure out how to make it more integrated; redesign days are always approved."

READ FIRST, whole, and BEFORE anything else: /Users/ember/dev/redregg/work/ACTIVITIES-GPT-RAW-20261020.md (the three GPT-6 documents RAW, 1,318 lines; the condensed ACTIVITIES-PROPOSAL file lost two thirds of them, including the parts this memo needs most: doc 1 §5 ludics/orthogonality as the guard, §6 the boundary theorem with its four strengths of preserved property, §7 stable-model alternative worlds and grounded cycles, §8 the algebra of checked repair with its three results and first-class repair objects; doc 2 §5 interface automata / alternating simulation and polarity, §6 'which proofs survive' with at_policy_revision-style transport and the reactive view's dirty-means-potentially-affected, §7 the four logical statuses incl. Refuted vs Outside-this-procedure; doc 3 §4 PUMPKIN Pi repair hints with mathematical content, §7 certificate acceptance explicit about the logic (OpenTheory), §8 the first integration experiment). Then the existing memo itself, then /Users/ember/dev/redregg/work/PROOF-ENGINEERING-20261021.md (the proof-engineering topic Ember liked),
ACTIVITIES-PROPOSAL-20261022.md (the GPT proposal: repair hints with pruning reasons, guarded holes as persistent interfaces,
typed substitution, response-dependent continuations, derivability vs admission), ACTIVITIES-DESIGN-20261022.md (esp. §9),
DECISIONS-20261021.md CARD 9 (Ember ruled (B): contextual holes in the deployed language, a redesign day), ACTIVITIES-LOG.md,
and on hbox main: Lang/Contextual/*.lean + Lang/Proofs/Contextual/*.lean (LANG-66/67/68: the CMTT core, the guarded contextual
closure with judge/provenance/repair/locality/the five outcomes, open protocols, the Lang instance), decisions/lang.md
LANG-66..68, gates/ (the judge: read-sets, convergence, the premise question), the memory rules quoted in LANE-RULES-NANODREGG.md.
Then minidregg's proof layout (~/dev/minidregg: how theorems depend on each other, how a redesign day re-proved them, the
`∨ Collision` sites cv 01a15630-cf43) and breadstuffs' (~/dev/breadstuffs/metatheory: the statement-audit and vacuity
campaigns in docs/, cv 01a15630-cf60; dregg2's premise spreads).

THE QUESTION: can the closure theory nano just proved (holes with supports and blockers, provenance as a polynomial, judge,
withdrawal never refuting, repair agreeing with from-scratch, locality, the five outcomes incl. strengthening) be the MECHANISM
of our proof engineering, rather than a thing our proofs are about? Concretely: (1) a theorem as a hole whose supports are the
landed theorems and definitions it depends on and whose blockers are the disjunct check / premise spread findings; a redesign
day as withdraw + repair, with "repair agrees with from-scratch" as the guarantee that re-proving after a redesign is the same
as proving fresh, and locality as the bound on what a redesign touches (= the premise spread we price by hand today); the judge
as an ATMS over the proof library. (2) What nano's judge (read-sets, the premise question, convergence) already is in those
terms, and what is missing (persistent hole objects for theorems? a Lean metaprogram that emits the support list per theorem =
its axioms + the constants it unfolds?). (3) The integration path: what to build in nano first (an experiment on nano's own
Kernel proofs), what minidregg would need to adopt it (its proofs are the same Lean 4), what breadstuffs would (a far larger,
older library with vacuity wounds). (4) The three things most likely to be wrong with this idea, each with the measurement
that would refute it. (5) Price it: premises added to landed theorems (should be none: it is tooling), the flag days (none at
the Lang level; a `(B)` hole-with-context lands anyway). Every claim tagged MEASURED / READ (path) / INFERRED. 300–600 lines.
Append `DONE` to your REPORT with the memo path.
