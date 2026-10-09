# UPDATE 2 (P4-S2): stage 2 was ejected for a StoreEpoch conflict with kn2. It is rebased and RE-QUEUED as
# lane/P4-JP2-s2 = 5f2b951f..81bc2eb5 (base: GitHub next 5f2b951f). Its evidence is in bundles/evidence-jp2/s2r/.
# StoreEpoch is now 5 components parsed BY NAME. The KN2 agreement: accumulator parts history/spent/checkpoint
# fold by name. Stages 3 and 4: build on next, not on 91ed396d. Branch lane/P4-JP2-s2-next2 on burst2-b = the same
# commit. The build scripts are logs/s2r.sh (lake-slot / slot.sh). The journey ALSO needs the
# hyperdocument-link-sqlite-store and credential-signature-verifier crates rebuilt at the tip: a stale store
# binary makes every admission "unavailable".
# UPDATE 2026-10-07 by P4-S2: STAGE 2 (delegate) DONE. Stages 3 (birth) and 4 (JP2 PASS) remain.

- **Branch** `lane/P4-JP2-s2` = `91ed396d..198a74ed` (one commit), stacked on ranges 1 and 2. Box burst2-b, same lane.
  Bundle: `bundles/P4-JP2-s2.bundle`. Evidence: `bundles/evidence-jp2/s2/`. Reasons: `P4-STATUS.txt` (RANGE 3).
  Queue state: reviewed PASS by DEPUTY-PLATFORM and QUEUED stacked (queue/P4-JP2-s2.txt; keeper told). Never rewrite it. Stages 3-4 wait for the root to say go (drift-down).
- **What stage 2 changed** (READ the commit message `logs/commit-s2.txt`):
  - DescentEvidence has no root, and attenuate/delegate dropped `expectedPreRoot`;
  - delegation command frame v2;
  - StoreEpoch has a 4th component, `commands/v2`;
  - thin consent `checkPlanThin` now dispatches `.invoke` / `.delegate` and returns `Shown` (Host JSON `shownJson`).
  - **Stage 3 adds a `.birth` arm** to `checkPlanThin` and a `Shown.birth` constructor.
  - Rust `thin_views` sends no views for `delegate-source`. Birth needs its own branch there: today it refuses
    "thin consent signs invocations and delegations only".
- **Build recipes** in `logs/`:
  - `s2.sh`: closure (umbrella plus exes, then cargo and the client_consent tests);
  - `s2x.sh`: exes plus cargo only;
  - `thin-run.sh TAG "J0 J1 J2 J3 J4 THIN JP2"`.
  - Expected sole red: `Assurance.NativeAcceptedFixture` until the keeper regenerates it. Deputy ruling: do NOT
    regenerate it in a lane.
- **Gotchas**:
  - The kernel cannot `decide` through `String.splitOn` or `toUTF8`. Use `native_decide` + `#assert_compiled`, or
    state facts structurally.
  - `lean-ask --reload` after a Theory edit rebuilds hundreds of modules (5-8 min), and its daemon can die mid-reload.
    For wide changes, run `s2b.sh <modules>` in tmux instead.
  - The local mirror workflow: the source rsynced to `scratchpad/p4s2/src` (a git baseline), with `push.sh` rsyncing
    the changed files to the box. Refresh the mirror from the box before reusing it.
- **Stage 3 (birth)**: pointers below are unchanged. The deputy's conditions are in the brief: α from the REAL
  allocator with freshness proved; planted faults "Host shows a different debit" and "Host grants a different
  capability", both refused.
- **Stage 4**: JP2 frontier is still row 19 (`create notes`: "thin consent has no served target views"). The delegate
  rows 24-25 should pass once birth works (THIN d1 shows thin delegate commits).

# P4 range 2 (JP2 via thin consent): continuation for the next worker

Written 2026-10-07 ~03:30Z by P4-JP2 (the second P4 worker), at about 280K tokens, after stage 1 went green.
Read `P4-STATUS.txt` (the RANGE 2 section) and the deputy's rulings quoted below first.
Tags: READ = read in code, EXECUTED = run, INFERRED = mine, to check.

## Where things are (unchanged from the first worker, plus range 2)

- **Box and lane.** Box burst2-b; lane `/srv/lanes/plat-P4-PLAN-SCOPED-REPLAY/src`. Logs and scripts are in `../logs`.
  - `thin-run.sh TAG "STEPS"` runs the journey.
  - `s1.sh` is the stage-1 build: lean `minidregg-host` and both consent exes, then cargo build, then the
    `client_consent::tests` filter. Take a slot-1..4 flock and run it in tmux.
