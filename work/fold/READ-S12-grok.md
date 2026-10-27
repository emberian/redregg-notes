VERDICT: RELEASE S12

No rebuild in this read. Base checked: `origin/main` = `ac34521`. The candidate patch was read whole (it ends at the two plant strings). Census diff read whole. S12’s touched files match `origin/main` on the patch’s old side (lakefile root, plant strings, `Census/Certificate.lean`, `Census/CertificateData.lean`), so the S11 stack under it does not edit this step’s files.

## 1. The move

READ. The patch deletes four Lang files and adds the four Census files the map names, with no other Lean hunks:

| old | new |
|---|---|
| `Lang/Contextual/Certificate.lean` | `Census/CertificateReader.lean` |
| `Lang/Proofs/Contextual/Certificate.lean` | `Census/Proofs/CertificateReader.lean` |
| `Lang/Journey/Certificate.lean` | `Census/CertificateReaderTests.lean` |
| `Lang/Journey/CertificateMain.lean` | `Census/CertificateReaderMain.lean` |

Body text is the same except `import` lines and `Nanodregg.Lang.Contextual.Certificate` → `Census.CertificateReader` (tests: `….Certificate.Tests` → `Census.CertificateReader.Tests`). Consumers rewritten are only `Census/Certificate.lean`, `Census/CertificateData.lean`, `Census/Proofs/Certificate.lean` (qualified names and imports). `lakefile.lean` changes the comment `-- LANG:` → `-- CENSUS:` and `root := \`Lang.Journey.CertificateMain` → \`Census.CertificateReaderMain`. The exe name `certificate-tests` is unchanged.

MEASURED (`fold/diff-S12.txt`). `before 51151` / `after 51151`. `type-digest changed 0`. `module changed 243 of which from a module the step does not move 0`, and those 243 are only the three moved modules (164 + 41 + 38). `value-hash changed 33`, and the 33 lines are exactly the structure projections of `Certificate`, `Checker`, `Entry`, `Reader`, `Faithful`, `Tests.Body`, plus `Refusal.noConfusion`, `Refusal.noConfusionType`, `instReprRefusal.repr`, and `Tests.run`. No theorem is in that list.

The “0 deletions” claim holds as a content claim, with one census-tool caveat. The diff also says `vanished 8 declared 0 UNDECLARED 8` and `new 8`. All eight vanished names are `_private…instDecidableEqExcept_lang` (plus `_proof_1`–`_proof_6` and `match_1`); all eight new names are the same with `_census`. That is the private `DecidableEq (Except E A)` instance in the test file. Lean names it from the root namespace (`Lang` vs `Census`). The rename map rewrites the private prefix (`_private:Lang.Journey.Certificate` → `_private:Census.CertificateReaderTests`) but not the generated suffix, so the tool reports a vanish+new instead of a mapped rename. Nothing else vanishes. Row count is unchanged. Not a deleted theorem and not a type change.

Census is the right home. READ: after the move `Census/CertificateReader.lean` imports only `Std`. Its proofs import only `Census.CertificateReader`. The tests import only `Census.CertificateReader`. It does not depend on `Lang` or on `Lang/Contextual`. The adapter that does depend on Lean stays where it already was: `Census/CertificateData.lean` (`import Lean` plus the reader). Map §2.1 and the file’s own docstring (“a data/reader interface, not nano admission and not a new proof checker”) put it next to its only consumers.

No Lang → Census inversion. MEASURED on `origin/main` history: `git log -G 'import Census'` over `Lang Kernel Ledger Host Hosting Protocol Codec Emit Bench Ops` is empty, and `-G 'Nanodregg\.Lang\.Contextual\.Certificate'` names only the seven files this step rewrites (`a0eb75f`, never touched again). The patch adds no `import Census` under `Lang`. `Census/` is the GATES layer (`gates/OWNERS`); the reader moves into tooling, not the other way.

`CertificateReaderMain.main` does not appear in the census diff (not in the 243, not in the 8). READ: the file is the four-line exe root, `def main` unchanged except the callee. The digest simply does not carry that exe root. The source diff does.

