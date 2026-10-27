# IMPACT-S12 — the P6 certificate reader leaves Lang for Census (consolidation step S12)

Worker: CX-FOLD-3 (Claude). Written 2026-10-22 after building the candidate in scratch (`hbox:logs/cxfold/S12-tree`),
**stacked on the S11 candidate** (S10 + S11 + S12 touch disjoint files). GRANT R-0015 (Census/** and the lakefile
target, CROSS-LAYER: GATES; the 12 MB golden untouched). Map: §2.1 (:362–364), §3.2 (:496–497), §4.2 row S12.
Tags READ / MEASURED / INFERRED. Judge: fast (`lang:`). Candidate: `fold/S12-candidate.patch`. Edit script:
`fold/S12-s12edit.py`. Rename map: `fold/S12-renames.tsv`. Census diff: `fold/diff-S12.txt`.

## 0. Answer first

`Lang/Contextual/Certificate.lean` says of itself "a data/reader interface, not nano admission and not a new proof
checker" [READ :2–3]; every consumer is in Census [MEASURED grep]. S12 moves it, its proofs and its tests to Census,
verbatim except the namespace `Nanodregg.Lang.Contextual.Certificate` → `Census.CertificateReader` and the import
lines. **0 type changes, 0 deletions** [MEASURED]. The pinned certificate vector (`gates/certificate-grant.json.gz`)
re-emits GREEN unchanged: it names no module or constant of the reader [MEASURED].

## 1. The moves

| old | new |
|---|---|
| `Lang/Contextual/Certificate.lean` | `Census/CertificateReader.lean` |
| `Lang/Proofs/Contextual/Certificate.lean` | `Census/Proofs/CertificateReader.lean` |
| `Lang/Journey/Certificate.lean` (namespace `….Certificate.Tests`) | `Census/CertificateReaderTests.lean` (`Census.CertificateReader.Tests`) |
| `Lang/Journey/CertificateMain.lean` (the `certificate-tests` root) | `Census/CertificateReaderMain.lean` |

Name map: every `Nanodregg.Lang.Contextual.Certificate.X` → `Census.CertificateReader.X` (251 constants), plus the
three modules' private prefixes. Census's own namespace stays `Census.Certificate` (the command, the data adapter,
the two Census theorems); the reader beside it is `Census.CertificateReader`, the file name the map gives.

Consumers rewritten (qualified names and imports only): `Census/Certificate.lean`:16, `Census/CertificateData.lean`:5,
110, 115, 126, `Census/Proofs/Certificate.lean`:6, 15–35. `lakefile.lean`: the `certificate-tests` root
`Lang.Journey.CertificateMain` → `Census.CertificateReaderMain` and its comment `-- LANG:` → `-- CENSUS:` (exe name
unchanged, so `gates/runs.tsv`:56 is unchanged).

## 2. ASK: one path outside the grant

`devtools/certificate_plants.py` (owner CLIENT per `gates/OWNERS`) drives the reader's plants by path: `:16`
`root / "Lang/Contextual/Certificate.lean"` (the source it mutates) and `:69` the build target
`"Lang.Proofs.Contextual.Certificate"`. After the move both are stale: the plant driver would fail to find its source
(a falsifier that stops falsifying). R-0015 grants Census/** and lakefile.lean, not devtools/.
**Default: a GRANT (CLIENT, `devtools/certificate_plants.py`, these two strings only)**, landed in the S12 commit
under `CROSS-LAYER: CLIENT`. The scratch candidate includes the two-line edit (`fold/S12-candidate.patch`); I did not run
the plant driver (it rebuilds `certificate-tests` once per plant). Alternative: land S12 without it and open a cv task
for CLIENT. RULE which.

## 3. Census digest diff (S11 candidate → S12 candidate, under the map) [MEASURED `fold/diff-S12.txt`]

- 0 type changes. 243 module changes, all from the three moved modules.
- 8 vanished / 8 new: the private derived instance `instDecidableEqExcept_lang` (+ 6 `_proof_N`, `match_1`) of the test
  module is now `instDecidableEqExcept_census`: Lean names a derived instance after the root namespace. Generated.
- 33 value-hash changes: the structure projections of `Certificate`, `Checker`, `Entry`, `Reader`, `Faithful`,
  `Tests.Body` (a projection's value carries its structure's name, which the rename map does not rewrite inside
  `Expr.proj`; the S6 HoleDecl projections were the same class), `Refusal.noConfusion(Type)`, `instReprRefusal.repr`
  (prints the constructor's qualified name), and `Tests.run` (its strings). No theorem's value changes.
- Kernel/Ledger/Host/Lang outside the moved modules: 0 changes.

## 4. The inverted question: what surviving module or row is weaker?

None [MEASURED]. `certificate-tests` prints the same 16 lines (all 15 PASS + `certificate-tests: GREEN`);
`--harness-control` still FAILs on the same row, its message differing only in the constructor's qualified name
(`Nanodregg.Lang.Contextual.Certificate.Refusal.contextMismatch` → `Census.CertificateReader.Refusal.contextMismatch`;
`fold/S12-ctc-base.txt` vs `fold/S12-ctc-after.txt`). `gates/certificate.py` re-emits the certificate of
`Nanodregg.Ledger.Proofs.grant_moves_le_cap` (6,857 declarations, 3 target axioms) and compares the whole pinned
object: `certificate-vector: GREEN`. The journey is byte-identical.

## 5. Gates [MEASURED, scratch]

Whole tree `Lang Kernel Ledger Census Host Hosting Protocol Codec Emit Bench Ops host lang-journey codec-vectors
certificate-tests` GREEN (626 jobs); `certificate-tests` GREEN, control RED as before; `gates/certificate.py` GREEN;
`gates/check.py` GREEN with the generated SIZE (Census lines 986 → 1345, Lang lines 41908 → 41549; module counts
unchanged). Re-emit: none; the golden is not touched (its re-pin is cv 01a16131-5868).

## 6. What breaks

The four Lang paths no longer exist; `Nanodregg.Lang.Contextual.Certificate.*` no longer resolves (use
`Census.CertificateReader.*`); `certificate-tests` is built from `Census.CertificateReaderMain`. Lang no longer holds
any Census tooling.

## 7. Addendum after GRANT R-0017 (CX-FOLD-3)

The two `devtools/certificate_plants.py` strings are in the candidate (strings only). MEASURED: the plant driver,
run on the scratch candidate under `swarm-build` (a copy whose only change is its log directory, pointed at my scratch
`logs/cxfold/S12-plants/`, so CX-P6's logs in the shared `logs/` are not overwritten), prints `certificate-plants:
GREEN`: baseline GREEN, the harness control exits 1 by name, each of the 7 guard plants and the missing-target plant
builds and exits 1 with `FAIL certificate: <name>; … actual Except.ok ()` captured, and the restored source rebuilds
GREEN (`logs/cxfold/S12-plants.log`). Finding, not fixed here: the driver as landed writes `CX-P6-*.log` and
`CX-P6-plants.pid` into the shared `/tank/dregg-build/nanodregg/logs/`, overwriting the previous run's logs.
