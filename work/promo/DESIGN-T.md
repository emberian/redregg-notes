# DESIGN-T — typed nested-call arguments: a method composes a call from a value it computed (FABLE-T, 2026-10-23)

Card: cv 01a16679-198f. Base: origin/main `892647d` (hbox main fetched 20:23Z; mirror fast-forwarded).
Every claim is tagged READ (a file at that base), MEASURED (a command run on the tree) or INFERRED.

## 0. The problem, re-read before designing

- [READ `Lang/Package.lean:109–118`] the `invoke` arm of `callArms` is `("args", .bytes)`. [READ `:240–242`] `callSlotOk`
  accepts a slot only when every arm is EXACTLY its `callArms` entry (`Row.find? a.1 callArms = some a.2`). So the
  argument of a nested invoke is `bytes`, in every method's type.
- [READ `Lang/Call.lean:162–164`] `bodyOf` reads `args` with `bytesAt`. [READ `Lang/Term.lean:17–70`] no `Prim` and no
  `Term` constructor produces the wire bytes of a value: `cat` concatenates, `digest` is a literal.
- [READ `Lang/Wire/Data.lean:125–131`] the encoder EXISTS: `encodeData (T : Ty) (d : Data) : Option ByteArray`, with
  `decodeData` beside it and [READ `Lang/Proofs/Data.lean:233`] `decodeData_eq_ok_iff : decodeData T b = .ok d ↔
  encodeData T d = some b`. Its callers today [MEASURED `git grep encodeData`]: the resident reader `argsOf`
  (`Lang/Program.lean:553`), state slots (`:263`), row values (`Lang/Rel.lean:308`), keys (`Lang/Rel.lean:35,41`), Hosting's
  and the journeys' fixtures. The runtime encodes a method's STATE and its ROW VALUES at their declared types on the
  way out, and decodes its ARGUMENT at its declared type on the way in (`:443`). Calls are the one typed thing the
  runtime does not encode. That asymmetry is LANG-23 (iii) [READ `decisions/lang.md:374–375`], open since 10-17.
- [READ `Lang/StdOffer.lean:1–30, 175–184`] the fuse landed as a MATCHER that forwards one `deal : bytes` to two takes
  (LANG-75.11, fork M). [READ `Lang/Journey.lean:285–300`] the Relay forwards `rest : bytes`. Neither composes a call.
- [MEASURED `grep -rho "(calls [^)]*)" world/ …`] the deployed package texts declare `(calls (transfer))` three times
  (`world/escrow/Escrow.ob` and its rendered copies) and `(calls (rec))`/`(calls (record))` otherwise. **No deployed
  package declares an `invoke` slot.** The only invoke slots in the tree are Lean fixtures: the LC Relay family
  (`Lang/Journey.lean:295`), `Kernel/Proofs/InvokeTreeWitness.lean:102`, `Lang/Proofs/CallTeeth.lean:82,132`, and
  `Std.offer`'s matcher (`Lang/StdOffer.lean:172`, reused by `Lang/StdOfferEscrow.lean:131`).

## 1. The shape: the invoke arm is typed; the runtime encodes at the slot's declared type

### 1.1 Types (`Lang/Package.lean`)

```lean
/-- The `invoke` arm at argument type `A`: `args` is a VALUE of `A`; the runtime encodes it with the one data codec
(`Wire.encodeData A`), the same codec the callee's `runSetupWith` decodes its argument with (LANG-77). -/
def invokeArm (A : Ty) : Ty :=
  .record [("args", A), ("budget", .nat), ("method", .nat), ("obj", .digest), ("via", optTy .digest)]
/-- Every call an object may make, its invokes carrying a value of `A`; canonical order. -/
def callArms (A : Ty) : List (Label × Ty) := [account, credit, grant, ("invoke", invokeArm A), transfer]
def callTy (A : Ty) : Ty := .sum (callArms A)
/-- A slot of `kinds` other than `invoke` (an `invoke` in `kinds` is not an arm: the slot is then empty and
`callSlotOk` refuses it at install, `badMethod`). -/
def callOf (kinds : List Label) : Ty
/-- A slot that may invoke, its argument a value of `A`, and may make the other `kinds`. -/
def invokeOf (A : Ty) (kinds : List Label := []) : Ty
/-- The argument type of a slot's invoke arm, if the slot has one. -/
def slotInvokeArg : Ty → Option Ty
```

