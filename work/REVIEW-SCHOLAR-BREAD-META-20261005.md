# REVIEW-SCHOLAR-BREAD-META — the landed theorems, read for Bread's false-friend patterns (2026-10-05)

Reviewer: SCHOLAR-BREAD-META (domain: Bread's metatheory and its honesty lessons; my report
`work/SCHOLAR-BREAD-METATHEORY-20261004.md`, "META" below). I read the code at GitHub main `36fca3ac`
(via `gh api …/contents?ref=36fca3ac`, no local clone: the Mac's data volume is at 99%), the design
`designs/MINI-PROGRAM-MODEL-20261004.md` §3 (T1–T9), and the root's decisions and 10-05 rulings. Tags:
READ = I read it at the cited line; INFERRED = my conclusion.

The test applied to each theorem is META's catalogue: is the content in the statement, or is it a field
projection, an `rfl`, a definition read back, a premise nothing honest inhabits, or a statement about a model
the kernel does not run?

## 0. Verdict

Most of what landed last night is honest and several pieces are better than anything Bread had: the fast
machine's `@[csimp]` equalities are real kernel-checked equalities with exact axiom pins; the activity
kernel's witness structures (`Birth`, `Delivery`, `Accepted` with `private mk ::`) can only be built by the
executable admission functions, which closes Bread's commonest hole (theorems about a structure nothing
constructs); consume-once is proved over the kernel's own `DurableDataIntent.execute`. Four things are
not what their names or the design say: `second_delivery_refused` has a premise only a digest collision
inhabits; the resume contract proves the inductive STEP of "every stored checkpoint is typed" but not the
invariant; `unitName_separates_stores` separates 64-bit tags, not Stores; and the trivial-structure
allowlist's 17 baseline "reasons" are a single pardon template, two of whose entries are the exact
Bread ⊥-class shape. One fix is committed on my lane (§6).

## 1. Theorem by theorem

