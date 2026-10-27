## The surface writes the interface a method produces (2026-10-27; LANG-103 critique (e); cv 01a17de6)

**What a program could not say.** LANG-103's `produces I` existed only in the core text, `(ℓ N I)` in the
effects section: an author writing surface text could not declare the interface of the packages a
generator installs, so the grade was unwritable in the authoring language and every such generator had
to be built in Lean (`Std.generatorOf` plus a hand-set `effects` row, as GN22–GN24 do).

**What changed.** `Lang/Surface.lean`: a method's effect clause reads
`(effect (moves N) [(produces I)])`; `I` is written as the surface writes a package's interface — a
record of method and law names and types, `(rec (ℓ T)…)`, read by the surface's own type reader
(`methodHead` now carries the `Ctx`), so named types, `Req`, `Verdict` and the rest resolve as in any
surface type, and a bad interface refuses by name at the offset (law 7). The lowering fills
`Effect.produces`; install's `badProduces` and the run's `produces LABEL: lacks/type/extra M` are
unchanged and now reachable from authoring. The grammar texts (`Surface.grammar`, `Read.grammar`) and
`docs/spec/2-structure.md` §2.7 state the form; GN25 is GN23's surface twin.

**MEASURED.** (filled after the run)

**Premise price.** None: no theorem's statement changed, and the surface's produces rides the
round-trip cases LANG-103 already proved for the core text (`effectSx_ok`, `effect_read`,
`effects_mapM`) because the surface prints and re-reads the core text.

**What re-emits.** Nothing: no shipped package's surface text changes, and the wire and core text are
untouched.

**Critique.** The clause is ordered `(moves N)` first, `(produces I)` second, and both sit in the one
`(effect …)` clause: an author cannot write produces alone. That matches the abstract grade (one
`Effect` per method) and keeps one duplicate check, but a method that cannot move value still writes
`(moves 0)` to reach its produces — the same asymmetry the core text's `(ℓ N I)` has, inherited rather
than fixed. The interface is spelled as types the author must copy from somewhere (`Print.ty` of the
promised package, or by hand); the language has no name for "the interface of package P" in a type
position, which is rung 2's `quote` (`DESIGN-META` §10–11), so this form is honestly a promise written
out, not a derivation. A method with `(effect (moves N) (produces I))` and no install or createOf arm
is refused `badProduces` at install, the same as the core form (GN24).