`callSlotOk` [RESTATED]: a non-empty sum; every arm other than `invoke` exactly its fixed entry (as today); an `invoke`
arm exactly `invokeArm A` for some `A` with `A.isData && Wire.dataTy A` — `isData` is what `methodSig` asks of the
method's OWN argument [READ `Lang/Package.lean:466`], `dataTy = wf && tyWire` is what `encodeData`/`decodeData`
refuse without [READ `Lang/Wire/Data.lean:123`]. `Wire.dataTy` moves from `Lang/Wire/Data.lean` to `Lang/Wire.lean`
(beside `tyWire`; `Package` imports `Lang.Wire`, not `Lang.Wire.Data`) so the install check and the codec read ONE
predicate (law 1). A slot whose invoke arm is at a function type, or at a type the wire cannot carry, is refused at
install by the existing name `badMethod` (law 7; LC6 is the shape of that row).

### 1.2 Data ↔ Body (`Lang/Call.lean`)

- `bodyOf digestOf (A : Option Ty) : Data → Except String (Body D)`: the `invoke` arm takes `("args", a)` and returns
  `.invoke obj method bytes budget via` with `bytes` = `Wire.encodeData A a`; refused by name when the slot has no
  invoke arm (`"invoke: no arm"`) or the value has no bytes at `A` (`"args: no bytes at the slot's type"`). Both are
  arms of a total function that typing makes unreachable (§2.3), as `not a digest` already is past the boundary.
- `callData bytesOf (A : Option Ty) : Body D → Option Data`: the inverse, `("args", d)` with `decodeData A args = .ok d`;
  `none` when the slot has no invoke arm or the bytes are not a value of `A`.
- `callsOf (ks : List Ty) digestOf : Data → Except (Refusal D) (List (Body D))`: walks the slots WITH their declared
  types (`go : List Ty → List (Label × Data) → …`), handing `bodyOf` the slot's `slotInvokeArg`. A row whose length
  differs from `ks` is `program "calls: slots"` (unreachable: the extracted result conforms to `callsTy ks`).
- `callFits` drops the `args.size ≤ bytesMax` clause of its invoke arm: under T the bound on `args` is "decodes at
  `A`", which is `callData`'s own success; a clause nothing reads is a no-op kept for comfort (CLAUDE.md).

### 1.3 The run (`Lang/Program.lean`)

