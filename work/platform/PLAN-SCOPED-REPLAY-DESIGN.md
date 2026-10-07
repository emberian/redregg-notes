# PLAN-SCOPED-REPLAY — design (Phase A)

Worker P4-PLAN-SCOPED-REPLAY (DEPUTY-PLATFORM, burst 2), 2026-10-06.
Clone: `scratchpad/platform/psr/mini` at GitHub `emberian/minidregg` **4ef4e808**, plus the W06b bundle
fetched as `w06b/lane/W06b-wip` @5cab78d0. I ran no builds and used no box.

Tags: **READ** means I read it in the code at 4ef4e808 (file:line given). **RECORD** means a commit message,
brief or doc says it and I did not re-derive it. **INFERRED** means my reasoning; Phase B must check it at the
source before building on it.

---

## 0. The question, and the answer in one paragraph

What can "verifies against the chained root" soundly mean in Mini today, for a consent client that does not
replay the log?

**Answer.** A thin peer has no trusted root. The chain is a plain hash chain, so verifying that a root
`r_h` extends the client's anchor takes every record in between, which means a whole-log replay (§2.3). A
witness checked against a root the Host chose proves the Host's tree is self-consistent, and nothing more.
A lying Host can always build a consistent fake tree. So the root witness cannot be the soundness mechanism.

What makes the thin path sound is a different property, **WYSIWYG-modulo-R**:

1. The signed turn binds the plan's whole value-read set R.
2. The executor evaluates the turn on a view restricted to R. Any read outside R refuses by name.
3. The executor checks that R still holds at the current state.

With those three, a lying Host can only make the turn refuse. It can never make a different turn commit.
Under that property the Host's root claim is harmless, and it is not verified. Most of the binding already
exists: `Theory.PlanBinding`, the signed `SignedHeader.footprint`, `DataIntent.readGuards`, and the signed
`expectedTargetRoot`. What is missing:

- one read set covering *every* value-relevant read;
- an evaluator that refuses out-of-R reads instead of defaulting them;
- an observe filter on what is served.

---

## 1. Ground truth

### 1.1 The world root and per-cell witnesses (the deputy's ASSUMED claim, checked)

- **READ.** The world root is a sparse Merkle tree of depth 256 (`Theory.AuthMap.Scheme`, `deployed`, cSHAKE
  `DREGG.WORLD-ROOT/v1`). It is keyed by `Key.system | Key.cell c`, at the hashed index `deployedIx`. Each leaf
  is a slot root (`Kernel/WorldRoot.lean:626-670`; `Compiler/NativeHostCodec.lean:63-70`).
- **READ.** A cell's leaf is `ResourceBirthCodec.rootBytes (image.currentBytes c)`. That is a **flat**
  cSHAKE (`DREGG.CELL.LIFECYCLE/v1`) of the cell's whole lifecycle bytes, with no structure inside the cell
  (`Compiler/ResourceBirthCodec.lean:438`, `NativeHostCodec.lean:57-61`).
- **READ.** The system slot is `systemLeaf height logRoot`. The world root therefore commits to the height
  and to the log-chain head (`NativeHostCodec.lean:57-66`).
- **READ.** Per-cell inclusion openings exist in theory:
  - `Scheme.opening`, `Scheme.verify` and `verify_opening` (completeness);
  - `verify_sound` under `PathBinding`, and `forgery_exhibits_collision` (`Theory/AuthMap.lean:304-628`);
  - `NativeHostCodec.cell_opens` instantiated at the deployed root (`:80-122`);
  - a two-level form, `PlanBinding.Opened.twoLevel_sound` (`Theory/PlanBinding.lean:599`).
- **READ.** The *runtime* cache `WorldRootCache.Tree` has `set`, `find` and `digest`, but **no opening
  extraction** (`Kernel/WorldRootCache.lean:48-305`). An opening today costs the spec evaluation. Extracting
  one from the cache is a small new function plus a `Good`-based correctness proof (INFERRED: cheap).
- **READ, and it matters.** No field-level opening exists below the world root. Shared cells (the authority
  cell, the Book, the clock, policy source) can be witnessed only as whole cells. That would disclose every
  subject's entries.

### 1.2 What a plan already binds (signed) — READ