- **Branches.**
  - `lane/P4-PLAN-SCOPED-REPLAY` = range 1 (cb9559ac). QUEUED; do not touch.
  - `lane/P4-JP2` = range 2, on top of cb9559ac:
    - `4d311aba` journey(JP2): the laptop harness (its own executables, a storeless consent config, a no-Store row);
    - `91ed396d` host(codec)!: STAGE 1 (below).
- **Bundle and evidence.** Bundle: `/Users/ember/dev/redregg/work/platform/bundles/P4-JP2.bundle`.
  Evidence: `bundles/evidence-jp2/`, with stage 1 in `evidence-jp2/s1/`.
- **Queue state.** Stage 1 was ACCEPTED by the deputy and QUEUED as range 2 (`cb9559ac..91ed396d`, MERGE-QUEUE.md,
  stacked after range 1). Do NOT rewrite that range. Start stages 2-4 on a new branch on top of `91ed396d`
  (for example `lane/P4-JP2-s2`), and queue only when the deputy says "queue".

## Deputy rulings (DEPUTY-PLATFORM, agent a0c673b5e18434531)

- **Q1, birth: (i), deltas.** The display shows:
  - the new cells' contents, a function of signed fields;
  - the exact signed debit, with the guard balance ≥ debit (F5);
  - the capabilities granted to the signer.
  The ids are "allocated at admission". The theorem: there is an allocation map α (injective, and fresh with
  respect to the pre-directory) such that committed post = rename α (shown post) on every non-kernel address,
  and granted caps = shown caps up to α. α's inhabitant comes from the REAL allocator. Freshness is PROVED.
  No identity carrier.
- **Q2, delegate: (b).** The child's head/ancestry is a deterministic copy from the parent, so it is
  KernelOwned (like F6 blinding).
  - Signed: the parent capability id, grantee, rights, expiry and caveats.
  - "Rights ⊆ parent" and "parent belongs to the signer" are admission GATES (refuse-only; extend
    gate_refuse_only).
  - Delegate STOPS signing the whole authority root. The commit must say this changes what delegate signs, and
    why it is not a weakening: the parent is bound by its id plus the admission gate, which the executor checks
    against real state.
- **Order:**
  - (1) the codec twin, possession, offer paths: DONE (stage 1);
  - (2) delegate, with planted fault "signed delegate whose parent was swapped is refused";
  - (3) birth, with planted faults "Host shows a different debit, refused" and "Host grants a different
    capability, refused";
  - (4) JP2 PASS without editing its assertions, plus one planted fault turning it red (assert that the plant
    happened).
  Build once per stage in a burst2-b slot.
- **Epochs.** This is a codec/signing change, so there is a codec epoch. Follow the Store-epoch rule with
  DEPUTY-KERNEL: the second to land takes the next number, and old shapes refuse by name. Say what re-emits.
  Report each stage as it goes green.

## Stage 1: DONE (EXECUTED)

- **Code.**
  - `Host/Main.lean`: `pureCodec` is the one implementation of frames 7-11. `serveCodec` and the
    `minidregg-host CONFIG codec` loop never open a Store.
  - The consent provider's `codec` is deleted. Possession (226) is answered without admission.
  - The Rust `local_frame` runs `codec` instead of `stdio`.
- **Offer config.** The box paths in the offer config were VERIFIED harmless (READ): no laptop process opens them.
- **Runs.** J0 J1 J2 J3 J4 THIN PASS. JP2 enrollment rows 11-18 pass on a storeless laptop; the frontier is row 19
  (birth).
- **Remaining twin, not touched.** `Host/SourceAgreementReader.lean:277-286` still answers 7-11 over
  `SourceAgreementJson`. Filed as cv 01a1145d-b3f4 (CODEC-TWIN-2). It is not part of stages 2-4.

## Stage 2 (delegate): what I read (READ), not started

- **The signed declaration.** `Theory/CredentialAuthorityEffects.lean:714`, `DelegateDeclaration`, has the fields
  `{child, parentId, target, expectedPreRoot, operationNullifier}`. `expectedPreRoot` is the WHOLE
  authority-cell root.
- **DescentEvidence.** `DescentEvidence` (:550) carries `preRootExact : expectedPreRoot = pre.root` and is shared
  with issue/attenuate (31 uses in that file). The delegate must stop carrying it.
  - Either parametrise `DescentEvidence` without the root, or give delegate its own evidence.
  - The other fields (parentExact, parentLineageValid/Anchored, childSlotFresh, issuer/policyCurrent,
    selfUnregistered) are the gates.
- **The patch.** `DelegateDeclaration.patch` (:771) writes exactly 2 addresses
  (`patch_writeFootprint`):
  - `capability kind child.id` ↦ `⟨child, (parent.head, .delegated request) :: parent.ancestry⟩`
    (`delegatedCapability`, :755);
  - `registered (capability child.id)`.
  KernelOwned for delegate = the stored lineage component of the first address. Write a field-level KernelOwned
  if the Store address is the whole StoredCapability. Check this; it may need a layout split so that `child` is
  its own address.
