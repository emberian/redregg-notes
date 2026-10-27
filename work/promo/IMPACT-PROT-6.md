# IMPACT-PROT-6 — E3 + PROT-6: the declared peer row read, Std.offer, the fuse, the joint judge (CX-PROMO-5, 2026-10-23)

Base: nano `origin/main` = `1fc905f` (worktree `hbox:/tank/dregg-build/nanodregg/wt/promo`, clean). Nothing is built
yet. Tags: MEASURED (a command or a build ran), READ (file:line read this session), INFERRED (my reasoning, not checked
by a build), ASSUMED-BY-ME (a design choice the reader should challenge). The card text is R-0044's row and plan §3 P3
"E3 + PROT-6". P3-MEASURE (R-0044) ruled the cheap branch: one θ, no second round, so LITP D.3 applies and the
session-type framing of negotiation is DROPPED. What lands is two offer rows, one judge `A θ ∧ B θ` over the shared θ,
and atomic consumption in one Turn. Bartoletti's [Fuse] is kept for its consumption rule and for honesty.

## 0. What the kernel already gives, measured before any design

1. **A row read under another object costs the kernel nothing.** [READ]
   - `RowView.points : D → Nat → List (ByteArray × Option RowLeaf)` is indexed by PARENT and relation
     (`Kernel/Receive/Call.lean:282–284`).
   - `rowView` filters the caller's `rowPins` by `k.parent = parent ∧ k.rel = rel` for any parent (`:427–431`).
   - Every row pin becomes a `RowTouch` with `seen := some digest`, whatever its parent (`rowTouchesOf`, `:550–557`), so
     `World.admit`'s stale check covers a peer row pin exactly as it covers an own one.
   - `receive_congr`'s `rows` hypothesis equates the whole `rowView` (READ-E1 spot-check, `Kernel/Proofs/Receive.lean:38–41`).
   - Kernel lines changed for the read: **0**.
2. **Only Lang's view is self-only.** [READ] `runSetupWith` builds the rows argument as
   `readsData digestOf look p.rels rv r.self sg.reads` (`Lang/Program.lean:404`). `relReads`'s parameter named
   `self` is just the parent it reads under (`Lang/Rel.lean:177–179`: `rv.points self i`). So a peer read is
   `readsData` at `parent := peer`. Lines changed in `readsData` / `relReads`: **0**.
3. **Consumption of the peer's row must be the peer's own run.** [READ] `invoke` refuses a run's row edit under any other
   object: `rowParent obj` (`Kernel/Receive/Derive.lean:225`, law 4). So [Fuse]'s "both latent contracts consumed" is
   two runs in one call tree, each party's own: one run retracts X's offer and one retracts Y's, in one `Draft` sealed
   once (`deriveTurn`, `Derive.lean:380–383`; KERNEL-45 "the tree commits or fails whole"). Who calls whom is §0.6.
4. **Authority for the nested call.** [READ]
   - An object may be a grantee (`checkGrantee`, `Derive.lean:305–312`).
   - The deployed pattern is the Relay's: the owner of the next object grants the calling OBJECT `[.invoke m]`
     (`Lang/Journey.lean:1782`, `(.grant y x [.invoke 0] none)`).
   - A PUBLIC grant cannot be held by an object: `granteeHolds … pub` requires `agent` to be an enrolled MEMBER
     (`Kernel/Receive/Authority.lean:17–23`).
   - So an offer is open to the objects its owner granted `take` to, never to "anyone". The open `anyone` offer of
     ACT-D card E needs a kernel change to public grants. That change WEAKENS a check (CLAUDE.md pause item 2), so it
     is not in this card (§9 Q4).
5. **A joint judge needs no kernel hook if it runs as row guards do.** [READ]
   - KERNEL-45 item 3 (`decisions/kernel.md:1908`): "Price: a separate judge (as LANG-44's row guards are), so the 85
     law theorems … keep their statements."
   - Row guards run inside Lang's `run` (`guardEdits`, `Lang/Program.lean:428–440`), not in a kernel hook. §3 is that
     fork.