- `SignedHeader` has the fields `{codecVersion=2, footprint, validUntil, keyId, keyEpoch, algorithm, domain,
  message, nullifier}` (`Kernel/CredentialSignedEnvelopeController.lean:102-114`).
- `footprint` is `PlanFootprintCodec.encode` of a `Theory.PlanBinding.Footprint`. It holds exactly 4
  authority addresses: subject key epoch, the key at that epoch, `registered`, and `revoked`
  (`Compiler/CredentialSignatureAdmission.lean:146-171`). It is checked at admission:
  `header.footprint != state.footprint → footprintStale` (`…EnvelopeController.lean:296`).
- `message` is the canonical 17-field `Request`. Admission rebuilds the request and compares bytes
  (`wrongMessage`). The request contains:
  - `preStateRoot`;
  - `effectsDigest` (a hash of the **command bytes**, not of computed post-state:
    `Kernel/ResourceTransaction.lean:466-472`);
  - `policyEpoch`, `policyRevision` and `subjectKeyEpoch`;
  - `height := ambient.height` and `cost` (`Theory/TypedAuthorization.lean:193-210`).
- Every invocation `Target` carries `expectedTargetRoot`, the target's *logical* payload root. It is checked
  in `ResourceTargetAdmission.observe` (`Compiler/ResourceTargetAdmission.lean:42-62`).
- `PlanBinding` is already the right theory, covering the check, its refusal, and both poles:
  - `admit` and `footprintStale`;
  - `no_toctou`: the values checked are the values used;
  - `independent_commute`;
  - `IdToy.stale_opening_refused`, which explains why the signed binding is *values*, not openings or roots
    (`Theory/PlanBinding.lean:1-50, 376-390, 637`).

### 1.3 What execution reads but nobody signs — READ, with INFERRED consequences

- **READ.** Law dependencies of world instances produce `readGuards : List (Nat × Digest)` of
  **physical** roots (`Compiler/WorldKindLawDependencies.lean:27-49`). Those guards are derived by the Host
  *at admission* and are CAS-checked at durable commit (`Kernel/DurableDataIntent.lean:79`,
  `Kernel/GuardedDurableCommit.lean`, `Kernel/PhysicalResourceReadGuard.lean`). They are not in the signed
  bytes.
- **INFERRED; Phase B must confirm first.** If a world-kind method's post-state depends on the kind
  definition cell, then **even the full-peer consent path is not WYSIWYG today**. The sequence: a full peer
  consents at height h, the definition changes, the turn admits at h′ under the new definition, and the
  `effectsDigest` (command bytes) still matches. This is the strongest argument that R must be signed, and
  it holds independently of thin peers.
- **READ.** Post-state bytes depend on the *admission* height. `DeclaredEffectCell.blinding.patch pre.logical
  ambient.height` and `HyperdocumentCell.contentBlinding.patch … ambient.height` both take it
  (`Kernel/ResourceTransaction.lean:678-767`). Effect equality can therefore only be stated on the
  **logical** post-state, modulo blinding (fork F6).
- **READ.** `prepareLoaded`, the planner consent re-runs, takes the whole `Opened`/`Loaded` image
  (`Kernel/NativeHost.lean:139-184`; `prepareFrom … opened.durable (some opened.directory)`). There is no
  narrow read interface. This is the main refactor (§6).

### 1.4 Consent and observation today — READ

- `NativeClientConsent.checkPlan` re-derives `prepareLoaded config basis.opened draft` and compares the bytes
  exactly. Its header says: "This is the full-peer producer… A selective-witness producer must establish the
  same derivation before it can replace this one" (`Kernel/NativeClientConsent.lean:1-15, 78-87`).
- `ClientConsentCore` header: "Thin peers need a separate selective authenticated witness producer"
  (`Host/ClientConsentCore.lean:1-10`). Consent frames 228/229 are the anchor frames (from schema-v2-2).
- `ConsentAnchor` is as the deputy stated it (`Kernel/ConsentAnchor.lean`). Its trust premise is that the
  anchor bytes are the client's custody.
- Observation (`Kernel/NativeObservationController.lean:1-15`) works like this:
  - every selected resource needs its own observe capability, a request signature, and the current policy;
  - "Mutating capabilities do not implicitly grant observation. Blind submissions remain a separate receiver
    API";
  - account views return a sparse balance cut and never the shared Book;
  - pre-signature refusals collapse to `undisclosed`, except `unknownKey` and `staleRoot`.