- **Root uses in the controller.** `Kernel/CapabilityDelegationController.lean`:
  - :51 (the operation marker hashes expectedPreRoot);
  - :165 (DescentReady);
  - :197 and :221 (the evidence).
- **JSON authoring.** `Host/Json.lean`:
  - :609-623 (the delegate-source author: expectedPreRoot is a required field);
  - :1427 (the "delegate-source" kind).
  The Rust client fills it from somewhere; grep `expectedPreRoot` in `native/resource-client/src`.
- **Plan preparation.** `Kernel/NativeHost.lean:212-221` builds the `.delegate` plan: one slot, role 6,
  `CapabilityDelegationController.request`. Thin consent needs `checkPlanThin` for `.delegate`; today it
  refuses `notInvocation` (`Kernel/NativeThinConsent.lean`, checkPlanThin, first line).
  - Rebuild the request locally from the command (as `legValues` does), taking subjectKeyEpoch and policy
    epoch/revision from the proposal (gates).
  - Display the child capability record minus lineage.
- **Rust.** `workspace.rs` thin wiring covers only the non-append `submit_intent`. Delegate submits go through
  another path (check `client_consent::plan` callers at main.rs:1901/2029). Views: the delegate needs none (the
  parent is bound by id plus the gate).
- **Codec epoch.** Changing `DelegateDeclaration` changes the delegation command codec. Re-emit what encodes it;
  old command bytes must refuse by exact decode. Coordinate the epoch number with DEPUTY-KERNEL.

## Stage 3 (birth): pointers (READ)

- **Preparation.** `Kernel/NativeHost.lean:144-169` builds the birth plan, with slots:
  - factory (role 0);
  - authority (role 1);
  - allocations (role 2 × createRequests);
  - sources (role 3 × operations).
- **Writes.** `Kernel/ResourceBirthController.lean`:
  - `planWrites` (:305): allocationWrites ++ [factory (pre=post), Book before→after] ++ authorityWrites;
  - `prepareDraft` (:834);
  - `prepareBirth` (:669);
  - `preparePostAuthority`, where the allocator is `allocate? Registry pre.directory.directory descriptor`
    (this is α's real inhabitant);
  - `PreparedDraft.user_source_preserved` (:852): births, grants, initialPolicies, funding, fee and
    transactionId are the user's.
- **Today's refusal.** The Rust birth path refuses "thin consent has no served target views; nothing signed".

## Stage 4 (JP2 PASS): what is already true and what remains

- **The harness is done** (`4d311aba` plus `91ed396d`). The friend's laptop has:
  - its own Host (MINI_LOCAL_HOST, used as the `codec` loop and as `--verifier`);
  - its own consent provider and credential verifier;
  - `consent.json` with no Store;
  - MINI_THIN_CONSENT=1.
  Do NOT edit JP2's assertions. Row 2 (the laptop config names no Store) is new, and it was shown red
  (run-jp2diag).
- **Families JP2 needs.**
  - possession: works (stage 1);
  - `create` (birth): stage 3;
  - `invoke first-write` (scalar): supported;
  - `read` (observation 231): supported;
  - `delegate`: stage 2;
  - publish/export: local, no signing.
- **Proxy and tamper rows.** Rows 42-55 (proxy and tampered frames) cascade from the missing `first-write`
  call.bin. They should go green once rows 19-21 pass. Do not touch them.
- **Planted fault.** Add one planted fault that turns JP2 red, and assert that the plant happened (a log line or
  file check) before you read the verdict. Candidate: the thin proxy (`journey.d/lib/thin-proxy.py`,
  `THIN_PROXY_MODE=view=...`) serves the friend a different notes view, and `submit first-write` is refused
  `servedRootMismatch`. To use it, the friend's `MINI_CONSENT_HOST` must point at the proxy with
  `THIN_PROXY_REAL` set to the laptop provider. Run that as a separate pass so that JP2's own rows are unchanged.
- **Run.** `bash ../logs/thin-run.sh TAG "J0 J1 J2 J3 J4 THIN JP2"` (about 1 min). Control: J0-J4 and THIN must
  stay green.

## Gotchas found in range 2 (EXECUTED)

- **zsh quoting.** Remote python heredocs break on apostrophes inside `ssh '...'`. Write the script locally, scp
  it to `../logs/`, and run it there.
- **lean-ask on Main.lean.** `lean-ask check Host/Main.lean` takes about 20 s after an edit near line 1900.
  When you insert defs, move docstrings with them: an orphan `/-- -/` gives "expected 'lemma'".
- **Full stage build.** About 6 min for minidregg-host plus the consent exes, cargo, and the filtered tests.
