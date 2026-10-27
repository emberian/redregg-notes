# FAERIE-HYGIENE: nanodregg be589b7e (pushed to origin/main)

| item | status |
|---|---|
| 1. Lang imports Hosting | DONE. NanoBridge moved to Hosting/Contextual/NanoBridge.lean; the Nano section of Lang/Proofs/Contextual/Protocol.lean moved to Hosting/Proofs/ContextualNano.lean (same namespace, names unchanged); Failures.lean moved to Hosting/Proofs/ContextualFailures.lean. No Lang module imports Hosting now. `lake build Lang Hosting` green (354 jobs) before rebase; main moved (6caf3fdd), rebase was clean, NOT rebuilt after rebase. |
| 2. World.lean theorems + @[csimp] | SKIPPED. The csimp (World.admit_eq_admitImpl) only rewrites callers that import its module; moving it to Kernel/Proofs/* would silently drop the KERNEL-48 single-rowsRun path from Receive/Submit (off-limits, and nothing imports Proofs). Needs a design call (e.g. a defs-side Kernel/AdmitImpl module holding the csimp). The two private lemmas only serve the csimp. |
| 3. Double contextual check | SKIPPED, sites found: Program.lean admitContextual (`p.checkContextual ifs`, and `checkE` on the prepared body) vs LiveHoles.lean instantiateHoles (`p.checkContextual Δ`, `checkE Δ body`). Keeping one requires dropping the one in instantiateHoles (admitContextual also serves the unresolvedBody path that has no check), which rewrites instantiateHoles_typed/_cost and admitContextual_inv proofs and the refusal order (instanceRecheck vs instanceType). Not mechanical. |
| 4. Reply peak row | CONFIRMED: gates/build-peaks.tsv row `Hosting.Proofs.Reply 2560` exists (build_peak.py is live). Nothing done. |
| 5. Other B6 | Not done: decls.py `partial def go` and "no deployed consumer" are not mechanical. |

No theorem statement or wire byte changed.