| theorem (file) | class | why |
|---|---|---|
| `stepRaw_eq_fast`, `step_eq_fast`, `runBounded_eq_fast`, `forceWith_eq_fast` (`Theory/ObjectiveBendDemandMachineFast.lean`, `ObjectiveBendDemandData.lean:54`) | **REAL** | Equalities between the specification and the implementation, proved by case analysis and induction (`runFrom_eq_runBounded`, `forceWithFast_unique`); `forceWith`'s instance discharges `forceWithFast_unique`'s defining equations by `rfl`, which is correct because they are `forceWith`'s own equations. Exact axiom sets are pinned with `#guard_msgs` (`[propext, Quot.sound]`, no `Classical.choice`, no compiler trust). `allocateFieldsFast_eq := rfl` is right: the difference is evaluation order, visible only to the compiler. Nothing here is a false friend. The performance claim is evidence, not a theorem, and is labelled so. |
| `resume_consumes_once`, `slot_decided_once`, `spent_claim_never_accepted` (`Kernel/ObjectiveActivity.lean:961-1030`) | **REAL** | Through `install_consumes` and `consumed_nullifier_refused` of the durable commit protocol, under every schedule. Scope stated exactly: the quantifier is over later intents that CARRY the await claim. The docstring's "a forged intent claiming it" is covered; an intent that overwrites the record cell WITHOUT claiming is not, and is excluded only by object authority (ruled 10-05, not landed). |
| `second_delivery_refused` (:1012) | **HYP (collision-only premise)** | Premise `sameAwait : second.await.id = first.await.id` with `second : Delivery config next …`. After the first installs, the cell holds `first.next` at generation + 1, so any second delivery of that cell ends `awaitId cell (g+1) …`; the premise holds only if `awaitId` (a tagged digest) collides across generations. Its own docstring says the record moved — the theorem never states that. Proved now on my lane: `delivery_advances_generation` and `second_same_await_is_collision` (§6). The design (T1) calls it "the corollary for deliveries"; the other Bread review (REVIEW-SCHOLAR-BREAD §1.1) praised it. Both should cite the new pair instead. |
| `birth_checkpoint_typed`, `delivery_checkpoint_typed` (`Kernel/ObjectiveResumeContract.lean:100,123`) | **REAL step, invariant missing** | Genuine: they compose `typed_stepRaw_preserved`, `typed_resume_preserved`, `checked_initial_state` and `state_roundTrip`. But `delivery_checkpoint_typed` takes `prior : ∃ types, Nonempty (StateTyping … delivery.state …)` — the induction hypothesis. No theorem closes the induction ("in every reachable snapshot, every record cell's checkpoint is typed"), and none can until only `birth`/`deliver` may write a record cell: `DurableDataIntent.execute` checks pre-roots, guards and nullifiers, not which cells an intent may write, so the restriction must come from admission (INFERRED from `execute` and the receiver shape; the object-authority ruling of 10-05 is that restriction, not yet landed). The module header ("no foreign checkpoint is ever admitted"), resolution B3 and design T1 ("every stored checkpoint decodes to a well-typed state") state the invariant. This is META §3.1's `stepComplete_preserves` shape: a preservation step presented as the invariant. |
| `stale_reads_conflict`, `current_reads_exact` (:1042,1056) | **DEF** | The `outcomeExact` field plus `revalidate`'s definition. Honest; superseded by RESUME-WITH-VIEW. |
| `resume_binds_checkpoint` (:1071) | **DEF (projection bundle)** | A conjunction of `Delivery` fields. Acceptable only because `Delivery` is `private mk` and built solely by `deliver`; name it as such. |
| `resume_deterministic` (:1087) | **REAL-small** | Field functionality chained; true because admission is a function. |
| `refund_measurement_free` (:1123) | **REAL second conjunct, first conjunct about a call that never happens** | The first conjunct evaluates `movements … 0 first`, with `pair := 0`; the delivery calls `movements` with `pairOf escrow yielded`. True by `rfl` and unrelated to the delivery's actual postings. State it on `delivery.accountsExact`'s list. |
| `admit_signature_first` (`Theory/Receiving.lean`) | **DEF, but the right DEF** | `simp [admit, resolved, refused]`. Its content is parametricity: it holds for every `prepare`, so preparation cannot be consulted. A good regression pin on the order of checks. Caveat: a family that declares `claims := []` is "signature-first" vacuously; nothing obliges a family to claim the signer's key (the rotation family does, and proves `admitted_possession`). |
| `replay_after_install` (`Theory/Receiving.lean`) | **REAL via the journal law** | Its content is `J.lookup_install`, a STRUCTURE FIELD; the deployed instance proves it over the executor's own install (`Kernel/Receiving.lean:76`, `simp` through `lookupRecorded`), and `replay_after_execute` composes it with `execute_accepted_install`. So the chain reaches the kernel. |
| `receive_committed`, `receive_committed_verified` | **DEF at `Id`** | Reads `receive`'s definition back. The live pipeline runs at `IO`; the theorem transfers only by the parametricity of a monad-generic definition, which is an argument, not a theorem. Fine as a pin; not evidence about the IO run. The fixture inhabitants (`committed_reachable`, `unauthenticated_reachable`) are exactly the premise-inhabitation discipline META asked for. |
| `LayoutCodec`, `layoutCodec_binds`, `layoutCodec_not_foreign` (`Assurance/ObjectiveZkLiteralInstance.lean:228-280`) | **REAL, but trivially inhabited** | `bound` makes any answer agree with the layout decoder, so `layoutCodec_binds` is that field composed with the prepared program's translation-validated `initialExact`; `layoutCodec_not_foreign` is genuine for every codec. But a decoder that answers nowhere is a `LayoutCodec` (`acceptedStep` and `bound` vacuous), so "a LayoutCodec exists" certifies nothing; the content is which rows decode. `regionCodec` answers on the orbits (fuel 4) of five programs, certified by `native_decide` (`reach_certified`). docs/ZK.md names the universal codec as open — honest. Missing: a coverage obligation (below). |
| `unitName_separates_stores` (`Kernel/ApplicationLifecycleResidentProfile.lean`) | **REAL, misnamed: the content is the premise** | Premise `storeTag store ≠ storeTag other`; `storeTag` keeps `store.value % 2^64` (:29-31). The theorem is append-cancellation. "Distinct Stores get distinct units" needs `storeTag` injective on Stores, false in general at 64 bits; the honest bound is a 2^64 second-preimage / 2^32 birthday floor, with the broker's owner check as the fail-closed backstop. META §3 "width-blind injectivity". Rename to `unitName_separates_tags`; state the floor. |
| `#assert_axioms` (`Theory/AxiomPin.lean`), the statement snapshot | **REAL tooling** | Checks only axioms, and says so. The 1,721-row statement snapshot is the best instrument here: it is the statement gate Bread lacked ("the arithmetic was checked, the statements were not"). |
| trivial-structure probe + `scripts/trivial-structure-allow.txt` | **REAL instrument, allowlist is a pardon list** | See §2. |

