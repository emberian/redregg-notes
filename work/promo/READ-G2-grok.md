VERDICT: RULE G2

Do not land the card's three pins, and do not delete the certificate. Three conditions, then the six answers. Base: nanodregg `origin/main` = `1fc905f` (fetched 2026-10-22; local `main` is `7e02852`, 52 behind, and was not read). Every gate, census and certificate file below is that `origin/main`. No build. The 48 / 67 / 2,444 counts, the 1.3 s pin, the 119 s closure, and the ~10.8 KB JSON are IMPACT-G2's measurements, not re-run here.

Conditions:

1. **A1 is required.** The vocabulary pin lands with the other three. It hashes declaration payloads (the body), not a second copy of the type. Without it the measured vacuity edit is green, and GATES-20t does not catch that edit either. Default-if-refused (three pins, P3 recorded as a known green) is refused.
2. **F1 is delete, in this landing, not a cv task.** The closure walk, the theorems whose subject is that walk, `certificate-tests`, and `devtools/certificate_plants.py` go. The one-level projection `#certificate_pin` calls stays.
3. **A2 is delete.** `devtools/certificate_environment_plants.py` goes. Two of its three families are re-homed by the new plants; the collectAxioms-versus-closure coverage guard is not, and the decision says it was retired, not that P4 replaced it.

---

## (1) The fourth pin — A1 yes

P3 is not a failure GATES-20t already refuses.

The edit, as planted: `MovesThrough`'s body gains `∧ False`, and `move_weight`'s proof becomes an elimination of that false. [READ IMPACT-G2 §2; READ `Ledger/Proofs/GrantCap.lean:50-52`, `:188-198`, `:256-264`] `MovesThrough` is a `def` whose type is the telescope ending in `Prop`. The conjunction sits in the body. The theorem's statement names the constant `MovesThrough` and does not contain the body. `Dispatched` is named in that body (`:52`) and is not named in `grant_moves_le_cap`. So a body edit need not move the theorem's type, `MovesThrough`'s type, the axiom set, or the constants the proof term references. IMPACT measured those three sections equal and the vocabulary section changed at exactly `MovesThrough`. That run was not repeated here. The first plant (body replaced by `False`) is not this edit: it dropped the unused `[Ord D] [DecidableEq D]` binders out of the type and moved the statement digest, so it did not isolate the vocabulary pin. [READ IMPACT-G2 §2]

GATES-20t's direct diff refuses a vanished declaration and a theorem or axiom whose statement digest differs. [READ `decisions/gates.md` GATES-20t check 1; READ `gates/decls.py:187`, `:438-441`, `:521-528`] `STATEMENT_KINDS` is `theorem` and `axiom`. A non-theorem's value digest is computed and stored, and `same` compares it, but check 1 never calls `same` on a definition. The only forward refusal for a changed statement is the theorem/axiom branch. Check 2 compares a definition's type and value only for a lack the text detector already forwarded (`decls.py:568-572`): a stale copy of some prior commit, not a new edit of a body. A forward `∧ False` in `MovesThrough` is not a restatement of `grant_moves_le_cap` and is not a stale lack. 20t is green. The axiom census does not look at definition bodies. [READ GATES-4]

So the three pins and the two existing gates are the same blind spot: words of the statement unchanged, meaning of a word emptied. That is the 10-20 shape the worker cites. Recording P3 as a known green would land a pin that cannot see it.

The fourth pin is the right cut, and it does not re-pin the closure.

