# IMPACT-C6 · boundary = Ω (docstring only)

CX-PROMO-3, 2026-10-22, nano main `100ad08`. Plan §3 P2 C6. The deletion half (`Consumer`, `Consumer.holds`,
`consumer_boundary`) already went in LANG-75.3 (its decision line 19: "go with Closure").

**What the deployed boundary is (READ).** A package's holes show the rest of the system exactly two things:
- **Typing.** `holeSignature p.holes` (`Lang/HoleROM.lean:41`) gives each hole's name, context and type (Ω). This is all
  that `checkE … (Ω := holeSignature p.holes)` sees at install (`Lang/LiveHoles.lean:85`). It is also all that
  `unresolvedBody` uses to refuse a residual hole by its type (`Lang/Program.lean:181`).
- **Cost.** `Package.holeCharge` (`Lang/LiveHoles.lean:256`) is the expansion bound plus one guard allowance per hole.
  The static charge is taken at the largest candidate, the actual charge at the resolved ones.

What a selected candidate DOES is not part of either. No deployed consumer is stated over a projection of a filling.
The abstract `Consumer`/`consumer_boundary` was that statement and had no deployed reader.

**What lands: two docstrings, `lang:` fast, LANG-75.8, no theorem.**
- On `holeSignature`: "The whole boundary a package's holes present to typing (C6, LANG-75.8): name, context and type.
  The install check and the residual-hole refusal see nothing else of a hole. A candidate's behaviour is not part of it."
- On `Package.holeCharge`, appended: "With `holeSignature`, this is the hole boundary (C6, LANG-75.8): typing and cost,
  never behaviour. No consumer reads a projection of a selected filling. The abstract `consumer_boundary` left with
  LANG-75.3 for that reason."

**Price.** 0: comments only. Journey, vectors and statements unchanged.