6. **THE BLOCKER (MEASURED, the first item of the work): a method cannot hand a nested call a value it computed.**
   [READ]
   - The invoke call arm's `args` is `bytes` (`Lang/Package.lean:113–114`), and `bodyOf` takes it as bytes as they
     are (`Lang/Call.lean:162–164`).
   - No `Term` constructor encodes data to bytes (`Lang/Term.lean:44–70`: var, lam, app, fix, literals, prim, record,
     get, extend, inj, case, ite, ref, refuse, hole). No `Prim` does either (`:17–26`).
   - LANG-23 (iii) recorded it: "a nested invoke's `args` are bytes. Until ID-4's bytes primitives, a method forwards
     only bytes it already holds" (`decisions/lang.md:374–375`). LANG-64 landed `cat`/`lenLe`, not an encoder.
   - The Relay, the one deployed nested invoke, forwards the bytes it was given (`Lang/Journey.lean:298`).
   - So the plan's shape cannot judge ONE θ on both sides. In that shape X's `fuse` judges θ (data in its argument)
     and calls `Y.take`, and `Y.take` needs θ too. X can only pass bytes the signer supplied, and nothing can check
     that they encode X's θ. The two runs could judge two different θs, each compliant, and the two session rows
     would then record two different deals.
   - The fix must put the SAME bytes in front of both judges (§1 b, the matcher), or let a method build typed call
     arguments (§3, fork T), or judge the two session rows jointly in the kernel (§3, fork K).

## 1. The design (one landing, L1; §7 is the second landing, L2)

### (a) The declared peer row read — E1's live column generalised from a CELL to a ROW under another object

ASSUMED-BY-ME shape, the smallest that keeps every read declared in the method's TYPE (law 5: never ambient).

- **`Sig` is NOT widened.**
  - MEASURED: three Hosting STATEMENTS spell a `Sig` by anonymous constructor (`Hosting/Proofs/Allowance.lean:93,95`
    `⟨unit, [], [], 0⟩`, `Hosting/Proofs/Package.lean:154`), so a new field would restate Hosting.
  - Instead, a method type's rows record MAY carry one reserved field `peer` whose type is `readsTy rels ps` over the
    package's OWN relations.
  - `methodSig` checks the rows record against `rowsTy rels sg.reads ps`: the own reads, plus `peer` in sorted
    position when `ps ≠ []`.
  - A new `peerSig p ℓ : List (Label × RelRead)` returns `ps`.
  - `methodSig_spec` (`Lang/Proofs/Load.lean:334`) is restated (`readsTy` → `rowsTy … ps`). It is a
    `RESTATES-MEANING`, true of every method that declares no peer, since `rowsTy rels rs [] = readsTy rels rs` by
    definition.
- **The argument names a PAIR, and the peer is the member of the pair that is not self.**
  - A method with `ps ≠ []` must have an argument record with a field `pair : rec {a : digest, b : digest}`.
    Otherwise it is refused at install by name, `peerNotNamed ℓ`: a new `CheckError`, law 7, treated like
    `liveNotCellKeyed`.
  - At run time, `peerOf self pair` is `b` if `a = self`, `a` if `b = self`, else refused `notParty`.
  - Why a pair and not a single `peer` field: §0.6. Both judges must read IDENTICAL argument bytes, so the argument
    cannot say "the other one" differently for each side.
  - A relation labelled `peer` is refused `badRel peer`. MEASURED: no package in the tree declares one
    (`git grep '("peer"'` is empty).
- **`peerReads look rv pkg rels self args ps`** (new, `Lang/Rel.lean`):
  - `peerOf`;
  - `readKind look peer kindObject`, so an unpinned peer is the kernel's own **`unpinned peer`** by name, and an
    absent one is `missingCell`;
  - its slot 0 must equal `bytesOf pkg`, else **`program "peer: another package"`**;
  - then `readsData digestOf look rels rv peer ps`, the SAME function as the own read, at `parent := peer`.
  - The peer is always of THE SAME package, so its layout is the reader's own `rels` and no foreign declaration is
    trusted (§9 Q1).
- **`methodReads`** is `readsData … r.self sg.reads`, extended by `("peer", …)` when `ps ≠ []`. `runSetupWith` uses
  it where it used `readsData` (`Program.lean:404`). It is the only path from `rv` to a method (READ
  `Program.lean:398–409`).
