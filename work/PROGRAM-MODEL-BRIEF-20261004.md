# Program model — scholar brief (2026-10-04)

## Ember's steer (verbatim, 10-04)
"calls across objects we gotta support in some how some way and very rich, we want more laws and
contracts, we want more concurrency, and we don't mind the checkpoint/heap design. but these are each
really deep topics and we would spend a lot of time on them if we were wise ;) but getting you to find and
read the best/newest/most important papers here is vital before we spend a lot of time trying to discuss."
Also: "bread offered an interesting take on these things (or maybe it didnt) with regards to its cells and programs..? idk."

## The system (READ facts)
Mini: a small world computer. Lean 4 owns semantics and admission: a single Host process admits each
signed invocation by RE-EXECUTING it deterministically (no proof system in admission). Rust is the
client/custody boundary only. State is a store of cells (one sparse Merkle root); each cell has a LAW, a
decidable predicate (difference-logic fragment, with satisfiability checks and refusal explanations) that
judges every write. Turns are atomic. Multi-machine: a Simplex BFT mesh (n=4, f=1) exists for committee
domains; genuinely multi-party domains are the goal. Greenfield: re-genesis is free.
Language: Objective Bend, core "Core4": lazy call-by-need demand machine (stepRaw/runBounded), general
fix, Fare-style specifications/mixins/prototypes with one final self and super, reflection, sums,
and ACTIVITIES (perform plan / yield / resume with a typed response; effects are a type
Activity<P,R,A> so they cannot hide in shared thunks; an exact checkpoint codec of the whole machine
state). Certifying type checker; adequacy, preservation, completeness and data-soundness proofs.

## The proposed model (root's, to be stress-tested)
- Package = published .obend source + checked core, a read-only content-addressed cell.
- Object = a cell holding state (Core4 data) + law + pinned package hash + current activities.
- Method call = a signed invocation; admission re-executes the method; it returns a Plan (a sum of
  typed actions); the kernel applies the Plan atomically; every target cell's law judges the actions
  touching it. Code proposes, law disposes.
- Resident = an object with a running activity: yields a Plan + what it awaits (reply, message, time);
  kernel stores the checkpoint; each resume is one admitted, paid turn (a guarded fixed point).
- Presentation = a projection: a card is an authorized view plus affordances (the methods this viewer
  may invoke); web/Discord/AI-resident render the same projection.

## The forks (Ember wants these RICH, not minimal)
1. Calls across objects: root leaned "reads + pure calls in-turn, effects only via the Plan, async
   messages between residents". Ember: support them "somehow and very rich".
2. Laws and contracts: more of them; the law language (keep the decidable predicate language, generate
   it from .obend, or unify into a decidable Objective Bend fragment); behavioural contracts, requires,
   laws as checked evidence, future-indexed certificates.
3. Concurrency: more of it; several activities per object; how they share state; optimistic vs
   locking; deterministic parallel execution of independent turns; multi-party atomicity across domains.
4. Evolution: governed upgrade of an object's package with typed migration.
5. Checkpoints/heap: Ember is fine with the design (full machine state, GC at yield, storage charged).

## Deliverable rules
Write ONE file at the path your brief gives. Every claim about a paper cites it (authors, year, venue,
URL) and, if you downloaded it, its ~/paperbin path. Tag READ (you read the paper/code), SKIMMED, or
INFERRED. Prefer the best, newest and most important work (2018-2026 heavily, classics where they are
the foundation). For each idea: what it is, the evidence it works, what it would mean concretely for
Mini's model (which fork, which decision it pushes, what we would build), and its cost.

## Tools
- Kagi search: `KAGI_API_KEY=$(grep -E '^KAGI' ~/dev/allgame/.env | cut -d= -f2-)` then
  `curl -s -H "Authorization: Bearer $KAGI_API_KEY" "https://kagi.com/api/v1/search?q=<urlencoded>"`
  (JSON: data.search[] with url,title,snippet). Be frugal: ~40 queries max.
- Scry: the scry MCP tools if your harness exposes them (mcp__scry__*: sql, find, fetch; key in
  ~/.scry-key). Use for HN/Reddit/forums discussion and for finding papers.
- Papers: cryptography/ePrint papers come from the LOCAL MIRROR ~/dev/gh/forks/IACR-eprint-mirror/<year>/<number>.pdf (never fetch eprint.iacr.org). Others: download PDFs to ~/paperbin/world-program-model/<firstauthor>-<short-title>-<year>.pdf and
  extract text beside it with `pdftotext -layout X.pdf X.txt`. arXiv: https://arxiv.org/pdf/<id>;
  ePrint: https://eprint.iacr.org/<year>/<n>.pdf. $ANNAS_SECRET_KEY exists for papers behind paywalls;
  use it only if the paper is clearly essential. Read the .txt with your file tools.
- Do not edit any repository. No builds. No paid provider calls beyond Kagi/Scry.
