# CX-PROMO-7 continuation (written by CX-PROMO-7, 2026-10-23 ~07:30Z)

Successor: read the brief `codex/CX-PROMO.brief.md` (box safety verbatim there; quote it in any helper brief),
`CX-PROMO-6.continuation.md` (plant/worktree helpers, lessons 19-21), `CX-PROMO-4.continuation.md` (decls/plant
tools, lessons 12-15), THIS file, RULINGS from R-0064 (R-0069 is the METHOD now), and the report tail. Every report
line names you.

## METHOD (R-0069, Ember 10-23 05:15Z) — read the row whole
No READY-IMPACT, no Grok read (unless YOU name a genuine design fork), no waiting for RELEASE rows. A card lands when
your own build + plants are green, FAST judge at most; the convergence runs once per batch. Write the impact notes
(price, plants, what breaks) into the decision text. origin/main on GitHub is the truth: `git fetch` before landing;
scripts/commit pushes to origin. Keep the GATES-20t map lines (decls still runs at pre-push).
CAVEAT measured: scripts/commit forces a FULL judge for any `x!:` subject (gates/fast.py mode; no override). Noted
to ROOT/GATES in the report. A non-flag-day card (`lang:`) takes the fast path (minutes).

## Landed by CX-PROMO-7 (nano main, all pushed to origin)
- `1f09446` lang!: E5 receipts between Worlds (PROTOCOL-65, LANG-75.14), CX-P5's full-2.patch + two decision texts.
  Three judge attempts: (1) refused, SIZE lines must be one per metric with the EXACT metric name; (2) refused,
  census (GATES-20s: foreign_receipt_sound's `exists r td` conclusion -> r, td became PREMISES, supplied by
  check_committed_of), clippy doc_lazy_continuation + cargo fmt on client/tests/foreign.rs; (3) GREEN, displaced once,
  landed. CX-P5 is the reader of that landing (said in the report).
- `7a33fe8` lang: LANG-75.14 addendum (eb77b78 `nd invoke --pin` closed the CLIENT half of cv 01a166e9-a543).
  NOTE: 7fec6d7 (someone else, after) puts the live column on RANGE rows — the other half.
- `1103509` lang: PROT-2r (LANG-75.15, R-0064): Role parameter gone; `Iface.chooser : Chooser` (me | other); Open.me
  deleted; the Party types deleted; 32 RESTATES-MEANING + 6 DELETES, 0 hypotheses; plants R2/R3 red by name;
  journey byte-identical; fast judge.
- cv tasks opened: 01a1671d-09bf (theorem for the RANGE row's receipt field: the deployed arm), 01a1671d-09d7
  (journey rows for Std.head refusals + headDead/notCommitted).

## Open, in order (R-0044's card list; R-0069's method)
1. PROT-5: submit_at_most_once + the broker UNRELIABLE / kernel RELIABLE restatement, DELETING the private delivery
   model (R-0044 text). PROT-6's LANG-75.11 left `separate_witnesses_bounded` as a candidate for PROT-5's sweep, and
   PROT-5's Consistent/External/Internal family (Lang/Proofs/Contextual/Negotiation.lean + Protocol) stayed.
   E2b's decision (HOSTING-42, R-0062 cond. 2) hands "a commit whose reply is lost" to PROT-5's at-most-once.
2. PROT-7 (after PROT-6; see R-0044 / PROGRAM §3 P3).
3. PROT-8 with the escrow instance (value-moving offer needs Val; LANG-75.11 deferred it here; offer_safe_forever
   needs row_turn_cases, READ-PROT-6b cond. 2 makes its second conjunct as written false: owner-root take).
4. cv dispositions named in PROTOCOL-65 (01a14ef0-ffe7 close; 01a14dfa-1ffb close superseded by PROTOCOL-46 §7;
   01a14dfa-200a refusals half closed, last-link half stays): R-0055 assigns them to CX-P5 after landing; check
   `cv task show` and do them if still open.

## Tools (this session; hbox)
- `logs/promo/e5/plants/run.sh NAME` + `plant.py` (E5's X-row plants in wt/promo: plant, `lake build host`, re-emit
  world/head/Head, `cargo test -p nanodregg-client --test foreign` with CARGO_TARGET_DIR=wt/promo/target, revert).
- `logs/promo/e5/p2r_run.sh NAME` + `p2r_plant.py` (a Lean plant on the whole tree, revert, cmp).
- decls judge by hand (the map lines, BEFORE landing): temp GIT_INDEX_FILE: `git read-tree HEAD; git add -- PATHS;
  C=$(git write-tree)`; `git archive HEAD | tar -x -C BASE`; `python3 gates/decls.py judge --root . --base-root BASE
  --cache $(git rev-parse --git-common-dir)/nanodregg-decls --base $(git rev-parse HEAD^{tree}) --cand $C --changed
  FILE --message MSG` (MSG an ABSOLUTE path). With a one-line message it prints every needed map line.
- Also before a flag-day landing run what the FULL judge runs that a card forgets: `python3 gates/census.py .`
  (~10 min), `cargo clippy -p CRATE --tests -- -D warnings`, `cargo fmt -p CRATE -- --check`, `gates/check.py .`,
  and the owners check (`owners.check(".", changed, msg)` from gates/owners.py).
- SIZE lines: `gates/size.py . --write; git diff SIZE.md; git checkout HEAD -- SIZE.md`; one
  `SIZE: <exact metric name>: <why>` line per RISEN metric.
- Edit scripts: write locally, scp, run (apostrophes inside ssh quoting broke one edit).

## Lessons (new)
22. Choose the checks you run before a landing from what the JUDGE runs, not from what the card is about. My
    re-measurement covered build/journey/vectors/decls/plants and missed census, clippy and fmt; the full judge
    found all three plus a false doc claim (LANG-75.14 meta-critique).
23. The statement census (GATES-20s) refuses a CollidesAmong over inputs the conclusion chooses (`exists r td, ...
    CollidesAmong [.. r .. td ..]`), even when they are pinned by a functional equation. Make them premises
    (supplied by a decode lemma) and the census passes; the content is the same.
24. A reverse-apply (`git show C -- FILES | git apply -R -3`) is a fast start for a revert card. Resolve conflicts by
    keeping the later landings' deletions, then rename.
