# LANG-SURFACE report (2026-10-27)

## Landed

| hash | contents |
|---|---|
| `57111733` | lang: holes in the surface text, and `ob` checks a package with holes against a stated view (LANG-104, LANG-105) |

Pushed by hand under rule 1. `scripts/commit` built the whole tree on the rebased commit (Kernel Protocol Host Lang Hosting Ledger Spec Web Emit Bench Ops and every exe). 25 of 26 touched rows were ok. The one red was `rows --deployed` UNREAD: it ran past the 600 s wall clock with load at 30–40. `f95ed6c4` raised that limit to 1200 s while this was landing. An earlier attempt had the same single red on `cargo:launcher:resident_bell` (600 s, UNREAD). After the last rebase (no file overlap with `2efa6a57`, `0f86881d`, `f95ed6c4`), `lake build Lang lang-journey ob` was green and `lang-journey` was GREEN, RM0–RM16.

LANG-103 was taken mid-flight by FABLE-META-4 (`c17cf0f0`, produces). My entries are LANG-104 and LANG-105. I adapted to its restated lemmas: my round-trip theorems carry its premise that produced interfaces are well formed.

## What the system can do now

1. **Holes in the surface** (`Lang/Surface.lean`, LANG-104). A hole is declared as `(hole u ((x T [fact])… ⊢ A) (select rel key) [(guard [fact] e)] (candidate e fact…)…)` and used as `(hole u e…)`.
   - Binders name the context and a key is a record literal.
   - A fact is one of `(row rel key ver)`, `(cell #id)`, `(cell #id (law #pkg))` or `(cell #id (runs #pkg))`.
   - Holes are numbered in the order they are declared. A name with no hole behind it is refused `noHole`.
   - The grammar texts (`Surface.grammar`, `Read.grammar`) show the new forms. `Read.grammar` also gains the effects, claims and holes sections and the hole term. `Surface.grammar` gains `install` and `(claim keeps …)`.
2. **Round-trip hole case** (`Lang/Proofs/Print.lean`). Theorems: `supportPin_read`, `supportOptPin_read`, `holeCode_read`, `holeROM_read`, `readPackage_packageText` (the closed-text theorem without `holes = []`) and `package_eq_packageText`. The last one says `Print.package`'s contextual re-read never refuses a printable package. All existing statements are kept. The teeth are `PrintTeeth.holePkg_*`.
3. **`ob` checks packages with holes** (`Lang/Resident.lean`, LANG-105).
   - `ob (check P)` runs install's own `admitContextual` on a package with holes. Before, it refused every such package with `illTyped noHole`.
   - `ob (check P [(with …)] (view fact…))` resolves every hole with `instantiateHoles` on the facts the view states. Facts are `(select HOLE I|none)`, `(row REL KEY VER|none)`, `(live #ID [(law #L)…] [(runs #P)])` and `(dead #ID)`; anything not stated is unpinned.
   - The answer is `ok … hole N candidate I`, or the refusal a run would get, by name.
4. **README "One program"** is now surface text, and the seven named types are gone. `Lang/Journey/Readme.lean` reads the block from README.md itself, so the literal text on the page is what gets lowered, installed and run:
   - RM0: the block is read and is surface text.
   - RM1–RM14: as before.
   - RM15: `ob (check P)` admits the text.
   - RM16: five `ob` views give the same answers as the World in RM4, RM6, RM7, RM9 and RM11. Refusal names and coordinates match; the id of G is written as G because Sim ids are 8 bytes and deployed ids 32.
5. **`docs/spec/2-structure.md`** §2.5 shows the surface form of a hole with a field-by-field table. §2.11 says the README program is surface text.

## Findings / not done
- `HolePrintable` is not yet derived from the contextual install check. That needs `hasType_canon`/`hasType_wf` at a nonempty Ω. Until then, the claim that a checked contextual package reads back rests on `Print.package`'s re-read, not on a theorem.
- When `ob` meets an ill-typed candidate (`holeCandidateType h i`), the refusal names no line of the surface text.
- The surface still has no `(createOf T)` call kind (SPEC-DOCS finding 1's second half).
- The testground shows the new grammar text only after the next wasm build; the wasm is not tracked in git.

## Housekeeping
- hbox worktree `~/nd-land/surface` (branch `lang-surface`, at `57111733`).
- hbox `~/nd-land/surface-land`: the lander's build dir.
- hbox `~/nd-land/surface-scratch`: logs, PID files, test texts.
- Local mirror in my session scratchpad.
