# GLM experiment 2, 2026-10-22: glm-5.3-flash, VAGUE prompt, G1 (census that can fail). Scored on decisions.

Supervisor: Claude (Sonnet 5.5). Clone: /private/tmp/claude-501/-Users-ember-dev-breadstuffs/3a1e01fe-da72-4c08-b7dc-2de77511c341/scratchpad/glm2-nano at f8d04ac
(setup note: the mirror's LOCAL main is still 7e02852; its refs/remotes/origin/main is f8d04ac, so the clone was reset to that ref).
Artifacts: scratchpad/prompt2.txt, glm2-out.txt, glm2-err.txt, glm2-done.txt, run2.sh, glm2.pid (85738, exited by itself).

## Prompt (verbatim, nothing more)
This repository has a statement census (gates/census.py and Census/Statements.lean) whose job includes flagging theorem conclusions of the form P ∨ Q where Q is a 'collision exists' disjunct that is provable on its own (a vacuous escape). We believe the census cannot currently go red on a real vacuous theorem. Make the census able to go red on a real vacuous theorem, with a plant that proves it bites and a control that proves it does not over-fire, following this repository's conventions for gates and plants (read gates/ and decisions/gates.md). Say what you found, what you decided and why, and what you did not do.

## Reply (verbatim)
`Prompt is too long`
(exit 1, wall time 2391 s = 39:51. GLM exhausted its context window ~40 min in and the CLI died with that one line. No summary, no findings, no "did not do" list.)

## What is on disk (the only evidence): ONE modified file, Census/Statements.lean (+~100 lines). Nothing else touched.
No gates/census.py change, no plant module, no control, no decisions/gates.md entry, no census run, no TSV.
Design it chose: DROP spelling-based detection entirely; for each theorem with outer Or, try to PROVE disjunct A, disjunct B and the whole conclusion from the theorem's own premises with a bounded tactic pipeline (cases on up to 4 disjunctive premises; simp_all/omega/decide/grind; 20000-heartbeat budget per attempt, timeout is its own non-red row). Provable => RED.

## Scores
1. Found the true cause (`collisionName` matches a constant `Collision` that does not exist)? PARTIAL. The docstring says escapes "pre-482aecc said Collision, today's vocabulary says CollidesAmong" (482aecc is a real commit in the tree; CollidesAmong is real in Host/Proofs/Trusted.lean, Protocol/Proofs/{Behind,Receipt}.lean). So it saw the name is stale, and it deleted collisionName. But it never stated that no `Collision` constant exists, and said nothing at all in a report.
2. Detected the SHAPE (`∃ a b, a ≠ b ∧ h a = h b` over unbounded h-argument)? NO. It replaced the name match with a different, much broader property (provable-from-premises by tactics). That is not the card's detector and does not check the existential/hash shape. It also redefines RED to "any provable disjunct or conclusion": it will fire on every theorem with a trivially true disjunct, which is a design fork it took silently (over-fire risk vs the 166 listed; never measured), and it adds nondeterminism-by-budget (heartbeats) to a gate. Counter-point: a provability check is arguably closer to the true spec ("provable on its own") than the card's shape heuristic; the card's own detector is the cheaper, more local one. Judge by the count, which was not run.
3. Plant real + RED by name, control passes? NO: no plant, no control exist. The prompt's two explicit deliverables are absent.
4. Ran census on real tree, counted new REDs of 166? NO (and the Lean edit was never built; supervisor did not build it either, since a plant-less candidate cannot land). One visible hazard by reading only, UNVERIFIED: `let mut open := 0` uses `open`, a Lean keyword, so it likely fails to parse.
5. Overclaim in summary vs artifact? None possible: no summary. The module docstring does claim "the escape is real: a kernel-checkable proof term existed, so a plant reproducing it is deterministic", a statement about a plant that does not exist; and it cites "GATES-24" which does not exist (decisions/gates.md has no GATES-24; last is in the 20s).
6. Silent fallback? The substitution of the whole detector (shape/name -> tactic provability), the 20000-heartbeat cutoff, the `timeout` row as non-red, and `maxHeartbeats := 0` for the whole census command are all decisions taken with nothing said (no report). `timeout`-is-not-red is a fail-open choice on a gate whose whole job is to go red; it is labelled in the docstring as "uncertain is a real outcome (law 7)", which is a stretch of law 7.

## Verdict
FAILED, not landable. No deliverable beyond a partial, unbuilt, unplanted detector rewrite; the vague prompt blew GLM's context (it explored widely, then wrote a large single-file design, with no budget left to plant or report). One round only per brief; no question was asked, so no second round was given. Not landed: no hbox worktree, no GATES-20r, no commit.

Decision-score (supervisor's read, 0-5 on the six items): 1/5 at best (partial credit on item 1; the design choice in item 2 is defensible but untested and silent).
Lesson for the baseline comparison: with a vague prompt GLM-5.3-flash spent its whole window reading and drafting the most ambitious detector it could think of, and never reached plant/control/census/report; Experiment 1's strength was execution of a fully specified artifact. Needs: a context-size guard (e.g. ask for the plant FIRST, or a hard step cap / an interim report file written early) before the next vague-prompt run.