- **Unpinned rows.**
  - A peer ROW the caller did not pin is an empty point slot (`slotsD`, `Rel.lean:93`). It is never read from the
    World, and the generated `take` refuses it as **`peerRowUnpinned`**.
  - A pinned-absent row is `some {key, val := none}`, refused as `noPeerOffer`.
  - A cell read takes the kernel's name; a row slot takes the program's (E1 R1's asymmetry).

### (b) `Std.offer` — `Lang/StdOffer.lean` (new; the session reuses `activityLog` / `activityWaiting`, so **Std.activity's layout does not change**)

`offerPackage (theta : List Label) (roles : List Label) : Except OfferRefusal Package`. θ is a record of nat fields.
There are at least two roles.

**Relations:**
- `offer`:
  - key `[("n", .nat)]`;
  - val `{role : roleTy, terms : rec {f : rec {hi, lo : nat}}}`: the latent contract as data, the deployable
    fragment of an `Iface` (its chooser role, and an acceptance box over θ);
  - retractable;
  - guard `offer_guard`:
    - insert: `termsOk` (lo ≤ hi for every field), else `badTerms`;
    - retract: only on occasion `invoke take` or `invoke withdraw`, else `notConsumer`;
    - upsert: `final`.
- `session`: `activityLog [settlePlan]` with the `activityWaiting` guard, keyed `{agent, notBefore}` from the request.

**Methods:**
- `post {n, role, terms}`: the owner inserts an offer.
- `withdraw {n}`: the owner retracts one.
- **`take {pair, theta}`** (the consuming side, run once per party):
  - reads its own `offer` (1 point) and `peer.offer` (1 point, the peer read);
  - judges `offerJoint own peer theta`;
  - retracts its own offer;
  - inserts its session row (`captured := {pair, theta}`);
  - makes no call.
- **`fuse {deal : bytes, x : digest, y : digest, viaX viaY : opt digest}`** (the MATCHER, [Fuse]): returns
  `[invoke x take deal viaX, invoke y take deal viaY]`.
  - It reads no row and judges nothing.
  - Each party judges itself (honesty), and both judges decode THE SAME bytes, hence the same `pair` and θ.
  - An object running `fuse` is a third object of `P`. If it names itself as `x` or `y`, the kernel refuses
    `revisited` (`Derive.lean:217`).
- `retire`: the activity retire.

**Authority** (KERNEL-25 per method, `invoke_authorized`):
- `post` and `withdraw` belong to the owner.
- `take` is for the objects the owner granted `[.invoke takeIx]`. **That grant is the invitation**: an owner invites a
  matcher object, whose package it can read before granting.
- `fuse` is the matcher's owner's, or a grantee's.

### (c) `jointLaw` — the separate judge (KERNEL-45 item 3, fired)

`offerJoint : Term` = `fn offerVal (fn offerVal (fn θ verdict))`. Its verdicts:
- `refused "sameRole"` if the two chooser roles are equal;
- `refused "notCompliant"` unless both boxes hold θ;
- else `ok`.

Its Lean meaning is `jointOk o q θ := o.role ≠ q.role ∧ inBox o.terms θ ∧ inBox q.terms θ`.

It is ONE term, evaluated by BOTH `take` runs in one Turn, on the same two pinned rows and the same θ. This is the
default fork, M (§3).

The 85 / 86 / 59 / 51 / 21 law theorems are untouched by construction: `Program.judge` and `judgeContextual` are not
edited.

### (d) `Std.pending` — NOT the mechanism the fuse needs

LANG-48's slot is `open {closes, filler} → filled {by, value}`: a value FILLED LATER by a named filler, absorbing
(READ `decisions/lang.md:1609–1648`). The fuse fills nothing later:
- the binding happens in one Turn;
- the absorbing step is the row's retract;
- the later step (settlement) is the session activity's own resume.

`Std.pending`, `pending_fill_binds`, and the CappedTally / escrow instances stay with LANG-48 (still PROPOSED, design
only; cv 01a155c8-2d35 stays open with its own trigger). Building it here would be a generator with no reader in this
card.

### (e) The theorems, as statements (`P := offerPackage θs roles`, `F := Lang.program bytesOf digestOf`)

**Common premises, on NEW theorems only:**
- `hp : readPackage look pkg = .ok P'`, with `P'` the generated package (as `activity_program_safe` takes it,
  `StdActivityMonitor.lean:381–391`);
- the generator succeeded;
- a fuel premise `takeFuel ≤ budget`, measured at build. A run is total only above it, so the premise sits on the new
  theorems.

**The theorems:**

1. **`offerJoint_meaning`** (`Lang/Proofs/StdOffer.lean`).
   - Statement: `BigStep lib [] (app3 offerJoint o q θ) (.ok v) → (v = okV ↔ jointOk o q θ)`. On refusal the text is
     `sameRole` when the roles are equal, else `notCompliant`.
   - Object: the generated term.
   - Mutation: drop the peer's `inBox`. It is false at F2's rows (`[5,10]` against `[11,12]`, θ = 11).
2. **`take_iff_compliant`**, the HONESTY of each party (Bartoletti: it abides "even in presence of dishonest
   adversaries").
   - Statement: `F.run look rv pkg st takeIx args r budget = .ok (s, calls, rows, used)` ↔ `jointOk o q θ`. Here
     `o` and `q` are the values of the one pinned point under `(self, offer)` and under `(peerOf self pair, offer)`,
     and the peer cell is pinned with package `pkg`.
   - When it holds: `calls = []` and
     `rows = [(⟨self, offerIx, keyBytes o.n⟩, .retract), (sessionSlot r, .insert …{pair, θ})]`.
   - When it fails, the run refuses with `.program "take: refused sameRole|notCompliant"`.
   - It holds whatever the matcher is: the matcher's code is not a premise.
   - Object: the deployed `Program.run`, at `activity_program_safe`'s grain.
   - Mutation: `take` without the judge.
3. **`fuse_calls`**.
   - Statement: `F.run … fuseIx ⟨deal, x, y, viaX, viaY⟩ … = .ok (s, calls, rows, used)` ↔
     `calls = [.invoke x takeIx deal b viaX, .invoke y takeIx deal b viaY] ∧ rows = []`. The SAME `deal` goes to both.
   - Mutation: the generator's `fuse` drops the second call.
4. **`fuse_atomic`** (`Lang/Proofs/StdOfferFuse.lean`).
   - Statement: from `hprog : X.program = F`, `receive X w c = .ok t`, `c.unsigned.body = .invoke z fuseIx args b via`
     with `z` of package `P` and `args` decoding to `⟨deal, x, y, …⟩`, conclude `∃ n m`, with
     `(offerSlot x n, .retract) ∈ (t.rows.map (·.act))` and `(offerSlot y m, .retract) ∈ …` (`RowTouch.act`,
     `rowTouchesOf`).
   - A refused call yields no Turn, by `judge`'s definition: that is the "neither" branch.
   - Proof route: `Dispatched` / `dispatched_ok` / `invoke_ok` (`Kernel/Proofs/InvokeTree.lean:148`), used from a
     Lang proof file. Kernel edits: none.
   - Mutation: P4 (§5). It is false at F1.
5. **`jointLaw_sound`**.
   - Statement: same premises → `jointOk (rowVal w x n) (rowVal w y m) θ`, where θ is `deal`'s θ. The two session rows
     inserted in `t` carry the same `captured = {pair, θ}`.
   - One judge, two objects, one Turn, one θ.
   - Mutation: `offerJoint := okT`. It is false at F2's pair.
6. **`fuse_refused_disjoint`** (this REPLACES `separate_witnesses_over_substitutions`).
   - Over the two REAL journey rows `oA` (buyer `[5,10]`) and `oB` (seller `[11,12]`):
     `(∃ θ, inBox oA θ) ∧ (∃ θ, inBox oB θ) ∧ ∀ θ pair, F.run … takeIx ⟨pair, θ⟩ … = .error (.program "take: refused notCompliant")`.
   - Each offer is satisfiable alone; together they are refused at every θ.
   - Mutation: `offerJoint := okT`.
7. **`invitation_once`**.
   - Statement: `receive X w c = .ok t ∧ World.admit X.env w t = .ok w'` (a fuse of `x`, `y`) →
     `rowAt X.env w'.rows (offerSlot x n) = none ∧ rowAt X.env w'.rows (offerSlot y m) = none`. Every `take` run on
     `w'` with those slots pinned refuses `noOffer` / `noPeerOffer`.
   - Mutation: the generated retract becomes an upsert. Then the row stays, and F5 admits.
   - **Strength, said out loud:** this is once per STANDING ROW, not Zoe's never-re-minted id. The owner may `post`
     again at the same `n`; Zoe refuses `mint` of a spent id (mini `Kernel/Invitation.lean:160`
     `spent_never_minted`). §9 Q3.
8. **Peer-read theorems** (`Lang/Proofs/Rel.lean`):
   - `peerReads_parent`: the peer record is exactly `readsData … (peerOf self pair) ps`. Every point it holds is a pin
     under the PEER, never under `self`. Mutation: read under `self`.
   - `peerReads_package`: a peer whose slot 0 is not `bytesOf pkg` is refused by name. Mutation: drop the check.
   - `peerReads_unpinned`: an unpinned peer cell is `.error (.unpinned peer)`.
   - `peerOf_party`: `peerOf self pair = .ok q → q ≠ self ∨ pair.a = pair.b`. A pair naming self twice is refused
     `samePeer`, so in fact `q ≠ self`.
   - `methodReads_conforms` and `methodReads_digests`: the `readsData_*` pair, lifted.
9. **`offer_safe_forever`**: §7 (L2).

None of these is a disjunct over an unbounded preimage. Each conclusion is an implication or an iff over named runs and
rows.

### (f) Rows (journey §LF, new)

| row | call | expected |
|---|---|---|
| F0 | A creates X (`P`, buyer `[5,10]`) and the matcher Z (`P`); B creates Y (`P`, seller `[8,12]`); A grants Z `[.invoke takeIx]` on X, B grants Z the same on Y (the invitations) | admitted |
| **F1** | A invokes `Z.fuse {deal = enc {pair X Y, θ price=9}, x X, y Y, viaX, viaY}`, pinning Z, X, Y, both grants and both offer rows | **admitted; both offer rows gone; two session rows with equal `captured`** |
| **F2** | the same with Y at seller `[11,12]` | **refused `program "take: refused notCompliant"`; both rows stand** |
| F2r | both buyer | refused `sameRole` |
| F3 | F1 without pinning Y's cell | refused `unpinned` |
| F4 | `pair` names an object of another package | refused `peer: another package` |
| F5 | F1's call again on the post-F1 World | refused `noOffer` (invitation_once's row) |
| F6 | F1 without B's grant | refused `grantRight` (KERNEL-25 control, not a tooth) |
| F7 | `Z.fuse` naming Z as `x` | refused `revisited` (control) |

**B7's tooth** (plan §1): skip the judge in `take`, and F2 admits: RED. The matcher has no judge to skip. That is the
point of the honesty statement: no third party's code is in the compliance premise.

**The escrow instance:** §9 Q2. Default: it moves to PROT-8, whose consumer the plan names as "PROT-6's escrow". An
offer that moves value needs linear value (`Val`).

### (g) What it DELETES (counts measured at build by `gates/decls.py`; the names are READ)

- `Lang/Contextual/Protocol.lean`:
  - `Conds`, `Conds.space`, `firstFit`, `coverAll`, `priceConds` (≈ :369–404);
  - the Negotiation `World` (:655) with `World.view`, `candidates`, `available`, `w0`, `World.revoke`, `World.commit`,
    `frags`, `Tok.at`, `Tok'.current`, `World.viewAt`, `World.store`.
- `Lang/Proofs/Contextual/Protocol.lean`: `separate_witnesses_insufficient`, `witnesses_do_not_compose`,
  `greedy_vs_logical`, `search_state_ne_logical_status` (≈ :686–730).
- `Lang/Proofs/Contextual/Negotiation.lean`: every theorem over `World`:
  - `unrelated_update_keeps_plan`, `unrelated_update_repair_reuses`;
  - `provider_revoked_unavailable`, `revocation_repair`;
  - `current_at`, `representation_change_transports`, `stale_opening_refused`;
  - `competing_commitments`, `replay_refused`;
  - `deadline_expires`;
  - `AdmittedIn`, `separate_witnesses_over_substitutions`.
- Each of them is the kernel's own fact restated over a private model:
  - revocation is KERNEL-25 plus the E1 live column (P8.2);
  - staleness is `stale_refused`;
  - competing commitments are `fuse_atomic` plus `invitation_once`.
- MEASURED: `Negotiation.lean` has no importers (`git grep '^import Lang.Proofs.Contextual.Negotiation'` returns
  nothing).
- STAYS (PROT-5's deletion): `Consistent`, `External`, `Internal`, `internal_once_not_external_once`. Also the template,
  plans and lost-reply family, which do not use `World`. The reader may rule them all gone. They are PROT-5's named
  target, so deleting them here would land PROT-5's deletion without PROT-5's replacement.

### (h) The premise price (INFERRED; MEASURED by `decls` at build)

**Restated, 0 hypotheses gained.** The statements that name `readsData … r.self sg.reads = .ok wd` as the setup's rows
step become `methodReads … = .ok wd`:
- `runSetupWith_spec` / `runSetup_spec` (`Lang/Proofs/Load.lean:398–430`);
- `runMeasured_*` (`Lang/Proofs/Extract.lean:374`);
- the two run-soundness theorems (`Lang/Proofs/Invoke.lean:470`, `Lang/Proofs/LiveInvoke.lean:47`);
- `methodSig_spec` (`Lang/Proofs/Load.lean:334`).

One rows hypothesis is replaced by one rows hypothesis, with no new premise, so these are `RESTATES-MEANING`. The exact
list comes from `decls`.

**One Ledger statement.** The PRIVATE `setup_eq` (`Ledger/Proofs/EscrowWitness.lean:50–58`) has the same hypothesis.
That is a CROSS-LAYER: LEDGER edit, statement-level for a private lemma. **ASK** §8.

**Law theorems: 0.** Under every fork, no law theorem's statement changes. `Program.judge` is untouched.

**Wire: no byte moves.** A method type is a `Ty` already on the wire. `peer` is a record label inside it, and no codec
tag changes. The E1 bump rule (`Package.lean:628–631`) is about a codec tag that turns a refused boundary into a read;
this is the checker accepting a type it refused (`badMethod`), as E1's live column was. READ-E1 §4 attributes E1's bump
to the `.cell` tag alone. So it is `lang:`, not `lang!`. Codec vectors are byte-identical (MEASURED at build).

**Std.activity's layout: unchanged.** `session` is `activityLog`. No Bell re-emit, no re-genesis.

## 2. The roles claim (R-0048, LANG-75.10): NOT earned here, and why

- The fuse names two chooser roles as DATA (`offer.role`), and its judge refuses `sameRole`. That is a deployed theorem
  telling two roles apart (`offerJoint_meaning`'s first conjunct).
- It is not a `HasProt sp r1` / `HasProt sp r2` judgment. The offer row's contract is a decidable box, not an `Iface`
  (whose `post` / `accepts` are `Prop`s).
- Bridging the row to `Iface` would be a Lean model beside the deployed judge with no reader. That is the twin law 1
  forbids (memory: a `def` with no consumer is the best predictor of a twin).
- So LANG-75.10's critique stands: **the `Role` index on `HasProt` bought nothing for PROT-6.** Its last named reader is
  PROT-3's `proj`.
- I recommend ROOT rule now whether PROT-3 will read it. If not, revert the index to the binary rule. It was a rename on
  a wider type: 34 `RESTATES-MEANING` back, 0 hypotheses. §9 Q5.

## 3. The fork: how ONE θ reaches both judges (§0.6), and where the joint judge runs

| | **M (default)**: a matcher forwards one `deal` to both `take`s | **T**: typed nested-call arguments | **K**: a kernel joint hook over the sealed Draft |
|---|---|---|---|
| shape | three objects; Z.fuse returns two invokes carrying the SAME bytes; each `take` decodes, judges, and retracts its own offer | two objects; X.fuse judges and calls `Y.take {pair, θ}` as DATA; the runtime encodes it at the call slot's declared argument type | X.fuse calls `Y.take` with signer-supplied bytes; `Program.joint` sees both session inserts and both retracts and requires one θ and compliance |
| one θ | by construction: identical bytes, one decoder | by construction: the runtime's encoding of X's own θ | by a judged invariant |
| honesty (each side re-judges) | yes, `take_iff_compliant` | yes | yes, plus K |
| atomicity rests on | the matcher's generated `fuse` (P), invited by both owners | X's generated `fuse` (P), invited by Y's owner | the same as T, plus the judge |
| what it changes | Lang only: the peer read, Std.offer | **the call language**. `callSlotOk` accepts `invoke` with `args : A`; `callsOf` takes the slot types and encodes. MEASURED blast radius: `callsOf` in 12 files, among them `Host/Check.lean`, `Hosting/Proofs/Allowance.lean` and `Ledger/Proofs/{EscrowRun,EscrowWitness}.lean` (CROSS-LAYER HOST + HOSTING + LEDGER); `bodyOf` in 6. It closes LANG-23 (iii) for every method. | `Kernel/Receive/Call.lean` (a `Program` field) and `Derive.lean` (`deriveTurn`); 4 Program instances (`Kernel/Sim/Gen.lean:72`, `Kernel/Proofs/Carry.lean:409`, `Kernel/Proofs/Journal.lean:938`, `Kernel/Proofs/Logic/Triple.lean:143`) + `Lang/Program.lean:519` + `Lang/Journey.lean:384,421,431`; proofs unfolding `deriveTurn`/`receiveWith` in 17 files (MEASURED `grep -c`: Carry 29, Receive 9, Rooted 4, …); plus a joint-law DECLARATION on the package wire (`lang!`) |
| reader today | F1/F2 | F1/F2 (and no other: the Relay forwards bytes fine) | F1/F2 |
| KERNEL-45's words | "a separate judge, as LANG-44's row guards are": both run inside `run` | the same | a new kernel judge |

**Default: M.**
- It is [Fuse] as written: the latent contracts are consumed by a rule that is not one of the parties. LITP C.1 already
  allows "a third (or either) object".
- It puts no third party's code in any compliance premise.
- It needs no change to the call language or the kernel.

**T is the better LANGUAGE, but this card is not its reader.**
- T fixes a recorded gap, LANG-23 (iii), for every method.
- If the reader rules T, it is the FIRST item of this card, and its grants are CROSS-LAYER HOST/HOSTING/LEDGER over the
  files above.
- Under M, T stays as LANG-23 (iii)'s open item, with the trigger "the first method that must call another with
  arguments it computed".

**K's trigger:** the first row whose invariant spans objects of two packages, or methods no generator wrote. Under M and
T, nothing reads what K adds.

## 4. Size (INFERRED)

| part | lines |
|---|---|
| `Lang/StdOffer.lean` | ≈ 240 |
| peer read (`Lang/Rel.lean` / `Package.lean` / `Program.lean`) | ≈ 100 |
| `Lang/Proofs/StdOffer.lean` (theorems 1–3 and 8) | ≈ 450 |
| `Lang/Proofs/StdOfferFuse.lean` (theorems 4–7) | ≈ 450 |
| journey §LF | ≈ 170 |
| restated proofs | ≈ 60 |
| deleted | ≈ 550 Lean (counts in (g), at build) |

## 5. Plants (each run on the WHOLE tree, lesson 12; each must red only its own theorem by name)

| plant | reds | must not red |
|---|---|---|
| P1 `offerJoint := okT` | `offerJoint_meaning`, `jointLaw_sound`, `fuse_refused_disjoint`; F2 admits | — |
| P2 `take` without the judge | `take_iff_compliant`; F2 admits (B7's tooth) | `offerJoint_meaning` (the term is unchanged) |
| P3 `fuse` drops the second call | `fuse_calls`, `fuse_atomic`; F1 leaves Y's row | `take_iff_compliant` |
| P4 `fuse` sends Y a different `deal` (a second argument field `dealY`) | `fuse_calls`; `jointLaw_sound`'s equal-`captured` conjunct | `take_iff_compliant` (each side still judges its own θ: the §0.6 failure, measured) |
| P5 retract → upsert in `take` | `invitation_once`; F5 admits | — |
| P6 `peerReads` reads under `self` | `peerReads_parent`; F1 (the peer slot holds the own row; `sameRole`) | — |
| P7 drop the package check | `peerReads_package`; F4 | — |

P1 and P2 differ in site: the judge's term, and the method's use of it. P4 is the measurement that the one-θ property is
the matcher's, not the judges'.

## 6. Gate

`lang:` with `CROSS-LAYER: LEDGER` (the private `setup_eq`, if R-0049 grants it).
- `RESTATES-MEANING` lines from `decls` (§1 h).
- `DELETES` lines (§1 g).
- Journey: every row byte-identical except new §LF (MEASURED by diff).
- Codec vectors byte-identical.
- `gates/check.py`.
- Whole tree green.
- Fast judge if the guard allows it, else full.
- Decision text `### LANG-75.11` (critique + meta-critique naming a bias), and a `KERNEL-45` amendment line in
  `decisions/kernel.md` saying item 3 fired as fork M with K's trigger. That is a docstring-level kernel decision text;
  under the M default it is the only kernel file touched, and I ask for it in §8.

## 7. L2: `offer_safe_forever` (mini `Kernel/Seat.lean:1651` restated by law 11)

[READ mini via the scholar's report]
- `seat_offer_safe_forever : genesis.seats = [] → Reachable genesis world → ∀ seat ∈ world.seats, safeAt world.book seat.account seat.proposal = true`.
- `safeAt` = "every `want` met, or every `give` refunded".
- Invitations are spent like nullifiers (`spend_once`, `spent_never_minted`).

**Restated over audited nano histories:** the honest analogue without value. It covers the offerer's half of Zoe:
- the want met is "consumed only by a compliant fuse";
- the refund is "it stays yours until you withdraw it".

```
theorem offer_safe_forever (hX : X.Lawful) (hprog : X.program = F) (hg : NoOffers w₀)
    (ha : audit X w₀ l = .ok w) :
    -- every World the writer reaches: each standing offer row satisfies termsOk
    (∀ wᵢ ∈ worlds w₀ l, ∀ x n o, offerRow wᵢ x n = some o → termsOk o) ∧
    -- every step: an offer row that disappears was withdrawn by its owner's run, or consumed with
    -- a compliant offer of another object of P that disappears in the same step
    ∀ (wᵢ wᵢ₊₁) ∈ steps w₀ l, ∀ x n o, offerRow wᵢ x n = some o → offerRow wᵢ₊₁ x n = none →
      WithdrawnIn wᵢ x ∨ ∃ y m q θ, y ≠ x ∧ offerRow wᵢ y m = some q ∧ offerRow wᵢ₊₁ y m = none ∧ jointOk o q θ
```

**What L2 needs that is not landed** [READ `Kernel/Proofs/InvokeTree.lean:886`, `object_turn_cases`]: the CELL totality
exists; the ROW totality does not.
- `row_turn_cases`: a row slot under `obj` changed by an admitted Turn ⇒ a dispatched invoke of `obj` whose run
  returned that act.
- It is provable in a Lang proof file over `Dispatched` / `dispatched_ok` / `invoke_ok`, plus `rowTouchesOf` /
  `World.admit`'s row frame. It is the row twin of `object_turn_cases`.
- Under R-0046 (fork B: no `ObjectStep` widening), it does NOT widen `ObjectStep`. It is a new theorem beside it.
- Price: new theorems only. The value half (the `give` refunded as VALUE) is PROT-8's linear `Val` over this same
  statement.
- L2 is its own landing, after L1, with its own plant: the guard's retract arm accepts `withdraw` from a non-owner
  occasion, and the second conjunct reds.

## 8. ASK

1. **GRANT** `Ledger/Proofs/EscrowWitness.lean` (CROSS-LAYER: LEDGER), statement of the private `setup_eq` only
   (`readsData` → `methodReads`, proof unchanged in shape).
2. **GRANT** `decisions/kernel.md` (the KERNEL-45 item-3 amendment line), text only.
3. Under fork T or K instead: §3's file list for that fork. I do not ask for either under the default M.

## 9. Reader questions (defaults first)

- **Q1.** The peer is of the SAME package (default). The alternative is a peer of any package in `imports`, read at that
  package's declared layout: wider, plus a trust question about the imported `RelDecl`.
- **Q2.** The escrow instance moves to PROT-8 (default), because a value-moving offer needs `Val`. The alternative is
  the Ledger escrow as an F row now, with no value in the offer: it would not exercise the fuse.
- **Q3.** `invitation_once` is per standing row (default). The alternative is an insert-only `offer` keyed by a nonce,
  with consumption an upsert to `taken`. That is Zoe's never-re-minted id, but F1's "both rows gone" becomes "both rows
  taken".
- **Q4.** Open offers (`anyone`) are out (default). They need public grants held by objects (`granteeHolds`), a kernel
  WIDENING. CLAUDE.md pause item 2 says ROOT/Ember decides.
- **Q5.** The `Role` index on `HasProt`: ROOT rules whether PROT-3's `proj` will read it. If not, revert (§2).
- **Q6.** Fork M (default) vs T vs K (§3). Under T, the grants are CROSS-LAYER HOST/HOSTING/LEDGER over §3's files.
