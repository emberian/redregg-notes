# DESIGN-CTX — the contextual theory taken seriously, and its most powerful instantiation on nano (real 2026-10-26)

Author: a Fable, designer. Read in this order: VERDICT-20261024 §2, HOLISTIC-LANG, HOLISTIC-LANGPROOFS,
REORIENTATION-20261022, NANO-VS-MINI-20261022, decisions/lang.md LANG-66 and LANG-75.1–75.24, LANG-76/77/80/81/82,
TOPLEVEL-SPEC, then the code at nano `origin/main ad90a47` (`Lang/LiveHoles.lean`, `Lang/HoleROM.lean`,
`Lang/StdHole.lean`, `Lang/StdContextualHole.lean`, `Lang/StdOffer.lean`, `Lang/StdOfferEscrow.lean`,
`Lang/StdActivity.lean`, `Lang/Bell.lean`, `world/resident/Bell.ob`, `Lang/Contextual/Protocol.lean`,
`Kernel/Receive/Call.lean`, `Kernel/Receive/Derive.lean`). Tags: READ (path), MEASURED (a command), INFERRED
(my reasoning; attack these first). Ember's ask: "elaborating the contextual theory thoroughly into the most powerful
possible instantiation of itself seems reasonable." Non-vacuity lives at the top (§2.4) and nowhere else.