- It hashes the declaration payload, which includes `values` (the body) as well as the type. [READ `Census/CertificateData.lean:77-106`] A type digest would not catch P3: the type did not change, and the supports pin is already a type digest. Simplifying vocabulary to "the statement's constants, hashed like supports" makes P3 green again. The payload is the pin.
- One level is the constants the statement's type DAG names. IMPACT measured 48 (15 repo, 33 core), about 5 KB of a 10.8 KB file. Not remeasured here. The closure H3 pinned is 6,857 declarations and 11,961,094 gzip bytes [MEASURED `git cat-file -s origin/main:gates/certificate-grant.json.gz` = 11961094; the declaration count is LANG-P6's, READ `decisions/lang.md`]. The meaning cone IMPACT measured, theorems read by type only, is 2,444 declarations (1,269 in repo). Pinning that cone is H3 again. [READ IMPACT-G2 §1, §8(a); the cone size is IMPACT's MEASURED]
- It closes this P3 because `MovesThrough` is one of the statement's own words. It does not close the same edit one level further down: `∧ False` in `Dispatched` leaves `MovesThrough`'s payload naming `Dispatched` and not containing `Dispatched`'s body, so vocabulary stays equal. [READ `:50-52`; INFERRED from what `declaration` hashes] That cut is stated in the decision as the cut, not as a fifth pin and not as a cv task. Theorems about `Dispatched` own `Dispatched`. The meaning cone is how this pin becomes the blob it replaces.
- `grant_credits_le_cap` is the twin and is not pinned. A vacuity in `CreditsThrough` alone is outside this card. Do not widen the pin to it.

H3's own sentence was "pin a digest of the statement and its axiom set, and re-derive the context on demand." [READ REVIEW-20261021.md H3] Re-deriving the closure and comparing it is the over-pin. Re-deriving it and not comparing it is a reader with no consumer (F1). The program card added direct supports; the measurement added vocabulary. Both stay. Statement-plus-axioms alone is the design this read refuses.

## (2) What the certificate certifies

Not an offline check, and not an exchange certificate. `#certificate_pin` runs in `lake env lean` over the environment the gate just built. Producer and checker are the same process. LANG-P6's object (target, statement, closed context, assumptions, checker identity, compared payload-for-payload) had no deployed caller then [READ `decisions/lang.md` LANG-P6] and the re-pin does not grow one. Checker identity is correctly dropped: nothing compares it. A toolchain bump reds only when one of the pinned encodings moves.

After the re-pin, with A1, the consumer is the gate row `script:gates/certificate.py` [READ `gates/runs.tsv:57`]. It freezes one theorem, `Nanodregg.Ledger.Proofs.grant_moves_le_cap`, against four identities. Two of them are not what the census and GATES-20t already decide:

| pin | census | GATES-20t |
|---|---|---|
| statement digest | no (GATES-20s classifies disjunction shape; it does not pin this statement) | an undeclared restatement is refused; a `RESTATES-MEANING` line lands. The pin still reds until `--emit-pin`. That is a freeze of one named theorem, secondary to the two rows below. |
| axiom set | a new axiom outside `propext` / `Quot.sound` / `Classical.choice` is already red for every tree declaration [READ GATES-4]. The pin also freezes which of those three this cone uses. P4's fresh axiom reds both. | no |
| direct supports: type digest of each constant the proof term references, one level (67 at the measured commit) | no | no. "A theorem's proof is irrelevant." [READ GATES-20t; READ `decls.py:14-16`] A re-proof that cites different constants is green there and red here. P2 (a rewrite inside `left_falls`, two levels down) stays green. That is the card's cut and it is the right one: the theorem's own proof is what it rests on; the cone under those lemmas is not. |
| vocabulary: payload of each constant the statement names, one level | no | no, by (1). |

Delete would be right if the pin were only statement plus axioms. It is not, once supports and vocabulary are on it. Those two are why C1's cone edit must still pass this row: a legitimate edit under the cut stays green, and an edit of what this theorem cites or of what its words mean goes red by name. The census will not say so. The statement diff will not say so.

What it does not certify: that the kernel accepted the proof (the environment already did), that `collectAxioms` agrees with a second inventory (that check dies under F1), or that a definition two levels down still means what it meant.

## (3) F1 — delete, by the consumer test

The new pin does not call `read`, `gather`, or `accept`. The only production caller of `read` on `origin/main` is `#certificate_census`. [READ `Census/Certificate.lean:8-28`] The worker's landing deletes that command. After that, nothing reads a closure out of a real environment.

What remains is the demonstration LANG-P6 already called not nano admission: the synthetic 15 cases (`Census/CertificateReaderTests.lean` says so in its header), `devtools/certificate_plants.py` (it flips `accept`'s guards and rebuilds `certificate-tests`), and the theorems of the walk (`accept_faithful`, `read_faithful`, `accepted_reachable_definition`, `missing_reachable_refused`, `changed_definition_refused`, plus `read_environment` and `accepted_environment_reachable` in `Census/Proofs/Certificate.lean`). A test of a component with no consumer is not a consumer. Keeping them "and cv-tasking the question" is the deferral this read is for. It is also H2 at component grain: true, and irrelevant. The card is already deleting the two trivial theorems for that reason. The same test applies to the walk they were decorating.

Delete in this landing:

- `read` / `gather` / `accept`, `Faithful`, `Reaches`, and every theorem whose subject is that walk, including both of `Census/Proofs/Certificate.lean`.
- `Census/CertificateReaderTests.lean`, `Census/CertificateReaderMain.lean`, the `certificate-tests` executable, and the `certificate-tests` row of `gates/runs.tsv`. The card's "gate: certificate-tests" tested synthetic closure acceptance, not this pin. The pin's tooth is `gates/certificate_plants.py`.
- `devtools/certificate_plants.py`. Its subject is `accept`. It also writes `CX-P6-plants.pid` into the shared logs directory [READ the script; the LANG-74.12 finding].

Keep the projection the pin uses: `reader env`'s lookup, `typeOf`, `dependencies`, `references`, and `expression` / `declaration`. `isAxiom` on the reader exists for the closure's assumption list; the pin's axiom source is `collectAxioms`. Do not keep a second axiom walk in order to have something for the old guard to compare.

`DELETES:` lines name the theorems, not a shrug. Price on landed nano theorems: none. These were never admission.

## (4) A2 — delete the file; one control is retired, not moved

`devtools/certificate_environment_plants.py` is not a gate row. [READ `gates/runs.tsv`: the only certificate rows are `certificate-tests` and `script:gates/certificate.py`] It imports `gates/certificate.py`'s `emit` and `--check-json` over the old object, so the re-pin breaks it. [READ the script] Three families:

1. **Extra axiom.** A twin of `grant_moves_le_cap` whose value is a scratch axiom, against the twin whose value is the real theorem. `collectAxioms` must see `CX_P6_extra`, and `compare` must red on `axioms`. Re-homed by P4, which plants the axiom in the real cone (`left_falls`) rather than in a twin. Stronger, not weaker.
2. **Unfolded constant.** `CX_P6_small`'s statement and axioms stay equal while `CX_P6_dependency`'s body changes, and `compare` reds naming that constant. This is P3's class on a toy. Re-homed only by A1: P3 against the real `MovesThrough`, plus the comparator mutant that drops the vocabulary section and must then read P3 green. If A1 had been refused, this family would have been lost. It was not refused.
3. **Coverage guard.** A scratch copy of the adapter with `ci.isAxiom` forced false, so `collectAxioms` reports an axiom the closure's `assumptions` do not contain. The guard in `#certificate_census` (`unless axs.all (fun n => c.assumptions.contains n)`) must refuse `collectAxioms escaped the context`; with the guard replaced by `unless true`, the bad inventory is emitted and a separate assertion exits 1. [READ `Census/Certificate.lean:16-20`; READ the plant] Nothing in the new pin re-homes this. There is no second inventory once the closure is gone. P4 does not: it checks that an added axiom reds the pin, not that two readers of the axiom set agree. Retire it in the decision in those words. `collectAxioms` was already a named trusted read-off in LANG-P6; it becomes the only one. That is critique (c), accepted, not papered over.

The disabled-comparator tooth (family "the comparison itself is what reds") is re-homed by the new comparator mutants, one per section. Those stay.

## (5) The two theorems

Confirmed. They are field projections, not a fact about certificates.

```
theorem contexts_distinguish {a b : Certificate Name Expr Body}
    (different : a.context ≠ b.context) : a ≠ b := by
  intro h
  exact different (congrArg Certificate.context h)

theorem checkers_distinguish {a b : Certificate Name Expr Body}
    (different : a.checker ≠ b.checker) : a ≠ b := by
  intro h
  exact different (congrArg Certificate.checker h)
```

[READ `Census/Proofs/CertificateReader.lean:139-150` on `origin/main`] Each is "this field differs, so the structure differs," the trivial direction of constructor injectivity, discharged by `congrArg` on the projection. REVIEW H2 named them exactly that, against a card that had asked for a theorem that two same-statement certificates with different contexts are different objects. [READ REVIEW-20261021.md H2] The `omit` line above them exists only so those two can drop the `DecidableEq` assumptions the real theorems use. Delete the theorems and the `omit`. The worker's grep (nothing references them outside judge copies) was not re-run; the proofs have no consumers inside the module.

## (6) Size

The blob on `origin/main` is 11,961,094 bytes. [MEASURED `git cat-file -s`] `gates/size-allow.tsv` has one data row, that path, ceiling 11961094. [READ the file; READ GATES-20q]

`size_limit` reds a tracked file above 1,048,576, and reds an allow row whose file is gone or now at most 1,048,576 ("no longer needs its allow row"). [READ `gates/size_limit.py:13`, `:81-89`] The re-pin deletes `gates/certificate-grant.json.gz` and adds `gates/certificate-grant.json`. The allow row names the gz. Leaving the row in is a stale-row red whether or not the json exists. The row goes in the same landing as the blob. The new file needs no row: IMPACT measured it at ~10.8 KB with all four sections, and a pin of 115 sha256 lines cannot approach 1,048,576. Not re-encoded here. `size_limit` is ok on that file. It is not ok if the allow row survives.

---

**Meta-critique.** The pull was to call the certificate redundant because 20t landed under the card and "a digest of the statement" is what H3 asked for. That reading is comfortable and it is wrong: 20t does not hash definition values on a forward edit, and it ignores proofs on purpose. The opposite pull was to keep the closure reader because deleting proved theorems feels like a scope expansion. The consumer test is the one this program already uses, and a cv task would be me declining it.