`RunSetup` gains `calls : List Ty` (the resolved method's slot types, `sg.calls`); `runMeasuredWith` calls
`callsOf S.calls digestOf c`. `runSetupWith` is the only constructor [MEASURED `git grep RunSetup`: 30 proof sites
destructure it, none constructs]. The kernel is untouched: `Body.invoke … (args : ByteArray)` [READ
`Kernel/Receive/Call.lean:71`], `invoke`/`invokeRun`/`callStep` [READ `Derive.lean:176–230`], 13 Body kinds, the
codec vectors. The callee still decodes at ITS declared argument type [READ `Program.lean:443`]: a caller whose slot
declares `A` and a callee whose method declares `A'` agree exactly when `decodeData A' (encodeData A v)` reads: by
construction of the type-directed stream, when `A` and `A'` have the same shape (labels are not on the wire [READ
`Wire/Data.lean:5–12`]). A mismatch is refused where argument bytes enter a run — the callee's `runSetupWith`,
`program "arguments: …"`, the SAME refusal a root call with wrong bytes gets. The caller's `A` is a claim its type
states; the callee's check is the one check (law 1: not re-checked in `callsOf`, which cannot see the callee's package
without a second lookup of the pins that the kernel's dispatch performs one step later).

### 1.4 Authoring

- Surface [READ `Lang/Surface.lean:15, 605–609, 655`]: a slot's kind list may hold `(invoke T)` in place of the atom
  `invoke`: `(calls ((invoke TakeArg) transfer) (transfer))`; `T` is read by the one type reader (`ty c …`, so a
  `(type N …)` name works). `methodHead.calls : List (List Label × Option SExp)`; `methodSx` lowers to `invokeOf`/`callOf`.
  The bare atom `invoke` reads as a kind that is not an arm: the slot is empty and install refuses `badMethod`. The
  `(KIND (f e)…)` call item is unchanged: `(invoke (args {n (+ arg.n 1)}) (budget 1000) (method 1) (obj o) (via v))`,
  with `args` now any term of `A`.
- Lean generators: `Std.methodWith`'s slots are terms as before; `someCallT (invokeOf A) (.inj (invokeOf A) "invoke"
  (.record [("args", <a term of A>), …]))`.

### 1.5 What does not change

Call kinds: 13 Body constructors, 5 callable [READ `Call.lean` `callable`]. Kernel codec vectors: 0 bytes (the judge's
`codec-vectors` target is the control). `Sig` gains no field (`Sig.calls : List Ty` already carries each slot's type).
`callsMax = 8`, `reqTy`, `resultTy`, `methodTy`: unchanged.

## 2. The price, as premises on landed theorems (MEASURED at build by `gates/decls.py`; the list below is READ)

### 2.1 Statements that change shape (RESTATES-MEANING: a slot type or an `Option Ty` enters the statement)

`Lang/Proofs/Call.lean`: `bodyOf_callable`, `callsOf_go_callable`, `callsOf_callable`, `callsOf_go_length`,
`callsOf_length`, `bodyOf_callData`, `callData_not_callable`, `callData_isSome`, `callData_bodyOf`, `callData_conforms`
(now `Conforms d k` for the SLOT type `k`, the fact a method needs to return the datum in that slot: `callTy` alone
cannot say it any more), `runMeasuredWith_calls`, `runMeasured_calls`, `runMeasuredWith_extract`.
`Lang/Proofs/CallLive.lean`: `bodyOf_live`, `bodyOf_ok_of_total`, `callsOf_go_live`, `callsOf_go_kinds`, `callsOf_live`.
`Lang/Proofs/Extract.lean`: `runMeasured_means`. `Lang/Proofs/MethodRun.lean`: `runMeasured_inv`.
`Lang/Proofs/Load.lean`: `runSetupWith_spec`, `runSetup_spec` (the record gains `calls`).
`Lang/Proofs/Provenance.lean`: the six past-extraction statements naming `callsOf digestOf c` (`:1171, :1221, :1293,
:1319, :1349, :1405`) — they gain the slot list `S.calls`, NOT a hypothesis: `hks : ∀ k ∈ ks, callSlotOk k = true`
is already their premise through `methodSig_slots` [READ `:38, :88`], and `callSlotOk` now carries `dataTy A`.
`Lang/Proofs/CallTeeth.lean`: the concrete rows (`callsOf_skips_none`, `callsOf_not_digest`, `callsOf_not_option`,
`invokeD_conforms`, `invokeRow_conforms`, …) at `invokeOf A`.
`Lang/Proofs/StdOfferFuse.lean`: `fuse_calls` (the calls carry `encodeData (offerTakeArg theta) deal`).
Proof-only edits (statements unchanged): `Lang/Proofs/Bell.lean:306`, `Lang/Proofs/StdOffer.lean:1188`,
`Lang/Proofs/StdOfferEscrow.lean:235–247`, `Ledger/Proofs/EscrowRun.lean:254–270` (simp sets name `callsOf.go`,
`bodyOf`, `bytesAt`), `Kernel/Proofs/InvokeTreeWitness.lean:102–106` (its slot and call datum). CROSS-LAYER: KERNEL
(one proof fixture), LEDGER (one simp set). Count target: ≤ 45 RESTATES-MEANING, 0 hypotheses gained except §2.2.

### 2.2 The one honest new hypothesis

`callData_isSome` (every callable Body has call data): for `invoke`, "and its `args` decode at the slot's `A`". That IS
T: a method can emit any callable Body whose invoke argument is a value of its slot's type, and no other. Today it
can emit any byte string, which is exactly the power nothing could type.

### 2.3 Why `callsOf` still never refuses a checked run (the refuter the card named, answered)

The refuter: "the encoder cannot be total over `Data` at every declared type, and a partial encoder makes 'a program
composes a call' a lie." Answer, as a lemma this landing proves (`Lang/Proofs/Data.lean`, new):
`encodeData_of_conforms : dataTy T = true → Conforms d T → ∃ b, encodeData T d = some b`. [READ `Data.lean:20–31`]
`Conforms` bounds exactly what `ofData` [READ `Wire/Data.lean:98–121`] requires: `nat n` with `n < natLimit = 2^64`
(`Lang/Bounds.lean:15`) against `n < 2^64`; `bytes` ≤ `bytesMax`; `digest` ≤ `digestBytesMax`; a record's labels pairwise
equal in order (`RowConforms` / `rowOfData`'s `ℓ = k`); an injection's arm the FIRST with its label (`Row.find?` /
`armOfData`). So on a checked run — `extract_conforms` gives `Conforms c (callsTy ks)`, `methodSig_slots` gives
`callSlotOk` of every slot, hence `dataTy A` — the encode arm of `bodyOf` is unreachable, and `callsOf_live` keeps its
conclusion (`DigestRefusal`: the only refusal is bytes `digestOf` refuses) with NO new premise. Had `Conforms` been
looser than `ofData` at any leaf, the design would have needed a run-time refusal reachable from typed code, and the
card's refuter would have fired. It does not.

### 2.4 The homonyms (READ-PROT-6b condition 9, re-read)

[READ `Host/Check.lean:98`] `callsOf : Nat → List (Turn D) → Except Nat (List (Receive.Call D))` decodes a Store's
journal segment into the calls it holds. [READ `Hosting/Proofs/Allowance.lean:63`] a `private def callsOf (m : Label)
(arg st : Data) : Outcome`, a test helper. Neither is `Lang.callsOf`'s fact (data → Bodies). Not twins; not deleted;
untouched. [READ `Lang/Proofs/StdOffer.lean:842–871`] `Std.runMeasured_inv` IS a twin of
`Lang.runMeasured_inv` (`Lang/Proofs/MethodRun.lean:75–104`, same statement, same proof): DELETED, the Std proofs
import `Lang.Proofs.MethodRun`.

### 2.5 E5's receipt argument

[READ `Package.lean:170–175, 399–405`] a receipt rides as the method's OWN argument field `receipt : bytes`, verified
by the runtime against the head object a read's key names. That is an argument on the way IN, signer-supplied; T is the
way OUT. T does not subsume it; it makes forwarding one expressible: a method that received `receipt : bytes` may now
call a peer declaring `{receipt : bytes}` with `{receipt := arg.receipt}` (a `bytes` VALUE, encoded at `bytes`), where
today it could only forward a whole byte string as the callee's entire argument. No E5 statement changes.

## 3. The consumer: the fuse without the matcher — two objects, one call tree

### 3.1 Shape (`Lang/StdOffer.lean`, `Lang/StdOfferEscrow.lean`)

- `fuse {keys, pair, theta, via}` (`offerFuseArg theta := offerTakeArg theta ++ [("via", optTy .digest)]`), run by a
  PARTY as itself: the take's case tree (`offerTakeTree`: `offerUnpinned`, `noOffer`, `peerRowUnpinned`,
  `noPeerOffer`, `offerNotNamed`, `sameRole`, `notCompliant`), and on `ok` its own retract, its own session insert, and
  ONE call: `invoke <peer> take {keys := arg.keys, pair := arg.pair, theta := arg.theta} budget arg.via`, the slot
  `invokeOf (offerTakeArg theta)`, the peer term `ite (deq req.self pair.a) pair.b pair.a` (the runtime's `peerOf`
  already refused a `self` outside the pair). Its type says it: `fuse` invokes `take` with an `offerTakeArg`.
- `take {keys, pair, theta}`: unchanged (judge, own retract, own session, no call).
- The matcher object, `offerFuseBody`'s two forwarded invokes, `x`/`y`/`viaX`/`viaY`: DELETED. Nothing needs a third
  party: Bartoletti's [Fuse] "a third or either object" — this is "either".
- Authority: Y's owner invites X by granting X `[.invoke take]` on Y (`via`); X's owner, or whoever X's owner grants
  `[.invoke fuse]`, signs the fuse. `rowParent` (law 4) still makes each retract its own object's; `revisited` still
  forbids X calling X.
- The escrow instance: `fuse` = the escrow take's leg payment + the invoke, slots `[escrowCallTy, invokeOf
  (offerTakeArg theta)]`; `take` as today.

### 3.2 What the theorems become

- `fuse_calls` → `fuse_run_sound` (`Lang.program`'s run of `fuse` at `self = X`): the decoded `{keys, pair, theta,
  via}`, the two pinned rows read, `NamedKey`, `JointOk`, rows = own retract + own session insert, and
  `calls = [.invoke peer offerTakeIx bytes budget via']` with `encodeData (offerTakeArg theta) {keys, pair, theta} =
  some bytes` and `peerOf … X = .ok peer`.
- `fuse_atomic`: a root call invoking `x'.fuse` (x' of P; its args decoding to the deal whose `pair` names x' and y',
  y' of P) that `receive` turns into `t`: `t.rows` holds x''s retract at the key the deal names for x' AND y''s at the
  key it names for y'. The premise set loses `z`, `viaX`, `viaY`, `hz`.
- `jointLaw_sound`: the SAME θ at both judges is no longer the matcher's guarantee: y''s take decoded the bytes x''s
  run encoded, so by `decodeData_eq_ok_iff` its datum IS `{keys, pair, theta}` of x''s own argument. The sentence
  "a package other than this one, granted take, could hand the two takes different bytes" leaves the docstrings: no
  third party holds the bytes. What remains outside the theorem: the owner's root `take` (one session row; READ-PROT-6b
  condition 2). I checked whether `take` could refuse a root call: [READ `Kernel/Receive/Authority.lean:49–61`,
  `Derive.lean:188`] a nested call's `Req.principal` is the grant's ROOT ISSUER (the owner), the same as the owner's
  own root call, and `reqTy` carries no actor. It cannot. K's trigger stays as LANG-75.11 recorded it.