- **RECORD (from the W06b commit message).** Op 155 returns every cell's committed bytes to anyone who
  reaches the public socket. W06b also deleted `verifyInitial`/`refresh` and allocated consent frames
  228/229, which collides with main.

---

## 2. Trust model

### 2.1 What consent trusts

- its config: `expectedSeed`, domain, semantics and tariffs;
- the pinned credential verifier;
- the planner's code, which is the same Lean as the Host's.

**Not trusted:** any Host-supplied root, height, cell bytes or field values.

### 2.2 The guarantee (WYSIWYG-modulo-R)

If the executor admits a turn whose signatures came from thin consent over witness `w`, then:

- the logical effect it commits equals the effect consent computed and displayed from `w`;
- every cell and field consent read had, at admission, exactly the value `w` showed.

What consent **cannot** know is whether `w` was *current* or *real* when shown. The display must say:
"this commits only if these values hold." That is the honest semantics, and it is all a thin peer can have
without a trusted root.

### 2.3 Question (6) settled: the attack on every alternative

**A1. Trust the Host's `r_h` and witnesses; do not bind R.**
- The Host builds a consistent fake tree in which a kind-definition (or any unbound) cell shows method M.
  Consent displays effect E(M) and signs.
- The real cell holds M′. Admission recomputes under M′, and `effectsDigest` (command bytes) matches, so the
  turn commits E(M′) ≠ E.
- **Broken.** Witnesses against a Host-chosen root are always satisfiable by the Host.

**A2. Sign `r_h` itself (whole-root binding).**
- This is sound, but every unrelated admission moves `r_h` and refuses every pending plan. That is exactly
  the M8 contention `PlanBinding` was built to remove (`IdToy.stale_opening_refused`,
  `whole_root_refuses_B`).
- It also makes `planValidityWindow = 256` meaningless.
- **Rejected.** It is sound but contends globally.

**A3. Require `r_h` on a chain the client admitted.**
- The system slot opens to `(h, logRoot_h)`. Linking `logRoot_h` to `anchor.chain` needs every record in
  between (`chainAfter` is a fold with no skip-proof). That is op 155's whole-log replay again, which is what
  this item replaces.
- A browser client has no anchor at all.
- The only other source of a trusted root is a committee finality certificate (GenericSimplex). Whether a
  certified block binds the world root is **not established** (INFERRED; `GenericSimplexCodec` blocks carry
  opaque `payload` bytes). It would also add an honest-majority premise.
- **Not available.** File it as a future fork, not a v1 dependency.

**A4 (chosen). Bind R, restrict the executor to R, re-check R at admission.**
- A Host lie about any value in R makes R stale, so the turn refuses `footprintStale`.
- A Host that omits a read makes the scoped run refuse `readOutside` at consent.
- A Host that adds or forges extra entries changes nothing: unread entries are inert, and the signed R
  holds only what was read.
- The Host's `r_h` is carried only as *information*, the height the witness claims.

**Residual attacks on A4. None of them change what commits.**
- *Withhold or delay*: a liveness issue.
- *Show a fake state on which the plan refuses*: consent refuses, a liveness issue.
- *Show a fake state F and hold the signature until reality equals F*: it commits only if reality equals F on
  R. That is exactly what was consented to, and `validUntil` bounds the wait.
- *Replay one signed plan twice*: the nullifier refuses the second.

### 2.4 What root witnesses buy, and why v1 omits them (fork F2)

They buy early detection of an *inconsistent* Host, and nothing against a malicious one. A verify step that
cannot go red against the adversary it is named for is not a check (the "documented ≠ detected" doctrine).

Recommendation:
- v1 serves R without openings.
- The basis `(h, r_h)` is displayed as "Host-claimed".
- Openings come back only together with a trusted-root source (finality certificate or same-height anchor).
  Their cost is then small, because the theory is done (§1.1).

---

## 3. What is signed

One **ReadSet** replaces both `SignedHeader.footprint` (4 authority addresses) and `Target.expectedTargetRoot`:

