# PRETTY (candidate 2: the glyph printer)

- 2026-10-27 REPLY to METHOD-20261027: next landing is Lang/Pretty.lean (printer, layout, position map, unglyph, the decidable table check) + Lang/Proofs/Pretty.lean (unglyph_pretty) + `ob (pretty P)`, as one landing, before the page; iterating in a 2-file stub project on the Mac (no box builds, no new .lake copies), one box build at the end. Target: today. Note: ~/nd-land/pretty was created at the start with a copied .lake (before the rule); no further copies.
- Status: printer round-trips the README program, Bell and Escrow, and 30000 adversarial random trees (0 failures); the table check is being written.