- `invitation_once`: restated over the two-object premises; same conclusion.
- `take_iff_compliant`, `take_run_sound`, the six named take refusals: UNCHANGED (the take did not move).
- `escrow_take_run_sound` etc.: unchanged; the escrow fuse gets `escrow_fuse_run_sound` (one leg transfer, one invoke).

### 3.3 Journey (§LF, §LE)

LF0 creates X (A) and Y (B), no Z; B grants X `[invoke take]` on Y (the invitation); A invokes `X.fuse` pinning X, Y,
the grant and both offer rows. LF1 admitted: both offers gone, two session rows, equal captured. LF2/LF2r/LF8 refused by
the take's names, now read at `fuse` (X judges first) — the row text names which method refused. LF3/LF3r/LF4/LF5
unchanged in meaning. LF6a–c follow `via`. LF7 (`revisited`) is replaced: with two objects there is no matcher to name
as a party; a `pair {a X, b X}` is `peer: samePeer` (a new control row). LE likewise.

## 4. Plants (whole tree; each must red by name)

- PT1 `callsOf.go` hands `bodyOf` `none` for every slot (the slot "has no invoke arm"): `bodyOf_live`/`callsOf_live`
  red; journey LC3 refused `program calls: c0 invoke: no arm`, LF1 refused the same at `fuse`.