```lean
/-- Everything the plan's effect read, as signed. -/
structure ReadSet where
  /-- Whole cells: physical root (the world leaf), or absence. -/
  cells  : List (CellId × CellRead)          -- CellRead := present (physicalRoot : Digest) | absent
  /-- Field cuts of shared cells (authority, Book, …): `PlanBinding.Footprint` per layout. -/
  fields : List SharedCut                     -- SharedCut := Σ kind, Footprint (layoutOf kind)
  /-- Commutative guards on shared balances (fork F5): an interval, not a value. -/
  guards : List BalanceGuard
```

- The header becomes `SignedHeader` v3 (`envelopeCodecVersion := 3`), with `footprint` replaced by
  `readSet : List UInt8` (ReadSetCodec). Every signing slot of a plan carries the **same** ReadSet bytes.
- `expectedTargetRoot` is **deleted** from `Target` (fork F3). The target's read is the R cell entry, and
  `Request.preStateRoot` is derived from the R-bound bytes. Two commitments to one read are a twin.
- The physical root (lifecycle bytes) binds strictly more than the logical root, because it includes
  live/retired status.

## 4. The executor check

At admission, before any effect is computed:

1. `ReadSet.holds current rs`:
   - each cell's current physical root equals the signed entry (`durable.snapshot.model.roots`, which
     `PhysicalResourceReadGuard.current` already reaches);
   - each shared-cut field equals the signed value (`PlanBinding.Footprint.admit`);
   - each balance guard is satisfied.

   On failure it refuses `footprintStale (address)`, naming the first stale address. This reuses
   `PlanBinding.Refusal`.
2. The effect is evaluated **on `View.scoped (restrict current rs)`**. A read outside `rs` refuses
   `readOutsideSignedFootprint k`. It is never defaulted.