## 2. The gate

READ. `gates/certificate-grant.json.gz` is not in the patch. `gates/certificate.py` loads that gzip and compares the whole object to a re-emit of `Nanodregg.Ledger.Proofs.grant_moves_le_cap`. Its `--harness-control` (runs.tsv, the `script:gates/certificate.py` row) does not write the golden: it appends `"CX_P6_harness_control"` to the in-memory expected `axioms` and runs the real `compare`. The non-control path is the GREEN the step claims.

INFERRED, not re-run. The re-emitted object should match the untouched golden. The JSON is the closure of the target’s checked declarations (`certificateJson`), not a dump of the reader module. The census diff says no type or value change outside the three moved modules, so no declaration the grant theorem reaches mentions a renamed constant. Checker `imports` are the scratch file’s direct imports (`Census.Certificate`, `Ledger.Proofs.GrantCap`), which this step does not change. I did not decompress the 12 MB golden and I did not re-execute `gates/certificate.py`.

certificate-tests, control still RED. MEASURED by reading `fold/S12-ctc-base.txt` and `fold/S12-ctc-after.txt` against each other. Fifteen `PASS certificate:` lines, byte-identical, in the same order. Both then FAIL. The only difference is the constructor printed by `Repr`:

- base: `expected Except.error (Nanodregg.Lang.Contextual.Certificate.Refusal.contextMismatch); actual Except.ok ()`
- after: `expected Except.error (Census.CertificateReader.Refusal.contextMismatch); actual Except.ok ()`

That is a real GATES-15 control, and it is not a mutation of the reader. READ (`gates/runs.py` and the test `run`): the control must be an expectation nothing meets, judged on the ordinary path, and the output must read RED naming `harness-control`. The flag appends one row, `("harness-control", .ok (), .error .contextMismatch)`. Actual is the literal `.ok ()`; expected is `Refusal.contextMismatch`. The same comparator that prints `PASS` prints `FAIL certificate: harness-control;`. It does not edit `accept` or `read`. The qualified-name change is `instReprRefusal.repr` (one of the 33 value-hash changes) and still contains `harness-control`, which is what the runner matches. A gate that pinned the old namespace in that string would go stale; this one does not.

The source mutations are the plants, separate from that control. READ (`devtools/certificate_plants.py` on `origin/main`, and the patch): each guard needle `if <condition> then` is replaced with `if False then`, and the first `| none => .error .missingTarget` becomes `| none => .ok ()`, then `certificate-tests` must exit 1 with `actual Except.ok ()` on that row. Those needles are unchanged in the moved `accept`. The patch’s only plant edit is the two granted strings:

- `root / "Lang/Contextual/Certificate.lean"` → `root / "Census/CertificateReader.lean"`
- `"Lang.Proofs.Contextual.Certificate"` → `"Census.Proofs.CertificateReader"`

Both targets are files the patch adds (`Census/CertificateReader.lean`, `Census/Proofs/CertificateReader.lean`). `devtools/certificate_environment_plants.py` does not name either old path; it plants `Census/CertificateData.lean` / `Census/Certificate.lean` / `gates/certificate.py`, and those needles are outside the S12 hunks. IMPACT says the plant driver was not re-run. I did not run it either. Textually it still has a source to mutate and a module to rebuild.

## 3. The lakefile root and the gate rows

READ (`origin/main` `gates/runs.tsv`, `gates/generated.tsv`, and the lakefile hunk). `runs.tsv:56` is `certificate-tests`, pass line `certificate-tests: GREEN`, control `--harness-control`. `runs.tsv:57` is `script:gates/certificate.py`. Neither row names `Lang.Journey.CertificateMain` or `Census.CertificateReaderMain`. `generated.tsv` has no certificate row. The exe name in the lakefile stays `certificate-tests`, so those rows stay right without an edit. The thing that changed is the lean root behind that same exe, which is what the lakefile hunk updates.