## 2. The allowlist: classify by polarity, or it is Bread's baseline again

The probe is exactly the instrument META recommended, and its self-tests (planted `PackedRefinement`
must read TRIVIAL; the Polishchuk–Spielman plant must read VACUOUS) are the right teeth. But 17 of the 18
entries carry the same text, "degenerate inhabitant; review whether the premise carries content". Bread's
floor ratchet grandfathered its two apexes the same way and they stayed vacuous (META §3.2). A trivial
inhabitant means three different things, and the entry must say which:
- **DATA**: the structure is a value and its trivial inhabitant is a real value (`Kernel.Receiving.Payload`,
  whose entry already says so; `Theory.TypedAuthorization.Parentage` — `⟨fun _ => none, ∅, _⟩` is the real
  empty parent map, READ `:245-255`). Harmless.
- **PARAMETER**: consumers quantify over it, and the trivial instance is a legitimate instance
  (`Selvage.Oracle`, `Selvage.ProofSystem`). Harmless for the consumers' truth; the entry must name the
  deployed instance and the theorem instantiated at it.
- **PREMISE**: the trivial inhabitant makes consumers vacuous. `Kernel.ReplicatedSettlementFinality.QuorumSystem`
  (21 consumers; `isQuorum := fun _ => False` satisfies `intersects`, READ `:113-117`) is Bread's ⊥-class
  loophole verbatim (`FloorPole` accepted the ⊥ model, META §3.4); `Kernel.OutboxDelivery.AckVerifier`
  (13 consumers, accepts everything) and `Kernel.ProviderExecutionLease.CompletionBoundary` (16, predicates
  `False`) are the same question. Each needs either a non-triviality field (for `QuorumSystem`:
  `∃ q, isQuorum q`, or better the threshold form `isQuorum q ↔ 2f+1 ≤ q.card` at the deployed `n,f`) or
  a named deployed instance plus the theorems instantiated at it.

Proposed allowlist format: `<structure> DATA|PARAMETER <deployed instance>|PREMISE <non-triviality field or
deployed instance> <consumers>`, and the gate turns RED on any PREMISE entry without one.

## 3. Design disputes, with replacement text

**§3 T1, replace "`second_delivery_refused` is its corollary for deliveries" with:**
> `delivery_advances_generation`: a delivery admitted from the snapshot an installed delivery produced,
> on the same record cell, decoded exactly the record the first wrote, one generation on
> (`Delivery.installed_record`). Together with `resume_consumes_once` this is consume-once for deliveries.
> `second_delivery_refused` assumes two deliveries end one await id; `second_same_await_is_collision`
> shows that premise is an `awaitId` collision across generations, so it is retained only as a
> collision-conditional statement.

**§3 T1, replace "every stored checkpoint decodes to a well-typed state (resolution B3)" with:**
> `birth_checkpoint_typed` and `delivery_checkpoint_typed` prove the step: a birth stores a typed
> checkpoint, and a delivery that decoded a typed checkpoint stores one. *Still to state:*
> `stored_checkpoints_typed`: in every snapshot reachable from genesis by accepted intents, every record
> cell decodes to a record whose checkpoint is typed at its program's checked type. It needs (i) the
> object-authority ruling (only `birth`/`deliver` may write a record cell; any other intent posting to one
> is refused by name) and (ii) induction over accepted intents. Until it lands, B3's "no foreign
> checkpoint is ever admitted" is a design commitment, not a theorem.

**§3 (preamble), add after "none may be stated over a model the kernel does not run":**
> A premise inhabited only by a hash or digest collision counts as uninhabited. A structure-valued premise
> whose trivial inhabitant (predicates constantly true or false) satisfies it must carry a non-triviality
> field or be instantiated at a named deployed instance; the trivial-structure allowlist records which.

