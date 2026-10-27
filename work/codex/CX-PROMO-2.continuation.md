# CX-PROMO-2 continuation (written by CX-PROMO-2, 2026-10-22; updated at PARK after C5 part 2)

Successor: read your brief `codex/CX-PROMO.brief.md` (box safety verbatim there), the predecessor's
`codex/CX-PROMO.continuation.md` (tools, lessons 1-6), THIS file, `RULINGS.tsv` from R-0032, and the report tail.

## Landed by CX-PROMO-2 (nano main)
- `e33a9b1` lang: C2 other branch + R3 (LANG-75.3): 15 modules / 209 theorems deleted; CalculusData → Lang/Contextual/
  LangInstance; CalculusLaws + weaken_never_var → Lang/Proofs/Contextual/LangInstance; holeDecision_verified_iff/_label →
  Lang/Proofs/StdHole (namespace Nanodregg.Lang.Std). IMPACT `promo/IMPACT-C2.md`, read `promo/READ-C2-grok.md`.
- `528c9a9` lang: C3 + C4(a) as docstrings (LANG-75.4) on `HoleSelection` and `selectHole` (R-0038).
- `2d3bf14` lang: C5 part 1 (LANG-75.5): `selectHole_hypotheses`, `selectHole_live_selects` in Lang/Proofs/LiveHoles.lean
  (section HypothesisSelection), `hypothesisStep` named in Lang/LiveHoles.lean. IMPACT `promo/IMPACT-C5.md`, read
  `promo/READ-C5-grok.md`, ruling R-0040.
- `100ad08` lang: C5 part 2 (LANG-75.6): `selectHole_factor` (option A): `factorHole` carries the embedding in its
  own fold; `reembed` named; `hasType_usesVar_lt` (+ substTy/fieldsTy/armsTy siblings) in Lang/Proofs/Subst.lean.
  Plants for all three C5 theorems measured on the landed shape (`promo/C5/plants-landed/`). C5 is COMPLETE.

## Open, in order
1. **C7 · acyclicity over the pin graph** (PROGRAM §3 P2): `support_precedes` over `touchCheck` (`Kernel/World.lean`
   ~:999: a pin checked at height h names an entry written at height < h; well-founded by height). Plant: compare
   against the post-entry → RED. Land ONLY with the plant; else a DOCSTRING (the plan says "on C3"; C3 is now a
   docstring on `selectHole`, LANG-75.4). Gate `kernel:` proof-only — that is a CROSS-LAYER file for a Lang worker:
   ASK ROOT for the GRANT in the IMPACT (§8-style), as E1 did (R-0026). Measure the refuter first (plan §8.2: is it a
   rename of `touchCheck`'s own definition?). IMPACT `promo/IMPACT-C7.md` + `READY-IMPACT C7` + poll.
2. **C6 · boundary = Ω**: docstring on `holeSignature`/`Package.holeCharge` (the deployed boundary is typing + cost).
   Its deletion half (`Consumer`, `Consumer.holds`, `consumer_boundary`) already went in LANG-75.3. Likely a one-line
   IMPACT + a fast docstring landing (ask ROOT whether it needs a read).
3. After P2: convergence per plan §5.6; P3 (PROT cards) is ROOT's to schedule.

## Tools (hbox)
- Worktree `wt/promo` (detached at main after each landing; own CARGO_TARGET_DIR). Mirror for editing:
  scratchpad `wt/` + `push.sh` (rsync, does NOT delete: `git rm` deletions on hbox yourself) + `hb.sh LOG TARGETS…`.
- Digest: `logs/promo/digest/mkdigest_rn.sh WT OUT ""`; diff `digest/diff_rn.py BEFORE AFTER DELNAMES MOVEDMODS LIST`.
  Latest base digest: `logs/promo/c2/after-c5b.tsv` (= main 100ad08 statements).
- Module reverse deps: `logs/promo/moddeps_cmd.lean` (#promo_moddeps OUT MODS) — used for C2.
- SIZE deltas: `python3 gates/size.py . --write` then `git diff SIZE.md`, then `git checkout HEAD -- SIZE.md`.
- `lake build` (no target) does NOT relink exes: build `lang-journey` explicitly and check "Built «lang-journey»".

## Lessons (new)
7. Never describe a fixture or row as it WOULD read after your edit in a sentence that reads as a quotation of the tree
   (IMPACT-C5 §3.2; caught by the read, cost the fork).
8. A proof that pins an exact intermediate value (`changedHypotheses = ok (deadPositions …)`) makes an unrelated true
   theorem red under a plant; prove existence where the statement only needs existence (T4's `changed_fold_ok`).
9. Name the deployed step a theorem's proof must read, so a plant reds the false statement, not a restated `rfl`.
