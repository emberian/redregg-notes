# IMPACT-C9 — use-once grants as revocable certificates: the justification and the spend are read at one pinned World (C9, LANG-75.2)

Worker: CX-PROMO. Written 2026-10-22. Base: nano `origin/main` = **4916f3a** (E1 + C1 landed). Plan §3 P1 C9; LPCFS
(Morgenstern 2011, p2: the monitor checks "each certificate in a submitted request", atomically with the use-once
check). Tags READ / MEASURED / INFERRED. Nothing built.

## 0. Answer first

- **The atomicity is already structural, and E1 made it the justification's.** [READ `Kernel/Receive/Derive.lean:380–395`]
  `receive` takes ONE `look = pinned X.env w c.unsigned.pins` and threads it through `receiveWith → deriveTurn →
  derive → dispatch → tree`; `invoke` (`:215–232`) runs the method with that `look` (`X.program.run look rv …`) and
  derives the calls the run returned with `tree X look rv c n`, whose `.transfer` arm is `transfer X look …`
  (`:350`), which spends the counted right through `spendVia look …` (`Kernel/Receive/Ledger.lean:113`). Since
  4916f3a the method's fact read carries `cellLive look g` (`cited_authenticated`). So in P8's `commit` the
  provider's liveness and the unit's spend are read from one pinned view of one World, and `World.admit` checks every
  pin against that World before the Turn commits.
- **What is NOT yet a theorem:** (i) that the bit is the World's — `cellLive (pinned E w pins) g` is "g pinned and
  `w.live E g ≠ none`" (today only `cellLive_iff`, over an abstract `look`); (ii) that the method's run and the
  spends of the calls it returns share that `look` (true by the definitions above; no statement names it).
- **The card, therefore, is two theorems, one plant, one docstring, no wire, price 0** (`lang:` fast path):

## 1. The theorems (statements; each with its object and the mutation that falsifies it)

1. **`cellLive_pinned`** (Lang/Proofs/Rel, beside `cellLive_iff`):
   `cellLive (pinned E w pins) g = true ↔ (∃ p ∈ pins, p.1 = g) ∧ (w.live E g).isSome = true`.
   Object: the live column at the receive's World (`Kernel.Receive.pinned`, `World.live`). Mutation: `pinned`
   answering a pinned tombstone or absence with a cell (or `cellLive` reading `(look g).isOk`) → false at a revoked
   grant. Consumer: C2's `kernelWorld` (`live (.cell g) := cellLive look g` is then `w.live` at the pins).
2. **`commit_checks_justification_atomically`** (new module `Lang/Proofs/Atomic.lean`, importing Kernel.Receive and
   Lang.Proofs.Rel): for `X` whose program is `Lang.program bytesOf digestOf`,
   `invoke X look rv c sub wk actor obj m args budget via = .ok (d, wk') →
     ∃ cell p r old fuel new calls rows used,
       X.program.run look rv p old m args r fuel = .ok (new, calls, rows, used) ∧
       deriveCalls sub obj ⟨[], writeOf obj (diffOps old new), [], rows⟩ wk'' calls = .ok (d, wk')`
   — the method's run (its live read, `cited_authenticated`) and the derivation of every call it returns are under the
   SAME `look`; and at `sub = tree X look rv c n`, a returned `.transfer … (some g) …` is `transfer X look …`, whose
   spend is `spendVia look …` (`spendVia_ok`: the pinned live grant's `spendAt`). INFERRED proof: unfold `invoke`
   (the `do` block; the same `split` style as `runSetupWith_spec`). Mutation: derive the returned calls at a second
   view (`deriveCalls` under `pinned` of another World, i.e. "check then spend" in two Turns) → the conclusion's shared
   `look` fails.
   Reader question Q1: is (2) a rename of the definitions (plan §8.2)? It states nothing `invoke`'s text does not, but
   it is the one sentence that makes "the certificate is checked atomically with its use" a checkable claim; the plant
   below is the deployed tooth. Default: land it; if the read says rename, keep only (1) + the plant + the docstring.

## 2. The plant (the refuter the plan names: "the two-Turn plant must red")

P8's `commit` = `select` (the generated judgment over the live facts read) ∘ `transfer 1 via cap`, in one method
(READ `Lang/Journey.lean` `p8CommitPackage`). Plant: `commit` WITHOUT its `select` application — the spend alone,
the shape of a protocol that judged in an earlier Turn (select) and spends in a later one. Expected: `P8.2 re-pinned
tombstone` admitted (RED), the unit spent to the revoked provider's candidate, i.e. exactly the 10-22 probe. Run as
the E1 plants were: temporary edit, journey exe rebuilt under it (checked), whole output read, restored GREEN.
If it does NOT red, C9 is a docstring and (2) is not landed.

## 3. The docstring (LPCFS)

On `cellLive` (Lang/Rel): a provider's grant is a use-once, revocable certificate (Morgenstern 2011): revocation
retires the cell, every reader of a fact that names it reads it through the call's pins, and the spend that uses the
certificate is derived from the same pinned view in the same Turn. KERNEL-60's decision text is KERNEL's file
(`decisions/kernel.md`, not in R-0025); the citation lands in LANG-75.2 and on `cellLive`, not in KERNEL-60. Reader
question Q2: grant `decisions/kernel.md` for one sentence under KERNEL-60? Default: no; LANG-75.2 cites KERNEL-60.

## 4. Price, consumers, rows

- Premise price: 0 (two new theorems; no landed statement changes; no definition changes except a docstring).
- Consumer: P8.4 (`RE-EXECUTE atomic checked commitment`, the competing-use row) and P8.2 (re-pinned tombstone): the
  rows are the executed instance; (2) names why one Turn closes the gap; C2's `kernelWorld` uses (1).
- Rows: unchanged (no new row; the plant is recorded). Wire: none. Re-genesis: none. Gate: `lang:` fast path,
  `gates/check.py`, whole-tree build (a new proof module).
- The census digest diff: expected two new theorems and one new module, nothing else.

## 5. Absorbs

01a16502-c55e (the LPCFS item, if listed), plan §1 B3 (`spendVia_ok` under one `receive` = (2) at `X.program`).