- PT2 `bodyOf` encodes `args` at `unit` instead of `A`: `callsOf_live`'s encode arm fires (red); LC3 and LF1 refused at
  the CALLEE, `program arguments: …` — the row that shows the callee is the one check.
- PT3 the fuse sends `keys` where it sends `theta` (a different datum to the peer): `fuse_run_sound`'s calls conjunct
  red; `jointLaw_sound`'s one-θ conjunct red; LF1 refused `arguments:` (the record no longer decodes) — the shape
  difference from fork M's P4: a wrong VALUE is now a type error at the callee, not a second θ judged compliant.
- PT4 the fuse drops its call: `fuse_run_sound` and `fuse_atomic` red; LF1 admitted with Y's offer standing (red row).
- Rows (not plants): LC7 a method declaring `(invoke (fn nat nat))` is refused `badMethod` at install; LC8 a Relay
  whose next object takes `{n : nat, note : bytes}` is refused at the callee `program arguments: …` (the named
  refusal when the value does not fit the callee's type).

## 5. The flag day (`lang!`)

- What changed shape: the call-slot language. An `invoke` arm's `args` is a value of the slot's declared type; the
  runtime encodes it. Old shape — `callOf ["invoke"]` in Lean (now an EMPTY slot: install refuses `badMethod`), the
  bare kind `invoke` in a surface `(calls …)` (the same) — refuses to load. No silent reinterpretation: `args : bytes`
  as a declared type now means "a `bytes` VALUE, length-prefixed", and no deployed package declares one (§0).
- What re-emits: NOTHING deployed. [MEASURED] `world/` declares only `(calls (transfer))`; `callOf ["transfer"]`'s
  type is byte-identical, so `world/escrow/Escrow`'s id does not move (the judge's generated-file and rows gates are
  the control). Fixtures re-id: `Std.offer`, `Std.offerEscrow`, the LC Relay family, the Kernel witness relay.
