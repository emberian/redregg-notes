# GLM experiment 2 — Claude baseline (Opus 5.5), 2026-10-22

Task: make the statement census able to go red on a real vacuous theorem, with a plant that bites and a
control that does not over-fire. Wall time: 15:29:32 → 15:40:38 EDT (about 11 minutes, one agent, no subagents).
Result: an unlanded diff in `/private/tmp/claude-501/-Users-ember-dev-breadstuffs/3a1e01fe-da72-4c08-b7dc-2de77511c341/scratchpad/base2-nano` (base 7e02852 = origin/main of ~/dev/nanodregg),
also saved as `/private/tmp/claude-501/-Users-ember-dev-breadstuffs/3a1e01fe-da72-4c08-b7dc-2de77511c341/scratchpad/base2-final.patch`. Plant sources and logs: `/private/tmp/claude-501/-Users-ember-dev-breadstuffs/3a1e01fe-da72-4c08-b7dc-2de77511c341/scratchpad/plant/` and on hbox
`/tank/dregg-build/nanodregg/wt/base2/.lake/plant/`. Nothing landed, nothing committed, nothing written under hbox logs/.
I did not read PROGRAM-20261022.md, REVIEW-20261021.md or any redregg memo.

## What I ran (verbatim, in order)

1. `git -C ~/dev/nanodregg fetch origin`; `git clone -b main ~/dev/nanodregg /private/tmp/claude-501/-Users-ember-dev-breadstuffs/3a1e01fe-da72-4c08-b7dc-2de77511c341/scratchpad/base2-nano`; `git reset --hard origin/main` → 7e02852.
2. Read gates/census.py, Census/Statements.lean, decisions/gates.md (GATES-4, -15, -20k, -23 and the plant convention), scripts/plant's header, Kernel/Proofs/Fold.lean (CollidesAmong, Separates), Kernel/Proofs/Trie.lean (CollAmong), `git show 482aecc` (KERNEL-56) and `git show 7e02852` (GATES-23).
3. Grepped every `CollidesAmong` conclusion in Kernel/Host/Protocol for the shapes S takes.
4. hbox: found main at f8d04ac (39 commits ahead of 7e02852; `git diff 7e02852 f8d04ac -- Census/Statements.lean gates/census.py` empty); found `wt/cxfold` a clean, fully built f8d04ac tree (563 oleans, no recent writes) and used its oleans READ-ONLY through LEAN_PATH instead of building the tree; read `logs/kernel21-ver-pigeon.lean` (KERNEL-56's pigeonhole proof).
5. `git -C /tank/dregg-build/nanodregg/main worktree add /tank/dregg-build/nanodregg/wt/base2 main`; applied the diff; `SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 swarm-build lake build Census.Statements` (the target, not `lake build Census`: at f8d04ac the Census lib grew certificate modules, and only Statements was under test). Locally: `lake build Census.Statements` (it imports only Lean).
6. Plant: `.lake/plant/run.sh old|new` under `SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2 swarm-build`: compiles `Plant/Vacuous.lean` with `lean -R … -o`, writes the run file from gates/tree.py exactly as census.py does (only the `#statement_census` line), runs `lean` on it. `old` puts main's Census.Statements.olean first on LEAN_PATH, `new` mine. Then the same run with the plant import removed (tree-only control).
7. Harness mutations (local): equation test `&& false`, then the membership bound `if false &&`; rebuilt, ran the fixtures, restored from a saved copy (md5 of the tested file = the clone's: 10a6a136…).

## What I found

- **The belief is right, and the cause is simple.** GATES-23 flags an existential containing a constant named exactly `Collision`. KERNEL-56 (482aecc, 10-18) deleted `Collision`, `Trie.Coll` and `HashColl` two days before GATES-23 (7e02852, 10-20) landed. The rule matches nothing the tree can contain; its plant declared a fresh `Collision` to make it bite, so it planted its own fixture, not the class.
- **Measured, not inferred.** Main's census over the whole built tree plus three real vacuous theorems: `STATEMENT-CENSUS ok: 171 disjunctions`, all three plant rows `ok`, exit 0.
- Second blindness: it reads only a conclusion whose OUTERMOST connective is `∨`; a disjunction under `∧`, `↔`, `∃` or a definition of the tree was never listed (78 theorems with such disjunctions were invisible).
- The real plant exists in-repo history: KERNEL-56's `lawful_collision` proves the old escape from `E.Lawful` alone. I reused it with the conclusion written inline.

## What I decided, and why

1. **Key on the shape, not a name.** RED = a digest equation `f a = f b` (same head, different args) whose two sides BOTH mention variables the statement chooses (an `∃` of the disjunct or the conclusion) that no conjunct `t ∈ L` bounds to a list of the theorem's own objects. Why: that is exactly the pigeonhole shape that is provable without premises; `CollidesAmong hash S` / `Trie.CollAmong` unfold to `∃ p ∈ S, ∃ q ∈ S, …`, so the sanctioned forms read ok over own lists and RED over a chosen list (`∃ S, CollidesAmong hash S`) with no special case. A name list (Collision/Coll/HashColl) was rejected: it would repeat the failure on the next rename.
2. **Walk through ∧/↔/∃ and up to four unfoldings of the roots' own definitions**, so an alias (`def Escape …`) is read through its body. Why: aliases were GATES-23's own named gap.
3. **Fixtures inside every run (GATES-15's known-red control pattern)** rather than a one-off log plant only: two statements must read RED, two must read ok, a misread prints `STATEMENT-CENSUS harness:`, which census.py already reads as red. Why: the original failure mode was a detector that silently stopped detecting; this makes that impossible to print as ok. Both detector mutations were caught.
4. **The first draft over-fired, and the control is what caught it.** "One chosen side suffices; membership only as the first conjunct of its own ∃" flagged five landed theorems: `Protocol.Settle.settle_refused_final/_absorbed/windowedIn_refused` (`∃ c' v a, recordOf X c' v a ∈ S ∧ txIdOf X c' = txIdOf X c`) and `Host.openWith_backup/_restart` (`∃ o' more, R = .ok o' ∧ o'.sealed = o.sealed`). I read each: none is provable on its own (one side is the theorem's object; Settle's witnesses range over S). I changed the RULE (both sides chosen; a membership guard anywhere in the ∧-spine bounds every chosen variable in its element term) instead of allow-listing them. I did not add an equation-pin rule (`R = .ok o'` bounds o') because no landed theorem needed it and every extra bounding rule is an evasion route.
5. **Number it GATES-23a** (an amendment, the repo's lettered style), since hbox main is 39 commits ahead and a fresh number could collide.

## Results

- Plant: `STATEMENT-CENSUS RED (3)`: `chain_binds_inline`, `chain_binds_chosen_list`, `chain_binds_alias` (each `right disjunct: \`E.hash … = E.hash …\` compares two inputs the statement chooses`); control `chain_binds_named` (the landed statement, `:= chain_binds hE`) ok. Each vacuous plant is proved by `.inr (lawful_collides hE)`, using no chain premise: a real vacuous theorem, compiled with exit 0 and no sorry.
- Control (tree alone): `STATEMENT-CENSUS ok: 250 disjunctions … (fixtures: 2 RED, 2 ok as required)`, exit 0; every theorem main listed is still listed; 81 `CollidesAmong` rows and 3 `Trie.CollAmong` rows read ok; 1.65 GB peak, 6 s.
- Diff: Census/Statements.lean (+147/-24), decisions/gates.md (GATES-23a: finding, decision, plants, critique, meta-critique, premise price), gates/census.py docstring (3 lines). census.py's verdict logic needed no change.

## What I did not do

- Did not land, commit or run scripts/plant / pre-push: `--no-build` skips the census, and `--build` would be a whole-tree build, which the brief forbids. The plant used the census's own module list over an existing built tree instead; a lander should re-judge it through pre-push.
- Did not build the tree, nor run the axiom/refine censuses (unchanged).
- Did not regenerate SIZE.md (scripts/commit writes it; a commit needs a `SIZE: Lean lines (Census)` line, +~147).
- Did not write plant logs into hbox `logs/`; they stay in the worktree's `.lake/plant/` and the scratchpad. The hbox worktree `wt/base2` is left in place (no deletes outside my scratch).
- Did not try to catch escapes outside this shape: a lucky second preimage, a closed list big enough for pigeonhole, contradictory premises, definitions outside the roots or deeper than four unfoldings, or a membership guard over a term that forgets its witness (`a.size ∈ L`). These are listed in GATES-23a's critique. The fixtures prove the classifier, not the environment walk; the printed row count is still the walk's evidence.

## Addendum (after the coordinator's message): landed as 98bf479

- Renumbered GATES-20s. The plant became standing: `gates/statement_plants.py`, a `script:` runs.tsv row with `--harness-control`, which also plants the in-run fixtures through a mutant census.
- `gates/size.py --write` caught four `partial def`s (law 4, ceiling 0). I made the walks total; past 256 connectives a statement fails closed as `not judged`.
- RELEASE G1 (R-0028) asked for Grok's projection-membership example to be named as the next tooth. I added it, verbatim, and filed it as cv task 01a1654c-543c.
- The first full judge refused the plant row twice: a `:` in the judge's {fresh} path split LEAN_PATH, and the census import wrote gates/__pycache__, which a concurrent row reads. My own runs had used colon-free paths and could not see the first. Both were fixed forward. The second attempt was GREEN, was displaced once by E1, was GREEN again re-based, and landed as 98bf479.