**The verdict in one paragraph.** The theory, taken seriously, is not "holes". It is that the MEANING OF AN INSTALLED
PROGRAM IS A FUNCTION OF THE WORLD, given by justifications: `⟦P⟧(W)` is the closed program obtained by filling every
deferred decision of `P` with the candidate whose justification (an ATMS environment of kernel facts: rows at versions,
cells live) holds at `W`, and a refusal names the justification that failed. That is contextual modal types (Nanevski–
Pfenning–Pientka) for the typing, assumption-based truth maintenance (de Kleer, Doyle) for the selection, and why-not
provenance (Grädel–Tannen's dual indeterminates) for the refusal, run inside a replicated state machine whose members
re-derive every fill. Five of nano's six pieces are instances of ONE object, the SLOT (§2.1): the ROM hole, the
waiting row of an activity, the offer, the law list, and the refusal-with-coordinates; the sixth (the protocol
calculus) is the slot's TYPE written beside the system instead of in it. The two readers' dispute is settled thus:
LANG is right that the deployed hole is dynamic dispatch with justification checks (a mechanism with no claim), and
LANGPROOFS is right that the system property has no name — because the property has never been STATED. It is stated
here as one clause of INTEGRITY (§2.4, CONTEXTUAL INTEGRITY ∧ REPAIR), with the trivial system it refutes. The most
powerful instantiation is the slot generalised along three axes the kernel does not yet carry: candidates that are
other members' PROGRAMS under a contract (§2.5a), the object's PACKAGE as a slot, so an object repairs without its
author (§2.5c, the one real kernel change), and the fuse as a slot over foreign offers, so one session row IS a fuse
(§2.5b, needs `Req.caller`). The second consumer is a DOCUMENT whose sections are slots (§4): it runs on nano as it is.
The calculus remnant is not deleted and not reconnected: it is SUBSUMED by the slot descriptor and goes when the
descriptor carries its two theorems (§5). First to build: the refusal that names its coordinates and the document,
because together they make the top clause inhabited by a run a member can see (§6).

---

## 1. What the theory IS, when taken seriously

### 1.1 The one sentence, in the field's terms

A nano program is installed once, as ROM, and runs many times, each time against a World the author did not see.
Every place where the program's behaviour depends on something the author could not fix at install — which provider
is authorised, which counterparty's offer is taken, what text a contributor supplied, which laws govern, whether a
reply has arrived — is a DEFERRED DECISION. The contextual theory says what a deferred decision IS:

- **a typed slot** `u :: [Ψ ⊢ A]` — a metavariable with a context and a type, so that any filling checked once at
  `Ψ` is valid under every substitution (CMTT, Nanevski–Pfenning–Pientka TOCL 2008; READ `Lang/HoleDecl.lean`,
  `Lang/Check.lean:177` the `mvar` rule; `Lang/Proofs/Fill.lean` `fillHoles_typed` is their Thm 4.3);
- **filled under a justification** — the filling stands exactly while a set of ASSUMPTIONS holds: rows at versions and
  cells that are live (de Kleer's ATMS environments; Doyle's well-founded support; READ `Lang/HoleROM.lean` `SupportPin`,
  `Lang/LiveHoles.lean` `supportLive`, `selectHole`); a withdrawn assumption retracts the justification "as if it never
  existed" (de Kleer 1986 §4.9), which in nano is a pinned tombstone refusing `supportDead` for ever
  (`stale_behind_forever`, KERNEL-54);
- **re-derived, never trusted** — every member recomputes the fill from its own pinned view (`receive_congr`; the
  follower's `rederive`), which is Mokhov's verifying-trace / Stein's from-scratch consistency made the consensus rule
  (REORIENTATION A.8);
- **refused by the name of the missing assumption** — a refusal carries the coordinate that did not hold, so a client
  can discover its read set from refusals (`rowUnpinned` with parent, relation and key, READ `Lang/Rel.lean:356`;
  `HoleRefusal.supportMoved hole position`). That is why-not provenance: the dual indeterminate `x̄` of Grädel–Tannen
  (2024), whose absorption-normal form lists the minimal repairs;
- **open to composition it did not anticipate** — a slot's candidates need not be in the ROM: they may be posted by
  members (`Std.hole`'s `candidates` relation, READ `Lang/StdHole.lean:16-21`), read from a peer object
  (PROT-6's `peer` read), or be other objects altogether (P8's providers). Optimistic composition in de Alfaro–
  Henzinger's sense: compatible if SOME World fills it.

So the theory is **justified instantiation of contextual types inside a replicated state machine**. In knowledge
representation this is a truth-maintenance system whose problem solver is a type checker; in PL it is CMTT whose
substitutions are chosen by an authenticated row and defended by capability facts; in security it is proof-carrying
authorization (Appel–Felten; Garg–Pfenning's PCFS) with "re-execute the check" in place of "verify a proof" — the
macaroon/biscuit trade (Birgisson et al. NDSS 2014), which the charter already made (scope item 1). Dung's
argumentation semantics (AIJ 1995) is the right name for the structure of a slot's candidates — arguments with
supports and attacks (`blocker`) — and nano's holes are its DEGENERATE case: supports are one level deep (no candidate
attacks a candidate; REORIENTATION A.11, LANG-75.7), so the grounded extension is computed by one subset test and
no stable-model search is needed (Elkan's NP-completeness needs OUT-lists over derived nodes). That degeneracy is a
design choice to keep, not a gap: it is what makes re-derivation O(touched).

### 1.2 The six pieces, sorted

| piece | what it is in the theory | instance or accident |
|---|---|---|
| (1) typed ROM holes, selected by an authenticated row, supports live cells / rows at versions, strengthening factor (`selectHole`, LANG-75.1/.5/.6) | THE slot, at ROM grain: candidates committed at install, chooser = whoever writes the selection row under `codeChosen`, justification = `supports` + used hypotheses, acceptance = the guard, life = revisable until `accepted` | **instance** (the reference one) |
| (2) laws indexed by the act, relaw judged by old and new (KERNEL-27/57, `Std.quorum`) | the LAW LIST of an object is a slot whose chooser is whoever the laws in force admit (`.relaw`), whose acceptance is BOTH regimes (`.relaw` by the old, `.adopt` by the new), whose justification is the owner's authority | **instance**, unrecognised: it is de Kleer §4.9 applied to a justification itself (the old regime judges its own retraction). Nano stops short in one place: a PROGRAMMED object's laws and package can never change (`hasMethods`, READ `Derive.lean:148,163`), so the most important slot of all, the program, is sealed. §2.5c opens it |
| (3) refusals carrying the missing pin coordinates (`rowUnpinned`, LANG-79's `unpinned support0`) | the why-not half of still-analyzable; a refusal is a negative literal of the provenance polynomial | **instance**, incomplete: `HoleRefusal.unpinned` and `supportDead n` name the hole, not the CELL (READ `LiveHoles.lean:24,33`); the kernel's `unpinned <id>` does. §2.3 completes it |
| (4) the fuse: one party judges and invokes the other on the value it judged; typed nested-call arguments; the want-leg judge (LANG-77/82) | an OFFER is a slot of chooser `other`: its candidates are the peer's standing offers, its justification is the peer's row at its pin plus the peer's object live, its acceptance is `offerJoint ∧ fair`, its life is affine (retract on fuse) with a patience | **instance** in substance, **accident** in implementation: it has its own judge, its own row machine and no slot vocabulary, and the ONE thing a slot would give it — that only the named chooser may fill it — is exactly what it lacks (a root `take` by the owner makes a session row that is not a fuse, LANG-77 L2 critique). §2.5b |
| (5) activities with a patience; the Bell (LANG-58/59/76) | the WAITING ROW is a slot of type `response`, chooser `other` (the resumer), affine (answered once: `WaitingStep`), with a deadline (patience), whose filling resumes a captured continuation (defunctionalised: LANG-75.12) | **instance**; the Bell is the slot with the resident as chooser |
| (6) the protocol calculus (`Prot`, `Iface`, `HasProt`, `Chooser me|other`, affine tokens, executed prefix) | the TYPE of (1)–(5): `Iface = {chooser, ctx, need, post, owes, accepts}` is the slot descriptor; `fill_skips_others`, `at_most_once`, `executed_prefix_blocks_replan` are the slot's laws | neither: a **type written beside the terms it should type**. Eight readers would delete it because nothing inhabits it; the honest reading is that its INHABITANTS exist (the five instances above) and the judgment was never stated over them. §5 |

What is NOT an instance and must not be dressed as one: gas (a cost model), the codec, the CEK machine, the law/guard
split by occasion as such (the split is a constitutional device; only the relaw-judged-by-both rule is the slot move),
the peer read (a capability discipline that slots USE), and receipts between Worlds (a trust structure slots may cite).

### 1.3 Settling the readers' dispute

LANG (§3.2(i)): "guarded dynamic dispatch through a vtable whose slot is chosen by a row, with ATMS-style
justification checks; the CMTT framing is decoration." LANGPROOFS (§1): "a CMTT meta-variable whose instantiation is
chosen per Turn from an authenticated row and gated on the liveness of kernel cells … I do not know a name in the
literature … closest in spirit to truth-maintenance systems."

Both are right about what they looked at, and the dispute dissolves once the two grains are told apart:

- As a MECHANISM (what `selectHole` does on one invocation), LANG is right. One index from a row, candidates checked at
  install, supports compared, a guard run, a body spliced. A `select r [c₀…cₙ]` core construct would do it in a week
  (LANG §3.2(i)), and the CMTT apparatus (factor, re-embed, re-check) is doing the work of closure application. I agree,
  with one correction: the strengthening factor is NOT decoration once candidates can be posted after install
  (§2.5a): a posted candidate typed at a context the poster did not write is exactly what `selectHole_factor` protects,
  and the LANG-75.6 plant (a mis-embedding that keeps the node count) is the defect class it catches.
- As a SYSTEM PROPERTY (what holds of every admitted Turn along an audited log, for every member), LANGPROOFS is right
  that there is no name, and the reason there is no contribution yet is not the mechanism but that **the property was
  never stated**. `selectHole_origin`, `selectHole_live_selects`, `revoked_support_refused`, `instantiateHoles_typed`
  are the run-grain lemmas; nothing lifts them to the log, and nothing deployed outside the journey runs a hole. The
  readers' "nothing reads it" and "no name" are the same fact.

So the contribution exists if and only if §2.4's clause is stated over the deployed system and inhabited by a run a
member can see. Mechanism-wise nano is at the field's level; property-wise it is one statement and one consumer short.
That is a cheaper position than either reader wrote, and it is the position this design takes.

The literature's nearest named thing, for the record, is Artemov's justification logic (`t : F`, "t is evidence for
F", with evidence terms that can be composed and WITHDRAWN only by moving to a different term): a slot's filling is
evidence for its type, and the ATMS environment is the evidence term. Nano has no need to internalise that logic; it
has the kernel's facts as the only evidence, which is the degenerate case again, and the right one.

### 1.4 Against the baseline (real 2026-10-27, FABLE-CTX-5; CRIT-CTX's comparison)

The baseline is an ACL-protected row store with a nullable `selected` id: a member the ACL admits writes
`selected := id`, and a reader reads the id. The slot (`Lang/Contextual/Slot.lean`, LANG-101) gives four things the
baseline does not, and each is stated as a theorem or a measured row.

1. *Stored is not usable, and a read says which.* The baseline's id stays selected after the writer's permission is
   revoked; a reader cannot tell. A slot's read returns `usable c evidence` (every support with its truth) or
   `blocked c dead` (exactly the failing supports, by name, at least one): `slot_repair` (1)-(2). Deployed: the
   resident's `serve` and `use` slots (HOSTING-59) and the document's read with evidence, `nd read --evidence`
   (LANG-109, BUILT-9).
2. *Withdrawal by name, permanent where the fact is.* Re-granting in the baseline silently revives an old selection.
   A support on a retired cell is a tombstone (ids are never reused, KERNEL-70), so `slot_repair` (3) keeps it blocked
   by that name at every later view; the resident's instance is `serve_keeps_withdrawn` + `withdrawn_blocked`.
3. *Repair is re-selection in the same slot, and nothing else moves.* `slot_repair` (4), `serve_repairs`: the next
   usable candidate reads usable the moment it is selected; no reinstall, no restart. Measured: `agent_hole` H4 (a
   ring through a retired grant withdrawn by name, the next ring answered in the same process).
4. *Every member re-derives the verdict.* The baseline trusts the server's column. A hole's fill is recomputed by
   each member from its own pinned view (`receive_congr`, the follower's `rederive`); a refusal names the coordinate.

What the deployed slot still lacks: the section's read checks its supports at read time (BUILT-9), but the
package's `select` still admits a support 0 that is not the contributor's grant, which the read then shows blocked
(cv 01a17e0d); and the `use` slot learns a dead cell by probing, since the member's refusal line names no coordinate
(cv 01a17d68).

---

## 2. The most powerful instantiation

### 2.1 The one object: the SLOT

```
-- the descriptor of a deferred decision (INFERRED design; the five instances in §1.2 are its inhabitants)
structure Slot where
  ty        : [Ψ ⊢ A]                 -- HoleDecl: context and type of the filling
  chooser   : Chooser                 -- me | peer (named by the argument's pair) | anyone holding [invoke choose] | quorum (a law)
  source    : Source                  -- rom (committed candidates) | posted (a relation of candidates under self, posted by members)
                                      --   | foreign (a peer object's exported row: an offer, a value, a package)
  justify   : Candidate → List Assumption   -- rows at versions, cells live, cells live AND governed by law L (§2.5a)
  accept    : Term                    -- the judge a filling must pass; for the LAW slot: old regime ∧ new regime
  life      : revisable | affine      -- a selection may be changed until executed/accepted; an answer is given once
  patience  : Option Nat              -- after it, anyone may retire the slot's pending state
```

Every power in §2.5 is a value of this record that nano cannot express today. Nothing in §2.5 adds a second
mechanism: the ROM hole, `Std.hole`, the activity row, the offer, the law list and (new) the package link are the
inhabitants, and the design's work is to let each field range over what the kernel can already justify.

### 2.2 What a Turn admits, what a member signs, what a receipt says

**A member signs** (unchanged shape: `Unsigned` with `pins`, `rowPins`, `ranges`; READ `Kernel/Receive/Call.lean:99-115`)
a call whose pins ARE the justification it asserts: for each slot the call will demand, the selection row at its
version, every support cell at its pin (a live cell, a tombstone, or absence: KERNEL-54's three pins), every
hypothesis pin, the guard pin. The signer is asserting an ATMS environment. No new field: the environment is the pin
list, which is why premise price in the kernel is zero for every slot source but `foreign` (§3).

**A Turn admits** (unchanged shape: `touches` with `seen`, `creates`, `rows`) exactly when, on the view those pins
denote, every demanded slot has a filling whose justification holds, the filling passes `accept`, and the filled
program's run passes every law in force; or the Turn is REFUSED by the name of the first justification that failed,
with its coordinate (§2.3). KERNEL-66 makes the order right: pins are compared before any receiver judges.

**A receipt says** (today `HoleSelection`: index, version, strengthened positions, body; READ `LiveHoles.lean:136-147`,
not stored) — and this is the one addition to what a Turn RECORDS: the Turn's event already fixes the selection
(the row is pinned), so the receipt is re-derivable and need not be logged (LANG-75.4 was right). What a member CAN
be shown is the PROVENANCE of a value it reads: "section 2 of this document is candidate 4, justified by A's editor
grant live at pin p and the selection row at version 7". That is a READ-side object (`nd read OBJ` prints the slot's
label), not a log-side one, and it is the consumer of C3's live label that LANG-75.4 said did not exist (§4).

### 2.3 Refusals that name the coordinate (why-not completeness)

Today `HoleRefusal.unpinned` names nothing and `supportDead n` / `derivationMoved n` name the hole only
(READ `Lang/LiveHoles.lean:14-38`). The kernel's `unpinned <id>` names the cell; `rowUnpinned` names
`(parent, rel, key)`; LANG-79 made `Std.hole`'s collector say `unpinned support0`. The theory requires one rule:
**a refusal is the negative literal of the assumption that failed, with the assumption's coordinate.** Concretely:
`unpinned (pin : SupportPin)`, `supportDead (hole) (cell)`, `derivationMoved (hole) (pin)`, `supportMoved (hole)
(position) (pin)`. Then a client that receives `holeSupportDead 0 <cell>` knows which cell to re-read and a client that
receives `holeUnpinned (row 2 <key> 7)` knows which pin to add. This is small (`lang:`; the refusal text changes, no
package byte moves — MEASURED below in BUILT-1) and it is half of the top clause. It is the first thing built.

### 2.4 The top statement: CONTEXTUAL INTEGRITY ∧ REPAIR, a clause of INTEGRITY (TOPLEVEL-SPEC §3)

The design is a consumer of ONE HISTORY ∧ INTEGRITY, not beside it. B3 (`Integrity.law`) today promises an object's
author that every state was admitted by its laws on the pinned view, for `NoRef` laws, and leaves contextual packages
"outside the author's promise" (TOPLEVEL §3.3 (i), §11.6). This clause is what brings them inside, and it is the ONE
place the contextual layer owes a non-vacuity argument.

```lean
-- Spec/Claims.lean, beside Integrity.law (NEW statement; every lemma named exists unless marked NEW)
/-- B4. CONTEXTUAL INTEGRITY. Along an audited log, every admitted Turn that ran a contextual package ran the body
`instantiateHoles` built from the caller's own pinned view: for every demanded hole, the selection the caller's
row pin names, every support of the selected candidate observed AND holding on that view (`selectHole_origin`,
`selectHole_cell_support`), the body typed at the package's interface (`instantiateHoles_typed`), with no digest
the ROM did not commit (`instantiateHoles_sources`); and every Turn refused for a hole was refused by the name AND
COORDINATE of a justification that did not hold on that view (NEW: `selectHole_refusal_names`, the contrapositive of
`selectHole_live_selects` read off §2.3's constructors). -/
def Integrity.contextual (S : System D) : Prop :=
  ∀ {w w' l}, CellsCanon S.X.env w → Receive.audit S.X w l = .ok w' →
    ∀ e ∈ foldSteps l, ∀ (h : HoleROM) (sel : HoleSelection), Demanded e h sel →          -- NEW: the Turn's run instantiated h as sel
      sel.index = selectionAt e.pins h ∧ (∀ p ∈ (h.code[sel.index]).supports, HoldsOn e.pins p) ∧ TypedAt sel ∧
    ∀ r, RefusedForHole e h r → ∃ p, Names r p ∧ ¬ HoldsOn e.pins p                        -- why-not completeness

/-- B4′. REPAIR. A justification withdrawn stays withdrawn: once a support cell is retired (or a support row moved)
in an audited log, no later Turn of that log fills any slot by a candidate citing it (its environment is a nogood
for ever: `stale_behind_forever` at the pin, LANG-75.1's `revoked_support_refused`); and a slot whose other candidate's
justification holds IS fillable in the very next Turn (NEW: `repair_available`, from `selectHole_live_selects` on the
post-revocation view). So an object repairs without its author: the author committed the alternatives; the World
chose. -/
def Integrity.repair (S : System D) : Prop := …
```

**FLOOR (the trivial systems this alone excludes).**
- `credulousHoles`: `supportLive := fun _ => true` (LANG-75.1 plant (a)). The P8.2 re-pinned-tombstone row ADMITS and
  spends the counted unit to a revoked provider: `¬ Integrity.contextual credulous` (the supports conjunct fails),
  `¬ Integrity.repair credulous`.
- `mutePins`: `pointData` writes `live := true` without the `look` read (plant (b)): a fact naming a cell the kernel never
  had is "current".
- `blindRefusal`: `HoleRefusal.unpinned` without a coordinate: the why-not conjunct fails because `Names r p` is
  unsatisfiable for an unpinned support (this is the DEPLOYED code until BUILT-1 lands; the floor would be red against
  `deployed`, which is the floor doing its job).
- `firstCandidate`: `selectHole` ignores the row and fills index 0: `sel.index = selectionAt …` fails on any row naming 1.
- **Inhabited by** a deployed run that reaches the non-trivial case: a slot filled by candidate `i ≠ 0`, then a
  revocation, then a refusal naming the dead cell, then a fill by another candidate. P8.2/P8.3 are the Sim rows; §4's
  document row is the member-visible one.

Why this cascades (TOPLEVEL §1.3): every contextual lemma in `Lang/Proofs/LiveHoles.lean`, `StdHoleCells.lean`,
`LiveJourney.lean` becomes a lemma of B4/B4′ or internal; the per-card plants of LANG-75.x become hygiene; the three
docstring cards (C3, C4a, C7, C6) are exactly what they were ruled to be, because they are definitional under B4.

### 2.5 The powers: what a program could DO that nothing today can

**(a) A program whose holes are filled by OTHER MEMBERS' PROGRAMS under a contract.** Today a candidate is a term the
package author committed, or a value a member posted (`Std.hole`, V first-order). The P8 composition selects a
PROVIDER (a digest) and spends to it, and its justification is "the provider's grant is live" — a capability fact
about authority, not about behaviour. The missing power is a justification about WHAT THE PROVIDER IS: a candidate
that links to another object `g` may demand that `g` be governed by a law `L` (a law id the kernel holds in `g`'s cell:
`lawsOf X obj cell`, READ `Derive.lean`). That is `Assumption.cellLaw g L`: "g is live and L ∈ laws(g)". A data
object's laws can change (`relaw`, judged by both regimes), so this assumption is DEFEASIBLE in exactly the slot way:
a relaw that drops `L` retracts every justification that cited it, and the refusal names `(g, L)`. Contract-by-law-identity
is the smallest behavioural contract nano can state without a proof system: not "g behaves like L says" (that needs
B3 for g, which the audited log gives: g's every state was admitted by L), but "g IS governed by L, and the kernel
promises L was consulted on every move of g". For a programmed provider `g` (laws fixed, package fixed:
`audit_package_fixed`), the assumption `cellPackage g P` ("g runs package P") is a permanent contract: the candidate
links to a KNOWN program, and `invoke g m` through it is a call into code the author read. With §2.5c that assumption
becomes defeasible too (a relink retracts it), which is right.

What a Turn then admits: a method of object `o` that invokes `g.m` with typed arguments (LANG-77) where the hole that
chose `g` was justified by `g` live, `L ∈ laws(g)` (or `pkg(g) = P`), and the caller's grant chain to `[invoke m]` on
`g` live — all on one pinned view, in one Turn, LPCFS-atomically (REORIENTATION A.9). Price: `SupportPin` gains two
constructors (`lang!`, the ROM wire version bumps, every package id moves, no deployed Store holds a ROM hole);
`supportLive` reads the cell's law slots and package slot through `look` (the slot layout is the kernel's
`slotOwner`/`packageOf`; zero kernel change); `selectHole_cell_support` gains two arms.

**(b) The fuse as a slot; the market.** `Std.offer`'s `fuse` is a party's method that judges its own offer against
one peer offer it names (`keys`) and invokes the peer's `take`. As a slot: the counterparty is a hole of chooser
`anyone-with-[invoke fuse]`, source `foreign` (the peer's `offers` relation read under `pair`), justification = the
peer's offer row at its pin and the peer object live, acceptance = `offerJoint ∧ fair`, life = affine with the
session's patience. Nano has the pieces and lacks two things:
1. the CALLER. `Req` carries `agent`, `principal`, `self`, the window and the occasion (READ `Call.lean:318-331`); a
   nested call's `actor` is the calling object (`callStep sub obj`, `invokeRun … actor obj …`, READ `Derive.lean:182-215`)
   and `reqOf u obj principal` DROPS it. So `take` cannot refuse anyone but its peer, and one session row is not a fuse
   (LANG-77 L2 critique; HOLISTIC-LANG §3.2 fourth point). `Req.caller : Option D` (none at the root, `some actor` one
   level down) lets `take` refuse `notFuser` unless `caller = peer`, and then **one session row IS a fuse**:
   `offer_safe_forever` (LANG-75.11's deferred second conjunct) becomes statable over `row_turn_cases`.
2. a BOOK: N standing offers under one object, a taker's `fuse` choosing among them by a justified selection. With
   `caller` this is `Std.offer` with `offerLimit > 1` plus a `pick` whose candidates are the book's own rows — a slot of
   source `posted`. The market is the third consumer (§4); it is the design's demonstration that "composition it did
   not anticipate" means strangers' offers, not two fixtures.

**(c) The PACKAGE as a slot: objects repair without their author; laws replaced by a judged negotiation.** This is the
deepest instantiation and the one real kernel change. Today an object's package is fixed for ever
(`audit_package_fixed`; B3's "a package never changes"), and a programmed object's laws cannot change (`hasMethods`).
So the ONLY repair nano offers is the one the author pre-committed as ROM candidates: a World can choose among the
author's alternatives, never beyond them. "A World whose objects repair across revocations without an author" needs
the program itself to be a slot:

- `Body.relink obj pkg' via` (KERNEL): the object's cell keeps its state slots and rows; its package becomes `pkg'`.
- Occasion `.relink pkg'` judged by the laws in force (the old regime: "may this object change program, to this one?"),
  then `.adopt` by `pkg'`'s own laws over the unchanged state (KERNEL-27's rule, verbatim, applied to the program slot).
- Acceptance the KERNEL checks, not a law: the state slots type at `pkg'.state` (`stateSlots`/`readState` succeed), the
  relations `pkg'.rels` are the object's declared heads at the same indices (the rows trie is keyed by relation index:
  a relink may not renumber a live relation), and `pkg'.iface` REFINES `pkg.iface` at every method index a grant could
  name: same argument type, same call slots or fewer, same edit type or a subtype (de Alfaro–Henzinger Def. 14 at the
  type grain: weaker input assumptions, stronger output guarantees). This is B.8's `refines_substitutive` with its
  consumer finally present: package replacement (REORIENTATION B.8 said "the row waits" for exactly this).
- Justification: `pkg'` live (a ROM cell) and the chooser's authority (`ownerAuthority … .mutate via`, as `law` uses).
- Who chooses: the owner, or — through a law of the object that admits `.relink` only on a quorum (`Std.quorum`'s relaw
  arm generalised to relink) — a NEGOTIATION. "Laws replaced by a judged negotiation" is then not a new mechanism: the
  quorum law judges `.relaw`/`.relink` proposals posted as rows, and both regimes judge the switch. A JURY (§4) is this
  object.

Price, in the spec's terms: `kernel!` (a Body kind: the 13-kind ceiling `callKindsMax` moves to 14; the codec vectors
re-draw; every Store re-geneses, which is free). Landed theorems that CHANGE MEANING: `audit_package_fixed` becomes
`audit_package_relinked_only` ("the package changes only by a Turn both regimes admitted and the kernel's refinement
check passed"); `object_turn_cases` gains an arm; B3's second conjunct in TOPLEVEL §3.3 is restated; `bell_monitored`
and `activity_program_safe` are stated at a package and stay true per package (the premise "this object runs P" is
read off the cell at each step, which `ObjectHistory` already does per step). Hypotheses gained by landed theorems: by
the KERNEL-45-style count, `fold_rom` (ROM never changes) is untouched (the ROM cell is immutable; the object's LINK
moves), `packageOf`-fixed consumers in Lang (`audit_package_fixed` has two: `Integrity.law`'s conjunct and
`object_history_runs`) gain the relink arm. Weeks, one lane. It re-genesises every deployed World. It is the change
that makes "repair" mean what Ember's sentence means, and under breadstuffs/CLAUDE.md its cost is "a rebuild".

**(d) Partial results: evaluation around holes.** Hazelnut Live's indeterminate forms (Omar et al. POPL 2019) would let a
run that demands a blocked hole RETURN a value with the hole in it. REORIENTATION D.3 asked whether any consumer needs
it. The document (§4) is the first that does: a reader wants the document with section 3 marked "withdrawn (A's grant
retired)", not a refusal of the whole read. The honest nano form is not an indeterminate VALUE (it would have to be
stored, and then the fill-and-resume commutation question returns under effects) but a READ: `nd read OBJ` renders each
slot's live label (§2.2) beside its selected value, so "partial" is a property of the read, not of a Turn. No Turn
admits a partial result. That keeps law 7 (a demanded blocked hole refuses by name) and gives the reader what Hazel
gives the editor. Price: a `label` method on the slot's package (C3's reader, which LANG-75.4 said did not exist) and
one `nd` verb. Days.

### 2.6 What the instantiation does NOT license, said out loud

- Holes supporting holes (card F (3)): forbidden still; the support graph stays depth one, the label a subset test.
  The market's `pick` cites offer ROWS, not other objects' selections.
- A second count of value: linearity is the kernel's (`admit_value`); the escrow's leg discipline is
  `escrow_retract_moves_leg`; no `Val` token in any descriptor (LANG-75.18 stands).
- Cross-World slots: a foreign candidate is a RECEIPT (`(receipt)` column, E5) and its justification is a held head;
  no atomic cross-World fill (charter scope 3).
- Liveness: "a slot is eventually filled" is measured, never proved; patience is the only clock.

---

## 3. What it needs from the kernel that is not there, each as a change with its price

| # | change | needed by | price in the spec's terms | status |
|---|---|---|---|---|
| K1 | `Req.caller : Option D` (none at the root; the calling object one level down; `reqTy` gains `caller : opt digest`) | §2.5b (one session row is a fuse; the market); every slot whose chooser is `peer` | `kernel!`+`lang!`: `reqOf` gains an argument; `invoke`/`invokeRun` thread `actor` into it; every package re-emits (the request type is in every method and law type) and every World re-geneses. Landed theorems: `invoke_authorized`, `receive_ok`'s invoke clause gain a binder, no hypothesis (INFERRED from `reqOf`'s shape; the IMPACT must measure). Lang: 85 law theorems in `Receiver.lean` are over `reqData` — a binder each | a week; the readers' first item |
| K2 | `Body.relink obj pkg via`, Occasion `.relink`, the kernel's refinement check at the type grain | §2.5c | `kernel!`: a 14th Body kind, codec vectors, `object_turn_cases`, `audit_package_fixed` → relinked-only, B3 restated; every Store re-geneses | weeks; the one change that makes "repair" real |
| K3 | storage that can be retired: `Body.retire obj via` judged `.retire` by the laws in force; a retired object is a tombstone (grants on it die, its rows are unreadable) | the readers' list; the market (a closed book), the document (a deleted doc); §2.5a's `cellLaw` has a tombstone semantics already | `kernel!`: a 15th kind (or `relink` to the empty package, which is the same thing and cheaper: a retire IS a relink to a package with no methods and no state, judged by both regimes — INFERRED, and the design's default) | with K2, at no extra kind |
| K4 | a value type linear where it must be | — | none: PROT-8 settled it; linearity is the kernel's conservation; the escrow's run theorems are the discipline | no change |
| K5 | fork consistency (TOPLEVEL §11.1: `nd sync --to`, a head channel, writer-signed heads) | B4′ REPAIR across MEMBERS: "withdrawn stays withdrawn" is a statement about one log; two members on two forks could each see a different fill | not this design's change; B4/B4′ are stated over an audited log and inherit ONE HISTORY's premise exactly as B1–B3 do | a premise, named |
| K6 | the `live` column on RANGE reads (cv 01a1671d-09bf) | the market's `pick` over a range of offers with each offer's object live | `lang:`; the point arm exists (`cited_authenticated`), the range arm is the E5 receipt pattern (`receipt_row_authenticated`) | days |
| K7 | `nd read` of a slot's label; `nd invoke --pin` exists (eb77b78) | §2.5d, §4 | CLIENT: one verb reading rows it already can read; LANG: the `label` method | days |

Not needed, and named so nobody builds it: multi-signer Turns (KERNEL-45 item 2: the fuse is one signer's tree; the
market's taker signs alone), joint laws across objects (item 3: the fuse's judge reads the peer by a declared read;
a book's law sees its own rows), an abstract vat, a nogood database (the pin domain is the nogood, LANG-75.1).

---

## 4. The consumer: the second running instance

**The DOCUMENT.** The charter approves two demonstrations, documents and escrow (CHARTER §Scope). The escrow exists.
The document is the slot at its most legible: an object whose SECTIONS are slots; each section's candidates are texts
POSTED by contributors; each candidate's justification is the contributor's EDITOR GRANT, a kernel cell; the section's
chooser is the editor; acceptance is a clause (a length bound today; a law id with §2.5a); a revoked contributor's
section blocks BY NAME on the next judgment, and the editor selects another contributor's candidate — the document
repairs, and no author re-installs anything. A reader sees the sections with their labels (§2.5d).

**Does it run on nano as it is?** Yes, for one section per object, today: `Std.hole` at `V := bytes` is exactly this
(`holeCandidates` posted by anyone with `[invoke propose]`, `by` the poster; supports = `facts` citing a cell, read LIVE
since LANG-75.1; `select` by the chooser under `codeChosen`'s authority; `rejudge` recording `suspended "support0 dead"`
after a revoke; `accept` dispatching the value as an activity). The journey rows LH0–LH14 and P8 ARE a document's life
in the Sim. What does not exist: a `world/doc/` text, a deployed row (`client/tests/*.rs` or `rows/`) that drives it
over `nd`, and the multi-section object. The first is Print's `contextualText` of the generated bundle (helper ids are
content digests, so a `world/` text can import them by fixed id); the second is `nd invoke --pin REL KEY` (landed) for
every judging method; the third is K-slot `Std.hole` (several `selected` fields; a generator parameter) or several
section objects under one `Doc` that reads them by peer read — the former is the honest one and is a `lang!` of the
generator only.

**The MARKET** (third; needs K1, K6): a book object of `Std.offerEscrow` with `offerLimit = 64`; members post offers with
legs and wants; a taker's `fuse` names the two keys and refuses `unfairLegs` or `notFuser` by name; a posted offer whose
poster's object was retired is refused `supportDead <cell>`. It exercises (b) and (a) together: a `pick` whose
candidates are foreign rows with the poster's law as the contract.

**The JURY** (fourth; needs K2): an object whose laws are `Std.quorum` over its members and whose program may be
relinked only by a quorum-admitted proposal: "laws replaced by a judged negotiation", with the old program's laws and
the new program's laws both judging the switch. A verdict object is a data object born under the jury's laws.

The Bell stays the running multi-party instance; the document joins it as the running CONTEXTUAL instance; §6's
sequence builds the document first because it is the one that needs nothing from the kernel.

---

## 5. What to DELETE: the protocol calculus remnant

`Lang/Contextual/{Protocol,LangInstance,NanoBridge}.lean` and `Lang/Proofs/Contextual/{Protocol,ProtocolTyping,
Negotiation,Failures,LangInstance}.lean` (MEASURED: no module outside `Lang/Contextual` and `Lang/Proofs/Contextual`
imports them, LANG-75.17). Ember kept them (R-0021) as a research line. The design's position:

- The calculus is the SEED of exactly one thing in this design: the slot descriptor (§2.1) is `Iface` with
  `chooser` widened to four values and `source`/`justify` added, and the slot's two laws are `at_most_once` (an affine
  slot fills once) and `executed_prefix_blocks_replan` (an accepted selection is never re-filled: `Std.hole`'s
  `accepted` guard, `WaitingStep`'s answered-once). Those two theorems are what the calculus has that the deployed code
  does not STATE; `HasProt`'s hole rule is the slot's typing. `Prot`'s `call`/`ret` and `Hist.inflight` are the
  activity's one exchange, restated beside it (LITP D.1: one exchange deep).
- `NanoBridge` is a wrong cut (Lang importing Hosting) and a rename of `interp_runs`: delete it in the first landing that
  touches the directory. `Negotiation` is `Std.offer`'s judge over a private World: delete with it.
- `Protocol.lean` + `ProtocolTyping` + their theorems: KEEP until the slot descriptor lands in the deployed language
  with `slot_fills_once` and `slot_executed_fixed` stated over `Std.hole`/`Std.activity` (§6 S5); then delete, because
  every statement will have a successor over a deployed object. `Failures.lean`'s deployed half
  (`submit_at_most_once`, `lost_ask_keeps_obligation`, `lost_reply_policy`) is already over deployed objects and MOVES
  out of `Contextual/` to `Lang/Proofs/` and `Hosting/Proofs/` where its subjects live.

So: not the seed of the design's mechanism (the mechanism is the deployed hole), the seed of its TYPE; and a type
written beside its inhabitants is deleted the day it is written over them. R-0021 is honoured by sequence, not by
keeping vocabulary.

---

## 6. The sequence: what to build first and what each step makes true (in Ember's terms)

| step | what the system can then do that it cannot now | needs | size |
|---|---|---|---|
| **S0 — refusals name their coordinate** (§2.3) | a client refused for a dead or unpinned support is told WHICH cell or pin, so it can re-plan without guessing; the why-not half of B4 is inhabited | nothing; `lang:` | hours (BUILT-1) |
| **S1 — the document** (§4) | a member can hold a document whose sections are other members' posts; revoke a contributor and see the section withdrawn BY NAME; select another's and see it return; all through `nd`; B4 ∧ B4′ inhabited by a deployed run; the contextual layer has a READER (the readers' one stop-doing becomes moot) | `world/doc/*` texts; a client row; K-section `Std.hole` (`lang!`, generator only) | days |
| **S2 — contract-by-law** (§2.5a) | a program can be filled by other members' programs and demand that they be governed by a named law (or run a named package); dropping the law withdraws the fill by name | `SupportPin.cellLaw`/`cellPackage` (`lang!`, ROM wire bump) | a week |
| **S3 — `Req.caller`; the market** (§2.5b, K1, K6) | `take` refuses anyone but its fuser: one session row IS a fuse, `offer_safe_forever` statable; a book of strangers' offers, taken by name, each refusal naming its coordinate | K1 (`kernel!`+`lang!`), K6 | 1–2 weeks |
| **S4 — relink; the jury** (§2.5c, K2/K3) | an object's program is replaced under both regimes with its state and rows kept; a quorum negotiates the replacement; objects repair without their author; retire = relink to nothing | K2 (`kernel!`) | weeks, one lane |
| **S5 — the slot descriptor; the calculus deleted** (§5) | one vocabulary for hole, row, offer, law list and package link; `slot_fills_once`/`slot_executed_fixed` over the deployed generators; `Spec/Claims.lean` B4/B4′ with their floors | S1–S4 | a week after S4 |

S0 and S1 first because they cost no kernel change and together make the top clause inhabited by a run a member can
see; S2 before S3 because its wire bump is the same version byte S3 needs; S4 last because it is the only change that
restates a landed promise (`audit_package_fixed`) and should land into a tree where B4's floor already runs.

What this sequence refuses to do: land a theorem with no reader (the LANG-75 lesson, nine times), build a second judge
beside `selectHole`, or price any step by its re-genesis.

---

## 7. Three ways this design is most likely wrong

1. **The slot is a rename.** If §2.5a–c land and no row needs a chooser other than `me`/`other`, a source other than
   `rom`/`posted`, or an assumption other than `live`, the descriptor is `Iface` with more fields and the calculus's
   fate (vocabulary without inhabitants) repeats. Measurement: after S2, count the rows whose refusal names a `cellLaw`
   coordinate; after S3, the rows refused `notFuser`. Zero of either ⇒ delete the field, not the row.
2. **Relink is too much power for one owner.** An owner relinking a document to a package that drops a section is an
   author re-installing by another name; "repair without an author" then means "repair by the owner". The design's
   answer is the quorum chooser and the refinement check (the new interface must refine the old), but the refinement
   is at the TYPE grain and a same-typed malicious package passes it. Measurement: the jury row where a relink proposal
   that keeps the type and changes the verdict rule is refused by the old regime's law, not by the kernel. If only the
   kernel can refuse it, §2.5c needs a behavioural contract nano cannot state, and relink should be owner-only.
3. **The document is a journey in a costume.** If the member-visible row is the Sim's LH rows re-run over loopback with
   nothing a reader does differently, the "second consumer" is a test. Measurement: the `nd read` label (§2.5d) must
   show a reader something the Turn log does not — the provenance of a section — or S1 has not produced a consumer.

---

## 11. The resident inside the open calculus (real 2026-10-27; FABLE-CTX-4; Ember's order: replace the `Empty`-hole embedding, then delete it)

**Where it stands.** The resident's tick is `Hosting.Resident.Prog` (cmd, keep, forget, ask, say), run by
`Prog.interp`. `Hosting/Contextual/NanoBridge.lean` embeds it into `Lang.Contextual.Protocol.Prot` with hole type
`Empty`, so no hole of the calculus ever meets the deployed system. Every decision the resident makes is written
as a Lean `match` inside the tree (`decideTick`, `deliverP`'s refusal arm, `forwardPin`). READ: `Hosting/Resident/Run.lean`,
`Hosting/Resident/Bell.lean`, `Lang/Contextual/Protocol.lean`, `Hosting/Proofs/ResidentRun.lean`.

**The resident's holes (the decisions that are contextual in fact).**

| hole | the question | candidates | supports of a candidate | chooser |
|---|---|---|---|---|
| `serve` | which ring this tick acts on | the pending rings the read returned; the kept ring | `pending[k]` live at the read; for the kept ring also the kept record on the volume | the resident, by `decideTick` (kept first, then lowest) |
| `text r` | the answer text for ring `r` | the kept text; an ask (the model's answer); the named texts `(unanswered WHY)` | the ring's capture (`pending[k]` with its text and aim); the ask also spends the ring's one ask token | the resident; the model supplies the ask's candidate |
| `pins r` | which support rows the answer pins | for an aimed ring, the target's `facts` row at `forwardKey via`; none otherwise | the `via` grant live; that `facts` row present | the resident (a function of the aim today) |
| `use r t` | what to do with `(r, t)` when the answer is refused | forget (the slot is closed); withdraw `r` by the name of the dead support and serve another ring; stop the queue | the failed support's coordinate, read from the refusal and the re-read | the resident |

The model's answer is therefore a CANDIDATE for `text r`, justified by the ring's capture, not a value. The kept
file is the candidate store; the intent `(unanswered restart)` is the candidate a restart holds when the ask's
outcome is unknown.

**What the calculus lacks (the first finding).**
1. *Resolution at run time.* `σ` is chosen before anything is observed; `interpret` ends `stuck` at a hole. The
   resident decides after its read. The calculus needs a resolution judgment: at the hole's reach, with the view
   then current, the filling is the selected candidate whose supports hold, or the run is withdrawn by name.
   `Result` needs a third outcome, `withdrawn h (failed supports)`, beside `done` and `stuck`.
2. *Candidates with supports.* `Iface` has `ctx` (what any filling may use) and `accepts`, but no candidate set, no
   per-candidate support list, no selection. This is the SLOT: `cands`, `supports : Cand → List Fact`, `select`.
3. *A view that moves during the run, and refusals as responses.* `View` is a static record beside the handler;
   `admits` is a precondition. On nano the kernel checks supports at the effect, and the resident learns of a dead
   support from the effect's RESPONSE (a refusal with its coordinate). The calculus needs the view as a function of
   the handler's state, and `Spec.names : Resp op → List Fact`: which supports a refusal names.
4. *One repair rule.* `Open.replan` (re-substitution, guarded by `Dispatched`) and `Frag.repair` (re-checking cached
   verdicts by support footprint) are two unconnected pieces. Repair must be one rule: after a withdrawal naming
   `f`, re-resolve exactly the holes whose selection cites `f` and that the history has not entered.
5. *Permanent and reversible supports.* `holds : Fact → Bool` cannot say that a retired cell or an answered ring
   stays false forever while a law membership may return. Withdrawal is permanent only for the first kind.
6. *Response-indexed hole names.* The resident's holes are named by data the read returned (`text r`). The
   calculus calls such naming foresight, because its `σ` is chosen in advance. Under run-time resolution the
   filling reads only the view at the reach, so data-named holes are sound; the statement must say so.
7. *A monadic interpreter.* `interpret` folds a pure handler. The deployed resident needs `interpM`, one call per
   node, as `Prog.interp`.

What already fits: the affine discipline. "Exactly one ask per ring" is a token `ask r` spent by the ask
(`at_most_once`, `commit_once`); a kept answer is a filling the history has entered (`Hist.inflight`,
`Dispatched`), so `Open.Replan` forbids re-planning it, which is the resident's "never ask twice".

**The term (sketch).** `RSig` is the resident's five effects (the signature NanoBridge defines, moved to
`Hosting/Resident`). `RHole := serve (pending : List Ring) | text (r : Ring) | pins (r : Ring) | use (r : Ring) (t : ByteArray) (refusal : Reply)`.
```
tickT m := describe? ; call (read sh) fun pending => hole (serve pending)
serve-candidate r := hole (pins r) ; hole (text r) ; call (invoke r t pins) fun
  | ok => forget ; ret next
  | refused x => call (reread sh) fun p' => hole (use r t x)
text-candidate ask := keep r intent ; call (ask r q) fun a => keep r (answerText a) ; ret t
```
The deployed tick is `interpM ioHandler (resolve m) (tickT m)`, where `resolve` is the SLOT resolver over the
resident's view (the read's rows, the volume's kept record, the refusal's coordinate). Behaviour that changes:
an aimed ring whose `via` grant was retired before the answer is refused `support0 dead`; today the resident
ends `answerRefused` and the whole queue stops behind that one ring. Under `use`, the answer is withdrawn by
that name, `r` joins a withdrawn set in `Mem` (permanent: a retired cell is a tombstone), and `serve` re-resolves
to the next ring in the same tick. That is repair without a restart.

**The theorem (over this instance, then over the SLOT).** The resident's answer `(r, t)` is invoked at a view
only if every support of its selection is live in that view; a support that dies is named in the withdrawal
the next read records, and no later tick invokes `(r, t)` while that support is a tombstone; when another
pending ring's supports are live, `serve` selects it in the same tick, without a restart or a reinstall.
Proved from the resolver's definition and the existing `tick_order`/`kept_follows` (which carry over by
`resolve_fills`: on every path without a withdrawal the resolved term is `tickP`'s tree).

**Order.** (i) The SLOT in `Lang/Contextual/Slot.lean`: resolution, `withdrawn`, the repair rule, `interpM`
(findings 1 to 4 and 7). (ii) The resident as `tickT` + `resolve`; `tick` runs it; ResidentRun carried by
`resolve_fills`; the new withdraw path and its theorem; `resident_bell`/`agent_hole` re-run, and a row in which the
via grant is retired before the answer (today: `answerRefused`; after: withdrawn by name, the next ring served).
(iii) The testground's inbox demo shows the holes filled and withdrawn (a line to TESTGROUND). (iv) Then delete
NanoBridge, ContextualNano and the `Empty` instance. K2 (`notFuser`) lands meanwhile; the document's evidence-bearing
read (CRIT-CTX's third requirement) follows as the SLOT's second instance.

---

## BUILT — appended per landing (the design memo is the record)

### BUILT-1 — S0: refusals name their coordinates (landed `18cd38b`, 2026-10-26, `lang:`, fast judge)

What a member sees now that it could not: `nd invoke` on a contextual object refused for a dead, moved or
unpinned support prints the support's coordinates — `holeSupportDead 0 cell:<idhex>`, `holeDerivationMoved 0
row:2:<keyhex>:0`, `holeSupportMoved 0 1 row:2:<keyhex>:0`, `holeUnpinnedRow 2 <keyhex>` — through the real
receivers (MEASURED: the LP rows "stale derivation blocked", "omitted blocker pin", "suspension preserves used
hypothesis refusal" in `lang-journey --contextual` print them). `HoleRefusal` (`Lang/LiveHoles.lean`):
`unpinnedRow rel key`, `unpinned (pins)`, `supportMoved hole position pin`, `derivationMoved hole (pins)`,
`supportDead hole (pins)`; `selectHole` throws the FILTER of the failed `all` (every failing support, never an
empty list when thrown); `SupportPin.wire`, `pinsWire`, `hexOf` (two pushes a byte, no list). No package byte
moved; the Std.hole package is byte-identical (its refusals are its own term's strings, LANG-79's `unpinned
support0` stays). Proofs: no statement over `selectHole` changed (the thrown term is not in them); the three
LiveJourney teeth now name the pin or cell they refuse on. Decls: 9 declared changes of meaning (the type, its
printer, `holeRow`, `supportPinned`, `hypothesisStep`, `selectHole`, the three teeth). One lesson, paid: a
printer defined by `match` on `SupportPin` placed ABOVE `supportLive`/`supportObserved` changed THEIR bodies
(Lean reuses an identical matcher, so their value named a new constant); the judge caught it as an undeclared
redefinition, and the printers now sit below the predicates. Journey: default 915 lines GREEN, `--contextual`,
`--contextual-checks`, `--hole-omitted-blocker-pin-admits` GREEN. Not done: `HoleRefusal.unpinned` for a HYPOTHESIS
cell pin and the guard's cell pin is one pin (`[p]`); the kernel's own `unpinned <id>` for an unpinned cell
still precedes it on the live path (KERNEL-66 compares pins first), so `holeUnpinned` is reached only by a
pinned-absent cell, which is exactly its meaning.

### BUILT-2 — S1: the document (landed `62a36ee`, 2026-10-26, `lang:`, fast judge; decisions/lang.md LANG-83)

What a member can do now that it could not: hold a SECTION (`Std.hole` at `bytes`, the shipped texts
`world/doc/Section.lib0..2` + `Section`, 4 × `nd install`), let a contributor it granted `invoke:2,invoke:3`
post a fact naming its own grant and propose a text under it, select that text (`--pin candidates … --pin
facts …`), revoke the grant and see the text withdrawn BY NAME on the next judgment (`nd read OBJ candidates
8` shows `suspended "support0 dead"`; a `select` of it is refused `select: refused support0 dead`), then select
another contributor's text. MEASURED: `client/tests/doc.rs` — two real members (A the founder and editor; B
joined over a signed invitation with its own follower) over `host serve` and two `host follow`s — passes in
5.6 s on hbox; `lang-journey` DC0 (the four shipped texts are the generator's, read from disk) and DC1–DC9c
(the same life through `Receive.submit` at the Sim's ids) GREEN; plant: one byte appended to `world/doc/Section`
turns DC0 red. `lang-journey --write DIR` is the one writer of the texts (deployed ids: `romIdOf` under
`Codec.Deployed.env`, what `nd install` prints). No theorem is new: the section is `Std.hole`'s package at a
value type, so `posted_support_checked`, `revoked_support_refused_hole`, `cited_hole_point` and
`holeDecision_verified_iff` are its theorems. Two things the Sim had not stated and the member run did: the
editor's `select` must pin the SUPPORT'S CELL (the grant) beside the rows, or the kernel refuses `unpinned
<cell>` before any judgment; and `nd read OBJ ?` prints the state's TYPE — the selected candidate is read from
`nd read OBJ`, the state printed by the one printer. Against §7.3's refuter: the member sees provenance only as
the candidate row's `s0` and `status` today; the live LABEL of §2.5d is not yet a read. Against the readers'
"nothing deployed reads the contextual layer": a cargo row and four shipped texts now do.

### BUILT-3 — S2: contract pins (BUILT, green on 62a36ee; the `lang!` landing refused by the full judge on a moved main for three bookkeeping reasons, recorded with the reland recipe in `redregg/work/FABLE-CTX-CONTINUATION.md`; decisions/lang.md LANG-84 is in the worktree)

What a program can do now that it could not: a candidate that links a hole to another member's object can
demand what that object IS — `SupportPin.cellLaw g L` (live AND governed by the law package `L`) or
`SupportPin.cellPackage o P` (live AND running `P`) — read off the cell the kernel holds through the caller's
pinned view, in the same Turn as the fill. A data object's `law g []` that drops `L` withdraws every fill
that cited it: the next demand of the hole is refused `holeSupportDead 0 cellLaw:<g>:<L>` by name (MEASURED:
`lang-journey --contextual` LG0–LG6 through `Receive.submit`; the boundary rows `cell-law-governed`,
`cell-law-ungoverned`, `cell-law-dead`, `cell-package-runs`, `cell-package-other`, `cell-law-unpinned`).
Theorem `selectHole_contract_support`; plant: the contract read as mere liveness reds it by name and admits
LG4. The ROM wire gains two pin tags (`node 2`, `node 3`); the package wire moves to version 6 (every package
id moves; a version-5 package refuses `lang/package-version/6`; `codec-vectors` re-drawn, 288 vectors of 59
sites; `world/doc/Section` re-emitted with the helpers' new ids; the doc cargo row passes with the host at v6).
Honest limits (LANG-84's critique): a contract by law promises "L was consulted on every move of g" (B3), not
"g behaves as L's name says"; on a programmed object both contracts are permanent until the package is a slot
(S4); nothing deployed cites a contract yet — the market (S3) is its first consumer. The LG rows are the
first run in which a World withdraws a program's justification by changing a LAW rather than a grant: the law
list acting as the slot §1.2 row (2) says it is.

### BUILT-4 — K1 `Req.caller` (BUILT 2026-10-26 in wt/fable-ctx-caller on c82f171, NOT LANDED: `kernel!` + `lang!`, KERNEL-76 + LANG-85 placed; lands after S2 under the queue; recipe in `redregg/work/FABLE-CTX-CONTINUATION.md` §3)

What a program is told now that it was not: who called. `Req.caller : Option D` is `none` for a call a member
signed and `some obj` for a call object `obj`'s run returned (`tree` dispatches each returned call as the calling
object AND as its caller; `derive` the signed Body at `none`); `At` carries it; every receiver arm passes it to the
program it judges or runs; `reqTy` gains `caller : opt digest` (its second field), so a law or method reads
`req.caller`. The kernel hunk is exactly §2.5b's K1 and §3's row, at TYPES §7's shape (one definition, no fork).
MEASURED: the whole tree green (774 jobs); fifteen mechanical passes over the proofs — `Dispatched` carries the
caller as an index (`root` at `none`, `call` at `some obj`), `effect_as_signed` says "as actor and as caller",
`Lang.RunSource` gains the caller's digest as a source, `reqData_digests` lists it, `Ledger.reqAt` takes it,
`MovesThrough`/`CreditsThrough` quantify it; no landed theorem gains a hypothesis. The tooth is the kernel witness:
`c1_invokeRunB` (B's invoke derived as A) returns `reqB` at `caller = some 6` by `decide +kernel` — had `tree`
passed `none`, it would not close. Every shipped text re-emits by its writer (the request type is in every method
and law type); `fixtures/pin/Live` has NO generator in the tree (brought to the printer's form by hand, `ob` reads
it: a gap to close with a generator); the bar row's `reopen-bytes-per-byte-past-base` plant moves 5.260 → 5.292
(the base World grew) and the worstcut-rows waste rows 20.184 → 20.191 (the Bell's id moves). No wire FORMAT moves:
an old package is refused at install by the method-type check, by name. Honest limit: nothing deployed reads
`caller` in this landing; S3's `take` (`notFuser` unless `caller = some peer`: one session row IS a fuse) is the
first reader, its term patch drafted (`offerGate … fuserOnly`) and its proof work (`offerTakeTree_inv` + the gate
lemmas) not begun. Against §7.1's refuter: the count of rows refused `notFuser` is the measurement, after S3.

### BUILT-5 — the journey's session registry (BUILT 2026-10-26 in wt/fable-ctx-k1 on c82f171, NOT LANDED: `lang:`, lands FAST when the queue is quiet; the board's session-line friction)

Not a slot: tooling the board asked of whoever next touched `Lang/Journey/Main.lean`. `Journey.register` (an
`initialize`d `IO.Ref` of `Session {name, run : IO Run, contextual}`), one `initialize register { … }` line at
the end of each session module, `Main` = imports + `main`; `runAll` runs every registered session in the default,
JUDGED journey (`--contextual`/`--contextual-checks` are filters, same last line). FOUND on the way: `gates/runs.tsv`
ran neither `--contextual` nor `--contextual-checks` — the contextual sessions (P8's cycle, LH, S2's LG rows, the
LP boundary/gate/wire rows) ran in no judge since they were written. MEASURED: all five modes as expected (1182
lines in the default run).

### BUILT-6 — S3's LANG half: one session row IS a fuse (BUILT 2026-10-26 in wt/fable-ctx-s3 on the K1 tree, NOT LANDED: `lang:`, LANG-96; lands after K1, whose `Req.caller` it reads)

What a program can refuse now that it could not: a `take` nobody's `fuse` made. `offerCallerIsPeerT` reads the
request's `caller` (KERNEL-76) against `some` of the deal's other party and `offerGate … fuserOnly` puts the whole
gate under it: a take signed at the root (`caller = none`) or made by any other object is refused `notFuser` before
the name check; the fuse (a party's root call) makes no such demand. MEASURED: journey LF9 (A, X's owner, invokes
X.take at the root on LF1's deal: `take: refused notFuser`, both offers stand) and LE9 (the escrow: refused, no leg
moves), LF1/LE1 admitted as before (the nested take's caller is the fuser); the whole tree green. Theorems:
`take_notFuser` (new); `take_iff_compliant` restated — a take returns iff `CalledByPeer ∧ NamedKey ∧ JointOk`;
`take_run_sound`/`take_core`/`escrow_take_run_sound` say the deployed run was called by its peer (over the request
DATA, `optData … r.caller`, the same grain as `NamedKey (bytesOf r.self)`); the method-grain refusals gain the
premise `CalledByPeer` (the arm they lost is `take_notFuser`); the fuse theorems are unchanged in statement. Nothing
shipped re-emits: the escrow WORLD is a lowered `.ob`, not `Std.offerEscrow`'s package; no vector row holds an offer
package. Against §7.1's refuter: rows refused `notFuser` now exist (LF9, LE9: two). Not in this landing:
`offer_safe_forever`'s second conjunct over `row_turn_cases` (the theorem composing `CalledByPeer` with
`fuse_run_sound`'s call conjunct: "the row a take inserted was inserted by the peer's judged fuse on the same deal")
and the market (a book, `offerLimit > 1`, a taker's `fuse` by name, K6's `live` column on range reads).

### BUILT-6 — K2/S3 `notFuser` (LANDED `48232e7b`, 2026-10-27; decisions/lang.md LANG-100)

`Std.offer`'s and `Std.offerEscrow`'s `take` refuse `notFuser` unless the request's `caller` is the deal's other party:
one session row is a fuse. The first reader of `Req.caller` (K1). MEASURED: lang-journey LF10/LE9 `take: refused
notFuser`, every mode GREEN on 276ded81 + K2. Pushed by hand: the lander's only red was `rows --deployed` at the 600 s
wall clock.

### BUILT-7 — the resident inside the open calculus (LANDED `2630ea32`, 2026-10-27; LANG-101, HOSTING-59)

§11 (i)-(ii) and (iv) built: the SLOT (`Lang/Contextual/Slot.lean`: `Slot`, `Reading`, `slot_repair`, `interp`,
`Slot.resolve`); the resident's tick a `Prot` term with two holes (`serve`, `use`), run by `Slot.interp`; NanoBridge and
ContextualNano deleted. §11's finding 3 was measured, not assumed: the member's refusal line for a dead `via` is
`refused missingCell` with no coordinate, so the `use` slot's supports are PROBES of the World (`read CELL ?`), not the
refusal's text. The deployed defect §11 named is closed: agent_hole H4, a ring through a retired grant is withdrawn by the
grant's name and the next ring answered in the same process. Not built from §11: the `text r` and `pins r` holes (the
model's answer is still a value, not a candidate); the testground line; the document's evidence-bearing read (§11 (7)).


### BUILT-8 — the withdrawal survives a restart (LANDED `2efa6a57`, 2026-10-27)

The `use` slot's withdrawal is kept on the volume (`vol/withdrawn-<bell>`, `Eff.note`, a keep at another name) before the
answer is forgotten, and `run` seeds `Mem.withdrawn` from it: the permanence `slot_repair` (3) asks for now holds across a
process restart, not only along one life's ticks. agent_hole H4 reads the file.

### BUILT-9 — the document's read with evidence (2026-10-27, FABLE-CTX-6; LANG-109)

§11 (7) and CRIT-CTX's third requirement. `Lang/Contextual/Section.lean`: a section is a `Slot` whose facts are the
package's supports (`current r s`, `unblocked s`) and the document's own, the ADVERTISED support (support 0 is a live
grant on the section held by the candidate's author; `omitted` when support 0 is absent). `readAt` reads the stored
selection at the reader's World: `usable C` with text, author and every support's state, or `blocked C` by exactly
the failing supports. `nd read --evidence S…` prints every section in order, a blocked one beside the rest. Theorems
(`Lang/Proofs/Contextual/Section.lean`): `usable_iff_verified` (usable iff the package's own label is `verified` AND
the advertised grant holds), `usable_evidence`, `section_repair` (slot_repair at the section, with a retired support
blocked at every later World), `viewOf_later` (the fold keeps a tombstone: `fold_tomb_stays`). MEASURED: lang-journey
DC6e–DC14; `client/tests/doc.rs` over three members. The rows CRIT-CTX named: a revoked grant blocks the text by name
while it is still stored and its row still says `verified`; a contributor who SUBSTITUTES its member cell for its
grant, or OMITS support 0, is admitted by the package and blocked by the read by name; another member's text,
selected in the same section, is usable at once; a document of two sections shows the blocked one beside the usable
one. Against the baseline (§1.4): an ACL row store reading `selected` shows all four of those texts as the section's.
Not done: the package does not refuse what the read blocks (cv 01a17e0d); §11's `text r` and `pins r` holes
(FABLE-CTX-6.continuation.md).