- What re-geneses: no Store (no deployed World holds an invoke-slot package).
- Decision text: LANG-77 (critique + meta-critique), LANG-23 (iii) marked closed by LANG-77, LANG-75.11's "T is its own
  card" sentence pointed here.

## 6. Landing plan (R-0069: land when build + plants are green; `lang!` = full judge)

- L1 `lang!`: §1 + §2 + the Relay journey rewritten to COMPOSE (`arm {via}` stores the hop's grant in state; `go {n}`
  invokes `next.go {n := n + 1}`; o5 ends with `n = 4`: the composed argument arrived) + the matcher's `deal` typed
  (`offerFuseArg := {deal : offerTakeArg theta, …}`, the one-line change that keeps every fuse theorem's shape) +
  LC7/LC8 + PT1/PT2 + LANG-77.
- L2 `lang:`: §3 + PT3/PT4 + the LF/LE rows + the theorems of §3.2 + the matcher deleted.
  Two commits so each GATES-20t map is readable and each plant reds its own module; both in this session.

## 7. Critique (what would make this wrong)

- A caller's slot type and a callee's argument type agree STRUCTURALLY, not by name: `{x : nat}` calls `{n : nat}`.
  That is the wire's existing property (labels off the wire), now visible from the caller's side. A nominal check
  would need the callee's package at the caller's install, which does not exist.
- The type agreement is checked at the callee, one step after the caller's run, inside the same tree: a mistyped call
  costs the whole tree. Checking in `callsOf` would be a second check of one fact with the same outcome.
- `callSlotOk` re-checks `dataTy A` though the iface's `wf`/`tyWire` imply it (as `methodSig` re-checks `isData`):
  a local premise the theorems can use alone, at the price of a redundant decide at install.
- The Relay journey no longer nests pre-encoded arguments, so LC3/LC4 no longer exercise a method FORWARDING opaque
  bytes; nothing deployed forwards opaque bytes, and a `bytes`-typed slot still can.
- `callData_isSome` gains a hypothesis (§2.2). It is the truth of the new language, not a lost theorem.

## 8. Meta-critique (the bias)

The first draft of §3 had `take` refuse a root call by `req.principal ≠ peer` and claimed a stronger theorem (a
session row implies a fuse). The bias: reading LANG-21's "a callee's principal is the calling object" as the kernel's
behaviour, when `Authority.principalOf` walks the grant to its ROOT ISSUER — the owner — so a nested call and the
owner's root call are indistinguishable in `Req`. READ-PROT-6b condition 2 had said so; I re-derived it from the
code before writing the statement. The second bias, watched for: pricing the design by `git grep callsOf` (12 files)
— two of those are homonyms (§2.4); the real reach is the 11 Lang proof modules plus one Kernel fixture and one
Ledger simp set, measured by the decls export, not by the name.
