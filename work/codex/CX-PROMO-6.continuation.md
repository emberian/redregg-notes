# CX-PROMO-6 continuation (written by CX-PROMO-6, 2026-10-23 ~04:40Z)

Successor: read the brief `codex/CX-PROMO.brief.md` (box safety verbatim), `CX-PROMO-4.continuation.md` (plant/decls
tools, lessons 12-15), `CX-PROMO-3.continuation.md` (land.sh, SIZE rule, GATES-20t), THIS file, RULINGS from R-0059,
the report tail. Every report line names you.

## Landed by CX-PROMO-6
- `28e2d88` lang: E3 + PROT-6 (LANG-75.11; P4 M1/M2 as LANG-75.12/.13; KERNEL-45 item-3 amendment appended to
  decisions/kernel.md). R-0063. Evidence in `promo/PROT6/` (built.diff, decls-lines.txt, int-journey.txt, plants/).
  New modules: Lang/StdOffer.lean, Lang/Journey/Offer.lean, Lang/Proofs/{PeerRead,StdOffer,DispatchRows,StdOfferFuse}.lean.
- Said, not proved: the run-grain converse of take_iff_compliant (missing machine completeness at Bounds.stackMax and
  extract completeness, ~400 lines). Later cards: offer_safe_forever via row_turn_cases; the escrow instance (PROT-8);
  the deal binding the offer keys (JR finding in LANG-75.11); T (typed nested-call args, LANG-23 (iii)).

## NEXT: E5 as ONE lang! (R-0059; coordinator heads-up)
- CX-P5 posted `READY E5-PATCHSET` (codex/CX-P5.report.md line ~17): promo/E5/full.patch (51 files, +1610/-339),
  promo/E5/restates.txt (89 RESTATES-MEANING), promo/E5/commit-msg-draft.txt, promo/E5/decision-protocol.md,
  promo/E5/statement-diff.*. It APPLIES ON b4a7f38, i.e. BEFORE 28e2d88. Expect conflicts in the Lang half: E5 adds
  ONE Lang.program parameter (the receipt check) and `receipt : Option Label` on RelRead; PROT-6 changed
  Package.lean (rowsTy/rowsOf/methodPeer, CheckError.peerNotNamed, methodSig), Program.lean (peerOf, methodReads,
  runSetupWith) and the ten restated statements (methodSig_spec … runMeasured_means, setup_eq). A new RelRead field
  is a new anonymous-constructor arity: grep `⟨1, none, false⟩` (Lang/StdOffer.lean `offerRead`, and others) —
  lesson 17. The four new PROT-6 proof files consume RelRead/methodReads/Lang.program: they will need the ripple.
- Do: worktree wt/promo is at 28e2d88 + nothing (clean after the land; verify). Apply full.patch with `git apply -3`,
  fix forward; the decls map = E5's lines re-derived by running `decls.py judge` with an empty message (recipe in
  report line of CX-PROMO-6 / this session: temp GIT_INDEX_FILE, write-tree, judge --message empty) — restates.txt
  was computed against b4a7f38 and will differ. lang! => FULL judge (not fast), package wire 5 -> 6: every vector /
  package id re-emits; say what re-emits in the message. CX-P5 is the second reader of your landing: post a READY and
  wait for its read / ROOT's RELEASE before landing. If the rebase changes E5's statements beyond the ripple, ASK.

## Tools added this session
- `hbox:/tank/dregg-build/nanodregg/logs/promo/p6/mkwt.sh NAME`: a helper worktree = main + promo's diff + a copied
  .lake (515M; replays in ~1 s). Helpers in parallel worktrees with disjoint files worked well (five lanes, ~30 min).
- `logs/promo/p6/plantw.sh WT NAME FILE`: plant (NAME.old/.new, optional .old2/.new2) in worktree WT, whole build,
  journey diff, restore, cmp against wt/promo. `runplants.sh` ran seven in parallel over four worktrees.

## Lessons (new)
19. A plant that reds a red module leaves its importers UNBUILT: the fuse theorems were reasoned, not observed, under
    P1-P5. To observe a downstream theorem red, plant at a site the upstream proof does not unfold, or build the
    downstream module against a stubbed upstream in scratch.
20. A guard can turn a theorem's tooth into a journey row: P5 (retract -> upsert) never reaches the theorem because
    offer_guard refuses `final`. Ask which layer refuses first before assigning a plant to a theorem (lesson 14 again).
21. Brief helpers with exact statements and file ownership; send the veteran back (KD did the kernel lemma and then
    the fuse theorems on it).
