# IMPACT-G2 — the 12 MB certificate re-pinned to what the theorem says and rests on (R-0053)

Worker: CX-G2 (Claude). Written 2026-10-22, BEFORE the build, for the cross-family read. Base: nanodregg `main` =
**1fc905f**; worktree `hbox:/tank/dregg-build/nanodregg/wt/g2` (made; nothing built in it yet). Measurements ran
READ-ONLY against wt/cxfold's built f8d04ac oleans (`Ledger/Proofs/GrantCap.lean` is byte-identical at f8d04ac and
1fc905f, MEASURED `diff`), scratch under `wt/g2/.lake/g2scratch/`. Card: PROGRAM-20261022 §3 P0 G2; REVIEW-20261021
H3 + H2; cv 01a16131-5868, 01a15f18-25f7. Grant R-0053 (gates/**, Census/**). Tags: READ / MEASURED / INFERRED.

## 0. Answer first

- **Pinned after the change** (gates/certificate-grant.json, plain JSON, ~10.8 KB MEASURED, replacing the 11,961,094-byte
  .json.gz): for `Nanodregg.Ledger.Proofs.grant_moves_le_cap`,
  1. **statement**: SHA-256 of the reader's exact DAG encoding of its type (`Census.Certificate.expression`);
  2. **axioms**: the `collectAxioms` set (a whole-cone fact, so an axiom added anywhere in the cone still reds);
  3. **supports**: the constants its proof term references one level down (the reader's `dependencies` of the
     target body: 67 at f8d04ac, MEASURED), each with the SHA-256 of its statement (its type's encoding);
  4. **vocabulary** (NOT in the card; §2 is the measured case for it): the constants the statement names (48,
     MEASURED), each with the SHA-256 of its declaration payload (a definition's body; an inductive's shape plus its
     constructors' payloads), one level.
- **Derived on demand** by a new `#certificate_pin` command in Census/Certificate.lean, through `Census.Certificate.reader
  env` (lookup / typeOf / dependencies / references) over the built environment, and `collectAxioms`. No closure walk:
  **1.3 s, 1.5 GB** per run (MEASURED) against the old 119 s, 1.9 GB (MEASURED, the full `read` dominates).
- **What no longer reds**: any change in the cone that leaves (1)–(4) equal: a proof re-proved anywhere (plant P2), a
  definition two levels below the statement, a module move that keeps names, a toolchain bump that keeps those
  48 + 67 declarations' encodings. **What reds**: each of (1)–(4) by section and NAME (plants P1, P3, P4, P5).
- **Deleted**: the blob; the allow row (gates/size-allow.tsv keeps its header, zero rows); `contexts_distinguish` and
  `checkers_distinguish` (Census/Proofs/CertificateReader.lean:139,145: `congrArg` on a structure field, REVIEW H2;
  nothing references them, MEASURED grep: only `.git/nanodregg-*` judge copies); `#certificate_census` +
  `certificateJson` (their only consumer was this gate, MEASURED grep).
- **Price 0**: no landed theorem gains a hypothesis; none is restated. DELETES lines in §6.
- **Two ASKs (§7)**: A1 the vocabulary pin; A2 a CLIENT grant to delete devtools/certificate_environment_plants.py.
  One fork (§7 F1): what becomes of the closure reader once no gate reads a closure.

## 1. What the old pin did, and why it was red-in-waiting [READ gates/certificate.py, Census/Certificate*.lean]

`gates/certificate.py` re-ran `Census.CertificateReader.read (reader env) 200000 target`, which gathers the whole
reachable closure (statement + every type, value and shape dependency, proofs included), and compared every one of
the 6,857 declaration payloads, their order and the checker identity (Lean version + githash + direct imports) with
the gzip. So the row was a whole-cone change detector (H3).

Two further measured facts:
- **Fuel at 81%.** The gather pops 162,250 names for the 6,857-declaration closure (MEASURED, a pop-counting copy
  of the walk), against fuel 200,000. A cone 23% larger is `CERTIFICATE RED: fuelExhausted`, a second red-in-waiting
  of the same class. It goes away with the closure walk (the pin does no walk).
- **The statement's meaning cone is not small either.** The declarations reachable from the statement with theorems
  read by type only: 2,444 (1,269 in repo modules), MEASURED. Pinning that would keep most of H3's over-pinning (any
  Kernel definition under `audit`), so (4) is one level, not the cone.

## 2. Why a fourth pin: the card's three are blind to the theorem going vacuous [MEASURED, plant P3]

Plant P3 (a scratch copy of the real GrantCap.lean, §4): `MovesThrough`'s body gains `∧ False`, and `move_weight`'s
proof becomes `obtain ⟨…, hfalse⟩ := hm; exact hfalse.elim`. Then every `amt` is forced to 0 and
`grant_moves_le_cap` bounds nothing. Measured against the real pin:
- statement digest: **equal** (it names `MovesThrough`, it does not contain its body);
- axioms: **equal**;
- supports: **equal**, all 67 (`MovesThrough`'s type and `move_weight`'s statement are unchanged);
- vocabulary: **changed, exactly `Nanodregg.Ledger.Proofs.MovesThrough`**.

So the card's design (1)–(3) reads that edit GREEN. The 10-20 lesson (61 kernel binding theorems that bound
nothing) is this shape: words unchanged, meaning emptied. (4) costs 48 digests (~5 KB) and reds when a word the
statement uses is redefined. It does not see a redefinition two levels down (`Dispatched` under `MovesThrough`):
that is the stated cut (§8).

My first P3 replaced the body with `False` outright. That changed the statement digest too (the unused section
instance binders `[Ord D] [DecidableEq D]` fell out of `MovesThrough`'s type), so it was not a plant of (4) alone.
The `∧ False` form keeps the signature; the plant asserts statement/axioms/supports equal before reading (4).

## 3. The pin format

`gates/certificate-grant.json` (the name loses `.gz`: a reviewable text file, its diff is the re-pin's evidence):
```
{ "target": "Nanodregg.Ledger.Proofs.grant_moves_le_cap",
  "statement": "<sha256>",
  "axioms": ["Classical.choice", "Quot.sound", "propext"],
  "supports": { "<name>": "<sha256 of its type encoding>", … 67 },
  "vocabulary": { "<name>": "<sha256 of its payload [+ constructor payloads]>", … 48 } }
```
Sorted keys, one entry per line. SHA-256 is taken in Python over the strings Lean emits (GATES-20t: no hash is
equality inside Lean). The checker identity (toolchain, githash, imports) is NOT pinned and not stored: no field is
kept that nothing compares. A toolchain bump reds only if one of the 115 pinned encodings moved, naming it.

`gates/certificate.py SCRATCH [--harness-control] [--emit-pin PATH] [--check-json A B]`:
- writes `CertificatePin.lean` (`import Census.Certificate`, `import Ledger.Proofs.GrantCap`, `#certificate_pin`) in
  SCRATCH, runs `lake env lean` on it, digests the emitted encodings, compares section by section;
- RED lines: `certificate-pin: RED statement (live: <pretty statement>)`, `axioms +X -Y`,
  `supports changed/added/removed: <names>`, `vocabulary changed/added/removed: <names>`; GREEN is
  `certificate-pin: GREEN`;
- `--harness-control` adds an impossible axiom to the expected set and must read RED;
- `--emit-pin PATH` is the explicit authoring step; no verdict run writes the pin.

The Lean command refuses by name: `CERTIFICATE RED: missing target`, `not a theorem`, `no declaration for <n>`.

## 4. The plants — gates/certificate_plants.py, a `script:` row (every judge, after the build)

Each plant is a scratch copy of the REAL `Ledger/Proofs/GrantCap.lean` (read at run time from the tree), with
`import Census.Certificate` added and `#certificate_pin` appended, elaborated by `lean -R SCRATCH/<p>` so its module
name is `Ledger.Proofs.GrantCap` and its private names are the real ones (MEASURED: `_private.Ledger.Proofs.GrantCap.0.…`
equal). It imports the built Kernel/Lang oleans and NOT the real GrantCap module, so the names do not clash. Each
mutation asserts its site occurs the expected number of times before running (minted: a falsifier that stopped
falsifying). All measured on f8d04ac oleans, ~1.5 s each:

| plant | mutation | measured verdict vs the real pin |
|---|---|---|
| C0 | none | all four sections EQUAL to the real environment's pin (the copy route is faithful) |
| P1 | direct support's statement: `leftAt_of`'s `leftAt … = l` → `l = leftAt …` (callers `rw [← …]`) | RED supports changed `…leftAt_of`; added `Eq.symm` |
| P2 | deep proof: `left_falls`'s first `exact Nat.zero_le _` → `Nat.le_trans (Nat.zero_le 0) (Nat.zero_le _)` | GREEN (all four equal) |
| P3 | vacuity: `MovesThrough … ∧ False` | RED vocabulary changed `MovesThrough` ONLY (§2) |
| P4 | deep axiom: `axiom g2_plant_axiom : True` used in `left_falls`'s proof | RED axioms +`…g2_plant_axiom` only |
| P5 | target statement: `≤ left` → `≤ left + 0` | RED statement; supports/vocabulary added `HAdd.hAdd`, `instHAdd` |

- **P2 is the over-pinning measured as the thing removed.** `left_falls` is two levels down (a dependency of the
  direct support `spends_le_left`, not of the target). The plant asserts, through a plant-local probe, that
  `left_falls`'s payload differs between C0 and P2 and that it is in `spends_le_left`'s dependencies, so it is in
  the closure the old vector pinned whole: the old row would be RED, the new one is GREEN.
- **Comparator mutants**: a scratch copy of gates/certificate.py with the `supports` section dropped must read P1's
  pair GREEN, and with `vocabulary` dropped must read P3's pair GREEN (each asserting its text occurs once), so each
  section is the thing that reds its plant.
- `--harness-control`: P2 is additionally expected RED, which it is not: the row reads RED.
- Last line on success: `CERTIFICATE PLANTS GREEN`. A mutation site that moved (GrantCap.lean edited there) is
  `CERTIFICATE PLANTS RED: plant P<n> site moved: <text>`, loud and named (critique §8).

The gate row `script:gates/certificate.py {fresh}` changes its pass string to `certificate-pin: GREEN`.
`certificate-tests` (the generic reader's 15 synthetic cases) is untouched and stays GREEN (the two deleted
theorems are not used by it, READ CertificateReaderTests.lean).

## 5. Files

- `Census/Certificate.lean`: `#certificate_census` → `#certificate_pin path target` (~40 lines).
- `Census/CertificateData.lean`: delete `certificateJson` (and `namesJson` if unused); header comment updated.
- `Census/Proofs/CertificateReader.lean`: delete `contexts_distinguish`, `checkers_distinguish` and the `omit` line
  that exists only for them.
- `gates/certificate.py` rewritten; `gates/certificate_plants.py` new; `gates/certificate-grant.json` new;
  `gates/certificate-grant.json.gz` deleted; `gates/size-allow.tsv` row deleted; `gates/runs.tsv` (SHARED) two rows;
  `decisions/gates.md` GATES-20u (+ the 71db964 wording fixed forward: its body said the table was "seeded empty" and
  main "RED by design"; it landed with the row and main green).
- Under A2 only: `devtools/certificate_environment_plants.py` deleted (CROSS-LAYER: CLIENT).

## 6. Price and the map (GATES-20t)

- Landed theorems gaining a hypothesis: **none**. Restated: **none**.
- `DELETES: Census.CertificateReader.contexts_distinguish`
- `DELETES: Census.CertificateReader.checkers_distinguish`
- `DELETES: Census.Certificate.elabCertificateCensus`, `DELETES: Census.Certificate.certificateCensus`,
  `DELETES: Census.Certificate.certificateJson` (+ `namesJson` if it goes); the guard prints the exact list and the
  landing pastes what it prints.
- What breaks: the 12 MB vector no longer exists; `#certificate_census` no longer parses; gates/certificate.py's
  `--emit-vector`/old `--check-json` objects are refused (a .json.gz is not read). Re-emit: the pin, once, by
  `--emit-pin` from the built candidate. Nothing re-genesises.

## 7. ASKs and the fork

- **A1 (the brief, amended).** Pin (4) the statement's vocabulary, one level, in addition to the card's three.
  Evidence §2: without it the vacuity edit P3 is GREEN. Cost ~5 KB; reds when a word of the statement is redefined
  (Kernel `audit`, `World`'s fields, `ledgerLeft`'s body: 15 repo declarations + 33 core). Default if refused: the
  card's three, with P3 recorded as a known GREEN in the decision.
- **A2 (CLIENT grant).** Delete `devtools/certificate_environment_plants.py`: it imports gates/certificate.py's `emit`
  and `--check-json` over the old object, so it is broken by this change; no gate runs it (MEASURED grep); its three
  families are superseded: extra axiom → P4; unfolded constant → P3/vocabulary; the collectAxioms ⊆ closure-axioms
  coverage guard has no closure to check against (§8 (c)).
- **F1 (fork, ROOT).** With `#certificate_census` gone, the closure reader (`read`/`gather`/`accept`, the six
  theorems of Census/Proofs/CertificateReader.lean, Census/Proofs/Certificate.lean's two environment theorems,
  `certificate-tests`, devtools/certificate_plants.py) has no consumer over a real environment: it is LANG-P6's
  "exchange certificate" demonstration, exercised only synthetically. (K) keep it as that demonstration, and cv-task
  the question; (D) delete it in this landing. Default taken: **K** (the card is the re-pin; deleting a proved
  component is a scope a reader should rule on). K leaves exactly the "true and irrelevant" shape H2 names at
  component grain, and I say so in the decision.

## 8. Critique (the decision will carry it)

- (a) One level is a cut. A redefinition two levels under the statement (`Dispatched`, `auditStep`) is GREEN. The
  meaning cone is 2,444 declarations and is exactly H3's problem again; the cut is where the statement's own words
  end. Theorems ABOUT those deeper definitions own them.
- (b) The encodings are exact: a binder rename in the statement or a support's statement reds (the statement digest
  is not GATES-20t's binder-erased one). Cheap to re-pin, and the red names it; stricter than needed, never weaker.
- (c) The old adapter cross-checked `collectAxioms` against the axioms the closure held; with no closure there is no
  second reader of the axiom set, and `collectAxioms` (already a named trusted read-off in LANG-P6) is the only one.
- (d) The plants are tied to GrantCap.lean's text at six sites; an edit at a site reds the plant row by name until
  the site is updated. A fixture copy would instead rot against the Kernel; the real file is the better coupling.
- (e) Supports include core constants (`Eq.mpr`, `And.intro`, `List.zip`…); a toolchain bump that changes one reds,
  naming it.

**Meta-critique (the bias to name).** Executing the brief's letter: the card listed three pins, and my first draft
had three. The measurement that refuted it (P3) was one I added to test the plant harness, not to test the card.
The opposite pull is also live: having found one blind spot, wanting the whole meaning cone, which the 2,444
measurement shows is H3 again.