**ZK (docs/ZK.md and the design's ZK paragraph), add:**
> A `LayoutCodec` whose decoder answers nowhere satisfies the structure, so the refinement claim is
> `LayoutCodec.Covers P`: the codec decodes every `Prepared` program in `P` at its initial bits and every
> row reachable from them. The landed `regionCodec` covers five programs to four ticks by compiled
> evaluation; the universal codec is `Covers (all prepared programs)` and is open.

**Upgrade (T7 teeth), keep and sharpen** the line on `migrate_conforms`: also require that a REFUSED
migration leaves the old schema in force (`upgrade_refusal_inert` (f) already), never the old value under
the new schema — Bread's fallback did the latter (META §7.1).

## 4. What the design and code got right against Bread's record

- `private mk ::` witness structures built only by the executable function (`Birth`, `Delivery`,
  `Resolution`, `Receiver.Accepted`): a theorem about a `Delivery` is a theorem about an admitted delivery.
  Bread's `ProtocolCell`, `JointBinding`, `CellContract` were constructible by anything (META §1, §4, §8.2).
- Premise inhabitants in-tree (`Theory/Receiving.lean` `Fixture`), and the refuters kept beside the
  corrected statement (`externalTables_not_refinement`, `constantCodec_initial_silent`,
  `packedRefinement_always_inhabited`).
- Exact axiom sets and a statement snapshot: the instruments point at statements, not only arithmetic.
- The fast machine leaves every theorem about the specification and moves only compiled code.

## 5. The OPEN questions, where my domain bears

1. **Synchronous cross-principal `call`: yes**, but only with T2 stated over the real call-stack executor
   and a `private mk` frame witness. Bread's evidence: every "atomicity" theorem it had was about a model
   (`and_congr`, one shared state; META §8.2).
2. **Laws: unify the syntax now; keep `Pred` the judge.** Bread had about a dozen predicate algebras that
   never met (META §2.1) and a decision procedure over one of them while the node evaluated another
   (`Pred` over ℤ vs `DConstraint` over ℕ mod 2^256, META §2.3). One surface compiled to one `Pred` avoids
   that by construction.
3. **REPLAY: dropped is right.** Bread's replay and rehydration theorems were definitional
   (`replayedDeterministic_iff_confined`, META §9.3) and the reversibility round trip was never proved.
4. **Build order:** OBJECT-RECORD (object authority) first — it is the premise that turns
   `delivery_checkpoint_typed` into the invariant and closes the "intent without the claim" gap in
   consume-once.

## 6. Commit and next quest

**`901422b3`** on persvati lane `bread-meta` (`/home/ember/workbox/claude-lanes/bread-meta/src`, branch
`main` of the lane, on GitHub main `3b709c87`, i.e. after RESUME-WITH-VIEW), not pushed; queued in
MERGE-QUEUE.md. Six theorems added to `Kernel/ObjectiveResumeContract.lean` (`bodyOf_image`,
`nextRecord_generation`, `Delivery.next_generation`, `Delivery.installed_record`,
`delivery_advances_generation`, `second_same_await_is_collision`), all `#assert_axioms`-pinned;
`protocol/lean-build-surfaces.json` re-pinned. Evidence class **compiled**: lane umbrella
`lake build Minidregg +Host.Main:leanArts ObjectiveProofs` 9658 jobs rc=0; host-closure OK 641;
proof-hygiene PASS; import-boundary OK; build-surfaces PASS 1396; check-objective-proofs PASS (1974
statements / 1522 axiom sets unchanged). `second_delivery_refused` still has the collision-only premise at
`3b709c87` (now with seals); it is left for the design scribe. (An earlier copy on the hbox lane,
`369fafbc` on `36fca3ac`, is superseded.)

**Lane hazard for the root (hbox warm base):** a lane made by `mk-lane.sh` at base `9ccd6a2d` and rebased to
`36fca3ac` replayed STALE oleans for changed sources (`Theory.TypedAuthorization` without
`CellField.atomsOf`; `Theory.AssertAxioms` still defining `standard` beside the new `Theory.AxiomPin`):
lake did not rebuild them. Fix used: delete the lane's `.trace` for every `.lean` in
`git diff --name-only 9ccd6a2d HEAD` (64 files), then rebuild. Advance the hbox base to `36fca3ac`, or make
`mk-lane.sh` refuse when the lane will be rebased past the frozen tip.

Next quest I want: **QUEST-CHECKPOINT-INVARIANT** — state and prove `stored_checkpoints_typed` (§3) on top of
the object-authority record: a predicate `RecordCellsTyped snapshot`, preservation by every accepted intent
(birth, deliver, resolve, writeState, and refusal of any foreign post to a record cell), and its
inhabitant on the Tally scratch world; plus the allowlist re-classification of §2 with the
`QuorumSystem` non-triviality field. Acceptance: the theorem is pinned, the foreign-post refusal is a named
check that a mutation (allowing the post) turns red, and no PREMISE allowlist entry lacks a field or an
instance.