3. **Gate reads** run against the *current* state and can only refuse:
   - nullifier unspent;
   - `height ≤ validUntil`;
   - capability scope and policy evaluation;
   - key standing (already in R's authority cut).

   They never feed the effect (`gate_refuse_only`, §5).
4. The durable commit's `DataIntent.readGuards` **are** `rs.cells`. The Host-derived law-dependency guards are
   deleted, because the signed set supersedes them, and the commit-time CAS covers the
   admission→commit race with the same data.

The full-peer path computes `rs` the same way (recording run on `View.full`). One planner, one read set, two
views.

## 5. Theorems (Lean statements; Phase B proves them, with no `sorry`, axioms or `#guard`)

The evaluator is a **free reader monad**, so "never defaults an outside read" is structural. Nothing can
catch the outside error. A function taking `Nat → Except E Slot` could catch it and default, so the frame
lemma would be false for arbitrary such functions. That is fork F4.

```lean
namespace Minidregg.Theory.ScopedRead

/-- A program that reads keys and returns `α`. No catch: an outside read aborts the whole run. -/
inductive Prog (K : Type) (V : K → Type) (α : Type) where
  | pure (a : α)
  | read (k : K) (next : Option (V k) → Prog K V α)
  | fail (e : Refusal)

/-- A finite view: listed keys with their value (`none` = known absent). -/
structure View (K : Type) (V : K → Type) where
  entries : List (Σ k, Option (V k))

inductive Outcome (K α : Type) | ok (a : α) | refused (e : Refusal) | outside (k : K)

def Prog.runOn  (p : Prog K V α) (w : View K V) : Outcome K α          -- unlisted key ↦ .outside k
def Prog.runFull (p : Prog K V α) (s : ∀ k, Option (V k)) : Outcome K α -- never .outside
def Prog.reads  (p : Prog K V α) (s : ∀ k, Option (V k)) : List K       -- keys the full run read
def restrict (s : ∀ k, Option (V k)) (ks : List K) : View K V
def View.Agrees (w : View K V) (s : ∀ k, Option (V k)) : Prop := ∀ e ∈ w.entries, s e.1 = e.2

/-- **Frame (soundness).** A scoped run that did not go outside is the full run on every state agreeing
with the view. This is the lemma the whole design rests on. -/
theorem frame (p : Prog K V α) (w : View K V) (s : ∀ k, Option (V k))
    (agree : w.Agrees s) (h : p.runOn w ≠ .outside k) : p.runOn w = p.runFull s

/-- **Completeness.** The recorded read set suffices: restricting to it never goes outside. -/
theorem runOn_restrict_reads (p : Prog K V α) (s : ∀ k, Option (V k)) :
    p.runOn (restrict s (p.reads s)) = p.runFull s

/-- **Refusal pole.** An omitted read refuses by name; it is never read as absent. -/
theorem omitted_read_outside (p : Prog K V α) (s) (k) (hk : k ∈ p.reads s) (w : View K V)
    (hw : k ∉ w.entries.map Sigma.fst) (prefixAgrees : …) : ∃ k', p.runOn w = .outside k'

/-- **The defaulting evaluator is wrong** (refuted pole, toy instance, by `decide`): reading an omitted
present key as `none` yields a different result than the full run. Named, not `#guard`ed. -/
theorem defaulting_breaks_frame : ∃ (p : Prog Bool (fun _ => Nat) Nat) s w, w.Agrees s ∧
    p.runOnDefaulting w ≠ p.runFull s
end Minidregg.Theory.ScopedRead
```

Binding of R to witness bytes reuses the AuthMap pattern: a scoped carrier, with an honest pole and a
refuted pole.

```lean
/-- The pair carrier: `rootBytes` separates these two cell images (not global injectivity). -/
def CellBinds (b₁ b₂ : List UInt8) : Prop := rootBytes b₁ = rootBytes b₂ → b₁ = b₂

/-- **Witness binding.** Signed R and a current state that `holds` it give the witness's view, cell by cell,
under the per-pair carrier; without the carrier, a mismatch exhibits an explicit collision. -/
theorem readSet_holds_view (w : ScopedWitness) (current : Image)
    (holds : ReadSet.holds current (ReadSet.ofWitness w))
    (bind : ∀ c ∈ w.cellIds, CellBinds (w.bytes c) (current.currentBytes c)) :
    w.view.Agrees (Image.state current)
theorem readSet_mismatch_exhibits_collision … : rootBytes x = rootBytes y ∧ x ≠ y
-- poles: honest witness meets the carrier at every hash; LengthToy forged witness verifies R and refuses at
-- admission (mirrors `PlanBinding.Opened.LengthToy.forged_verifies_held_refuses`).
```

The deployed statement:

```lean
/-- **What consent saw is what commits.** -/
theorem consent_is_commit {config} (draft : Draft) (w : ScopedWitness) (plan : SigningPlan)
    (consented : NativeScopedConsent.checkPlan config w draft candidate = .ok c)
    (admitted : NativeHost.admit config current (assemble plan sigs) = .ok accepted)
    (bind : ∀ c ∈ w.cellIds, CellBinds (w.bytes c) (current.image.currentBytes c)) :
    accepted.logicalEffect = c.logicalEffect                         -- modulo blinding (F6)

/-- **Gates refuse only.** Changing gate inputs (nullifiers, admission height, capability/policy state)
can turn acceptance into refusal, never into a different effect. -/
theorem gate_refuse_only (rs : ReadSet) (g₁ g₂ : GateState)
    (h₁ : exec rs current g₁ = .ok e₁) (h₂ : exec rs current g₂ = .ok e₂) : e₁ = e₂

/-- **Lying Host refuses.** A witness whose R disagrees with current state refuses `footprintStale`. -/
theorem stale_witness_refused … : ∃ a, admit … = .error (.footprintStale a)
```

Each carrier (`CellBinds`, plus the existing `PathBinding` if openings return) is a **named hypothesis with
an inhabitant** (its honest pole) and a **refuted pole**. There are no identity carriers: the carrier is
about `rootBytes`, the deployed cSHAKE, and never about `fun _ _ v => v`.

## 6. The observe filter, the witness, and the Host producer

**Host procedure** (new `Kernel/ScopedWitness.lean`). Given a signed observation intent (the existing
`NativeObservationController` authentication) and a draft:

1. Run the planner `Prog` on `View.full head` with recording. This gives `reads` and the basis
   `(h, r_h)`.
2. For each whole-cell read `c`, require the requester's **observe** authority on `c` through
   `ResourceObservationAdmission`, the same check as a resource view. Mutating capability does not count.
3. For each shared-cell field read, require that the field lies in the requester's observable projection:
   - their own subject's entries;
   - capability records they hold;
   - their own account balance cut;
   - public coordinates the challenge already publishes (policy epoch/revision, enrollment).
4. On the first read that fails, refuse **`scopedReadUnobservable (address)`**. There is no partial view,
   because consent cannot approve what it cannot see. Before signatures verify, the refusal collapses to
   `undisclosed` (the `preAuthentication` rule).
5. Otherwise serve:

```
ScopedWitness := { basis : Nat × Digest  -- Host-claimed, displayed as such, NOT verified (§2.4)
                 , cells  : List (CellId × (present bytes | absent))
                 , cuts   : List SharedCut          -- values only, requester-observable
                 , guards : List BalanceGuard }     -- e.g. own balance ≥ cost (F5)
```

A blind mutation (write without observe) gets no thin consent. It stays on the separate blind-submission
API, as today.

**Thin consent** (`NativeScopedConsent`, a generalised `NativeClientConsent`):
- decode the witness exactly (canonical bytes or refuse);
- run the same planner on `View.scoped w`, refusing on `outside`;
- rebuild R and the plan, then require the plan bytes to equal the candidate (`checkPlan` as today);
- display the logical effect, R's values, and the Host-claimed basis.

`NativeClientConsent` and the new path become **one** module, parameterised by the view
(`Basis → View.full`, `ScopedWitness → View.scoped`). They are not siblings.

## 7. Op 155 / W06b: **delete (do not land)**

- Op 155 exists to give a remote consent client a whole-log replay. It exposes every cell's bytes on the
  public route (RECORD, W06b message), and gating it on enrolment still leaks everyone's cells to every
  member.
- Under scoped consent, hosted friends and browsers do not need it.
- The full-peer path keeps reading its own Store (`verifyInitial`/`refresh` and the anchor, which W06b
  deleted and main still has).
- A remote auditor that wants the whole history is a *replica*. It belongs on the agreement/replication
  channel, not the consent route.
- The frame 228/229 conflict disappears with it. ServedLog's page codec has no other consumer, so nothing is
  absorbed.
- Keep the bundle as the written record of the replay trust model (its commit message §"What consent
  trusts").

## 8. What re-genesises, what refuses to load

| Change | Re-emit | Refuses |
|---|---|---|
| `SignedHeader` v3 (ReadSet replaces footprint) | envelope codec; Rust signer/client | v2 envelopes → `wrongEnvelopeVersion` |
| `Target.expectedTargetRoot` deleted | command codec version; every constructor (~30 files: Fn ingress, lifecycle, grain…) | old command bytes fail exact decode |
| Executor reads through `Prog`/view; `readGuards := rs.cells` | none (logic) | — |
| Logs hold v2 envelopes | **re-genesis**; `StoreEpoch` bump | old Store → epoch refusal (`ConsentAnchor.storeEpoch_*` pins move with it); old anchors → "genesis log differs" |
| New Host op "scoped witness" + consent frames (fresh numbers; not 155, not 228/229) | `protocol/host-operations.json`, `native/host-operations.rs`, consent frame table | old clients refuse by frame check |
| `PlanFootprintCodec` folded into `ReadSetCodec` | — | — (deleted) |

## 9. Module list (Phase B)

1. `Theory/ScopedRead.lean` (new): `Prog`, `View`, `runOn`/`runFull`/`reads`, `frame`,
   `runOn_restrict_reads`, `omitted_read_outside`, `defaulting_breaks_frame`. It re-uses `PlanBinding` for
   shared-cut footprints and `admit`.
2. `Compiler/ReadSetCodec.lean` (replaces `PlanFootprintCodec.lean`): ReadSet + ScopedWitness codecs, with
   exact decode.
3. `Kernel/StateView.lean`: the `Prog` key space (cells, shared-cut addresses), `View.full (Loaded)`, and
   `View.scoped (ScopedWitness)`.
4. Port `DeclaredResourceController.prepareFrom`, `prepareTuple` and the effect computation into `Prog`.
   **This is the dominant cost.** Start with the invocation path only. Birth, install, and roster drafts get
   thin consent refused by name until they are ported, and they stay full-peer.
5. `Kernel/CredentialSignedEnvelopeController.lean` and `Compiler/CredentialSignatureAdmission.lean`: header
   v3 and `ReadSet.holds`.
6. `Kernel/ScopedWitness.lean`: the Host producer and the observe filter.
7. `Kernel/NativeClientConsent.lean`: generalised over the view, with the scoped entry point.
8. `Host/Main.lean` op, `Host/ClientConsentCore.lean` frames, Rust `client_consent.rs`/`transport.rs`, and
   the protocol registry.
9. `ConsentAnchor` is unchanged in shape; its epoch pins move with the Store epoch.

## 10. Journeys and planted faults (each must turn red, with an artifact)

| # | Journey / planted fault | Expected |
|---|---|---|
| J1 | Hosted friend, invoke on an observable own object, thin consent → sign → admit | commits; the logical effect displayed equals the receipt's post-state |
| J2 | An unrelated turn by another subject between consent and admission | still commits (tolerance pole) |
| P1 | The Host serves a target with altered bytes (consistent fake) | consent builds a different plan → "remote signing plan differs"; or, if the Host's candidate matches its lie, admission refuses `footprintStale c` |
| P2 | The Host omits the kind-definition cell from the witness | consent refuses `readOutside c` |
| P3 | **Mutation: `View.scoped` reads an omitted key as absent** | `frame` no longer builds; a journey with P2 then shows consent displaying a wrong effect that admission refuses |
| P4 | Draft reading a cell the requester cannot observe | Host refuses `scopedReadUnobservable c`; the witness contains no bytes of `c` |
| P5 | A competing turn writes a cell in R | refuses `footprintStale`, naming that cell |
| P6 | **Mutation: the executor reads one cell not in signed R** (or the Host signs R minus one entry) | refuses `readOutsideSignedFootprint` |
| P7 | Kind definition changes between consent and admission (the §1.3 INFERRED gap) | on main: run it first, expecting **commit** (the motivating red); after: refuses |
| P8 | v2 envelope / pre-epoch Store | `wrongEnvelopeVersion` / epoch refusal |
| P9 | Payment into the payer's account between consent and admission | commits (F5 interval guard); with exact binding it would refuse, which shows the fork is load-bearing |

Every mutation (P3, P6) asserts that the mutation happened before reading the verdict.

## 11. Forks (genuine decisions), with recommendations

- **F1. Value reads vs all reads in R.**
  - Option (a): sign every read. This drags the authority cell's capability and policy planes into R and
    re-creates contention.
  - Option (b): sign value reads; gate reads run against current state and are proved refuse-only
    (`gate_refuse_only`).
  - **Recommend (b).** The proof obligation is what makes it safe.
- **F2. Root openings in v1.** **Recommend omitting them** (§2.4). Reinstate only with a trusted-root
  source, filed as a task.
- **F3. Delete `expectedTargetRoot` in favour of R's physical-root cell entry.** **Recommend delete.** It is
  a twin commitment of the same read, at ~30 constructor sites; the cost is a rebuild.
- **F4. How "never default" is enforced.**
  - Option (a): a free `Prog` monad, with the frame lemma proved once.
  - Option (b): a reader function, with the frame lemma per entry point (false in general, because an outside
    error can be caught).
  - Option (c): a runtime differential (full vs scoped) at the Host, which is a test, not a proof.
  - **Recommend (a).** It is the refactor of item 4 in §9 regardless.
- **F5. Shared balances (Book).**
  - Option (a): exact value binding of the payer's balance. Any incoming payment then refuses the plan.
  - Option (b): fees and transfers as **deltas** in `Prog`, with an interval guard `balance ≥ debit`
    (Pred interval atoms over the read set, as in SCHOLAR-LAWS §C14).
  - **Recommend (b).** The Book is the one shared written cell, and (a) is M8 again.
- **F6. Height in effects.** Blinding uses `ambient.height` (READ).
  - Option (a): bind effects to the *signed plan height*, with admission height only as the `validUntil`
    gate.
  - Option (b): state equality on logical post-state, modulo blinding.
  - **Recommend (b)** if blinding is per-commit randomness by design. Otherwise (a). Phase B reads the
    blinding derivation and picks.
- **F7. Op 155.** **Recommend delete** (§7).
- **F8. Browser client.** Thin consent needs the planner in the browser (Lean→wasm/JS), which is unbuilt
  (INFERRED). This design is its precondition, not its delivery. File it separately.

## 12. Follow-ups to file (`cv task`) once the deputy rules

- P7 verification on main: is the full-peer path not WYSIWYG today? If confirmed, that is a defect
  independent of this item.
- A trusted-root source (whether finality certificates bind the world root) for openings (F2).
- `WorldRootCache.Tree.opening` plus `Good`-correctness, only if F2 reverses.
- The browser planner build (F8).
