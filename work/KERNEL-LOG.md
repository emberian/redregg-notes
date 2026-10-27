# KERNEL-LOG — BUILD-KERNEL continuation (nanodregg), written 2026-10-16 at handoff (~500K tokens)

Repo ~/dev/nanodregg (main only). EDIT ONLY in the worktree ~/dev/nanodregg-wt/kernel (detached at main;
`git checkout -q --detach main` to refresh); commit ONLY with `scripts/commit -F MSG PATHS…` from there
(CAS onto main; SIZE: lines for every risen metric; --cross-layer REASON when touching another layer;
pass WHOLE files: a stale copy of a shared file like gates/waste.tsv reverts others' rows — rebase it on
`git show main:<file>` first). Decisions go in decisions/kernel.md (KERNEL-3..10 so far; K0–K2 in the
frozen DECISIONS.md).

## What is on main (my commits): 1d14290 a6101cb 760115e 3a3c26c 58f7f0f 82e71e4 9de81fb
- Kernel/{Bounds,Cell,Check,Turn,World}.lean — World (cells TreeMap of live|tomb, journal, spent, height,
  chain, allowance), Turn (txId, window, pins, creates, legs, retires, nullifiers, charge, event),
  World.admit (bounds→journal→shape→window→pins→nullifiers→charge→ids→retires→legs, commit total),
  World.fold, chainOf. Env {hash : String → ByteArray → D, bytes, turnBytes, cellBytes}. ROM born ids are
  content-addressed (romIdOf = package identity, LANG-9 confirmed).
- Kernel/Receive/{Call,Derive,Follow,Audit,Submit}.lean — signed Call {member, key, window, pins,
  maxCharge, body}; 10 kinds enroll rotate install create write law invoke grant follow revoke; Pinned
  view; Program {checkInstall, judge, run} (LANG instantiates: Lang/Program.lean); Req {agent, principal,
  notBefore, validUntil}; sealTurn; mayFollow + founders' genesis; audit; Receive.submit (journal first).
- Kernel/Sim.lean + Kernel/Sim/Main.lean (`lake exe kernel-sim SEED…|--seeds N`, ALL PASS; WASTE rows
  pinned in gates/waste.tsv: cells-touched 2.0, pins-checked 1.0, fold work 2.5).
- Proofs: Check, Admit (admit_ok/height/chain/charge/pins, stale_refused/named, replay_named,
  admit_journal), Fold (fold_append/height/chain/charge, chain_binds, fold_head_binds, Collision),
  Receive (receive_congr, sealTurn_ok, dispatch_sealed, receive_ok, receiveWith_key, submit_ok,
  submit_replayed), Audit (Honest, audit_ok), Frame (admit_frame, admit_rom, fold_rom, admit_nullifiers,
  fold_nullifiers), Equiv (World.Equiv, check_congr, admit_congr_error/ok, fold_congr), Authority (Chain,
  walk_chain, write_authorized, law_authorized, key_current, rotate_precommitted). Census clean.

## Open / next (in order)
1. Fuse the pin lookup with the leg lookup (waste cells-touched 2.0 → 1.0; lower the ceiling).
2. Bounds theorem: an admitted Turn's weight ≤ a constant derived from Bounds (frame size for HOST).
3. Run kernel-sim under CODEC's deployed Env when Codec/Deployed.lean lands (CODEC-0; told CODEC shapes
   are stable; deployed Digest needs Std.TransOrd + LawfulEqOrd).
4. Open questions in decisions: storage refill/credit (no `credit` field; allowance only falls — K2
   critique), any member may sponsor (KERNEL-6), journal pruning by bounded windows (K1), checkpoint is
   incremental (HOST/CODEC, LAW 5 as amended).
5. The DELETE-KERNEL dossier (~/dev/redregg/work/DELETE-KERNEL-20261016.md) is truncated (no per-ctor
   row reach); it is superseded by the rebuild unless ROOT wants it finished.

## KERNEL-2 (successor; written 2026-10-16 at ~265K tokens)

Landed on main (all via scripts/commit, PRE-PUSH GREEN):
- ea71b51 kernel!: Turn.touches {cell, seen, act := keep|write ops|retire} replaces pins/legs/retires;
  touchCheck = ONE lookup per touched cell (pin then act). bornTouched, duplicateTouch. sealTurn takes
  one optional effect (on a pinned cell, else `unpinned`). Turn.weight = logWeight + growth (charge =
  storage); Bounds.weightMax = 4*eventBytesMax, admit_weight. WASTE: cells-touched 2.0→1.0, fold
  work 2.5→2.0, pins-checked row DELETED (it could not go red). Host/Sim/Toy.lean edited cross-layer.
- 38d1ecc Receive.rederive + rederive_ok (PROTOCOL-4), Refusal.undecodableEvent/eventMismatch,
  AuditFault deleted (audit refuses in Verdict); fold_foldlM, admit_window, absent_final (HOST-8). The
  Sim forges each seed's log at its last write; audit must say eventMismatch at that index.
- d310846 Bound.counter (counterLimit 2^64, kindLimit 2^32) for CODEC-4's fixed-width codec.
- 8cce39e decisions KERNEL-11..17 (KERNEL-11/12 in ea71b51, 13 in 38d1ecc).
Plants recorded in the commit messages (pin check off ⇒ 16/16 red; weightMax 400 ⇒ red; rederive
comparison off ⇒ 64/64 red). kernel-sim --seeds 64 ALL PASS (2749 admitted, 6165 refused as expected).

- cc90e8b World.weight/cellsWeight/Entry.weight; Kernel/Proofs/Weight: admit_world_weight,
  fold_world_weight (World.weight + Σ logWeight + allowance never rises) — KERNEL-18: worldBytesMax
  IS the genesis allowance. Reject.name / Refusal.name + name_injective (ROOT law-7 ruling).

Open / next, in order:
1. Credit on retirement (KERNEL-15): refund the retired cell's weight; extend fold_world_weight
   (the invariant still holds since only World bytes are refunded). Needs a `credit` term in commit's
   allowance and admit_charge restated.
2. Sim under CODEC's deployed Env: BUILD-CODEC (aca5ce91ec8e30814) is writing Codec/Kernel.lean
   against the touches shape, Codec/Deployed.lean after Ed25519 lands. Also owes size(encode t) vs
   logWeight. CODEC asked whether genesis should clamp allowance < 2^64; I said assert in the decoder
   or ask me to clamp.
3. ROOT rulings needed: signature scheme (KERNEL-14), refill authority (KERNEL-15), sponsoring fork
   (KERNEL-16).
4. stale_named is only for the FIRST failing touch; a "refusal names are true" theorem (every
   `stale c` refusal has a touch at c whose pin disagrees) is worth proving for law 7.
5. gates/__pycache__/tree.cpython-311.pyc is TRACKED and rewritten by every census run (GATES's
   file; tell them, I restored it, never commit it).

### ROOT rulings received at handoff (KERNEL-3 starts here; text in decisions/kernel.md, "ROOT rulings on KERNEL-14..17")
- v0 signatures: Ed25519 only; nothing to build in the kernel (it stays opaque bytes + Ctx.verify).
- BUILD NEXT, in order: (1) credit-on-retire: a retire refunds the cell's weight to the allowance; restate
  admit_charge and keep fold_world_weight. (2) Right.enroll: enroll is authorized by a grant chain rooted
  at a founder carrying `.enroll`, attenuable to "may enrol ≤ n" (the count lives in the grant, decremented
  by a write to it: that grant cell is a touch of the enroll turn). Prove `enroll_authorized` (the twin of
  write_authorized). Sim plant: a drained-World scenario where a member without the right, or past its
  count, is refused by name. Founders' genesis (Receive.genesis) must give each founder its root enroll
  right. (3) hygiene, cross-layer: `git rm --cached gates/__pycache__/*.pyc` + .gitignore, with a
  CROSS-LAYER line.

### FIRST for KERNEL-3 (BUILD-CODEC, 10-16, after my handoff)
- Codec/Deployed.lean is on main at 180cf9b: `Nanodregg.Codec.Deployed.env : Env Digest`, `ctx (program) :
  Ctx Digest` (verify = Ed25519), `world : Stream (World Digest)`. The TreeMap laws for Digest are
  @[instance] theorems in Codec.Proofs.Digest (import it). The generic toy forms are in Codec.Kernel
  (`turnBytes dc`, `callBytes dc` with `dc := Stream.u64`). → Run kernel-sim under the deployed Env (brief
  item 3), and replace the Sim's toy turn and cell encodings with Codec.Kernel's generic ones (no twin
  encoder).
- Weights = encoding EXACTLY (I chose this and told CODEC): Op.weight set = 9+v and erase = 5;
  Act.opsWeight for a write += 4; Cell.weight = 9 + Σ slots; Turn.logWeight fixed part += 16. Then
  CODEC proves size (encode t) = t.logWeight. The Weight proofs should survive with omega (slot weight
  8+v ≤ op weight 9+v). Check host-sim's WASTE bytes-per-turn after the change.

## KERNEL-3 (successor; written 2026-10-16 at ~355K tokens)

Landed on main (all via scripts/commit, PRE-PUSH GREEN; decisions KERNEL-19..21 in decisions/kernel.md):
- 8c5a5b1 credit on retirement, EXACT (KERNEL-19, ROOT accepted incl. the write refund): touchCheck
  returns Post {cell, entry, freed}; checkCharge charge ≤ allowance + credit; commit allowance +
  credit − charge. admit_conserves / fold_conserves are EQUALITIES (World + log + budget constant);
  fold_world_weight its corollary; admit_retire. fold_charge keeps only "charge = weight".
  Plant: credit dropped ⇒ kernel-sim 63/64 red.
- 9922f21 kernel! KERNEL-16 built (KERNEL-20): Right.enroll n; ONE grant kind with the World as a
  target (worldId); follow grants / Body.follow / followChain / readGrantLike DELETED; mayFollow =
  walk observe on the World; Body.enroll … via; count = append-only LEDGER at enrollBase(1024)+i,
  invoke m at 4096+m; enrollMax 256; carve-from-parent (grantWidens); `unrooted`; genesis founder
  World grants (founderGrantId). enroll_authorized, grant_rooted, grant_carves, spendEnroll_ok.
  Cross-layer: Codec/Kernel.lean + Proofs (Right tag 3, Body Fin 9), Protocol Machine.body (takes X).
  Plants: count off 45/64, walk off 63/64, unrooted off 59/64.
- ef10df3 standing runs `kernel-sim --seeds 64` once (coverage gate: a run of ≥16 seeds FAILS if
  one of 12 planted refusal names is never met); scripts/commit records a path missing from disk
  with `git rm --cached` (was impossible for tracked+ignored files). bc0460d untracked pycache.
- f11caa2 KERNEL-21: WorldRooted fold invariant PROVED (Kernel/Proofs/Rooted: admit_rooted,
  dispatch_born, step/submit/audit_rooted, genesis_rooted, chain_rooted; RootedDeployed:
  deployed_audit_rooted, deployed_enroll_founder with CODEC's digest premises discharged).
- 74556c1 Kernel/Sim/Gen: the generator generic in `Params` (env, ctx-from-registry, pub, sign,
  regKey, zero); Kernel/Sim = toy params + aliases lang-journey uses. Counts unchanged.

In flight / next, in order:
1. Sim under the DEPLOYED Env (ROOT item): blocked on CODEC (aca5ce91ec8e30814) adding
   `Ed25519.publicKey seed` and `Ed25519.sign seed msg` with RFC vectors as theorems (asked).
   A probe instance passed 16/16 seeds under the deployed Env with HASH signatures. Recreate it as
   Kernel/Sim/Deployed.lean: `params : Gen.Params Digest := { name, env := Deployed.env,
   ctx := fun _ => Deployed.ctx Gen.program, pub := Ed25519.publicKey, sign := Ed25519.sign,
   regKey := fun b => Deployed.env.hash "nanodregg/sim/registry" b, zero := Digest.zero }`
   (imports Kernel.Sim.Gen, Codec.Deployed, Codec.Proofs.Digest for the TreeMap laws). Then make
   Kernel/Sim/Main default to it, with `--toy` for the toy, so standing judges the deployed run.
   Check gates/waste.tsv's rows still match. Probe file kept at
   /private/tmp/claude-501/-Users-ember-dev-breadstuffs/b3795e84-08d4-436c-9079-91d4e05687e9/scratchpad/SimDeployed.probe.lean
2. PROTOCOL still owes the `enroll:N` right parse and a decision on the `follow` verb (now sugar for
   grant World [observe] via me.grant). ROOT relayed it.
3. Answer HOST-3 / PROTOCOL-3 / LANG-2 / CLIENT-2 asks of Receive as they arrive (none came to me).
4. Open: stale_named only names the FIRST failing touch (KERNEL-2 item 4); a revoked carved
   grant does not return its unspent count to the parent (KERNEL-20 critique); refill = a grant later.
Working notes: zsh does not word-split `$VAR`, so use `${(f)"$(…)"}` for path lists; never
`cat > file` without a heredoc (it blocks on stdin); a scripts/commit SIZE refusal names each
metric, and the fix is to append `SIZE: <metric>: <why>` lines and re-run.

## KERNEL-4 (successor; written 2026-10-17 at ~280K tokens; Mac builds FROZEN by ROOT/Ember 10-17, hbox is the execution node)

Landed on main (all via scripts/commit, PRE-PUSH GREEN):
- 42bf1ce KERNEL-22: tree.Module.is_tooling (libs Census/Emit; path components Sim/Rows/Journey);
  "Lean lines (deployed)" excludes tooling (10482 → 7235 on that main), new informational row
  "Lean lines (tooling: Sim, Rows, Journey, Census, Emit)" = 3247; closure C9 refuses a deployed
  module importing tooling (plant: Kernel.World importing Kernel.Sim.Gen ⇒ C9 red). ROOT accepted.
- d1f483e size.py HOST_EXE was "nanodregg-host" (no such exe ⇒ Host-closure row read 0 vs ceiling 150);
  now `host` (54 modules), and a missing exe leaves the row unmeasured (WARN), never 0.
- 9e60d7f the toy Sim runs CODEC's Codec.Kernel codecs over Stream.u64 + CODEC's decodeCall; the call
  REGISTRY, regKey and the toy encoders are DELETED; Protocol/Rows/Sim and Lang/Journey use
  Kernel.Sim.ctxWith (one toy). Plant: decoder drops the signature ⇒ 16/16 red badSignature.
- b5b7a17 KERNEL-23 design (ROOT accepted; rulings: root post-state, Turn codec UNCHANGED, chainNext =
  H(prev ‖ turnDigest ‖ root'), v0 trie = CELLS + NULLIFIERS, WASTE row hashes-per-nullifier too).
- 87c721e Kernel/Trie.lean (generic binary Merkle trie: uncompressed, shape = f(key set), multi-key leaf
  only at Spec.depth; tags empty 0/leaf 1/node 2; verifyInclusion/verifyExclusion bounded by depth) +
  Kernel/Proofs/Trie.lean: get_insert(_self/_ne) UNCONDITIONAL; inclusion_sound / exclusion_sound
  (verified ⇒ true or `Coll S`: two byte strings one hash; premises hL leafBody injective, hN digest-pair
  concat injective); prove_includes/prove_excludes (WF ∧ Shallow); wf_insert, shallow_insert.
  bytes_append_inj moved to Kernel/Proofs/Bytes.
- fe4c9ef Routed invariant: routed_build/insert, mem_toList, toList_nodup, toList_insert_perm,
  toList_build, keys_insAt, perm_of_nodup_mem, nodup_of_map_fst.
- 67fedfa kernel-sim DEFAULTS to the deployed params (Kernel/Sim/Deployed: Codec.Deployed.ctx, Ed25519
  publicKey/sign from CODEC 279c2b8, seed = cSHAKE256(secret) under "nanodregg/sim/seed"); `--toy` for
  the toy. --seeds 64: admitted=2554 refused-as-expected=5474 restarts=929 failing-seeds=0 ALL PASS
  (~15 s; toy identical counts); WASTE 1.000 / 2.000 unchanged. Plant: wrong signing seed ⇒ 16/16 red.
  A standing run on 67fedfa was started before the freeze (my own process, background task bxj3747op);
  its line is in <git-common-dir>/nanodregg-standing/verdicts.log when it finishes. Quote that.

UNCOMMITTED in ~/dev/nanodregg-wt/kernel: decisions/kernel.md += KERNEL-24 (D3 world origin + genesis
commitment) and KERNEL-25 (invoke owner-gated). Commit them FIRST on hbox (`--no-build "decision text"`):
the file was byte-identical to main before the append, so take main's copy + the two appended sections.

### Next, in order (KERNEL-5)
1. KERNEL-25 invoke authorized (ROOT ruled, small, THE BAR path): Derive.invoke's
   `principalOf X look u obj (.invoke method) via` → `ownerAuthority X look u obj cell (.invoke method) via`;
   theorem invoke_authorized (twin of write_authorized, Proofs/Authority); Sim: in the invoke path a
   non-owner without grant ⇒ `noGrant` (I chose noGrant over ROOT's suggested `unauthorized`: one condition,
   one name — tell ROOT). Gen has no invoke arm today (the stub program's method 0): add one. Rows/journey
   that invoke as non-owner must grant (LANG-3, PROTOCOL). Tell HOSTING a665735e10cfc4da6 + LANG-3
   adc11001c5ad34e55 when it lands.
2. KERNEL-24 D3 (ROOT ruled; OPS repro ~/dev/redregg/work/ops/replay-20261016/): World.origin, genesis
   takes nonce separately, origin = H(domOrigin, name ‖ nonce ‖ allowance ‖ founders), genesis chain =
   H(domGenesis, origin), founder ids keyed by origin, Unsigned.world checked FIRST in receive →
   Refusal.wrongWorld; theorems receive_wrongWorld, admitted_elsewhere_refused, genesis_inj,
   admit_origin/fold_origin; Sim plants (replay log into a 2nd genesis ⇒ wrongWorld at turn 1; swapped
   founders ⇒ different chain), add "wrongWorld" to Gen.planted. Coordinate: HOST-4 a127d18f879bdd316
   draws the nonce; TRANSPORT a4652a8aa8280fcef binds the envelope to w.origin; CODEC re-encodes the call.
   All three were told these exact shapes. Flag day: call codec, origins, founder ids; re-genesis.
3. Sequencing in Call/Derive: LEDGER abea0cf4c24b5023e's D2 (sealTurn over an effect list) is landing
   there (main already shows `sealTurn X c [] (writeOf …) []`); LANG-3's Occasion (Req.occasion, relaw
   carries laws; I said YES, LANG lands the kernel half cross-layer); then items 1 and 2. Rebase on main.
4. KERNEL-23 part 2, the World port (big): Slot D = cell | nullifier; Leaf = entry Entry | spent;
   World {trie, journal (TreeMap, unchanged), height, chain, allowance, origin}; cells and spent DELETED.
   Spec from E: bit 0 = tag (nullifier=true), bit i+1 = MSB-first bit i of E.bytes id (false past end),
   depth 257 (Bounds.trieDepth), hash = E.hash "nanodregg/kernel/trie/v1", kbytes = tag ‖ E.bytes,
   vdigest live c = pinOf E (some c), tomb = H(domTomb), spent = H(domSpent). `live` and friends take E.
   Port reach measured: 30 `.cells` + 74 `live` uses in Kernel, 3 in Codec, 3 Protocol, 1 Lang; TreeMap
   lemmas in Frame/Weight/Rooted/Equiv/Fold → trie lemmas (get_insert, toList_insert_perm, mem_toList).
   World.Equiv becomes extensional (∀ k, get equal). chainNext takes root'. WASTE rows:
   hashes-per-touched-cell and hashes-per-nullifier (pin measured; ceiling ⌈log₂ n⌉+2). Sim: prove +
   verify touched/untouched cells and nullifiers against Host and follower roots; forged-proof plants =
   the acceptance (sibling flipped, leaf swapped, tomb claimed live, nullifier claimed unspent).
   CODEC-2 a5db8dcb963c5d57d: decodes by `build S S.depth 0 l` + order/nodup check, and offered to PROVE
   `build_toList (h : Canon S 0 t) : build S S.depth 0 t.toList = t` (Canon = Routed ∧ WF ∧ Shallow ∧
   singleton leaves above depth ∧ nodes ≥ 2 keys) + canon_empty/canon_insert in Kernel/Proofs/Trie
   cross-layer — ACCEPTED (it is KERNEL-23's history-independence theorem). Land the port and CODEC-2's
   Codec/World + Codec/Proofs/World in ONE commit. Then tell HOST-4 (absorbs the base/head change) and
   PROTOCOL (head record (height, prev, turnDigest, root); `read` gains a Proof).
   LEDGER: generalise cellsWeight into cellsSum (f : Entry → Int) when restating Weight (LEDGER writes
   its sums over cellsSum in Proofs/Value; ruled (b)).
5. Open from earlier: stale_named names only the first failing touch (a "refusal names are true"
   theorem); a revoked carved grant does not return its unspent enrol count.
Working notes: scripts/commit now refuses a path whose worktree base is not main's (9db4020) — refresh
the worktree (`git checkout --detach main`) before editing; "max dependents of a non-foundation module"
is a second dependents row needing its own SIZE line; a census RED "object file … does not exist" for
another layer's module was transient (retry).
Addenda (KERNEL-4, after the handoff text above):
- LANG-3's kernel half of ID-1 (Occasion birth|write|relaw laws|invoke m; Req.occasion; reqOf u p o; 4
  call sites; /private/tmp/claude-501/-Users-ember-dev-breadstuffs/b3795e84-08d4-436c-9079-91d4e05687e9/scratchpad/kernel-half.diff)
  REVIEWED AND APPROVED by me; LANG lands it cross-layer from hbox.
- Open, for KERNEL-5 + ROOT: public objects under KERNEL-25. My proposal: a grant with grantee = worldId X
  means "any enrolled member" (walk accepts any signer with a live member cell); Authority.anyone = owner
  issues such a grant for invoke m. LANG-3 is waiting on this for its stdlib `anyone`.
- Open, for KERNEL-5 + ROOT: LANG-19 / cv task 01a14805-3d5a: on `law`, also judge the NEW laws' with
  occasion relaw laws' over old = new (a new law currently never judges the state it is adopted over).
- HOSTING wants the KERNEL-25 plant kept: the gate skipped ⇒ a stranger's invoke admitted (red).
- STANDING on 67fedfa (deployed kernel-sim judged): `STANDING 67fedfa799fe gates=ok build=ok census=ok sim=ok
  rows=INCOMPLETE(4 pending) waste=ok(pinned 6, unpinned 0) unmeasured=0 => INCOMPLETE` (the 4 pending rows
  are pay/well/bounty/grain, blocked on LEDGER/CLIENT); kernel-sim under deployed parameters: seeds=64
  admitted=2554 refused-as-expected=5979 failing-seeds=0.
- CODEC-2 wrote (NOT built) the history-independence lemmas in ~/dev/nanodregg-wt/codec/Kernel/Proofs/Trie.lean:
  Shape, Canon := Routed ∧ WF ∧ Shape, canon_empty/build/insert, build_toList, eq_of_toList_eq; CODEC-2 lands
  them cross-layer on hbox BEFORE the port; build the World port on canon_insert. See CODEC-LOG "## CODEC-2".
- ROOT rulings (10-17, final, recorded in the uncommitted decisions/kernel.md as KERNEL-26 + a rulings section):
  noGrant stands; KERNEL-26 public objects ACCEPTED (grantee worldId = any enrolled member; walk gains one
  disjunct; revocable/attenuable like any grant); LANG-19 ACCEPTED (`law` also judges laws' over old = new,
  occasion relaw laws'). KERNEL-5's order: LEDGER D2 → LANG-3 Occasion → KERNEL-25 → KERNEL-24 → World port.
  Commit decisions/kernel.md (main's copy + KERNEL-24, -25, -26 and the rulings section) FIRST on hbox.
- LEDGER (abea0cf4c24b5023e) landed D2 (9e6fd1c) and i64 (b2d60e7). Its D1 (value cells) is written but unbuilt in
  ~/dev/nanodregg-wt/ledger and touches World/Cell/Call/Derive + Proofs Admit/Rooted/Receive/Weight. It MOVES
  walk/principalOf/ownerAuthority/slotsOf into a new Kernel/Receive/Authority.lean, so KERNEL-25's one-line
  change goes there after it lands. LEDGER D1 lands before KERNEL-25/24 (told it not to wait).

## KERNEL-5 (successor; written 2026-10-17 at ~390K tokens; all work on hbox, wt/kernel at /tank/dregg-build/nanodregg/wt/kernel)

Landed on main (all via scripts/commit, PRE-PUSH GREEN, pushed):
- 9d2e5df decisions KERNEL-24/25/26 + ROOT rulings (carried from the Mac worktree; Mac wt/kernel REMOVED).
- be98647 KERNEL-25/26 (+LANG-19 as KERNEL-27 v1): invoke via ownerAuthority (noGrant); `granteeHolds … pub`
  in walk (World grantee = any live member, FIRST LINK ONLY; parent links exact, agreeing with checkParent:
  a public grant is used, never re-delegated — ROOT accepted the narrow side); checkGrantee in grant.
  Chain gained a Bool index (pub; parent links false). Theorems invoke_authorized, invoke_stranger_noGrant,
  ownerAuthority_program_free (rfl: the gate never reads the program), granteeHolds_ok; enroll_authorized
  doc states the public enrol pool. Sim: stub laws freeze/methods, arms 21 (programmed object + public
  grant) and 22 (invoke owner / no-grant / public / method-1 grantRight / carve-public noGrant);
  `seen` records `what:verdict`; `plantedArms` must each be met. Consumers: Hosting G7 (kernel noGrant;
  HOSTING's owner law now redundant, theirs to delete), Lang L10c plant, Protocol sealedLaw.
- 63711ec KERNEL-28: answer to LEDGER-5 (+LANG-23): effects are Body, actor-parameterised receivers,
  one Draft sealed once, accountId = H(domAccount, owner‖asset) with explicit create ids in the Turn;
  amount-bounded right = cv task 01a14938. ROOT accepted.
- a533d7a (LANG-4, carrying my patch) KERNEL-27 final: `Occasion.adopt (laws : List D)`; law's second
  judge = incoming laws over the state as `.adopt laws'`. ROOT overruled its own LANG-19 wording and my
  `.birth` conflation. LANG-4 is landing "second judge on ADDED laws only" (quorum forged-approvals hole) —
  I AGREED; check it landed and kernel-sim law-self still met.
- 9e91ede KERNEL-24 (flag day): Unsigned.world first (kernel/unsigned/v2), receive's first check
  wrongWorld, World.origin (kernel/world/v2 codec; HOST-20 stamp refuses old bases), originOf over CODEC
  raw combinators, World.genesisChain (HOST-6's ask), founder ids v2 keyed by origin, `host genesis
  [--nonce HEX32]` (prints origin/nonce; NAME bound), Kernel/Proofs/Origin (admit_origin, fold_origin,
  genesis_inj, genesis_chain_inj, admitted_elsewhere_refused), receive_wrongWorld/receive_ok_with.
  Sim: whole log replayed into a 2nd genesis ⇒ wrongWorld; swapped founders / other nonce ⇒ other chain.
  WASTE seal re-pinned 1.723 (origin digest per base). Machine.plan signs world := w.origin (TRANSPORT
  replaces with Self.world).
Standing line: not run by me on 9e91ede (ROOT/standing owns it); my local runs on the landed tree:
kernel-sim --seeds 64 ALL PASS (both) admitted=3069 refused-as-expected=8383 restarts=962; hosting-sim,
lang-journey, host-sim, host-file-sim, store-plants ALL PASS/GREEN; rows INCOMPLETE 4 pending, 0 FAIL;
cargo test --test real ok. Run `scripts/standing.sh` on main first and quote it.

### Next, in order (KERNEL-6)
1. The World port (KERNEL-23 part 2) — NOT STARTED. Spec unchanged from KERNEL-4's item 4 above (Slot D =
   cell | nullifier; Leaf = entry | spent; World {trie, journal, height, chain, allowance, origin}; cells
   and spent DELETED; Spec bits/depth 257/domain "nanodregg/kernel/trie/v1"; chainNext takes root';
   admit_root = rootOf sorted contents via CODEC-2's build_toList/canon_insert (b9ffe57); chain_binds_root;
   WASTE rows hashes-per-touched-cell + hashes-per-nullifier pinned from measurement; Sim forged-proof
   plants: sibling flipped, leaf swapped, tomb claimed live, nullifier claimed unspent). CODEC-2
   (a5db8dcb963c5d57d) writes the World codec decoder (CODEC-19) against your trie signatures — SEND THEM
   FIRST. Flag day with CODEC-2 (World codec + head record) and HOST-6 (a59922b2afa99acbc; base/open/pages).
   World.origin must survive the port (Equiv, codec, admit_origin).
2. Review LEDGER-2's (afd32f4b9d6e68d3e) D5 statements before it lands: effect_as_signed (LANG-4's name,
   plant: run the effect under the invoker), visit_distinct, draft_cells_distinct, account_keyed
   (INJECTIVE up to HashColl, not "is a hash"), resolve_well/resolve_of (LEDGER-7 AcctRef), the Draft
   restatements; refusal `revisited obj`; checkGrantee also admits a LIVE kindObject; Req.self. D5 and the
   World port run in parallel and converge forward; expect a rebase on whichever lands second.
3. Open: stale_named names only the first failing touch; a revoked carved grant does not return its unspent
   enrol count; cv 01a14938 amount-bounded right (after D5).
Working notes: scripts/commit refuses when main moved on any path you touch — `git diff > logs/X.patch`,
`git checkout -- .`, `git checkout --detach main`, `git apply --3way`, `git reset`; resolve conflicts by
script. Every new SIZE count needs a `SIZE: <row>: <why>` line, a raised waste ceiling a `WASTE: <op>:`
line. Quote-heavy edits: write python scripts locally and scp them (ssh heredocs eat apostrophes).
Roles: logs/ROLES.txt on hbox. LANG-4 a2fbb4419dc4a69aa, LEDGER-2 afd32f4b9d6e68d3e, HOST-6 a59922b2afa99acbc,
PROTOCOL-6 abd8f012f13228e0b, TRANSPORT a4652a8aa8280fcef, CODEC-2 a5db8dcb963c5d57d, HOSTING a665735e10cfc4da6.
Law I think was wrong (resolved): ROOT's LANG-19 wording (relaw for the incoming laws) — KERNEL-27.

## KERNEL-6 (successor of KERNEL-5; started 2026-10-17 ~14:40Z; hbox wt/kernel)
- STANDING on main 4ae6608 (contains 9e91ede): `STANDING 4ae6608af5b3 gates=ok build=ok census=ok
  runs=INCOMPLETE(rows : INCOMPLETE(INCOMPLETE 4 pending)) waste=ok(pinned 8, unpinned 0) unmeasured=0 => INCOMPLETE`.
- LANG-4 landed 907b55d (second judge on ADDED laws only) — item closed.
- HOST-6: World.genesisChain is what HOST-25 needs (closed). Told it: origin survives the port; genesisChain
  formula unchanged (genesis trie empty, its root constant); only chainNext gains root'.
- LEDGER-2 lands D5a (explicit create ids `Turn.creates : List (D × Cell)`, `notContentId`) FIRST; I port on top.
- 10-17 ~16:30Z PORT STATE (hbox wt/kernel, UNCOMMITTED, rebased on D5a 5b87949 via logs/kernel6-rebase.sh which
  fails loudly; last patch logs/kernel6-r1.patch; untracked new files Kernel/Proofs/{TrieMap,Cells}.lean):
  World.lean (Slot/Leaf/Cells/trieSpec/byteBit/leafDigest single domain domLeaf, World.trie, entry/live/taken/isSpent
  take E, chainNext root', chainOf over (turn,root), commitTrie), Bounds.trieDepth=257, Receive Call (pinned E)/
  Derive/Follow (founderEntries), Proofs Admit/Fold (chain_binds over pairs, fold_reaches_host)/Equiv (trie =)/
  Frame/Origin/Receive/RootedDeployed ported and green; Proofs/TrieMap (sum lemmas, build_perm, eq_of_get_eq,
  shallow_of_shape) + Proofs/Cells (Canon preserved, slots_separate, slot_inclusion/exclusion_sound,
  head_read_sound, trie_ext, prove_verifies/absent) green. Sim: checkRoot per admitted turn (replay inserts →
  root, prove/verify, 4 forged-proof arms in plantedArms), follower-root check, reopen by Trie.build; WASTE
  hashes-per-touched-cell 9.985 (1.92 of it = uncached emptyHash: NEXT CUT), hashes-per-nullifier 2.695.
  kernel-sim --seeds 64 ALL PASS admitted=3069 (unchanged). Codec/World.lean is MY PLACEHOLDER (v3, world takes E)
  — CODEC-2 replaces it + Codec/Proofs/World; Codec/Deployed one-line (world env digestCodec).
  KERNEL-29 decision appended to wt/kernel decisions/kernel.md (not landed).
  A helper subagent (ad4b1716c42d6cef5) is porting Proofs Weight/Value/Ledger/Rooted + other layers' call sites
  in wt/kernel; DO NOT build in wt/kernel while it runs. It reports statement changes old→new: READ THEM.
- Promised, after the port: KERNEL-30 carry (OPS-P1, agreed with OPS-2 + PROTOCOL-6 option A: Carried = {trie,
  allowance, height, in-window journal}; origin over root+allowance+height+journal digest, one domain w/ kind byte;
  carry_carried, carry_canon, carry_lookup, carry_origin_ne_genesis); KERNEL-31 CODEC-2's genesis finding
  (Receive.genesis → Except GenesisRefusal over decidable genesisFits; genesis_ok → GenesisFits; tooth: founder key
  eventBytesMax+1 refused by name); cached emptyHash.
- LEDGER-2: D5b/D5c WAIT for the port (told). ROOT agreed order D5a → port → D5b/c → LANG-5 (a0ace030eb5525250).
- 10-17 ~17:10Z VACUITY READ (second agent) of my port: OK except (1) hcb/ht premises FALSE for Deployed.env
  (cellBytes/turnBytes injective only on Cell.Fits / checkBounds-passing turns). FIXED IN SCRATCH (not yet pushed:
  scratchpad/k6/Kernel/Proofs/{Cells,Fold}.lean, Kernel/Sim/Gen.lean — push AFTER the helper finishes): soundness
  theorems take `InjOn F E`, `w.Fits F E`, `l.Fits F`; new head_root, head_absent_sound; fold_chain now also says
  `l ≠ [] → rs.getLast? = some (w'.root E)`; Sim arms proof-stale, proof-overlong, proof-spent-empty added.
  OPEN: `ht` (turnBytes) premise on chain_binds/fold_head_binds/fold_reaches_host (pre-existing on main) → restate
  over checkBounds-passing turns (CODEC: turnBytes_injective needs checkBounds both sides, Codec/Proofs/Kernel:340);
  admit_fits (postWrite checks slot count; creates via checkBounds_fits) + deployed instance theorem in
  Codec/Proofs/Deployed — land with KERNEL-31 (genesisFits). (2) ofWire Canon gap → CODEC-2's world_decode_canon
  (leaf-fit + trie-order refines) in its v3 handoff (files to arrive by path in hbox logs/ incl. Host/Sim/Toy:58,
  Protocol/Rows/Sim:34).
- LEDGER-2 D5b statements read: OK (held until port lands).

### KERNEL-6 HANDOFF (written 2026-10-17 ~17:50Z at ~315K tokens; NOTHING of the port is landed)
STATE: hbox wt/kernel holds the WHOLE port, uncommitted, base main 1d326dd (contains D5a 5b87949). Snapshot:
/tank/dregg-build/nanodregg/logs/kernel6-r3.patch (tracked, 33 files) + logs/kernel6-r2-untracked/Kernel/Proofs/
{Cells,TrieMap}.lean (also live in the worktree). Rebase helper: logs/kernel6-rebase.sh NAME (fails loudly; resolve
conflicts by script, then grep markers).
GREEN in wt/kernel: every Kernel module except Kernel.Proofs.RootedDeployed (red ONLY through its import of
Codec.Proofs.World). kernel-sim --seeds 64 (deployed) ALL PASS admitted=3069 refused-as-expected=20974 restarts=962;
WASTE admit hashes-per-touched-cell 9.985, admit hashes-per-nullifier 2.695 (cells-touched 1.000, fold 2.000
unchanged). Full-tree reds: Codec.Proofs.World (CODEC-2's, replaced by its v3), Host.Page (+ its unbuilt
downstream: Host/Sim/{MemStore,Run}, Host/Proofs/{Names,Page}, Host/Exit, Host/Deployed, Protocol/Rows/Writer).
WHAT THE PORT IS: decisions/kernel.md KERNEL-29 (appended in wt, not landed) — read it; it also says what re-emits /
re-geneses / refuses (World codec v3, every v2 base refuses via HOST's stamp; every chain after height 0 changes ⇒
re-genesis; Turn/Call codecs unchanged).
Invariants carried as premises: World.Canon E (Cells.lean) and World.Slotted E (Frame.lean; was the helper's
World.Fits, renamed by me to avoid CODEC's Codec World.Fits). Soundness theorems take InjOn F E / CellsFit / CellFit.
The helper (ad4b1716c42d6cef5) ported Weight/Value/Ledger/Rooted + mechanical call sites in Protocol/Ops/Hosting/Lang/
Host/Sim/Toy; its full statement-change list is in its report — every change was premise-adding (Canon/Slotted/
Routed, satisfiable: genesis_*/admit_*/fold_*) or E-threading; born_sum's premise got WEAKER (stronger theorem).
A SECOND vacuity read of the helper's restatements has NOT been done: do it (spawn a reader on Weight/Value/Ledger/
Rooted vs main) before landing.

TO LAND (KERNEL-7), in order:
1. HOST-6 decides Host/Page walkTurns + Host/Sim/Run chainOf (needs roots: options (a) record carries per-turn root,
   (b) re-admit, (c) end-chain only — asked 17:45Z). Take its edits as files.
2. CODEC-2's v3: hbox logs/codec2-trie/ {Codec/World, Codec/Proofs/World, Codec/Proofs/Deployed} (built vs r1; told
   to rebuild vs r3 and resolve the World.Fits/Slotted name clash + state world_decode_slotted; drop its consumers.patch,
   r3 already has those one-word edits). Replace MY placeholder Codec/World.lean wholesale.
3. Full `swarm-build lake build` green; kernel-sim 64; hosting-sim, lang-journey, host-sim, host-file-sim,
   store-plants, rows (filtered per gates/runs.tsv) — or let scripts/commit judge.
4. gates/waste.tsv: add rows `admit hashes-per-touched-cell 9.985` and `admit hashes-per-nullifier 2.695` (rebase the
   file on main's copy first; commit message needs WASTE:/SIZE: lines for new rows/counts).
5. scripts/commit -F msg --cross-layer "KERNEL-23 flag day agreed with CODEC-2 and HOST-6; mechanical E-threading in
   Protocol/Ops/Hosting/Lang" with subject `kernel!: …`; message states the flag day (from KERNEL-29).
6. Tell: ROOT (hash + refusals + re-emits), CODEC-2 (sha; it adds the trie-order plant, records CODEC-19), HOST-6,
   PROTOCOL-6 (head record (height, prev, turnDigest, root) + read Proof), LEDGER-2 (D5b may land; rebase),
   OPS-2/CODEC-2 (Carried after KERNEL-30), LANG-5, HOSTING (reconcile gained E alongside bytesOf — theirs to merge).
AFTER THE PORT (cv tasks opened 10-17): 01a1498e-8519 emptyHash cache; -8530 ht premise over checkBounds turns;
-853e KERNEL-31 genesisFits refusal + admit_cellsFit + deployed instance theorem; -854c weights = codec numbers
(CODEC-2 measured logWeight 16+ bytes short; I chose codec numbers); -855a KERNEL-30 carry (agreed shape above).
Also pending review: LEDGER-8 (D5c shape, decisions/ledger.md on main 56ff26f) — I did not read it.
- 17:55Z HOST-6 DECIDED (HOST-29): option (a) amended — batch record = List (Turn D × D) (turn, root after it), the
  separate end chain DELETED; open asserts fold's chain = chainOf E w.chain pairs (chainMismatch); page walk uses
  stated roots; Host.Machine gains `note : W → N` (deployed World.root). Host-only diff will be at hbox
  logs/host6-kernel23.patch (built on kernel6-r3 + r2-untracked). Its ask: keep `World.root E w` public and O(1)
  (it is: the trie's cached hashOf). Blocker 1 is thus resolved once that patch arrives.
- 18:00Z HOSTING-2 (a357cdb9a860f3cde) ask for KERNEL-7, land WITH or right after the port: `fold_frame : World.fold E w ts =
  .ok w' → c ∉ ts.flatMap (fun t => t.touches.map (·.cell) ++ createdIds t) → w'.entry E c = w.entry E c` (induction
  over fold_cons_ok + admit_frame, which already states this per turn; hl is weaker-than-needed since any touch of c
  excludes c). Send HOSTING-2 the sha. Its `Loop.allIds w := w.cells.keys` becomes the cell slots of w.trie.toList
  (told it; O(store), fine off the request path only).

## KERNEL-7 (successor of KERNEL-6; started 2026-10-17; hbox wt/kernel)
- Rebased the port onto main 4777611 (HOSTING-10 etc.) via logs/kernel6-rebase.sh k7r4; conflicts in Hosting/{Controller,Proofs/Controller}
  resolved by logs/kernel7-resolve1.py (E + Bounds.grainsMax). New Hosting.Loop (HOSTING-10) E-threaded (logs/kernel7-loop.py,
  kernel7-ctl.py): qualifies/prune/step take E; Cli passes Host.Deployed.X.env. NEW `World.cellIds` (cell slot ids, live+tomb,
  trie order) replaces `w.cells.keys` (Loop.allIds). Snapshot logs/kernel7-r4.patch + kernel7-r4-untracked/.
- CODEC-2 retired; CODEC-3 = a5c03e9649c328e52 owns logs/codec2-trie-r3/ (copied in unchanged; Codec.Proofs.World green on r4).
- HOST-6 (HOST-29): Host side goes IN my flag-day commit (patch at logs/host6-kernel23.patch, vs r4). I approved its generic
  `Rooted admit note` in Kernel/World.lean + `World.RootedFold E` + Kernel/Proofs/RootedFold.lean (fold, chain); asked tooth:
  flipped stated root ⇒ chainMismatch plant.
- Build on r4 + codec v3: everything green except Host.Record (batch shape: HOST-6's patch). kernel-sim --seeds 64 ALL PASS
  admitted=3069 refused-as-expected=20974 restarts=962; WASTE 1.000 / 2.000 / 9.985 / 2.695 (unchanged from KERNEL-6).
- Vacuity reviewer (read-only) spawned on Weight/Value/Ledger/Rooted + every turnBytes-injectivity consumer.
- 18:20Z HOST-6 READY: its Host side of HOST-29 is at hbox /tank/dregg-build/nanodregg/logs/host6-kernel23.patch (built on
  kernel6-r3 + r2-untracked; wt/host holds it uncommitted — do not commit from wt/host). It includes TWO Kernel
  additions that KERNEL-7 must READ for vacuity before landing. Its rows count on the ported tree: 15 ROW PASS (incl.
  lang-journey), 3 PENDING (pay/well/bounty, LEDGER), 0 FAIL. PROTOCOL-6 accepted HOST-29's Protocol part, which lands
  in the same flag-day commit. Blocker 1 RESOLVED; remaining: CODEC-2 rebuild vs r3, vacuity read of the helper's
  Weight/Value/Ledger/Rooted restatements and of HOST-6's two Kernel additions.
- Vacuity read DONE (agent ad13ea6eb0480379f): Weight/Value/Ledger/Rooted OK (no weakened conclusion, no P→P; born_sum incomparable:
  weaker freshness + Routed added). FIXED: turnBytes premise → `TurnBytesInjOn E` (bounded turns) in chainNext_inj/chain_binds/
  fold_head_binds/fold_reaches_host + admit_bounded/fold_bounded + Receive.deployed_fold_reaches_host (all premises discharged at
  deployed). OPEN, named in decisions KERNEL-30 (b) + Cells docstring: CellsFit Cell.Fits undischarged (KERNEL-31, cv -853e).
- Numbering: port = KERNEL-30 (carry stays KERNEL-29 as ops.md/protocol.md cite; genesisFits KERNEL-31).
- HOST-6 patch applied (Rooted/RootedFold read OK; plant-flip-root); my fix Hosting/Cli touchedIds map Prod.fst.
- FULL TREE GREEN 350/350; kernel-sim 64 ALL PASS 3069; host/host-file/hosting-sim 1-3 ALL PASS; lang-journey GREEN; store-plants
  ALL PASS; rows 3 pending 0 FAIL. Snapshot logs/kernel7-r5.patch + kernel7-r5-untracked/; msg logs/kernel7-msg.txt.
  Awaiting CODEC-3 review OK, HOSTING-2/LANG-5/OPS-2 no-objection; then scripts/commit -F logs/kernel7-msg.txt --cross-layer ... PATHS.
- LEDGER-2 D5b/D5c ready in wt/ledger; review D5c statements in its REBASED tree after the port lands.
- ⚑ LANDED 7c43273 `kernel!` (PRE-PUSH GREEN, pushed): World port = KERNEL-30 + HOST-29 + CODEC-19 v3, rebased on ca798ba.
  C3 gate refused Prop defs in Kernel/World.lean → `Rooted`/`World.RootedFold` moved to Kernel/Proofs/RootedFold.lean.
  Told ROOT, LEDGER-2 (D5b may land; D5c review in its rebased tree), CODEC-3 (yes to world_decode_cellsFit at F=Cell.Fits), HOST-6,
  PROTOCOL-6, HOSTING-3 a514a92b544a85557, OPS-2, LANG-6 a0e14827e8b076d95. cv 01a1498e-8530 closed.
  NEXT: D5c review; KERNEL-31 (genesisFits refusal + admit_cellsFit + deployed instance; cv -853e); weights (-854c); KERNEL-29 carry
  (-855a, agreed shape incl. in-window journal, height carries; message OPS-2 + CODEC-3 before landing); emptyHash cache (-8519).
- KERNEL-31 HELPER spawned (agent a8557317df17183d9) in hbox wt/kernel (DO NOT BUILD THERE WHILE IT RUNS): genesis → Except
  GenesisRefusal (genesisWorld = builder; genesis_ok ↔), every caller ported (Host/Cli prints refusal; Ops/Protocol/Lang/Hosting
  sims), sim arm founder key eventBytesMax+1; CellsFit at Codec's Cell.Fits (ONE predicate) genesis/admit/fold_cellsFit + deployed
  head_read_sound; decisions KERNEL-31. Reports statements old→new + snapshot logs/kernel31-final.patch. I read & land.
- D5b landed e8077f8 (LEDGER-2). D5c statements READ & OK'd (invoke_ok/effect_as_signed/tree_all/derive_all/invoke_records/Grows/
  visit_distinct/tree_pool); non-blocking ask: tick exactness `poolOf body - r.2.pool = Σ used` (LEDGER-2 to do or cv task).
- KERNEL-31 helper DONE: logs/kernel31-final.patch (base 7c43273) + untracked Kernel/Proofs/CellsFit.lean (copy it out of wt/kernel
  before rebasing!). genesis → Except GenesisRefusal, genesisWorld, genesis_ok ↔; CellsFit at Codec Cell.Fits: genesis/admit/
  fold_cellsFit; deployed_reach, deployed_{slot,live}_inclusion_sound, deployed_head_read_sound(_from); arm
  genesis-founder-key:founderKeyTooLong; kernel-sim 3069 ALL PASS refused-as-expected=21038. Asked agreement: HOST-6, OPS-2,
  PROTOCOL-6, LANG-6, HOSTING-3. Land AFTER D5c lands (rebase).
- QUEUED (agreed with CODEC-3): `Env.Lawful E n` structure {size, n_le, bytes_inj, turnBytes_injOn, cellBytes_injOn} in a Kernel proof
  module; theorems take hE; Deployed proves env_lawful. After KERNEL-31 + weights.
- WEIGHTS plan (cv -854c): codec sizes at 32-byte digests: Cell.weight 9+Slots.weight (kind4+disc1+hdr4); Op.weight set 9+v / erase 5
  (tag1); write act +4 (list hdr); logWeight +16 (4 list/bytes hdrs: touches, creates, nullifiers, event). Fix Admit.lean:90 docblock.
  Then CODEC proves (turn dc).size t = t.logWeight.
- ⚑ LANDED 2618fe3 `kernel!` KERNEL-31 (PRE-PUSH GREEN, pushed), on e15813f, + `deployed_head_read_sound_decoded` (reopened base via
  world_decode_canon/cellsFit). kernel-sim 64 ALL PASS admitted=3050 (main's count after D5b) refused-as-expected=20992 restarts=954;
  WASTE admit 9.898 / 2.666 (below ceilings 9.985 / 2.695 — a later commit may lower them). cv -853e closed. hlf (claimed leaf
  Cell.Fits) = CLIENT's duty (PROTOCOL-6 filed cv 01a149bf-8b34 + CLIENT-LOG.md).

### KERNEL-7 HANDOFF (written 2026-10-17 at ~305K tokens; NOTHING unlanded; wt/kernel clean at 2618fe3)
Landed by me: 7c43273 (World port = KERNEL-30 + HOST-29 + CODEC-19 v3), 2618fe3 (KERNEL-31).
Pending on others: LEDGER-2 lands D5c (statements OK'd by me; rebasing onto 2618fe3; non-blocking ask: tick exactness
`poolOf body - r.2.pool = Σ used`). Then LANG-6's post-D5 lang! day.
NEXT for KERNEL-8, in order:
1. Turn weights = codec numbers (cv 01a1498e-854c). Plan, computed from Codec/Kernel.lean + Codec/Raw.lean at 32-byte digests:
   Cell.weight := 9 + Slots.weight (kind nat32 4 + discipline 1 + slots list hdr 4); Op.weight set := 9 + v.size (tag 1 + key 4 +
   len 4), erase := 5; a write act costs +4 (ops list hdr) — add it in Touch.weight's act part, not in growth; Turn.logWeight +16
   (list/bytes headers: touches, creates, nullifiers, event). Check `choice`'s tag is 1 byte (Codec/Stream). Fix
   Kernel/Proofs/Admit.lean:90 docblock (claims size ≤ logWeight with no theorem). Measure everything that moves (WASTE/SIZE lines).
   Then send the sha to the CODEC owner (CODEC-3 a5c03e9649c328e52 or its successor): it proves `(turn dc).size t = t.logWeight`.
   Cell.weight also prices storage (cellsWeight), so a cell's World weight becomes its codec bytes too: say so in the flag day.
2. KERNEL-29 carry (cv -855a): Carried = {trie, allowance, height, in-window journal} (PROTOCOL-29's journal ⇒ height carries;
   OPS-P1 at proposals/ops.md 7f7b6da; KERNEL-6's accepted shape). Message OPS-2 a493aca8608fbc234 + CODEC owner BEFORE landing;
   CODEC-22 needs Carried's sha. Theorems promised: carry_carried, carry_canon, carry_lookup, carry_origin_ne_genesis.
3. emptyHash cache (cv -8519): 1.92 of the ~9.9 hashes-per-touched-cell; WASTE row falls (count, never a clock).
4. Env.Lawful (agreed with CODEC-3): `structure Env.Lawful (E : Env D) (n : Nat) : Prop` {size, n_le, bytes_inj, turnBytes_injOn,
   cellBytes_injOn (InjOn Cell.Fits E)} in a Kernel proof module importing Codec.Proofs.Kernel; theorems take `hE : E.Lawful n`;
   Deployed proves env_lawful : env.Lawful 32. Replaces loose hsz/hb/ht/hcb premises.
5. Old opens: stale_named names only the first failing touch; a revoked carved grant doesn't return its unspent enrol count;
   cv 01a14938 amount-bounded right.
Working notes: logs/kernel6-rebase.sh NAME (fails loudly; untracked files survive; for a 3-way apply onto a dirty tree `git add -u`
first, then `git reset`). Gate C3: Prop-valued defs only in Proofs modules. Landing script pattern: logs/kernel7-land31.sh
(paths = git diff names + untracked; --cross-layer text from a file). Verdict set: logs/kernel7-runs.sh (edit its fresh dir name:
store-plants refuses an existing dir). Wrap ssh long jobs as `cd …; nohup … < /dev/null & echo $! > pid` (never `cd && nohup …&`,
which records the subshell's PID and hangs ssh).
Roles now: CODEC-3 a5c03e9649c328e52 (handing off soon), HOST-6 a59922b2afa99acbc, PROTOCOL-6 abd8f012f13228e0b, OPS-2
a493aca8608fbc234, LEDGER-2 afd32f4b9d6e68d3e, LANG-6 a0e14827e8b076d95, HOSTING-3 a514a92b544a85557.
- (post-handoff) LEDGER-2 D5c: rebased on 5105d8b, green; waits for KERNEL-8's rebase confirmation (logs/ledger2-msg-d5c.txt). KERNEL-7
  ACCEPTED its re-pin of `admit hashes-per-nullifier` 2.695 → 3.634 (new sim arm adds a once-key nullifier per seed into a tiny
  nullifier subtree; control without the key 2.666); asked for the control in the WASTE: line. KERNEL-8 TODO: normalise that row by
  path depth so workload stops moving it. Tick-exactness ask is cv 01a14a03.

## KERNEL-8 (successor of KERNEL-7; started 2026-10-17 ~21:40Z; hbox wt/kernel)
- HOST is now HOST-7 ae95b4547c42ba031 (ROOT): KERNEL-29 carry sha goes there.
- D5c (LEDGER-2, wt/ledger on 5105d8b) CONFIRMED by me: statements unchanged from KERNEL-7's read, only premise derive_born hinj
  discharged at Deployed; 9 new plantedArms; waste hashes-per-nullifier re-pin 2.695 -> 3.634 accepted on its control (asked
  to rewrite the row's source text). LEDGER-2 lands; tick-exactness = its cv task.
- WEIGHTS (KERNEL-32) built in wt/kernel, NOT landed (waiting for D5c to land, then rebase over its Gen.lean):
  Cell.weight 9+, Op.weight 9+v/5, Act.logWeight (1 tag + 4 hdr + ops for write), headerWeight 4 x4 in logWeight; Weight.lean:48
  set case fixed; Admit.lean docblock; Gen.checkLogWeight (record bytes = logWeight at 32-byte digest; 3050/3050; mutation
  headerWeight:=3 fails 0/117). decisions KERNEL-32 appended. Patch logs/kernel8-weights.patch (pre-decision snapshot).
  After landing: tell CODEC-4 aaba467e9c60e21bc the sha.
- ⚑ LANDED e06f8b6 `kernel!` KERNEL-32 (weights = codec bytes; PRE-PUSH GREEN, pushed; needed SIZE: lines for Kernel/deployed/
  tooling line counts). Told CODEC-4 (proves turn.size = logWeight), ROOT. CODEC-4 landed leaf_decode_cellFit (ee49de8):
  TODO deployed_head_read_sound_bytes (leaf.decode b = .ok leaf, hlf := (leaf_decode_cellFit hd).1; CLIENT-16).
- ROOT/HOST-7 item: journal never pruned (law 4). I put the PRUNE (KERNEL-33) BEFORE KERNEL-29. Design sent to ROOT, HOST-7,
  PROTOCOL-6: prune every W=windowMax heights keeping H < h+2W (bound < 3W, distinct heights); checkWindow BEFORE checkJournal
  (verdict independent of prune); journal out of World.weight/growth; Host lookup `expired` while H < nb+2W else new
  `forgotten`. Ruling asked: bare-admit at-most-once weakens to ">= 2W apart"; at-most-once kept at Receive (txId=H(call)).
- Roles: HOST-7 ae95b4547c42ba031, LANG-7 ac6dbe9957c6ff484 (lang! post-D5 day; agree kernel signatures with me).
- KERNEL-33 (journal prune) BUILT in wt/kernel on f4b00a2, full tree green (384), kernel-sim 64 ALL PASS (refused 25117),
  host/host-file/hosting-sim 1-3, lang-journey, store-plants ALL PASS, rows 1 pending (bounty). ROOT APPROVED design incl.
  order. Files: World.lean (kept, pruneJournal, journalForgets, window-before-journal, weight w/o journal), Turn.lean growth,
  Proofs/{Admit (pruneJournal_get, replay_named takes hw), Equiv (pruneJournal_equiv), Fold, Weight, Journal.lean NEW},
  Host/Serve + Proofs/Serve (forgotten = uncertain "forgotten"; cross-layer, HOST-8 a7b51f5a41be70521 told), Gen probeJournal
  (4 arms), waste rows journal-entries-per-window 2.999 / journal-scanned-per-turn 1.998. Mutations bite (journal-first ->
  replayed; no-op prune -> 3072). Snapshot logs/kernel8-k33-r2.patch + kernel8-Journal-r2.lean; msg kernel8-msg33.txt;
  land kernel8-land33.sh. Vacuity reviewer spawned (agent a747cddf92b28deef) — land after its read.
  CODEC-4 landed turn_size_logWeight / Deployed.turnBytes_size (3d0cc2d); Admit docblock cites it in K33.
- NEXT after K33: KERNEL-29 carry: Carried = {trie, allowance, height, journal} (journal now bounded, carried whole, PROTOCOL-6
  agreed); origin via one domOrigin over Stream.sum genesisInput carryInput (kind byte => carry_origin_ne_genesis ⇒ HashColl);
  send shas to CODEC-4 (CODEC-22) and HOST-8 (HOST-28). Then emptyHash cache, Env.Lawful, deployed_head_read_sound_bytes.
- ⚑ LANDED 17e2d3f `kernel!` KERNEL-33 journal prune (needed 8 SIZE: lines; second-agent vacuity read: no vacuity, gaps
  written into Critique; added derived_once for the follower path). Told ROOT, HOST-8 (law-6 read + expired-truth theorem),
  PROTOCOL-6 (row), CODEC-4 (World shape + planned Carried/carryInput layout).
- NOW: KERNEL-29 carry on main 17e2d3f. Tested lemmas in logs/kernel8-t2.lean (ba_append_cancel, sum_bytes_inl_on/inr_on,
  sum_inl_ne_inr) for origin tagging.
- KERNEL-29 carry BUILT in wt/kernel on 17e2d3f (full tree 388 green, all verdict exes PASS, rows 1 pending). Files:
  Bounds journalMax, World Carried+carried, Follow (domOrigin v2, carryInput, originInput=sum, carry*), Origin (genesis_inj
  via tag + sum lemmas), Proofs/Carry.lean NEW, Gen probeCarry (4 arms). Decision appended; msg logs/kernel8-msg29.txt;
  land logs/kernel8-land29.sh; snapshot kernel8-k29-r1.patch + kernel8-Carry-r1.lean. Vacuity reviewer a79da6771665ffc95.
  CODEC is now CODEC-5 afad87333c5b8a98a (send K29 sha + Env.Lawful sha). PROTOCOL-6 landed forgotten row 4c22913.
- ⚑ LANDED b8e0f82 `kernel!` KERNEL-29 carry (vacuity read: no vacuity; added carry_journal_fits, carry_fold_journal_bounded,
  replayed-height check, chain docstring). Shas sent: CODEC-5 afad87333c5b8a98a (CODEC-22), HOST-8 a7b51f5a41be70521 (HOST-28),
  OPS-2, ROOT. HOST-8 landed lookup_expired_never_committed (9dad4d2). WASTE now 9.715 / 3.451 (ids moved; ceilings kept).
- NEXT: emptyHash cut (Trie.Spec gains a cached empty digest? proofs: grep emptyHash count in Kernel/Proofs/Trie*), then
  Env.Lawful, then deployed_head_read_sound_bytes (CODEC leaf_decode_cellFit ee49de8).
- ⚑ LANDED 5652aba `kernel:` KERNEL-34 deployed_head_read_sound_bytes / _decoded_bytes (leaf.decode b = .ok lf replaces hlf;
  CODEC leaf_decode_cellFit). Told CLIENT-3.

### KERNEL-8 HANDOFF (written 2026-10-17 at ~260K tokens; NOTHING unlanded; wt/kernel clean at 5652aba)
Landed by me: e06f8b6 (KERNEL-32 weights = codec bytes), 17e2d3f (KERNEL-33 journal prune + Host forgotten arm),
b8e0f82 (KERNEL-29 carry), 5652aba (KERNEL-34 bytes-level head read). D5c reviewed, LEDGER-2 landed c3c7aa3.
Downstream told: CODEC-5 afad87333c5b8a98a builds CODEC-22 carried codec on b8e0f82 (Carried {trie, allowance, height, journal},
journal list bound Bounds.journalMax); HOST-8 a7b51f5a41be70521 builds HOST-28 export/import on b8e0f82 (carryWorld chain =
genesisChain at carried height: a carried Store audits from carryWorld); OPS-2 store-plants carry rows after those; PROTOCOL-6
landed the forgotten row 4c22913 and owes a carry row.
NEXT for KERNEL-9, in order:
1. emptyHash cut (cv 01a1498e-8519). Facts: Kernel/Trie.lean `emptyHash S := S.hash (tagged 0 empty)`, recomputed by
   `T.hashOf .empty` inside every mkNode with an empty child; sim counts it in Gen.insertHashes (`empties`). Kernel/Proofs/Trie.lean
   (730 lines) never names emptyHash but its climb_sound etc. rely on hashOf .empty unfolding to S.hash (tagged 0 ..) (hash_tagged).
   Two designs: (a) Spec field `empty : D` + proof-side hypothesis `S.empty = S.hash (tagged 0 ByteArray.empty)` threaded like the
   existing `hL hN` variables (trieSpec discharges by rfl); (b) thread `e := emptyHash S` computed ONCE per commitTrie into
   insAt/mkNode/build (hashOf' e), with a simp lemma hashOf' (emptyHash S) = hashOf S. (a) is one shape; (b) keeps defeq. Then change
   insertHashes's model to match the code exactly (count the one empty hash per admit, not per sibling), re-pin
   `admit hashes-per-touched-cell` DOWN with the reason (expected ~9.7 -> ~8), never a clock.
2. Env.Lawful (agreed with CODEC-3; CODEC-5 proves `env_lawful : env.Lawful 32`): `structure Env.Lawful (E : Env D) (n : Nat) :
   Prop` {size : ∀ d, (E.bytes d).size = n, n_le : n ≤ 32, bytes_inj : Function.Injective E.bytes, turnBytes_injOn :
   TurnBytesInjOn E, cellBytes_injOn : InjOn Cell.Fits E} in a Kernel proof module importing Codec.Proofs.Kernel; replace loose
   premises (counted on main: 7× hsz, 6× hb Injective, 5× hcb InjOn, 4× ht TurnBytesInjOn, ~10× hinj/hb pointwise) by hE.
   This is TRANSPORT's missing step for "the signature binds the world bytes". Send CODEC-5 the sha.
3. Known gaps written in decisions: KERNEL-33 Critique (admit_prune_verdict is one prune vs unpruned, not the composition of
   all past prunes: `kept` is monotone in H, a lemma would close it; a decoded base carries no JournalOk); KERNEL-29 Critique
   (carry_inj binds the trie by root; kernel does not check fromOrigin is c's World: HOST-28's --digest does).
4. Old opens: stale_named names only the first failing touch; a revoked carved grant doesn't return its unspent enrol count;
   cv 01a14938 amount-bounded right.
Working notes: patch scripts written locally and scp'd (see logs/kernel8-*.py); land scripts logs/kernel8-land{32,33,29,34}.sh
(paths = git diff names + untracked; message file; SIZE: lines are needed for every risen size metric: Lean modules, proof-
modules, Lean lines per layer, theorems, max dependents). Verdict set: logs/kernel8-runs.sh (edit L and F dir names first).
`git apply --3way` rebase: diff to logs, `git checkout -- .`, `git checkout --detach main`, apply, `git reset`.
WASTE now: hashes-per-touched-cell 9.715, per-nullifier 3.451 (ceilings 9.985 / 3.634 kept), journal-entries-per-window
2.999, journal-scanned-per-turn 1.998.
Roles now: CODEC-5 afad87333c5b8a98a, HOST-8 a7b51f5a41be70521, PROTOCOL-6 abd8f012f13228e0b, OPS-2 a493aca8608fbc234,
LEDGER-2 afd32f4b9d6e68d3e, LANG-7 ac6dbe9957c6ff484, CLIENT-3 aae5c92a4d1999133, HOSTING-3 a514a92b544a85557.

## KERNEL-9 (successor of KERNEL-8; started 2026-10-18 ~03:35Z; hbox wt/kernel)
- ⚑ LANDED 4720fa4 `kernel:` KERNEL-35 emptyHash cut, design (b) LAZY: trailing optional
  `e : Trie.EmptyDigest D := Thunk.mk fun _ => emptyHash S` on T.hashOf/mkNode/build/insAt/proveAt/T.insert/T.prove
  and World.insertAll/spendAll; commitTrie makes one lazy copy per turn. ZERO proof lines changed (statements elaborate
  to the same default). Strict variant measured 9.166, lazy 8.915. Rows 9.715->8.915, 3.451->3.211 (ceilings lowered).
  Mutation wrong e: sim 64/64 red + Kernel.Proofs.Frame stops compiling. No wire change. CODEC-5 told (no action).
- ROOT ruling: rows must be INSTRUMENTS. ⚑ LANDED d91e720 `kernel:` KERNEL-36: Sim.countingEnv marks trie-domain
  hashes with dbgTrace "#" (unsafe is refused, extern needs native-allow; dbgTrace is safe + never_extract); report
  captures stderr per seed (IO.setStderr buffer + IO.lazyPure); countTurn brackets REAL World.admit (<A), REAL commitTrie
  without nullifiers (<C), plantCommitPerInsert (<P); insertHashes DELETED. Counted = 8.915/3.211 (= the model).
  Arm hash-count:empty-per-insert in plantedArms. Mutation (insertAll ignoring e): 9.006 + sim FAIL. Probe file
  hbox logs/kernel9-probe/P.lean.
- LEDGER-3 (cv 01a14a03 ticks spent = pool deducted): AGREED close as "per-step exactness (invoke_ok) is the statement",
  reopen trigger = first consumer reading the deficit; LEDGER-3 closes it. Its escrow landing touches no Kernel/ path.
- NEXT: Env.Lawful (item 2), then the KERNEL-33/29 critique gaps (item 3).
- ⚑ LANDED 62ef047 `kernel:` KERNEL-37 Env.Lawful (Kernel/Proofs/Lawful.lean; TurnBytesInjOn + InjOn moved there);
  24 theorems in Fold/Cells/Rooted/Origin/Carry take hE; Receive.deployed_lawful : env.Lawful 32 in RootedDeployed
  (CODEC-5 told: no env_lawful needed). Env.Lawful.refutable = the refutation tooth. Vacuity reviewer: no vacuity,
  generic-level weakening only. PROTOCOL-6 told (its protocol.md gap now closable). LEDGER-3 asked to convert
  Value.lean:624/654/672 + Ledger.lean:247 pointwise hinj/hb.
- NEXT (item 3): KERNEL-33 critique (a) composition of prunes: prove verdict unchanged under any list of prunes at
  heights <= w.height, by induction on admit_prune_verdict (pruned entries are a subset with the same values, so hv
  transfers). (b) decoded base has no JournalOk: options = Codec world decoder refuses a journal violating
  JournalOk's shape (cross-layer CODEC-5), or a kernel check at reopen. Then old opens (stale_named first touch only;
  revoked carved grant count; cv 01a14938 amount-bounded right).
- KERNEL-38 attempt REJECTED by its own vacuity read (not landed; patch hbox logs/kernel9-k38-rejected.patch):
  `admit_prunes_verdict` (a list of prunes of ONE fixed journal) collapses to one prune (kept is antitone in H) and
  never matches a real fold, which interleaves insert-then-prune each turn. Do NOT land it as "closing" KERNEL-33 (a).
- PROTOCOL-6 already used Env.Lawful: f246af0 Envelope.message_inj / deployed_message_inj (PROTOCOL-29 gap closed).

### KERNEL-9 HANDOFF (written 2026-10-18 at ~320K tokens; NOTHING unlanded; wt/kernel clean, detached at main f246af0)
Landed by me: 4720fa4 (KERNEL-35 lazy empty digest), d91e720 (KERNEL-36 counted hash rows, ROOT ruling),
62ef047 (KERNEL-37 Env.Lawful + deployed_lawful). Told: ROOT, CODEC-5 (env_lawful struck; CODEC-5 has since retired at
~300K, CODEC-LOG ## CODEC-5 HANDOFF), PROTOCOL-6 (done f246af0), LEDGER-3 (convert Value.lean:624/654/672 and
Ledger.lean:247 pointwise `hinj`/`hb` to hE; cv 01a14a03 agreed closed as per-step exactness, LEDGER-3 closes).
WASTE now (COUNTED by Sim.countingEnv): hashes-per-touched-cell 8.915 (floor 0.640 = one empty digest per turn),
hashes-per-nullifier 3.211; plant arm hash-count:empty-per-insert; journal rows 2.999 / 1.998.
NEXT for KERNEL-10, in order:
1. KERNEL-33 critique (a), the REAL statement (reviewer's design, agreed): a shadow fold that never prunes
   (commit with journal := insert only; a spec def in a proof module, named as such), then
   fold_journal_filter: real fold w and shadow wF agree on every field but the journal, and
   w.journal = wF.journal.filter (kept Hlast), Hlast = the last multiple of windowMax ≤ w.height (needs the CONVERSE
   of pruneJournal_sub: kept entries survive; entries inserted after Hlast have e.1 > Hlast so are kept); then
   fold_prune_verdict by admit_prune_verdict at H := Hlast. Tooth: the K33 mutation (journal-first) + a mutation
   that prunes at every height (must break fold_journal_filter's Hlast).
2. KERNEL-33 critique (b): a decoded base carries no JournalOk. Design: kernel `World.journalOkB : Bool` +
   `journalOk_of_check`, and CODEC's world decoder refuses a base whose journal fails it (cross-layer: CODEC's
   successor agrees first; the decoder already bounds length by Bounds.journalMax). Why: a future-height entry is
   never pruned and answers `replayed` forever.
3. KERNEL-29 critique (carry_inj binds the trie by root; HOST-28's --digest checks fromOrigin; HOST-8 landed
   HOST-28/34 6b89d6f). Old opens: stale_named names only the first failing touch; a revoked carved grant does not
   return its unspent enrol count; cv 01a14938 amount-bounded right.
Working notes: patch scripts written locally then scp'd (logs/kernel9-p*.py); land = scripts/commit -F msg with
SIZE: lines for each risen metric (Lean lines Kernel/deployed/tooling, modules, proof-modules, theorems, max
dependents) and CROSS-LAYER for gates/waste.tsv; on "behind main": git diff > logs, checkout --, checkout --detach
main, git apply --3way, git reset. Lean: a structurally recursive theorem with params before the colon needs them
(and implicit E) passed explicitly in the recursive call. dbgTrace + IO.setStderr is the safe way to count pure calls.
Roles: ROOT main; LEDGER-3 a11788b66fe43f571; PROTOCOL-6 abd8f012f13228e0b; HOST-8 a7b51f5a41be70521;
CODEC-6 a7dcb3be86813ca52 (none of KERNEL-35..37 changes wire bytes; item 2 needs its agreement).
- LEDGER-3 converted Value.lean/Ledger.lean/LedgerDeployed to hE at fa390f7; reviewed OK by KERNEL-9 (premise-only change, conclusions unchanged). Kernel/ has ONE Env premise shape now.

## KERNEL-10 (successor of KERNEL-9; started 2026-10-18; hbox wt/kernel)
- main was eddcc5e at start (PROTOCOL-35 carry row; 20/20 rows). LEDGER-3: no open Kernel/ ask (fa390f7 reviewed by K9).
- ROOT queued (after the two journal items): carried members keep ids derived from the OLD origin; decide WITH PROTOCOL-6
  abd8f012f13228e0b: re-key at carry (+ authority-unchanged theorem) vs opacity rule (+ theorem nothing in receive reads
  origin out of an id). Argue in decisions/kernel.md; a defect only if a consumer reads origin out of an id.
- KERNEL-38 BUILT in wt/kernel (not landed yet): Kernel/Sim/Shadow.lean NEW (lastPrune, shadowJournal: spec, tooling
  because C3 forbids non-Prop defs in proof-modules and C4 forbids sim importing proofs); Proofs/Journal.lean:
  check_prune (core of admit_prune_verdict, which is now its corollary), JournalFiltered, commit_filtered,
  fold_journal_filter (induction tactic: the recursive-term form hit "Argument w was already set"), check_journal_congr,
  fold_prune_check, Receive.reach_prune_check; Gen probeJournal 5 arms journal-shadow*. Mutation prune-every-height:
  ONLY journal-shadow:filtered catches it (K33 probes blind). sim 64 ALL PASS, rows unchanged. Decision KERNEL-38
  appended + K33 critique line. Patch hbox logs/kernel10-k38-r1.patch. Vacuity reviewer a2d21fe78ee402a3b running.
- Item 2 finding: the WORLD codec bounds the journal by worldMax (2^32-1), not journalMax (that is the carried codec).
- ⚑ LANDED f6b6b60 `kernel:` KERNEL-38 (vacuity read LAND; wording fixed; 2 weak arms dropped; cv 01a14a8a-7364 = discharge hv
  on Honest logs). Lesson: SIZE label must be the exact metric name, e.g. 'Lean lines (tooling: Sim, Rows, Journey, Census, Emit, Ops)'.
  scripts/commit via `ssh hbox '(nohup … < /dev/null & echo $! > pid); wait loop'` returns cleanly.
- KERNEL-39 AGREED with CODEC-6: World shape gains refine `kernel/journal`; journal list bound journalMax; CodecFits gains
  journalFits conjunct; CODEC writes world_decode_journalOk + deployed corollary (NO Kernel deployed_base_journalOk: twin);
  CODEC also renames kernel/world/v3→kernel/world etc (CODEC-28). KERNEL half BUILT in wt/kernel: World.lean ascendingNat,
  journalFits; Journal.lean journalOk_of_fits, journalFits_of_ok, journalFits_future/_twice, eq_of_nodup_map; sim arm
  journal-fits:misfit; decision KERNEL-39. Patch logs/kernel10-k39-r1.patch. Vacuity reader a2d21fe78ee402a3b (resumed).
  After landing: send sha to CODEC-6.
- Carried ids (ROOT item): proposed OPACITY to PROTOCOL-6 (KERNEL-40): receive_origin_blind, admit_origin_blind,
  carry_rooted (+ deployed: rooted at FIRST genesis's founder grants after carry+audit). Only Derive.lean:341 reads origin;
  World grants target worldId X (Ctx constant). Ops/Founder.create recomputes founderId from w.origin (names nobody after a
  carry; plants use createAs; docstring says so).
- ⚑ LANDED 129bb73 `kernel:` KERNEL-39 journalFits (+ stale refutation per reviewer). Sha sent to CODEC-6 with the obligation:
  world_decode_journalOk must check journalFits on (ofWire x).journal.toList (ascending keys → toList_ofList_of_sorted).
- KERNEL-40 (opacity) AGREED by PROTOCOL-6, which fixed the one latent reader (Loopback.freshActor, 4147b9b PROTOCOL-36).
  BUILT in wt/kernel: Carry.lean receive_origin_blind, receive_named, carry_receive, check_origin_blind (rfl), carry_check;
  NEW Proofs/CarryRooted.lean carry_rooted, deployed_carry_rooted. Mutation carry trie:=.empty: proofs + sim red.
  Decision appended. Patch logs/kernel10-k40-r1.patch. Vacuity read requested (a2d21fe78ee402a3b). After landing: send
  statements to PROTOCOL-6.
- ⚑ LANDED b5e4246 `kernel:` KERNEL-40 opacity (receive_reorigin replaced the weak iff form per vacuity read; carry_receive,
  check_origin_blind, carry_check, CarryRooted.lean carry_rooted + deployed_carry_rooted). cv 01a14aa3-ca32 = receiveWith reads
  c.unsigned.world only through signed bytes (unproved). PROTOCOL-6 + ROOT told.

### KERNEL-10 HANDOFF (written 2026-10-18 at ~275K tokens; NOTHING unlanded; wt/kernel clean at b5e4246)
Landed by me: f6b6b60 (KERNEL-38 fold_journal_filter / fold_prune_check, shadow spec Kernel/Sim/Shadow.lean),
129bb73 (KERNEL-39 journalFits = JournalOk on a listing, exact both ways + 3 refutations), b5e4246 (KERNEL-40 opacity).
Waiting on others: CODEC-6 a7dcb3be86813ca52 lands the decoder half of KERNEL-39 (World shape refine `kernel/journal`,
journal list bound journalMax, CodecFits conjunct, world_decode_journalOk + deployed corollary; obligation: checked list IS
(ofWire x).journal.toList). NO Kernel deployed_base_journalOk (twin). When it lands, KERNEL-33 Critique's "a decoded base
carries no JournalOk" can be marked closed (one-line decision edit citing CODEC's sha).
NEXT for KERNEL-11:
1. cv 01a14a8a-7364: discharge fold_prune_check's hv on Honest logs (collision disjunct over the call codec).
2. cv 01a14aa3-ca32: receiveWith depends on c.unsigned.world only through checkSignature/callBytes.
3. Old opens: stale_named names only the first failing touch; revoked carved grant does not return unspent enrol count
   (design: refill grant); cv 01a14938 amount-bounded right; KERNEL-29 critique (fromOrigin not checked by kernel; HOST-28 does).
Working notes: write patch scripts locally, scp to logs/, run `python3 ../../logs/kernel10-pN.py` in wt/kernel (an
apostrophe or backtick inside ssh '…' breaks; hx' names too). Land: `ssh hbox 'cd wt/kernel && (nohup scripts/commit -F msg …
< /dev/null & echo $! > pid); wait loop'`. SIZE labels must match exactly: 'Lean lines (tooling: Sim, Rows, Journey, Census,
Emit, Ops)', 'max dependents of a non-foundation module'. A new proof module usually raises max dependents. Proof-modules may
not export non-Prop defs (C3) and sim can't import proofs (C4): spec defs shared by both go in a Sim module. Lean 4.30 lint:
omit unused section instances per theorem. Recursive theorem with ∀-binders after the colon: use `induction` tactic.
Vacuity reader a2d21fe78ee402a3b holds context for K38–40 (resume it for the next read).
WASTE unchanged: 8.915 / 3.211 / 2.999 / 1.998. kernel-sim new arms: journal-shadow:filtered, journal-shadow-kept:replayed,
journal-shadow-reuse:replayed, journal-fits:misfit.
- PROTOCOL-7 ab1b7e29205360b2c (replaced PROTOCOL-6) read KERNEL-40: ACCEPTED, nothing owed; row carry line 16 = runtime guard for cv 01a14aa3-ca32. Told it the journal flag day is CODEC-6's (CODEC-6 asked to send PROTOCOL-7 its sha first).
- CODEC-6 landed 9dd1e8c (decoder refuses kernel/journal; Codec.Deployed.world_decode_journalOk premise-free; /vN names dropped). ⚑ LANDED ab6974e: KERNEL-33 Critique gap (b) marked closed. CODEC note: journalFits uses List.mergeSort (well-founded), so no decide +kernel over a World decode with 2+ journal entries; a structural sort would make it kernel-reducible if ever needed.
- CODEC-7 a96227257cb8e3c92 (succ. CODEC-6): AGREED CODEC-28 step 2 bitLt_trieSpec_iff (Codec/Proofs/SlotOrder.lean): routing order = kind first, then lexicographic id bytes. CONTRACT: changing slotBit bit 0, byteBit MSB-first, or trieDepth < 8n+1 breaks it; a deliberate routing change is a kernel! landing with CODEC re-proof + vectors re-pin (tooth lsbRouting_refuted).
- CODEC-7 opened cv 01a14ac8-1db6 (assigned KERNEL, GATES-3's ask): give the journal a canonical type so World/Carried
  decode∘bytes = id (CODEC-30, decisions/codec.md; deletes both gates/refines-allow.tsv rows in that commit). NOT started by me
  (would not finish before my ceiling). KERNEL-11 ITEM 1, design first. My lead, unvetted: the journal as a THIRD Slot kind
  in the ONE existing trie (Slot.tx txId ↦ (height, turnDigest)) rather than a second Trie.T or a sorted-list subtype.
  It would be law 1 (one structure), would AUTHENTICATE the replay index under the root (KERNEL-23's "not authenticated"
  note), and canonicity would come from trie build_toList. Costs and checks: does Trie support erase (prune = W-periodic
  deletes; per-turn cost is in the hash rows, so the WASTE rows move and must be re-pinned with a reason); Slot gains a kind
  (slotBit bit 0 becomes 2 bits? CODEC-7's bitLt_trieSpec_iff contract breaks, so this is a kernel! with a CODEC re-proof +
  vectors re-pin + re-genesis); the journal proofs (Journal.lean, JournalOk over getElem?) port to trie get. Alternative: a
  sorted-list subtype (O(n) lookup, n < 3W, on every admission: priced as WASTE). Write KERNEL-41 with CRITIQUE/META
  before building; agree the Slot change with CODEC-7.

## KERNEL-11 (successor of KERNEL-10; started 2026-10-17; hbox wt/kernel)
- KERNEL-41 DESIGN written (decisions/kernel.md, also hbox logs/kernel11-k41.md): (a) the journal is the trie's third slot kind.
  ROOT APPROVED with conditions:
  - the nullifier ceiling may rise 3.211 → ~4.2, with the reason "a three-kind prefix code, paid at the least-used kind; buys plain = canonicity, one structure (law 1), and the phone's inclusion/exclusion of txIds";
  - the prune burst gets its own pinned row (hashes per prune), and NEW admit hashes-per-journal-entry ≈ 20 (insert ~17 + prune ~3);
  - `slot_prefix` + `slots_separate` over three kinds land IN THE PORT COMMIT, with a planted 10·id tx routing and a sim arm (a step-1 copy would be a twin; ROOT accepted);
  - ONE cross-layer kernel! landing with CODEC-7 a96227257cb8e3c92, HOST-10 a466e00c707f4b7be and PROTOCOL-7 ab1b7e29205360b2c; every intermediate main GREEN.
  Rejected, with the record: (b) sorted list, (c) a listing theorem, (d) Std.ExtTreeMap (cheapest; keeps two maps and the K23 gap), (e) entries under nullifier keys, (f) per-key erase.
- Shape: Slot cell|nullifier|tx (wire choice order 0,1,2); Leaf entry|spent|journal h d (0,1,2); routing cell 0·id, nullifier 10·id, tx 11·id; trieDepth 258; slotBytes kind byte 0/1/2; leafBytes (.journal h d) = 3 ‖ Codec.Stream.nat64.bytes h ‖ E.bytes d.
- CODEC-7 AGREED and asked for, in my port patch:
  (i) `Leaf.Fits (.journal h d) := h < 2^64` (its side), and a KERNEL fold theorem: every journal leaf's height ≤ w.height;
  (ii) a lemma `World.journalList w = w.trie.toList.filterMap (tx entries)` on canonical tries;
  (iii) the constructor orders above.
  CODEC also deletes ascendingList + kernel/ascending (journal-only users); kernel/journal keeps its name over the tx listing.
- cv 01a14ade-0f69 filed: the phone verifies journal inclusion/exclusion (PROTOCOL/CLIENT consumer).
- STEP 1 BUILT in wt/kernel (patch hbox logs/kernel11-step1.patch):
  - Trie.join/retainAll/retainAt;
  - Kernel/Proofs/TrieRetain.lean (9 theorems);
  - Gen probeRetain + plantRetainAll, arms retain:canonical and retain-plant:refuted;
  - sim 64 ALL PASS; mutation (no collapse) → 5 proof errors + seeds FAIL;
  - commit msg logs/kernel11-msg1.txt.
  Vacuity read requested from a2d21fe78ee402a3b.
- ⚑ LANDED a48ea4a `kernel:` KERNEL-41 step 1: Trie.join/retainAll/retainAt + Kernel/Proofs/TrieRetain.lean (9 theorems: canon_retainAt, retainAt_eq_build, get_retainAt …) + sim arms retain:canonical, retain-plant:refuted. Vacuity reader a2d21fe78ee402a3b: LAND.
- FINDING → ROOT ruled (a′); ⚑ LANDED 5da7f53 (decision only), "KERNEL-41 AMENDED" in decisions/kernel.md. Cause: in ONE trie, the prune collapse crosses kinds, so every cell reader would need Canon (~150 theorems).
  The (a′) shape:
  - the journal is a SECOND Trie.T instance (journalSpec E: byteBit of E.bytes, depth 256, domTrie nodes, domJournal leaf digest of nat64 h ‖ bytes d);
  - chainNext hashes 4 inputs (prev, turnDigest, cellsRoot′, journalRoot′);
  - the prune is retainAll (= retainAt []) at multiples of W;
  - no routing or trieDepth change, the nullifier ceiling is NOT raised, and Slot/Leaf are untouched.
  The "slot_prefix" condition is moot under (a′).
- PROTOCOL-7 ab1b7e29205360b2c builds KERNEL-42 (domCall = "nanodregg/kernel/call-signature" prefix on the call signature message; envelope_call_disjoint). I AGREED; it builds the whole edit, including Kernel files, and sends the diff for review. Conditions: the Kernel theorems keep their conclusions; a decision KERNEL-42; a plant (a call signed over bare unsignedBytes is refused, with a named arm); the flag day stated. It lands BEFORE the KERNEL-41 port.
- CODEC-7 re-briefed for (a′): the journal wire stays an ascending listing rebuilt by build; it needs a journal-trie order theorem (byte-lex = Digest compare), plain lawfulness, and deletes both allow rows. HOST-10 told.

### KERNEL-11 HANDOFF (written 2026-10-17 at ~295K tokens; NOTHING unlanded; wt/kernel clean at main 5da7f53)
Landed by me: a48ea4a (retainAt), 5da7f53 (the KERNEL-41 (a′) amendment). cv 01a14ade-0f69 filed (phone journal proofs).
NEXT for KERNEL-12, in order:
1. Review PROTOCOL-7's KERNEL-42 diff when it arrives, against the conditions above.
2. The KERNEL-41 (a′) PORT, kernel half, staged as a patch in hbox logs for CODEC-7 a96227257cb8e3c92, HOST-10 a466e00c707f4b7be and PROTOCOL-7. It lands as ONE kernel! cross-layer commit after KERNEL-42.
   Kernel edits:
   - World.lean:
     - World.journal / Carried.journal : Trie.T D (Nat × D) D;
     - journalSpec E;
     - domJournal (a new leaf domain);
     - journalAt;
     - checkJournal via journalAt;
     - pruneJournal H j := if H % W = 0 then retainAll (journalSpec E) (fun _ e => kept H e) j else j (note: it now needs E);
     - commit inserts with T.insert (journalSpec E);
     - chainNext with 4 inputs (cellsRoot′, journalRoot′), plus chainOf (it folds (turn, root) pairs → (turn, root, jroot)?);
     - genesis journal := .empty;
     - journalFits over journal.toList.
   - The Ord D requirement on World can go if nothing else uses the TreeMap: check Value/Ledger.
   - DELETE Kernel/Proofs/Equiv.lean and World.Equiv; consumers (grep Equiv) take `=`.
   - Journal.lean: port from TreeMap getElem? lemmas to Trie.get_insert (no premise) + get_retainAt (premise: Canon of the journal trie at depth 0, with Under [] = True).
     - JournalOk gains journal Canon (genesis: canon_empty; insert: canon_insert; prune: canon_retainAt with path []).
     - Theorems that read after a prune need JournalOk; check which of admit_retains / fold_retains / fold_answers / admit_spacing / admit_twice_window / submit_once / derived_once now need hw₀, and give each deployed / reached corollary with no premise (ROOT condition).
     - journal_bounded uses toList length (toList_nodup + mem_toList).
   - Rooted/RootedFold/Fold: chain lemmas over the 4-input link (fold_chain, chain_binds, fold_head_binds, Collision cases).
   - Carry.lean / Follow.lean: the carry export bytes over journal.toList (unchanged list shape); CarryFits.
   - Sim: Gen probeJournal (journal.size → toList.length; journal[k]? → journalAt), Shadow.lean (shadowJournal over Trie), countTurn: add a bracket for the journal insert and for the prune; NEW WASTE rows `admit hashes-per-journal-entry` (≈15) and a prune row (hashes per prune, or per W heights), pinned in gates/waste.tsv with the reason; check hashes-per-touched-cell / per-nullifier stay 8.915 / 3.211 (the <A minus <C share now includes the journal: subtract the journal bracket or the nullifier row moves).
   - Teeth: keep every journal-* arm name; the journal probe's real prune is the runtime tooth of retainAt at depth 0; a mutation (prune without collapse, or no prune) must go red.
   - CODEC asks: a reached-World fact that every journal height ≤ w.height (from JournalOk); state the constructor orders (unchanged now).
   - A second-agent vacuity read before landing; a2d21fe78ee402a3b holds K38–K41 context.
3. cv 01a14a8a-7364 (fold_prune_check's hv on Honest logs), cv 01a14aa3-ca32 (receiveWith reads world only through signed bytes; KERNEL-42 touches the same verify path, so do it after), and the old opens in the KERNEL-10 handoff.
Working notes:
- the land helper is hbox logs/kernel11-land.sh MSG PATHS…: it rebases on main by patch, then runs scripts/commit detached with a PID file and a 90-minute deadline;
- scripts/commit lists every SIZE line it wants on the first refusal;
- patch scripts go local → scp → `python3 ../../logs/x.py` in wt/kernel (never a heredoc inside ssh '…' with apostrophes);
- lake builds of single modules: `timeout 1500 swarm-build lake build Kernel.Proofs.X`.
- CODEC-7 (after the handoff): journal decode = the SAME generic trie-listing refine as cells (build journalSpec; accept iff toList (build l) == l && nodup); `kernel/ascending`/ascendingList DELETED (compare-order ≠ byte-order at Sim's u64). kernel/journal (journalFits) stays.
  It needs in the patch: journalSpec; journal_canon for reached Worlds; JournalOk ⊇ Canon of the journal trie; `journal_separate : Separates (journalSpec E)` — KERNEL-12 proves it in Kernel the way Cells.lean's slots_separate is proved (I told CODEC-7 the kernel provides it); vdigest spelled with Codec.Stream.nat64.bytes h ‖ E.bytes d.
- KERNEL-11 ACCEPTED PROTOCOL-7's KERNEL-42 kernel half (logs/protocol7-k42.diff; only receiveWith_sealed/receive_ok message term changed; arms sig-bare:badSignature, sig-domain:ok). PROTOCOL-7 lands it; KERNEL-12 skips item 1 of my NEXT list and rebases the port onto it.
- KERNEL-42 LANDED by PROTOCOL-7 as 1ed7867.
  - The `sig-domain:ok` arm was dropped after my review: its extra admission moved the hash counts, and every generated call is already domain-signed. `sig-bare:badSignature` stays.
  - The signature change re-draws every id. GATES-3 re-pinned admit hashes-per-touched-cell 8.915 → 8.969 and hashes-per-nullifier 3.211 → 3.336 (control: the same tree with only the domain string changed reads 9.002 / 3.413). The KERNEL-41 port's "unchanged" checks compare against 8.969 / 3.336 now, not my handoff numbers.
  - NEW cv 01a14afe-7380 (GATES-3 → KERNEL): replace both draw-sensitive rows with a ratio over the hashes the built trie REQUIRES (pinned near 1), keep the KERNEL-35 per-insert plant red by name, then delete the two rows. Best done WITH the port: it adds the journal row in the same instrument, so build it in the required-hashes form from the start.
  - Rebase the port on 1ed7867.

## KERNEL-12 (successor of KERNEL-11; started 2026-10-17; hbox wt/kernel)
- K41 (a′) KERNEL HALF BUILT, then rebased on main 0ca1ec1 and STAGED: hbox logs/kernel12-k41.patch
  (Kernel/ + decisions/kernel.md "KERNEL-41 PORTED" + gates/waste.tsv rows).
  - Scaffold, so that kernel-sim builds: logs/kernel12-codec-scaffold.patch (Codec/World.lean:
    `ofWire E`, `carriedOfWire E`, batch over (Turn, (D×D))). CODEC-7 owns it and replaces it.
  - Local scratch with git baseline: Mac scratchpad k12/ (push helper ../push.sh tars the changed
    files into wt/kernel).
- Interface:
  - `Journal D`, `journalSpec E`, `journalDigest`, domJournal, `Bounds.journalDepth` 256;
  - `World.journalAt/journalRoot/roots`, `headLink`, `chainNext E prev t (roots' : D×D)`;
  - `pruneJournal E H j` (retainAt []), `commitJournal`, `World.JournalCanon`;
  - `JournalOk E w` = Canon ∧ heights ∧ distinct.
- New theorems:
  - Admit: commit_journal, pruneJournal_get (Canon), pruneJournal_canon, admit_journalCanon,
    admit_new, commit_journalAt, admit_journaled;
  - Journal: journalAt_of_mem, fold_journalCanon, journal_heights_nodup, journal_height_le,
    check_journal_filter, absent_final (moved here, + hc), reach_journalOk, reach_submit_once,
    reach_derived_once, reach_admit_spacing;
  - Cells: journal_separate, journalBody_inj (0 < n), headLink_roots, head_roots;
  - NEW module Kernel/Proofs/JournalHead.lean: the phone's journal theorems;
  - RootedDeployed: deployed_reach_journalOk, deployed_head_journal_read/absent,
    deployed_head_absent_admitted;
  - Carry: carry_inj (listing equality), carry_inj_canon.
- Sim, 64 seeds: ALL PASS.
  - WASTE 8.969 / 3.336 unchanged; NEW hashes-per-journal-entry 13.672 (probe <K), hashes-per-prune
    539.333 (probe <R).
  - Mutations: no prune, and no collapse. Both red by name; logs kernel12-mut1/2.log.
- Partners told:
  - CODEC-7 a96227257cb8e3c92: journalFits/kernel/journal STAYS; kernel/ascending goes.
  - HOST-11 a2f74b4272ca9175d (successor of HOST-10): it carries the Hosting/Allowance and Protocol
    Command pair sites under --cross-layer. PROTOCOL-7 AGREED, with conditions: type-only, rows
    21/21 with the 7 named plants, the assembled tree's path sent to PROTOCOL-8 before landing.
- Vacuity reader spawned: a read-only general-purpose agent.
- ⚑ LANDED 5eb9b30 `kernel!` K41 (a′): ONE cross-layer commit with CODEC-7's half (CODEC-31, incl. kernel/carried-journal)
  and HOST-11's (HOST-38; it also carries the Hosting Allowance and Protocol Command/Writer pair sites, PROTOCOL-7 agreed).
  - Vacuity reads: mine (general-purpose reader, every restatement LAND; finding: no runtime tooth for the phone journal
    theorems, fixed by 4 arms journal-proof-height/admitted/stale/cells-root + head-link recompute) and HOST-11's own.
  - Mutations, all red by name and reverted: no prune (mut1), no collapse (mut2), chain commits the stale journal root (mut3).
  - WASTE: 8.969 / 3.336 unchanged; NEW hashes-per-journal-entry 13.672 and hashes-per-prune 539.333; HOST rows moved
    (bytes-per-turn 1.635, plus three seal rows).
- Incident: my first judge's PID file held only the subshell wrapper. scripts/commit re-execs ITSELF from a frozen tree
  (main/.git/nanodregg-commit-main/<pid>/tree) as a CHILD, so stopping the recorded PID orphaned the judge. It ended on
  its own; nothing landed; ROOT told. The frozen-tree dir .../1180086/ is left for ROOT. LESSON: never stop a judge by
  its PID file; wait for it. A wait loop must watch `pgrep -f nanodregg-commit-main/<pid>` as well as the PID.
- Told LANG-12 (aa6fec46b5067cd28): AGREED that it adds the digest round-trip law (`∀ x, X.digestOf (X.env.bytes x) =
  some x`, cv 01a14b28-7029) under --cross-layer after K41, with a refutation tooth, discharged for Sim and Deployed.

### KERNEL-12 HANDOFF (written 2026-10-17 at ~410K tokens; NOTHING unlanded; wt/kernel holds the landed tree, reset with `git checkout --detach main`)
NEXT for KERNEL-13, in order:
1. cv 01a14afe-7380, a draw-independent hash ratio (GATES-3's ask).
   - Replace admit hashes-per-touched-cell / hashes-per-nullifier with counted ÷ REQUIRED, pinned near 1.
   - REQUIRED per admitted turn = the trie nodes of w' whose hash is new: walk w'.trie against w.trie in parallel; a
     subtree whose hash equals the old one at that position counts 0; a node with a new hash counts 1 plus its children;
     a single-entry leaf counts 1 iff `w.trie.get k ≠ some v` (a leaf hash is depth-independent, so a split's moved leaf
     is NOT required: the row then shows that waste).
   - The empty digest is required 0 (KERNEL-35's floor shows as waste).
   - Do the same for the journal: <K ÷ the new journal nodes, plus a prune ratio.
   - Keep the KERNEL-35 plant hash-count:empty-per-insert red by name: plant ratio > honest.
   - Then delete the two draw-sensitive rows (and the journal row if it is converted), with reasons in waste.tsv.
   - Sim-only code goes in Kernel/Sim/Gen.lean (countTurn, report).
2. cv 01a14a8a-7364: fold_prune_check's hv on Honest logs (the shadow entry at txId written by the same call: same
   window, so validUntil ≤ e.1 + W; another call with the same txId is a collision over the call codec). After K41 it
   also takes `hc : w.JournalCanon E`; the reach_ form discharges it.
3. cv 01a14aa3-ca32: receiveWith reads c.unsigned.world only through checkSignature/callMessage (KERNEL-42 domain).
4. Old opens (KERNEL-10 handoff):
   - stale_named names only the first failing touch;
   - a revoked carved grant does not return the unspent enrol count;
   - cv 01a14938 amount-bounded right;
   - the KERNEL-29 critique.
5. Open from my critique: `World` keeps `[Ord D]` (firstDup); both tries share domTrie for nodes. No action is needed
   unless a reader asks.
Facts for the successor:
- Journal theorems take `w.JournalCanon E` (in Kernel/Proofs/Admit.lean); `JournalOk E w` = Canon ∧ heights ∧ distinct.
- Phone journal theorems: Kernel/Proofs/JournalHead.lean; deployed forms are in RootedDeployed.
- A head is `headLink E prev td root' jroot'`; `World.roots`.
- A CODEC decoded base gives `world_decode_journalOk : w.JournalOk env`.
- HOST's lookup theorems take JournalCanon, discharged by openWith_journalOk / admitBatch_journalOk.
- Patch workflow: Mac scratch k12/ is a git baseline of Kernel/ (re-baseline it before reuse); ../push.sh tars the
  changed files into wt/kernel.
- SIZE lines: scripts/commit lists each one it wants; every Lean-lines layer that rose needs its own line.

## KERNEL-13 (successor of KERNEL-12; started 2026-10-18; hbox wt/kernel)
- ⚑ LANDED 891e80b `kernel!` KERNEL-43 (cv 01a14ba9-cbf4 DONE).
  - Change: GenesisFits/CarryFits/World.CodecFits bound `weight + allowance < 2^64`. The sum REPLACED the allowance-only clause, and the genesis budget check is LAST.
  - New module Kernel/Proofs/Budget.lean: fold_budget_lt, genesis_budget, carry_budget, genesis_fold_budget_lt, carry_slotted, carry_fold_budget_lt, deployed_budget_lt.
  - HOST: Kept gained the sum, and openWith_exportFile_ok is now premise-free.
  - The World refine was RENAMED `kernel/world-budget`, because the vectors gate refused the boundary vectors under the unchanged tag. ROOT ruled the re-genesis.
  - Every Store re-geneses. Carried exports are unaffected.
  - Teeth: sim arms carry-budget / -edge / -plant. Mutation: 64/64 seeds red.
  - Vacuity reader: LAND, with 2 findings, both taken.
- Land helper: hbox logs/kernel13-land.sh N MSG CROSS PATHS…. It `cd`s first and backgrounds ONLY scripts/commit, so the PID file holds scripts/commit's own PID.
  - Lesson: in `ssh 'cd … && … && nohup X &'` the `&` backgrounds the WHOLE && chain, and `echo $!` then runs in ~.
  - Wait loop: `kill -0 PID` with a sleep and a deadline.
- Orphan judge dir main/.git/nanodregg-commit-main/1180086 REMOVED (4 MB).
- HOST-LOG `## HOST-11 HANDOFF` carries the rebase note for host11-wip over 891e80b.
- AGREED for LANG-13: cv 01a14b28-7029 (Receive.Ctx.Lawful, deployed_ctx_lawful). Additive; Env.Lawful is untouched.
- Queue:
  - KERNEL-44 PROPOSED: refusals as records + checkpoint/replay. Note: the brief called it 43, but 43 is the budget fix.
  - KERNEL-45 PROPOSED: the hyperedge decision (ROOT, from MINI-CONCEPTS-IN-NANO-20261018.md §4): a Turn is the hyperedge for one signer; multi-signer DEFERRED with a trigger; cross-World behind "a second writer".
  - Then co-sign LANG-44's kernel half: relations, plus LANG-13's cap/sum head amendment. State as a theorem that the head is never pinned by an insert. Send LANG-13 the real signatures.
  - Then cv 01a14afe-7380, 7364, ca32.
- ⚑ LANDED 897911b: KERNEL-44 PROPOSED (refusals + replay/checkpoint) and KERNEL-45 PROPOSED (hyperedge for one signer; multi-signer, joint-law and cross-World turns deferred with triggers). Decisions only.
- ROOT RULED on 897911b:
  - KERNEL-45 APPROVED.
  - KERNEL-44 refusals APPROVED as designed. Conditions:
    (a) a sim arm for the A→B→A defect (a refused call later admitted when its pin returns), RED on the old code and GREEN on the new;
    (b) a WASTE row "refusals per member per window" (max over seeds), plus a plant: the 17th is refused `refusalBudget` by name;
    (c) "no premise on any cell reader" is checked at landing;
    (d) ONE day with CODEC-8 and HOST-12: ROOT spawns them against my STAGED patch, and I tell ROOT when it is staged.
  - KERNEL-44 checkpoint half: stays PROPOSED. It went to Ember as a pause item (ROOT recommends retention by operator, default keep-everything, CheckpointTrusted named and planted).
- ⚑ LANDED 7679aac: KERNEL-46, LANG-44's kernel half CO-SIGNED.
  - Amendments: a length-prefixed row key (rows_separate needs no World invariant); heads born by `RowAct.declare`; admit_comm states BOTH orders admit, with additive heads; one `Roots` digest in the head link; World.weight counts rows.
  - LANG-45 (ii) capped sum accepted: head (count sum limit cap width retract), row (amt val), head_sum, sum_le_cap.
  - Signatures are in the entry. LANG-13 was told, and given my view on LANG-47's range pins: pin the CONTENT (a listing digest under the prefix, recomputed, early stop, `rangeTooLong`), not a trie node. ROOT has not ruled on range pins for v0.

### KERNEL-13 HANDOFF (written 2026-10-18 at ~340K tokens; NOTHING unlanded; wt/kernel clean at main 7679aac)
Landed by me: 891e80b (K43 budget, kernel!), 897911b (K44/K45 proposals), 7679aac (K46 co-sign).
NEXT for KERNEL-14, in order:
1. **BUILD KERNEL-44 refusals, kernel half, STAGED as a patch** (not landed alone). ROOT spawns CODEC-8 and HOST-12 against it, and it lands as ONE kernel! day. The design is in decisions/kernel.md KERNEL-44 Part 1, with ROOT's conditions above.
   Shape:
   - `World.refusals : Trie.T D D RefusalLeaf D`. Leaves: `refused h code` at the txId; `count win n` at H(domRefusalCount ‖ member ‖ u64 win).
   - `refusalSpec`, `recordRefusal` (only after keyRule passes), `Bounds.refusalsPerWindow` 16, `refusalBudget`.
   - Pruned by retainAt at multiples of W: refused kept while h + 2W > H; counts kept for the current window only.
   - submit/lookup consult it: a recorded refusal answers `refused NAME` without re-deriving (`submit_refused_final`).
   - Refusals do not advance height. The chain advances by a domain-separated `refusalLink prev callDigest rootsDigest`.
   - INTRODUCE the `Roots` digest (KERNEL-46 amendment 4): headLink E prev td rootsDigest, with rootsDigest = H(domRoots ‖ cells ‖ journal ‖ refusals). The rows day then adds one field.
   - World.fold over `List (Step D)` (turn | refusal call code). This is the big statement churn: ~109 statement lines in 35 files name World.fold. Measure it first. Cheaper alternative to weigh BEFORE building: keep `World.fold : List Turn` and add `World.foldSteps` beside it, only if every landed fold theorem keeps holding for turn-only logs AND the host's open uses foldSteps. But two folds is the "two shapes" smell; argue it in the decision before choosing.
   - The batch record carries (call bytes, code) per refusal; the follower's audit re-derives each refusal and requires the same code.
   - Carry carries no refusals.
   Teeth:
   - sim arm A→B→A (old code: a refused stale call is admitted after the pin returns, RED; new: `refused stale`);
   - the 17th refusal is refusalBudget (plant);
   - WASTE rows: admit hashes-per-refusal, log bytes-per-refusal, refusals-per-member-window max.
   Vacuity read; the cell-reader premise census at landing.
2. Then the rows day (KERNEL-46 + LANG-44). LANG-13 (ae50e96cec584e649) writes the Lang half against KERNEL-46's signatures. Tell it when they exist in code.
3. Then cv 01a14afe-7380 (draw-independent hash ratio), 01a14a8a-7364 and 01a14aa3-ca32, plus the KERNEL-10 opens.
Facts:
- hbox logs/kernel13-land.sh N MSG CROSS PATHS… starts scripts/commit detached. The PID file holds scripts/commit itself. Wait with `kill -0` plus a deadline.
- The Mac scratch k13/ git baseline is STALE (pre-891e80b). Re-baseline it from hbox before reuse.
- The vectors gate refuses new vectors under an unchanged tag. A tightened refine is a meaning change, so rename the refinement.
- SIZE lines: scripts/commit lists each one it wants on the first refusal.
- ADDENDUM after the handoff (LANG-13, 2026-10-18):
  - LANG-13 ACCEPTED all five KERNEL-46 amendments and the content-digest range pin.
  - ROOT ruled range reads INTO v0. They join the rows day. Conditions:
    (a) a theorem that the supplied rows are exactly the keys under the pinned prefix, in key order, with a tooth: a mutation that drops a row makes the seal's arg-max wrong, and the pin theorem refutes it;
    (b) WASTE `rows-read-per-range-read`;
    (c) the range pin is a second pin kind in the act.
  - Design: `rangePin = H(domRange ‖ parent ‖ rel ‖ prefix ‖ listing of (key, leaf digest))`, recomputed at admission with an early stop. `rangeTooLong` refuses, never truncates. `range_stale_refused` has the same conclusion as stale_refused.
  - LANG-13 retired. Its successor LANG-14 writes the Lang half (LANG-LOG.md ## LANG-13). KERNEL-14: message LANG-14 when the rows signatures are in code.

## KERNEL-14 (successor of KERNEL-13; started 2026-10-18; hbox wt/kernel)
- FOLD CHOICE (KERNEL-47, ROOT accepted all six amendments): ONE `World.fold` over `List (Step D)`, `Step := turn | refusal`, `World.step` with two arms (admit, refuse). Amendments:
  - `World.steps` counter. fold_reaches_host binds on (steps, chain); the HOST follower compares steps.
  - One chain domain with a tag byte.
  - Refusal keys carry a kind byte and raw bytes, no hash.
  - Only IN-WINDOW authenticated refusals are recorded. The early-call case is a DEFECT in KERNEL-44 as approved.
  - refusedFinal is checked in checkJournal.
  - Authenticated means the current key, or the precommitted next key for a rotate (keyRule skips rotate).
  - Non-final replies (U codes, early outsideWindow, refusalBudget) went to PROTOCOL/CLIENT via ROOT.
- STAGED: hbox logs/kernel14-k44.patch, on main d52ad3d, Kernel + journeys + decisions + waste. It excludes Codec/Emit, which is CODEC-8 (a4fb8cf96b85a9b74): logs/codec8-k44.patch.
  - The joint tree in wt/kernel builds `lake build Kernel` green. kernel-sim --seeds 64 is ALL PASS. lang-journey, ledger-sim and hosting-sim are green.
  - Red until HOST-12: Host.Record, Host.Serve, Protocol/Command/Machine `absorb` (needs a refusal step), Emit.Vectors (imports Host).
- New: Kernel/Proofs/Refuse.lean and Kernel/Proofs/Refusals.lean. `refusals_separate` lives in Cells.lean. Receive.judge, authKey, authenticated, refusedOf, Verdict.code and codeName live in Receive/Submit.lean. auditRefusal is in Receive/Audit.lean.
- commit shares ONE empty-digest thunk across the three tries. Without it, the empty refusals root cost a hash per turn.
- refusalsDisjoint and fold_refusalsDisjoint were added at CODEC-8's ask.
- WASTE: three refuse rows added; two admit rows re-pinned down.
- cv 01a14d89-b259: the toy sim's carry-budget-plant is vacuous at the 8-byte digest. It was there before this patch and is ungated.
- Days: refusals and rows land as TWO days (CODEC-8 agreed). LANG-14 is to be spawned when the rows signatures are in code.
- Vacuity reader running (read-only, background).
- Vacuity reader (agent aa404bfe3debd5422, resumable by SendMessage):
  - First read: HOLD on F1 (refusalCount_le bounded the counter, not the records).
  - Fixed: refuse_refusalCount, admit_refusalCount, fold_member_refusals and fold_member_refusals_le (the DoS bound over the LOG).
  - Also fixed: F2 submit_refused_never / judge_recorded_never (never admitted, ever); F5 reach_height_le_steps; F4, F6 and F8 docs.
  - Re-read: LAND.
  - Filed: F3 cv 01a14d95-36b0 (refusal inclusion theorem: the phone's receipt) and the early-plant reshape, cv 01a14d95-36cf.
- After the LAND, from CODEC-8's and HOST-12's finds:
  - (A) `checkSteps` runs LAST in check and in checkRefusal, with step_steps_lt / fold_steps_lt. F7 cv is done. check_origin_blind is no longer blind to steps; carry_check compares with `{w with refusals := .empty, steps := w.height}`.
  - (B) refusalFits requires `1 ≤ h`.
  - (C) counting invariants deferred: cv 01a14da3-3e7a.
  - THESE DELTAS ARE NOT YET RE-READ by the vacuity reader. Ask aa404bfe3debd5422 to re-read checkSteps / Checked.steps / carry_check / check_origin_blind / refusalFits before landing.

### KERNEL-14 HANDOFF (written 2026-10-18 at ~high context; NOTHING landed; wt/kernel holds the joint tree UNCOMMITTED)
State of hbox wt/kernel, detached at main d52ad3d, uncommitted:
- My kernel half. Staged copy: logs/kernel14-k44.patch, 249962 bytes, which is `git diff -- . ':(exclude)Codec' ':(exclude)Emit'`. The new files Refuse.lean and Refusals.lean are `git add -N`'d.
- CODEC-8's Codec/ and Emit/ applied from logs/codec8-k44.patch (an older take). Re-take its latest with `git checkout -- Codec Emit && git apply ../../logs/codec8-k44.patch --include='Codec/*' --include='Emit/*'`.
- `lake build Kernel` and kernel-sim are green; 64 seeds ALL PASS.
NEXT for KERNEL-15: LAND THE ONE kernel! COMMIT once all four halves are in.
- Halves: kernel (mine), CODEC-8 a4fb8cf96b85a9b74 (logs/codec8-k44.patch), HOST-12 a28e294ce7b0dcec6 (logs/host12-k44.patch, not yet written), PROTOCOL-8 a74791bc5155933fa (logs/protocol8-k44.patch; it waits on HOST-12's Machine shape for rows 22/22).
- Before landing:
  - Apply all four halves to wt/kernel.
  - Run a full `swarm-build lake build`.
  - Run kernel-sim --seeds 64, host-sim, the journeys (lang-journey, ledger-sim, hosting-sim), rows, and codec-vectors.
  - Get the reader's re-read of the post-LAND deltas listed above.
- Land with `logs/kernel14-land.sh N MSGFILE CROSS PATHS…`. The message draft is logs/kernel14-k44-msg.txt; extend it with the halves' SIZE/WASTE lines and with CROSS-LAYER for codec/host/protocol, since each owner is party to the one commit.
- `kill -0` wait with a deadline.
After that: the rows day (KERNEL-46 + LANG-44 + range pins). ROOT spawns LANG-14 when the rows kernel signatures are in code. Then cv 01a14afe-7380, 7364, ca32, and the new refusal cvs.
Facts:
- The toy kernel-sim reds carry-budget-plant independently of this work: cv 01a14d89-b259 (GATES-4).
- PROTOCOL-8 finding: a resubmit of a recorded txId gets judge `.declined (rejected (refusedFinal code))`, not `.recorded`. Settle reads finality from the World, which is consistent.

## KERNEL-15 (successor of KERNEL-14; started 2026-10-18 ~02:13 hbox time; hbox wt/kernel)
- Start: main d52ad3d (has not moved). wt/kernel holds the joint tree uncommitted (41 paths). Patch files in logs/: codec8-k44 (02:12), host12-mine (02:12, no host12-k44 yet), protocol8-k44 (02:05).
- Messaged CODEC-8, HOST-12 and PROTOCOL-8: I am the lander; asked each for its final patch path, its CROSS-LAYER and WASTE lines, and its checks.
- Asked the reader aa404bfe3debd5422 to re-read deltas (A) checkSteps etc. and (B) refusalFits `1 ≤ h`.
- Reader re-read of the post-LAND deltas: LAND. No cell reader gained a premise. Two findings, both taken:
  - (a) checkSteps is SECOND in checkRefusal; decisions/kernel.md now says so.
  - (b) a tooth was added in Refuse.lean: checkSteps_refuses, admit_refused_at_step_ceiling, refuse_refused_at_step_ceiling.
- Joint tree, applied in wt/kernel with --index on d52ad3d:
  - logs/kernel15-k44b.patch (the kernel half, without waste);
  - logs/kernel15-waste.patch;
  - codec8-k44-final2;
  - kernel15-host12-final (= host12-k44, md5 f2b1d09c);
  - kernel15-protocol8-final (02:21, generated.rs included).
- Verdicts:
  - umbrella 466 jobs green;
  - kernel-sim 64 ALL PASS;
  - lang-journey, ledger-sim, host-sim ×3, host-file-sim ×3, hosting-sim ×3, store-plants: all green;
  - rows 22/22, every plant caught;
  - cargo client (7/10/2/1/1), clippy and fmt clean;
  - CODEC-8: vectors 95/35 byte-identical, census ok, emit-* --check 0.
- Land attempt 1 was RED on closure C3 (proof-modules exporting defs) plus the missing SIZE/WASTE lines. Fixed forward:
  - plantRefusalKeyBytes/Spec made private;
  - Step.dheight moved to Kernel/World.lean;
  - HOST's stepWeight and judgeStaged made private.
  Also added 20 SIZE lines and 3 WASTE lines.
- **LANDED 38d94e1** kernel! (97 files, pushed). Message in logs/kernel15-k44-msg.txt. ROOT and the three lanes are told.
- NEXT: the rows day (KERNEL-46 as co-signed + the kernel half of LANG-44, incl. the listing-digest range pin as a second pin kind; ROOT's conditions (a) rows-exactly-under-prefix theorem with a dropped-row tooth, (b) WASTE rows-read-per-range-read, (c) range pin in the act). Stage it, then tell ROOT when the rows signatures are in code. Then cv 01a14da3-3e7a, 01a14d95-36b0, 01a14d95-36cf, 01a14afe-7380, 7364, ca32, and the KERNEL-13 opens.

### KERNEL-15 HANDOFF (written 2026-10-18 at ~300K tokens; LANDED 38d94e1; the rows day is STAGED, uncommitted in wt/kernel)
Landed by me: **38d94e1** kernel!: refusals day, four halves. The message is logs/kernel15-k44-msg.txt.

wt/kernel is detached at main 38d94e1 and holds the rows wiring UNCOMMITTED. Snapshot: hbox logs/kernel15-rows-wire2.patch (`git diff HEAD --binary`; re-apply with `git apply --index` on a `--detach main` checkout). It contains:
- Kernel/Turn.lean:
  - RowKey, RowSlot, RowLeaf, RowAct (incl. declare), RowTouch, RangeRead (placed before Turn);
  - Turn.rows / Turn.ranges, the LAST two fields, defaulted [].
- Kernel/Bounds.lean:
  - keyBytesMax **128** (LANG-44 said 64; a two-digest key in Lang's encoding is 66 B);
  - rowDepth 280 + 8·keyBytesMax;
  - rowsPerRelationMax 4096, rowsMax 32, rangesMax 4;
  - Bound.rows.
- Kernel/World.lean:
  - Reject + names for the 13 new constructors, each `(parent : D)`: keyTaken relationFull relationCapped rowParentUnpinned orphanRow rowsRemain keyWidth noRelation retractForbidden declareLate rangeTooLong duplicateRow rowShape;
  - `Rows` abbrev and World.rows (after refusals, default .empty);
  - rows section after refusalSpec: rowsPrefix, rowKeyBytes (length-prefixed), rowLeafBytes (val rawBytes-prefixed, CODEC-9's ask), rowDigest, rowSpec, RowLeaf.fits, rowAt, rowPin, startsWith, `under` (prefix walk), rangeRows, rangePinBytes (nat32 count) + rangePin;
  - rootsDigest has 4 roots; World.rowsRoot; roots;
  - decode invariants: ascendingBytes, rowFits, rowsFits, rowsHeaded (CODEC-9 refines on kernel/rows and kernel/rows-headed);
  - admission: rowPath, headOf, setHead, rowStep, rowsRun, checkRanges, checkRowsRemain. `check` runs checkRowsRemain, then checkRanges, then rowsRun after checkCreates, with checkSteps still LAST. commit writes `rows` (a match fallback that is unreachable after check) and the 4-root digest. commitRefusal digests w.rows.
- Kernel/Proofs/Admit.lean: Checked gains rowsRemain / ranges / rows; check_ok is fixed.
- Kernel/Sim/Gen.lean: roots arg and Turn literals.
- Codec/Kernel.lean:89: a minimal `[], []`. CODEC-9 replaces it.
- decisions/kernel.md: KERNEL-48 (the signatures and the plan).
Builds: Kernel.World and Kernel.Proofs.Admit are green. The umbrella is RED in Codec (World.mk has 9 fields; Proofs/Kernel). That is CODEC-9's (addd21abb78660a69), whose half comes as logs/codec9-rows.patch. Downstream Kernel proofs have not been built past Codec yet, so expect breakage in Rooted*, Fold, Carry, Weight, Frame, CellsFit, Value, Sim.

NEXT for KERNEL-16, in order:
1. Get `lake build Kernel` green past Codec. Use CODEC-9's patch, or keep the interim fix in Codec/World.lean:166 until it arrives. Fix the kernel proofs the new check and commit arms break. The rows frame: rowsRun touches only `rows`; the cells, journal and refusals readers are unchanged. No cell reader may gain a premise.
2. **CHARGE / WEIGHT: NOT DONE, and a real hole as staged.** Rows are admitted without being charged. Do KERNEL-46 amendment 5:
   - World.weight = cellsWeight + rowsWeight;
   - Turn.growth counts row bytes (insert/declare and an upsert of a fresh key at the full leaf+key size; an upsert of an existing key by the delta, which needs the World, so put it in `credit`/posts like a touch's freed bytes; a retract credits back);
   - fold_conserves and weight + allowance < 2^64 must keep holding. Do not land without this.
3. Theorems, each with a tooth:
   - rows_separate as `SeparatesOn (rowSpec E) RowSlot.InDomain` (CODEC-9's finding: byte8 truncates, so "unconditional" is false);
   - rows_stale_refused and range_stale_refused (stale_refused's conclusion);
   - range_rows_exact (ROOT condition (a)): rangeRows returns exactly the keys under the prefix, in key order. Tooth: drop a row and the pin differs, and the seal arg-max is refuted;
   - head_sum and sum_le_cap over every reached World, plus rowsHeaded/rowsFits of a fold (for CODEC's refine);
   - admit_comm: BOTH orders admit, additive heads;
   - the plant "an insert that pins its head" makes the second insert stale.
4. WASTE `rows-read-per-range-read` (ROOT condition (b)) in kernel-sim, with rows arms in Sim/Gen. `under` lists the whole subtree, so make it stop at most + 1.
5. Vacuity reader (statements only), then land ONE kernel! with CODEC-9's, LANG-14's (afa6eabec1b239454: Unsigned.rowPins/ranges, RowView, run's row edits, rels → declares, receive refusal `.rowParent`) and HOST-12's halves. Re-genesis every Store; vectors re-emit (the kernel-functions section is ROOT-ruled; its boundary pair is now 128/129, so tell ROOT).
6. Then the cv tasks: 01a14da3-3e7a, 01a14d95-36b0, 01a14d95-36cf, 01a14afe-7380, 01a14a8a-7364, 01a14aa3-ca32, and KERNEL-13's opens.
Agreements made (LANG-14 R1–R5, all accepted):
- a moved row pin and a moved range pin are both `stale parent`;
- an unpinned row effect must be insert or declare (rowShape otherwise);
- declares come from the create receiver in rel-index order.
Facts:
- Helpers: logs/kernel15-land.sh N MSG CROSS PATHS… (PID file = scripts/commit). The pre-push gates include closure C3: a proof module may not export a def, so make it private or move it to a def-module. SIZE/WASTE lines are named on the first refusal.
- Heredocs inside `ssh '…'` eat backticks: write scripts locally, scp them, and run them.
- ADDENDUM after handoff: **wire3 supersedes wire2** (hbox logs/kernel15-rows-wire3.patch). CODEC-9's asks (C)–(E) are taken:
  - (C) checkBounds carries the rows' and ranges' syntactic wire bounds (`overBound .rows`);
  - (D) RowSlot.weight, RowAct.logWeight, RowTouch.weight and RangeRead.weight, with Turn.logWeight += the two lists (each with its header);
  - (E) `rowEntryWeight` / `rowsWeight` are defined, but World.weight is STILL cells-only and Turn.growth does not count rows. That is handoff item 2: move both together with the proofs; CODEC-9 moves kernel/world-budget when weight moves.
  Kernel.Proofs.Admit is green.
- ADDENDUM 2 (LANG-14, afa6eabec1b239454): its R1–R4 are in hbox logs/lang14-receive.patch, which touches Kernel/Receive/{Call,Derive,Ledger}.lean on main + wire2; Kernel.Receive.Derive builds.
  - `receive` passes `rowView X.env w u`; dispatch, tree, derive, deriveTurn and receiveWith take `rv : RowView D` after `look`; sealTurn takes the rows; create emits declares from X.program.rels; invoke asserts `rowParent`.
  - LANG-14 does the mechanical threading of `rv` through Kernel/Proofs (Tree, Receive, Rooted*, Authority, Ledger…) in ITS half. KERNEL-16: message it first, to agree who owns which file.
  - STATEMENT CHANGE to read: `receive_congr` gains the premise "the two RowViews agree". That is honest, since the derivation now reads rows, but the vacuity reader must confirm it adds no premise to any cell reader and that no other receive theorem silently gains one.
  - The patch is cut on wire2. Re-take it on wire3, which differs only in checkBounds/Turn weights/rowsWeight, so it should apply clean.

## KERNEL-16 (successor of KERNEL-15; started 2026-10-18; hbox wt/kernel)
- Start: wt/kernel = wire3 exactly (md5 da871e25). ROOT: main moved to 2db5853 (README; GATES-14 deleted `kernel-sim --toy`, scripts/commit writes its own PID to $NANODREGG_COMMIT_PID_FILE). wt/kernel moved onto 2db5853 by `git checkout --detach` (no overlap; carried cleanly).
- Messaged LANG-14 (afa6eabec1b239454), CODEC-9 (addd21abb78660a69), HOST-12 (a28e294ce7b0dcec6), PROTOCOL-9 (aa5673280c5f1b5e6): I am the lander. PROTOCOL-9 has NO Protocol patch for the rows day; it runs rows ALL PASS on the joint tree when told.
- Joint tree in wt/kernel now = main 2db5853 + my kernel half + logs/lang14-receive.patch (LANG-14's Receive glue, not its final half) + logs/codec9-wip.patch (CODEC-9 WIP; my Codec/Kernel.lean stub reverted first). Snapshots: logs/kernel16-kernel2.patch (Kernel + decisions only, md5 5e42b4e8), logs/kernel16-joint2.patch (everything, md5 00b72e09). Earlier: kernel16-snap1 (pre-joint), kernel16-kernel1/joint1.
- MUST-DO (1) CHARGE: DONE. Turn.growth += Σ RowTouch.growth; World.weight = cells + rows; rowsRun → (rows, freed); rowsAfter; commit credits freed; check order now … checkNullifiers, checkRowsRemain, checkRanges, rowsRun, checkCharge(credit + freed), checkCreates, checkSteps. fold_conserves holds exactly (Weight.lean green). Text: decisions/kernel.md KERNEL-48 "KERNEL-16 addendum".
- CARRY (CODEC-9's question): rows ARE carried this day. Carried.rows (last field); carryInput gains the rows root after the cells root; checkCarry bounds cells+rows+allowance and the rows-root bytes; carry_inj/_canon gain the rows-root equality; carry_of_carried gains w'.rows = w.rows. CODEC-9 moves the carried wire (cells ‖ allowance ‖ height ‖ journal ‖ rows) and kernel/carried's tag.
- New module Kernel/Proofs/Rows.lean (green): RowsCanon; rowStep_weight, rowsRun_weight, rowsAfter_weight; admit_rows, admit_rowsCanon, refuse_rows, refuse_rowsCanon, fold_rowsCanon, genesis_rowsCanon, receive_genesis_rowsCanon; admit_range_pins + range_stale_refused; rowStep_pin, rowStep_get_other, admit_row_pins + rows_stale_refused. ⚑ `attribute [local irreducible] rowPath` is REQUIRED there: whnf of any statement mentioning `rowPath` (List.range 1304) hits maxRecDepth, even `exact` with an identical type.
- Green on the joint tree: Kernel.Proofs.{Admit, Rows, Cells, Weight}, Kernel.Sim.Gen (stub program fixed for LANG's Program: run takes RowView, returns 4-tuple; rels). Budget.lean EDITED (fold_budget_lt/carry_fold_budget_lt gain hr; carry_rowsCanon; deployed discharges) but UNBUILT: it imports Carry → Origin → Kernel.Proofs.Receive, which is RED (LANG-14's rv threading; LANG-14c is repairing it in wt/lang). Carry.lean edits also unbuilt for the same reason.
- Premise spread (for the reader): admit_world_weight, admit_conserves, fold_conserves, fold_world_weight, fold_budget_lt, carry_fold_budget_lt gain `w.RowsCanon E`; discharged at Deployed. World.Canon unchanged, so no cell reader gains a premise. admit_charge/admit_retire conclusions add (rowsAfter E w t).2. Cells' rootsDigest_inj/head_roots/head_root/head_read_sound/head_absent_sound open four roots. Checked.charge/Checked.rows changed shape.
- Told LANG-14: kernel-sim owns the keyTaken and relationCapped plants (LANG cites them). LANG-14 reports LT5/LT6b/LT7 (630)/LT7c/LT7d green on wt/lang (pre-charging snapshot); it will rebase onto kernel16-kernel1 or later and re-check LT7.
- CODEC-9 asks (open): (a) RowsOk preservation for HOST's Kept: per-entry rowFits + rowsHeaded (head_sum) under admit; ascending order CODEC derives from canon + its order theorem; (b) rows_separate on the domain; the rowKeyBytes size lemma CODEC proves itself.

### KERNEL-16 HANDOFF (written 2026-10-18 at ~285K tokens; NOTHING landed; wt/kernel holds the JOINT tree uncommitted)
State: wt/kernel detached at main 2db5853 with the joint tree (see above). Re-create: `git checkout --detach main && git apply --index logs/kernel16-joint2.patch` (it includes CODEC-9's WIP and LANG-14's receive glue; for the kernel half alone use kernel16-kernel2.patch). Scratch mirror of my edited files on the Mac: /private/tmp/claude-501/-Users-ember-dev-breadstuffs/a8357d63-efef-43bb-a4da-cdc3905383e7/scratchpad/k16 (push helper ../push.sh tars named files into wt/kernel).
NEXT for KERNEL-17, in order:
1. When LANG-14 delivers Kernel/Proofs/Receive (or lang14-rows.patch), build `lake build Kernel` and fix forward Budget.lean, Carry.lean (my edits are unbuilt), CarryRooted, Fold, Frame, Rooted*, Refusals, JournalHead, LedgerDeployed for the 4-root digest, Carried's fifth field and the new premises. Keep "no cell reader gains a premise".
2. Theorems still owed, each with a tooth: rows_separate as SeparatesOn (rowSpec E) RowSlot.InDomain; range_rows_exact (`under` = the listing filtered by startsWith of the prefix; key order from CODEC's order theorem) with the dropped-row tooth; head_sum / sum_le_cap and RowsOk (rowFits per entry + rowsHeaded) preserved by admit/refuse/carry, genesis empty (CODEC-9 + HOST-12 need it for Kept); admit_comm (both orders admit, additive heads).
3. `under` early stop at most + 1 (KERNEL-48 critique), then WASTE rows-read-per-range-read (+ hashes per row insert, per retract) in kernel-sim; Sim/Gen rows arms incl. plants: stale row pin, stale range pin (a row landing under the range), keyTaken, relationCapped, declareLate, rowsRemain, uncharged-row plant (growth without rows ⇒ fold_conserves breaks).
4. Then the vacuity read, the partner patches (CODEC-9 final, LANG-14 final, HOST-12: Roots stamp flip + Carried.rows + reopen/backup + plants), the full gate run, and ONE kernel! commit as the brief says.

## KERNEL-17 (successor of KERNEL-16; started 2026-10-18 ~03:15 hbox time; hbox wt/kernel)
- Start: main 2db5853; wt/kernel = kernel16-joint2.patch exactly (md5 00b72e09). Messaged LANG-14, CODEC-9, HOST-12, PROTOCOL-9: I am the lander. LANG-14: Kernel/Proofs/Receive repair lands at logs/lang14-kproofs-receive.patch (+ .txt of changed statements).
- Took LANG-14's kproofs-receive-only, tree-auth (Tree/Authority/Rooted) and Submit.lean (refusalNames +5); appended the 13 Reject names to rejectNames (every reject code shifts: vectors re-emit). Rebased wt/kernel onto main 0c63e85 (HOST-41; no overlap). Snapshots logs/kernel17-joint1/2.patch.
- World.lean design edits (mine): `under` takes a bound n + `takeList` (rangeRows reads most+1; checkRowsRemain reads 257 and refuses a full listing); `dropHeads` (a retired parent's heads leave with it, credited to freed — without it heads of a retired parent were garbage that never gave weight back); rowStep refuses `orphanRow` for a row under a parent the same turn retires (was a REAL hole: a turn could retire p and insert under p); checkRanges refuses `keyWidth` unless pre.size ≤ width (a longer prefix routes SHORTER keys into the listed subtree, so `under` ≠ the filtered listing); `rowsParented` (CODEC-9's refine site kernel/rows-parented).
- CODEC-9 keeps rows_separateOn (Codec/Proofs/RowOrder.lean) + tooth rows_kindByte_needed (Codec/Proofs/WorldTooth.lean); no Kernel twin.
- Spawned K17-HEAD a5b74088afbbb8a22 (Rows.lean repair + RowsHead.lean: RowsOk, head_sum, admit_rows_listing for HOST), K17-RANGE a3a0aa2d594a5e5ed (RowsRange.lean: range_rows_exact + dropped-row tooth), K17-COMM a6bcaa8badce6a08e (RowsComm.lean: admit_comm + plants), K17-SIM aa19bc67d16d48f07 (Sim/Gen arms, plants, WASTE). Common brief: hbox logs/kernel17-brief-common.txt.
- Rebased onto main 70eb282 (PROTOCOL-42/43; no overlap). Took CODEC-9's final half whole (logs/codec9-rows.patch md5 20977ee8; lines in logs/codec9-rows-lines.txt) and LANG-14c's Ledger.lean. Fixed JournalHead, RootedDeployed (4 roots), Carry (rowView), Budget (omit). `lake build Kernel Codec Emit` GREEN except the in-flight lane files. Snapshot logs/kernel17-joint4.patch. Waiting: LANG-14's lang14-rows.patch, HOST-12's half (needs Lang), the four K17 lanes.
- K17-RANGE DONE: Kernel/Proofs/RowsRange.lean (takeList_eq, under_eq, under_needs_long tooth, range_prefix_long, under_rows, range_rows_exact (i)(ii)(iii), range_rows_none, admit_range_exact, rangePinBytes_erase_ne, range_rows_erase_not_exact, range_seal_tooth, range_rows_satisfiable). Gap hfit → discharged by fold_rowsOk (asked for fold_range_exact). Dedupe of byte lemmas into Kernel/Proofs/Bytes.lean agreed with CODEC-9 (conditions in its message; CODEC-10 now codec owner).
- K17-SIM DONE: 64/64 ALL PASS; 13 rows arms + 3 plants (k17-sim-gen.patch); WASTE row-insert 1127.7 hashes (!), row-retract 1137.5, rows-read-per-range-read 2.4. Cause of 1128: check's rowsRun result thrown away and commit recomputes (2x), two paths (row + head), and ~280-level unshared paths (no path compression; every key under a parent shares parent‖rel‖tag‖width). Fix in this day: thread check's rows into commit. Path compression = separate design (cv task + ROOT). Also hashes-per-nullifier mislabeled (empty rows root forces the empty digest): SIM bracketing it apart.
- K17-COMM DONE: Kernel/Proofs/RowsComm.lean — admit_comm (World level; premises hjc hrc RowsCommFoot RowsFitTogether windows at h+2, combined charge ≤ allowance, steps; conclusion: both orders ADMIT, rows+cells extensionally equal, heads additive), admit_comm_trie (structural cells equality), rowsRun_comm; teeth two_rains (premises satisfiable), plant_second_rain_stale (head-pinning design refuses the second rain), write_repin_refused. Limits named: NoRetire, insert-only, ranges = [] (a range over a relation the other turn inserts into is genuinely order-dependent). insN/insA to move into World.lean beside headOf (they appear in public statements). SIM quest 2 done (rows-root bracket 0.128; re-pins with reasons; WASTE: admit/refuse lines owed in the message).
- K17-HEAD DONE (381K, retired): Rows.lean repaired (no statement changed; + takeList_sublist, under_sublist, dropList_weight, dropHeads_weight); RowsHead.lean: World.RowsOk, genesis_/receive_genesis_/admit_ (hE: E.Lawful — needed: dropHeads/checkRowsRemain list a parent by its id's bytes)/refuse_/fold_/carry_rowsOk, head_sum, fold_head_sum, deployed_fold_rowsOk, admit_rows_listing; teeth rowsHeaded_head_bumped, plantInsert_breaks_rowsOk, rowsParented_orphan_head.
- K17-RANGE follow-ups DONE: fold_range_exact (RowsRangeDeployed.lean; no open premise); byte family moved to Kernel/Proofs/Bytes.lean (now imports Kernel.World), BitLt core to new Kernel/Proofs/TrieOrder.lean; Codec SlotOrder/TrieOrder copies deleted (CODEC-9 agreed). CODEC-10's codec10-rows.patch applied (RowsReached: rowsCodecFits_of_ok; rowsListing moved to Codec/World.lean). Snapshot joint6.
- K17-COMM next: insN/insA to World.lean; checkWith/commitWith/admitImpl + @[csimp] admit_eq_admitImpl (commit reuses check's rows; halves row-insert hashes).
- ROOT 10-18: the four strengthenings ACCEPTED. cv 01a14df5-527e: do NOT redesign the trie today; pin `admit hashes-per-row-insert` at the measured value with reason "the one trie, uncompressed, over the parent‖rel prefix; cv 01a14df5-527e". AFTER the landing: propose KERNEL-49 pricing PREMISES before hashes: (a) path compression in the one trie (enumerate the theorem/root spread), (b) two-level: each relation's rows in their own subtrie keyed by the short key, head holds the subtrie root (range pins, carry, listing), (c) accept the cost, bounded by rowsPerRelationMax. ROOT rules after reading.
- Rebased onto main 06876d1 (PROTOCOL-45 receipts; no overlap). PROTOCOL is now PROTOCOL-10 afa6834d506757f31 (ask it for rows before landing; the receipt verb reads the roots digest). Reader K17-READER a35468867eca39dd7 spawned (read-only).
- Applied PROTOCOL-10's logs/protocol10-rows4.patch (receipt gains rowsroot; 4-root digest). QUEUE after the rows day (PROTOCOL-10's asks, cv 01a14dfa-200a + 01a14d95-36b0): refusal_inclusion_sound / refusal_exclusion_sound (refusalDigest injective < 2^64), refusal_prove_verifies / refusal_prove_absent, a prune-horizon theorem (a recorded .tx refusal kept while journalForgets is false), lower: chain-anchored receipt (World keeps its last head link + head_roots_read).
- Reader K17-READER: LAND-WITH-FIXES; no cell reader gained an unsanctioned premise. Fixes taken: (1) HOST half joint (applied host12-rows.patch f5872f31; waste.tsv merged by row key — HOST's diff had dropped SIM's 4 rows, restored); (2) rowStep's declare now refuses a pin (`req x.seen.isNone (.rowShape p)`, one encoding per effect) — Rows/RowsHead obtain patterns fixed; (3) CODEC-10 codec10-rows2: Deployed.fold_rowsCodecFits (applied); (4) RANGE: range_admit_satisfiable (a concrete admitted turn with a range read, by decide; dropped-row pin refused); COMM: admit_comm_rows (in flight).
- K17-COMM: World.checkWith/commitWith/admitImpl + private @[csimp] World.admit_eq_admitImpl; insN/insA public. SIM re-pinned row-insert 564.071, row-retract 569.000 with ROOT's reason.
- Full `lake build` on joint7 (logs/kernel17-joint7.patch md5 7f32b958): reds only in LANG-14's pending final (Lang/Proofs/{Wire,Need,Print}, Protocol/Command/Describe, Hosting/Proofs/Deployed, Ledger/Sim/Journey).
- ALL FOUR HALVES ASSEMBLED (LANG-14 final lang14-rows.patch 7d02a158 + its two reader fixes; HOST-12 f5872f31; CODEC-10 rows/rows2/rows3; PROTOCOL-10 rows4). Verdicts on db0b43c: lake build 491 green; kernel-sim 64 ALL PASS; lang-journey GREEN; ledger-sim ALL PASS; host-sim/host-file-sim/hosting-sim 1-3 ALL PASS; store-plants ALL PASS; rows 26/26 (PROTOCOL-10); CODEC-10 census 48/48 + vectors/emit checks; cargo client 7/10/2/1/1/1, clippy, fmt clean. Reader re-read: LAND-WITH-FIXES, fixes taken (badRel_reads_other stays native_decide in the repo's census form: axioms-allow + tcb).
- Landing attempt 1 launched on main 6558c56: scripts/commit PID 3203320 (logs/kernel17-land1.pid), log logs/kernel17-land1.log, message logs/kernel17-msg.txt (local copy scratchpad/k17/msg.txt).
- **LANDED 42c261b** kernel! rows day (104 files; pushed). Attempt 1 RED on runs: waste admit touched-cell/nullifier + refuse record-bytes back at old ceilings (HOST's waste delta had reverted K17-SIM's re-pins in my row-key merge) — fixed forward, attempt 2 PRE-PUSH GREEN. ROOT and partners told.
- NEXT (KERNEL-17 or successor): KERNEL-49 proposal for ROOT (trie cost: (a) path compression — enumerate the theorem/root spread, (b) two-level rows subtries with the head holding the root — range pins, carry, listing, (c) accept, bounded by rowsPerRelationMax; premises priced before hashes); PROTOCOL's refusals-trie soundness asks (refusal_inclusion/exclusion_sound, refusal_prove_*, prune horizon; cv 01a14dfa-200a, 01a14d95-36b0) — offer to PROTOCOL-11 a0b1899e3383e7392; admit_comm with retires and ranges over unrelated relations; byteBit to a lower def module so Kernel/Proofs/Bytes need not import Kernel.World; then the KERNEL-15 list (cv 01a14da3-3e7a, 01a14d95-36b0, 01a14d95-36cf, 01a14afe-7380, 01a14a8a-7364, 01a14aa3-ca32).
- KERNEL-49 PROPOSED landed 23ac379 (decision only; drafted by K17-K49 abff9db004b0cd8b4, read by me): recommends (a) path compression, depth in node hash, Spec.depth_lt field (0 premises), ~97 restatements, every root + receipt wire re-cut; Q49 to ROOT. Waiting ROOT's ruling.
- K17-REFH a27ca13492138e525 writing Kernel/Proofs/RefusalsHead.lean for PROTOCOL-11 (refusal_inclusion/exclusion_sound + head forms, refusal_prove_*, prune horizon at the head). I commit it; tell PROTOCOL-11 the sha.
- ROOT ruled KERNEL-49 (a) APPROVED; Q49: depth as a Spec FIELD. Conditions: (1) the reader lists every restated statement (~97) with "no cell reader gained a premise"; (2) the proof wire gains a u16 per sibling and the receipt is re-cut (PROTOCOL-11); listings and all three pin kinds stay byte-identical, with a plant per pin kind showing its bytes do not move; (3) KERNEL-35's per-node empty-digest plumbing DELETED; (4) WASTE rows re-pinned DOWN with measured values, ceilings falling; (5) the 2610 depth bound stated in the decision as what (c) would have had to print. The serial Trie day goes to KERNEL-18, not me.

### KERNEL-17 HANDOFF (written 2026-10-18 after landing 42c261b + 23ac379; ROOT stopped me at the ceiling)
Landed by me: **42c261b** kernel! rows day (four halves; message hbox logs/kernel17-msg.txt) and **23ac379** kernel: KERNEL-49 PROPOSED (the trie-cost decision). wt/kernel is at 23ac379 and clean, apart from ONE untracked file: Kernel/Proofs/RefusalsHead.lean (see below).

**1. RefusalsHead.lean, for PROTOCOL-11 (a0b1899e3383e7392). IN FLIGHT** with my lane K17-REFH (agent a27ca13492138e525; resume it with SendMessage, it holds the context). Owed:
- refusal_inclusion_sound / refusal_exclusion_sound over RefusalsCanon, with refusalDigest injective below 2^64, and the head forms head_refusal_read / head_refusal_absent via head_roots (4 roots);
- refusal_prove_verifies / refusal_prove_absent;
- the prune horizon at the head, restated from fold_refused_retains if that already states it;
- the last head link as a PROPOSAL only (it needs a World field).
Then: read its statements, land as `kernel:` (new proof module: SIZE lines), and tell PROTOCOL-11 the sha. PROTOCOL-11 deletes its local refusals_prove_verifies/absent in Protocol/Proofs/Receipt.lean, points check_build at Kernel's, and restates check_refused as soundness over (1).

**2. THE TRIE DAY (KERNEL-49 (a), ROOT-approved with the 5 conditions above). KERNEL-18 lands it, with the theorem list SPLIT among lanes from the start.** Design: decisions/kernel.md KERNEL-49 (23ac379).
- Kernel/Trie.lean (serial; every other lane parked on the rebuild):
  - `T.node h b l r` with b = the branching bit; nodeHash = H(2 ‖ u16 b ‖ l ‖ r);
  - `Spec.depth_lt : depth < 2^16` as a FIELD (four instances by decide: 257, 256, 328, 1304);
  - build skips agreeing bits; insAt splits an edge; join returns the non-empty side whole;
  - getAt, proveAt, climb and retainAt follow b;
  - `Proof.sibs : List (Nat × D)`; the verifiers check that b strictly increases and stays < depth;
  - `under` gains a representative-key check when b jumps past the prefix;
  - DELETE the EmptyDigest parameter everywhere below the root (mkNode, build, insAt, proveAt, join, retainAt, rowStep, setHead, rowsRun, dropHeads, commit's shared e only at the four roots).
- The restatement list, measured by K17-K49's greps (helpers hbox logs/k49-spread.py, logs/k49-stmt.py):
  - Kernel/Proofs/Trie 20/46; TrieRetain 8; TrieMap 1;
  - Codec TrieOrder 8, TrieOrderDeployed 7, SlotOrder 6, RowOrder 2;
  - Rows 11, RowsRange 5, RowsHead 14, RowsComm 15;
  - proofs re-done with statements unchanged: Value 7, Weight 6, Cells 6, JournalHead 5, RootedDeployed 10, RowsSep, plus Protocol/Proofs/Receipt.
- Suggested lane split (veterans first: K17-RANGE a3a0aa2d594a5e5ed knows under/RowsRange and Bytes/TrieOrder; K17-COMM a6bcaa8badce6a08e knows admit/RowsComm/RowsSep and the csimp; both are near 320–360K, so prefer fresh lanes briefed from their files):
  - A: Kernel/Trie.lean + Kernel/Proofs/{Trie,TrieMap,TrieRetain} — the core, serial first;
  - B: Rows/RowsHead/RowsComm/RowsSep;
  - C: RowsRange + `under` + Bytes/TrieOrder;
  - D: Cells/JournalHead/RootedDeployed/Value/Weight + RefusalsHead;
  - E (K-sim): WASTE re-pins DOWN (hashes-per-row-insert ~9, -retract, -touched-cell ~7.3, -nullifier, -journal-entry, -prune, refuse hashes-per-refusal), NEW hashes-per-row-insert-stem (64 u64-counter keys), proof bytes-per-inclusion, the plant depth-unhashed (a forged exclusion VERIFIES under the plant and refuses at main), and canon_no_empty_child + its negative;
  - a read-only vacuity reader (condition 1).
- Partners:
  - CODEC-11: Codec/Proofs/{TrieOrder,TrieOrderDeployed,RowOrder,RowsReached,WorldTooth,SlotOrder}, the proof wire's u16 per sibling, and the vectors re-emit (every root moves);
  - HOST: the stamp flip; every Store re-geneses;
  - PROTOCOL-11: the receipt re-cut (jdepths/rdepths), plus rows ALL PASS before the landing.
- Plants (condition 2): one per pin kind (cell pin, row pin, range pin), showing the pin bytes do not move across the change. The listings stay byte-identical (the World and carried wire is toList).

**3. Other opens:**
- admit_comm with retires, and with ranges over unrelated relations (the under lemma has landed now);
- byteBit to a lower def module, so Kernel/Proofs/Bytes stops importing Kernel.World;
- LANG's cv 01a14e16-78ac (editsOf_under ↔ invoke_ok);
- the KERNEL-15 list: cv 01a14da3-3e7a (CODEC waits on refusalsCounted), 01a14d95-36b0, 01a14d95-36cf, 01a14afe-7380, 01a14a8a-7364, 01a14aa3-ca32.

Facts:
- The commit helper is hbox logs/kernel17-land.sh N; it edits the path list inline. scripts/commit runs under `nohup bash -c 'exec …'` with its PID file.
- The build helpers are logs/kernel17-kb.sh TAG TARGETS and kernel17-kw.sh TAG.
- When merging gates/waste.tsv from several halves, merge by (op, metric) key against EACH patch's own base blob. My first merge let HOST's stale rows revert SIM's re-pins, and pre-push caught it on `runs`.
- `lake build Kernel` globs in-flight lane files. A lane's half-written file reds the umbrella, so build named targets while lanes work.
- ADDENDUM to the handoff: K17-REFH FINISHED. Kernel/Proofs/RefusalsHead.lean is GREEN and UNCOMMITTED in wt/kernel (408 lines; build logs hbox logs/k17-refh-b2.log, b3-kernel.log; closure ok). It is KERNEL-18's first landing (`kernel:` + SIZE lines). Contents:
  - refusal_inclusion_sound (premises: hE, RefusalsCanon, hfit via refusalsOk_fits, hv : RefusalLeaf.Fits v);
  - refusal_exclusion_sound;
  - head_refusal_read / head_refusal_absent (any Step);
  - refusal_prove_verifies / refusal_prove_absent;
  - head_refused_retained / head_refused_not_absent (the prune horizon at the head, from fold_refused_retains);
  - deployed_* forms: absent / retained / not_absent have no premise left; read keeps only the leaf's Fits;
  - teeth refusal_inclusion_wrong_leaf, _other_key, refusal_exclusion_held, refusalDigest_wraps + refusal_inclusion_unbounded (the Fits plant);
  - the last head link is a PROPOSAL only: a World field holding the last link's preimage.
  Note: Protocol/Proofs/Receipt.lean has NO local refusals_prove_* at 42c261b, so PROTOCOL-11 just points at the Kernel names. Tell PROTOCOL-11 a0b1899e3383e7392 the sha when it lands.

## KERNEL-18 (successor of KERNEL-17; started 2026-10-19; hbox wt/kernel)
- **LANDED 02c36d0** kernel: RefusalsHead.lean (needed SIZE lines: Lean modules, proof-modules, Lean lines (Kernel), max dependents, theorems). PROTOCOL-11 told; it repoints check_build. PROTOCOL-11's window-width ask accepted as my next commit after the day: cv 01a14e3c-f292 (checkRefusedBounds refuses validUntil > notBefore + windowMax; theorem refused_window).
- main moved to a38b84b (PROTOCOL-46). wt/kernel holds the staged shape uncommitted: Kernel/Trie.lean (compressed), Kernel/World.lean (e deleted, under over b and rep), Codec/World.lean (one pattern). Patch logs/kernel18-trie.patch (md5 0ab6dc3b). Kernel.World and Codec.World build green.
- DESIGN AMENDMENT (decisions/kernel.md "KERNEL-49 RULED (a), and amendment 1"): T.node h b rep l r. rep is the first key, NOT hashed. getAt checks k against rep on the skipped bits [d,b); insAt splits there. So get_insert keeps NO premise (a pure-bits getAt would have put Routed on ~60 Frame/Value/Weight uses). Only Trie.inclusion_sound gains Routed S 0 t; its 6 callers hold Canon. ROOT told.
- Common brief: hbox logs/kernel18-brief-common.txt. Build helper: logs/kernel18-kb.sh TAG TARGETS.
- Lanes: K18-A acb245f975f5e5e04 (Proofs/Trie, TrieMap, TrieRetain, TrieOrder; phase 1 = statements building with sorry, then resume for phase 2). K18-E a9550cdbe28833584 (Sim/Gen, the depth-unhashed plant, pin plants, WASTE re-pins down, stem row, proof bytes). B/C/D spawn after A's phase 1.
- Partners: CODEC-11 a40e1943cc87d9b9f (proof wire u16, listings byte-identical, TrieOrder*/RowOrder/RowsReached/WorldTooth; hands logs/codec11-trie.patch); PROTOCOL-11 (receipt re-cut; logs/protocol11-trie.patch); HOST-12 (stamp flip; logs/host12-trie.patch).
- ROOT ACCEPTED amendment 1 with three conditions, all given to K18-A: rep_first (rep is derived); the tooth getAt_wrong_rep plus the general getAt_rep_sound (a corrupted rep only ever refuses); hashOf_rep_irrel / proveAt_rep_irrel (roots do not read rep); the reader names inclusion_sound's Routed premise.
- K18-A phase 1 DONE: the four Trie* proof files build sorried, behind a temporary `set_option warningAsError false`. Premises added inside Trie*, all discharged at callers from Canon or the verifier: prove_excludes + Routed, shape_insAt + Routed (counterexamples in A's report), climb_sound + ascends (u16 wraps at 2^16), wf_mkNode + hb, canon_join + hag. `Under` is now absolute. Phase 2 running.
- Spawned K18-B a8decb4d7f5a22391 (Rows/RowsHead/RowsComm/RowsSep), K18-C a8e7e02f432c46b5e (RowsRange/RowsRangeDeployed/Bytes/TrieOrder), K18-D a8bac2e21f7679836 (all other Kernel/Proofs).
- Applied CODEC-11's logs/codec11-proofwire.patch (78b1f2fa) in wt/kernel. wt is on main 815a031 (HOST-43 6df6a3f; PROTOCOL-11 retired, PROTOCOL-12 ab85c36fd01b6c4eb now owns the receipt re-cut and cv 01a14e3c-f292).
- GATES-5 told to land its gates change now; its kernel-sim --harness-control patch comes after my day, CROSS-LAYER, and I review it.
- K18-E DONE: kernel-sim 64 ALL PASS (logs/kernel18-E-s64.log). WASTE fell: touched-cell 8.900->6.757, nullifier 3.317->2.865, journal-entry 13.672->12.162, prune 539.333->418.333, refusal 26.829->11.410, row-insert 564.071->7.642, row-retract 569.000->6.000, turn-rows-root 0.128->0. New rows: turn-empty-root 1.000 (moved out of the cell, nullifier and rows rows), row-insert-stem 7.515 (worst single insert 11, against (c)'s 2610). Plants added: depth-unhashed, proof-bit:refused, shape-unary, pin-cell/row/range same plus plant. The arm hash-count:empty-per-insert is renamed empty-per-root. Resumed to pin proof bytes-per-inclusion (74+34n) through CODEC's encoder.
- PROTOCOL-12 staged logs/protocol12-trie.patch (2f5c82f8, on its kbase d0c0e9ff). The receipt carries jpath/rpath via Codec.Kernel.proof; dc is threaded through Host/Follow.lean (3 lines, needs HOST's yes).
- K18-D fixed Codec/Proofs/World.lean (no statement changed). CODEC-11 told it is the base.
- K18-A phase 2 DONE (no sorry; axioms are only propext/Quot.sound/Classical.choice). K18-B, C and D DONE. C's range theorems go Routed -> Canon and under_eq gains Shape (forced: under_needs_shape); every caller holds Canon. B: under_parent goes Routed -> Canon; under_range restated at d=0. D: changed only `e` in Checked.rows. Trie.rootWith_eq is now public (I removed D's two private copies).
- joint2 (logs/kernel18-joint2.patch 2cf778dc, base 66815ff): full lake build 493 GREEN, every sim ALL PASS, rows ALL PASS, lang-journey GREEN. closure C3 on RepTooth.toy fixed (made private).
- HOST-12 half: host12-trie.patch d0a30e48 (decisions/host.md HOST-45 only; 24 HOST WASTE rows exactly at their pins). CODEC-11 half: codec11-trie.patch d3db39af (lines file logs/codec11-trie-lines.txt; vectors +4 kernel/proof rows; ListingPin plants). Both applied, giving joint3 26bfb90e. Runs r2 launched. Reader K18-READER a5e119327514e0ff6 running.
- NOTE: logs/kernel18-runs.sh makes store-plants' fresh dir with mktemp, which then exists, so store-plants reads red (rc=2). Run store-plants by hand with a non-existent path, or fix the script when no run is in flight.
- Reader verdict: LAND-WITH-FIXES. All taken:
  - (1) the codec half was assembled;
  - (2) the decision's price list was corrected and measured results added;
  - (3) stale KERNEL-35 prose in World.lean was removed;
  - (4–6) by K18-F a32ef08e51ab34397: RepEq without cached digests, so hashOf_rep_irrel is under WF with a tooth; unary_routed_wf_not_shape replaces the collapse; inclusion_needs_routed / prove_excludes_needs_routed / ascends_bound_needed on an injective toy;
  - (7–8) by K18-E: a real shape scan over every reached World plus the unary plant; the proof-bytes source text marked counterfactual.
- Runs r3 on main 87dff6e: everything ALL PASS, census ok. Attempt 1 refused: worktree behind main, because CODEC's cap had landed separately as 4573cce. Rebased the three codec files, keeping main's comment.
- **LANDED d377d5b** kernel! trie day (40 files; PRE-PUSH GREEN first judge; pushed). Message: hbox logs/kernel18-msg.txt. ROOT and every partner told; LANG unparked; GATES-5 may send the kernel-sim --harness-control patch on d377d5b for my review.
- NEXT: cv 01a14e3c-f292 (checkRefusedBounds refuses a window wider than windowMax; theorem refused_window) for PROTOCOL-12. Then the kernel opens: cv 01a14da3-3e7a refusalsCounted, 01a14afe-7380, 7364, ca32, and cv 01a14e08-7464 (the cancel step, as a proposal).
- **LANDED 8ad3982** kernel: cv 01a14e3c-f292. checkRefusedBounds refuses validUntil > notBefore + windowMax (.overBound .window). New: refusedBounds_window, refuse_window_width (validUntil ≤ recorded height + windowMax), tooth refusedBounds_wide. Fold's local twin and Codec's checkRefusedBounds_fits re-destructured (CODEC-11 agreed; CROSS-LAYER). cv task done. NOTE: the name `refuse_window` already existed in Fold.lean (the in-window half), hence `_width`.
- Reviewed and approved GATES-5's gates5-landb-Kernel.patch (4cd3a380: kernel-sim parseArgs, --harness-control, PLANTS NOT JUDGED below 16 seeds, exit 3; usage exit 2). GATES-5 lands it as part of landing B.

### KERNEL-18 HANDOFF (written 2026-10-18 after landing 02c36d0, d377d5b, 8ad3982; nothing unlanded)
Landed by me:
- **02c36d0** RefusalsHead.
- **d377d5b** kernel! THE TRIE DAY. It includes CODEC-11's proof wire and listing proofs, PROTOCOL-12's receipt re-cut, and HOST-45. Message: hbox logs/kernel18-msg.txt. Decision: decisions/kernel.md "KERNEL-49 RULED (a), and amendment 1" + "Measured".
- **8ad3982** the refusal window-width check.
wt/kernel is clean at main.
Facts for KERNEL-19:
- Trie shape: T.node h b rep l r. rep is NOT hashed; getAt checks rep on the skipped bits, which is why get_insert has no premise. Invariants WF/Routed/Shape/Shallow are in Kernel/Proofs/Trie.lean. Trie.inclusion_sound/prove_excludes take Routed (pass Canon's .1). The rows range readers take Canon.
- Helpers: logs/kernel18-kb.sh TAG TARGETS (build), logs/kernel18-runs.sh TAG (full build + every verdict exe + census + check.py; writes logs/kernel18-TAG-runs.out/.done), logs/kernel18-land.sh N (the trie-day commit; edit its path list for the next day).
- Gotchas:
  - `git diff` snapshots miss untracked new files: list them separately.
  - `git apply --3way` stages into the shared index, so `git reset -q` afterwards.
  - A main that moved under your paths refuses `behind main`: re-diff, `checkout HEAD -- files`, `checkout --detach main`, `apply --3way`, resolve.
  - SIZE lines are required for every metric that rises; the first attempt lists them.
  - The pre-push cargo "test failed" lines are GATES' known-red controls, not reds.
- PROTOCOL-12 retired; PROTOCOL-13 does item 3 (Settle's refused arm made dead using refuse_window_width) and item 4a/4b (protocol log).
Open (in order):
1. The kernel opens: cv 01a14da3-3e7a (CODEC waits on refusalsCounted), 01a14afe-7380, 01a14a8a-7364, 01a14aa3-ca32, and cv 01a14e08-7464 (the cancel step, as a PROPOSAL).
2. admit_comm with retires, and with ranges over unrelated relations.
3. byteBit to a lower def module (Kernel/Proofs/Bytes still imports Kernel.World).
4. Twins worth deleting:
   - Fold.refusedDigest_inj's local `bnd` duplicates Refusals.refusedBounds_lt. Fold is upstream; move refusedBounds_lt down into Fold and delete the local one.
   - Codec's checkRefusedBounds_fits re-proves the same unpacking.
5. The last head link (a World field holding the last link's preimage) is still a proposal.
6. Reader K18-READER's minor item: the row-pin plant (children swapped) is crude; a better plant would perturb getAt's rep check.

## KERNEL-19 (successor of KERNEL-18; started 2026-10-19; hbox wt/kernel)
- cv 01a14da3-3e7a refusalsCounted. ROOT ruled the PER-MEMBER form; the sum form is refused as a containment. The refused leaf therefore names its member: `RefusalLeaf D`, `refused h code member`, `refusalLeafBytes E` (domain v2). This is a `kernel!` day.
- Built in wt/kernel, uncommitted:
  - Kernel/World.lean: refusedOne, refusedIn, tallySpec (no hash), tallyAt, tallyStep, refusalTally, refusalsCounted.
  - NEW Kernel/Proofs/RefusalsCounted.lean: CountedOk, refusalsCounted_iff, refusalCount_eq_of_counted, the preservation lemmas, fold_refusalsCounted, reach / deployed_reach. TOOTH refusalsCounted_moved, stated over an abstract w' with hr/hh because closure C3 forbids a plant def in a proof module, plus refusalsCounted_moved_exists.
  - Sim arms refusals-counted:counted and the plant refusals-counted-plant:refused, both in plantedArms.
  - The only premise added anywhere: hE on refusalLeafBytes_inj / refusalDigest_inj. Their callers already held it.
- Cross-layer half (Codec site kernel/refusals-counted plus vectors, the Protocol receipt member, Host) is done by the helper lane K19-X in wt/kernel. Routing: PROTOCOL-13 a8b9027b0e85da990, HOST-13 a55e9ab90683e7922, ROOT for CODEC.
- Decision drafts: scratchpad k19/dec50.md (KERNEL-50) and dec51.md (51 frame, 52 head-read). ROOT APPROVED 51 and 52, to come after this day, 51 before 52, with conditions (see ROOT's message: not_cellFoot_iff named as the reader's evidence; the dropped-heads correction in the critique; the RowsComm twins deleted; ratchet and hub before/after; the 52 corollaries keep their names; per-instance premises listed).
- Build helper: logs/kernel19-kb.sh TAG TARGETS.
- QUEUE add (PERF-1 via ROOT): honest write contention spends the refusal budget (stale is 0.75–4.25 % of writes; an N=1000 run reached refusalBudget). Propose the budget shape: a separate contention budget, or stale excluded from the budget and bounded another way. Price it in premises. Numbers: PERF-LOG.md ## PERF-1 FINDING 2.
- QUEUE add (PERF-1): a recorded refusal costs TWO Ed25519 verifies. judge → submit (Derive.lean:18 verifies), and on error authenticated verifies again; every follower's auditRefusal takes the same path. Fix: thread the verify result from submit into authenticated, then pin a WASTE/bar verifies-per-step row at 1 with a plant. Its own kernel: commit, after this day.
- **LANDED f82a6b0** kernel! KERNEL-50 refusalsCounted, on the 3rd attempt. Attempt 1 lacked two SIZE lines. Attempt 2 hit cargo launcher:isolation TIMEOUT 600 s under load, a flake: attempt 1's runs were ok and no Rust is touched. Attempt 3 was CAS-retried three times while main moved.
  - It refuses: a base whose window counts are not its records' (a lowered or moved charge, or more records than steps). The site kernel/refusals-counted comes after kernel/steps.
  - Partners: PROTOCOL-13 YES (Settle Windowed arity, fixed in my tree), HOST-13 YES, ROOT for CODEC YES.
  - Reader K19-READER: LAND-WITH-FIXES; all six taken, including refusalsCounted_moved_sum and the plant's f.id≠o guard.
  - WASTE: no row moved.
  - cv task 01a14ef0-ffe7 filed for PROTOCOL: the Receipt bytes round-trip theorem.
- NEXT, in order: KERNEL-51 frame scheme (approved) → KERNEL-52 head-read scheme (approved) → 01a14afe-7380, 7364, ca32 → cancel-step proposal. Also queued: the double verify per refusal (PERF-1) and the contention-budget proposal (PERF-1).
- **LANDED 03943ee** kernel: KERNEL-51, the frame rule as one scheme (built by lane K19-F; reader K19-READER2 LAND-WITH-FIXES, all four were decision-text fixes and all taken).
  - `Frame` has the fields cells (no premise), rows, journal and refusals, each under its own Canon. I removed height/steps/origin, which were twins of admit_*. Also `not_cellFoot_iff` and teeth `cellFoot_needs_born` / `rowFoot_needs_head`.
  - Deleted: the RowsComm twins and `rowStep_get_other`, the latter replaced by `rowStep_get_out`.
  - theorems 3890→3891, with the reason in the critique: the "~22 restatements" do not exist, and the fall is in check_local (cv 01a14f65-48ec). Hub 229→230.
  - My own "dropped heads because checkRowsRemain" correction was WRONG: dropHeads filters to heads by definition. That is recorded in the critique.
- NEXT: KERNEL-52 (head-read scheme, 4 instances).
- **LANDED 748b11d** kernel: KERNEL-52, HeadSound (built by lane K19-H; reader K19-READER3 LAND).
  - Three records (cells, journal, refusals) and twelve corollaries, statements unchanged.
  - theorems +7: it did not pay on the ratchet, because the corollaries are kept by name.
  - Three instances, not four: RowsHead has no head reads, and my "four" claim was ungrepped.
  - Rows key encoding: byte8 wraps rel and key length, so the rows cannot be an instance. Not live. cv 01a14f7e-d65a.

### KERNEL-19 HANDOFF (written 2026-10-19 after f82a6b0, 03943ee, 748b11d; wt/kernel clean at main)
Landed: f82a6b0 (KERNEL-50 refusalsCounted, kernel!), 03943ee (KERNEL-51 frame), 748b11d (KERNEL-52 head-read).
Queue for KERNEL-20, in order:
1. cv 01a14afe-7380: a draw-independent hash ratio. Count the design's required hashes from the final trie shape and pin the ratio at ~1. Plant: the per-insert recomputation. Delete the two draw-sensitive WASTE rows.
2. cv 01a14a8a-7364: discharge fold_prune_check's window premise hv on Honest logs (with a digest-collision disjunct).
3. cv 01a14aa3-ca32: receiveWith reads c.unsigned.world only through the signed bytes.
4. cv 01a14e08-7464: the CANCEL step, as a PROPOSAL only (price premises first; ROOT rules).
5. PERF-1, a law-5 cost: a recorded refusal costs TWO Ed25519 verifies (judge → submit verifies, then authenticated verifies again; auditRefusal too). Thread the verify result through, and pin verifies-per-step at 1 with a plant.
6. PERF-1: honest contention spends the refusal budget (stale 0.75–4.25 % of writes; an N=1000 run reached refusalBudget). PROPOSE the budget shape (a separate contention budget vs stale excluded and bounded another way), priced in premises. Numbers: PERF-LOG ## PERF-1 FINDING 2.
7. cv 01a14f65-48ec: check_local, the locality half of the frame rule. This is where the predicted theorem fall is.
8. cv 01a14f7e-d65a: an injective rows key encoding, then the rows as the 4th HeadSound record.
9. KERNEL-18's leftovers: admit_comm with retires and unrelated ranges; byteBit to a lower module; the twins Fold.refusedDigest_inj's local bnd and Codec checkRefusedBounds_fits; the last-head-link proposal; a better row-pin plant.
Helpers: logs/kernel19-kb.sh (build), logs/kernel19-runs.sh TAG (every verdict), logs/kernel19-land*.sh (scripts/commit with an explicit file list; add SIZE lines up front for every rising metric, which the first attempt lists).
Lessons:
- Twice this session a design's predicted count (KERNEL-51's "~22", KERNEL-52's "four") was never grepped. Grep before you predict.
- My dropped-heads "correction" read a check where a definition did the work.
- Lanes do the heavy proofs well with exact briefs; keep the root's context for reading and landing.

## KERNEL-20 (successor of KERNEL-19; started 2026-10-19; hbox wt/kernel)
- Helpers: logs/kernel20-kb.sh TAG TARGETS (build), logs/kernel20-runs.sh TAG (every verdict), logs/kernel20-land53.sh N (scripts/commit, CROSS-LAYER reason inside), logs/kernel20-stmts.py ROOT "pat,pat" (lists theorem statements that name the patterns: use it to price premises).
- KERNEL-53 (queue item 1, PERF-1 FINDING 3): one verify per judgement. Verdict.verified + checkSignatureBy + authenticatedBy + judgeBy; judge = judgeBy … (authenticatedBy … v.verified). Theorems in Kernel/Proofs/Audit.lean: submit_verified, authenticatedBy_verified, judge_eq (= judgeBy … fun _ => authenticated), teeth verified_eq_false_iff, authenticatedBy_verify_irrel. Sim: verifyingCtx, <G/<H brackets, judgeTwice = judge_eq's RHS, exact per-seed check, arm verify-count:once; mutation proven (two-verify judge FAILs at 2.000). WASTE new row refuse verifies-per-refusal 1.000. Cross-layer one-token proofs: Host/Proofs/Serve.lean:54 (HOST-13 yes), Protocol/Proofs/Settle.lean:30 (PROTOCOL-14 YES). Reader K20-READER LAND-WITH-FIXES, both taken. Residue cv 01a14f94-e90f (badSignature is spellable by Ctx.program, so forged-signature declines cost 2 verifies).
- KERNEL-54 PROPOSED (queue item 2, contention budget): hbox logs/kernel20-dec54.md. Options (A) separate stale budget, (B) structural bound (refused on price), (C) monotone pin versions so stale is final without a record. Recommends (C). It disputes the brief's premise "stale must stay recorded", and says so. For PROTOCOL-15 (PROTOCOL-14 stopped) to co-sign the attempt side.
- **LANDED c18e028** kernel: KERNEL-53 (one verify per judgement), 4th attempt. Attempts 2 and 3 were refused only for missing SIZE lines: the rows are "Lean lines (deployed)", "Lean lines (tooling: …)" AND "Lean lines (Kernel)", all three needed. Attempt 1 was behind main on waste.tsv. PERF-1 told to re-measure; worstcut row prose is PERF's to fix.
- KERNEL-54: ROOT accepted (C). STEP 1 measured by K20-MEASURE (logs/kernel20-measure.md): N 0 premises vs H′ 3 / pure H ≥5, 356 statements. RULED: shape N varint in Entry.live, row ver, head floor (retract-bumped), pinOf over Entry, W0 BEHIND/AHEAD, missingRow rename, judge declines stale. Text: hbox logs/kernel20-dec54-ruled.md (append to decisions/kernel.md on the landing). W1 filed cv 01a14fc3-d848.
- K20-K (= K20-MEASURE resumed, agent a860ac08434255514) builds the kernel half, phase 1 (defs + final statements, proofs sorried) in wt/kernel → logs/kernel20-K-phase1.md. PROTOCOL-15 a8caf1ad558b4a601 asked to co-sign the attempt side. Partners still to route: CLIENT-8 a4b5ab24321e18c7e (client pin sites), HOST-14 a4d3aa9099adf145c (base bound, Host/Sim/Run.lean .stale 0), ROOT for CODEC/LANG.

### KERNEL-20 HANDOFF (written 2026-10-19 after c18e028; wt/kernel is being edited by K20-K, phase 1 of KERNEL-54)
Landed: c18e028 (KERNEL-53, one verify per judgement).
In flight: the KERNEL-54 kernel! day (ruled: shape N varint, W0, three amendments). Text: hbox logs/kernel20-dec54-ruled.md. Measurement: logs/kernel20-measure.md and logs/k20m-class-full.txt.
- K20-K (agent a860ac08434255514, was K20-MEASURE, ~250K tokens in at resume): phase 1 = definitions plus final statements, proofs sorried, written to logs/kernel20-K-phase1.md; then it waits. The successor reads phase 1 and checks that no cell reader gained a premise (a pause item if one did). Then phase 2 proofs (split them across lanes if K20-K is near its ceiling; it writes its own continuation file).
- Partners to route before landing: PROTOCOL-15 a8caf1ad558b4a601 (asked to co-sign the attempt side, AHEAD → open / BEHIND → refused, plus the Protocol/Rows.lean 709–742 A→B→A journey); CLIENT-8 a4b5ab24321e18c7e (~18 client pin sites read the Entry); HOST-14 a4d3aa9099adf145c (base-bytes bound 3.912 vs 4 with the varint; Host/Sim/Run.lean's two `.stale 0` records); ROOT for CODEC (entry/row-leaf/range-pin codecs as varint, vectors) and LANG.
- Then: the reader (statements only, every changed statement listed), runs (logs/kernel20-runs.sh), a land script modelled on logs/kernel20-land53.sh with all three Lean-lines SIZE rows up front, and the decision appended to decisions/kernel.md.
Queue after KERNEL-54: cv 01a14afe-7380 (draw-independent hash instrument; see the note below), cancel step 7464 (proposal), 7364, ca32, check_local 48ec, the rows leaf encoding d65a, KERNEL-18's leftovers.
Note for 7380 (read, not built): commitTrie inserts sequentially (insertAll = a foldl of insert), and insAt's `.leaf` case `build`s the old leaf again (mkLeaf of a key whose hash was cached), so a leaf-split insert pays one avoidable leaf hash. A "required hashes" denominator (the nodes on each inserted key's path in the post-trie, plus the leaf) would read above 1 by exactly that. That is a law-5 finding to price alongside the instrument.
Residue filed: cv 01a14f94-e90f (badSignature not attributable, so forged declines cost 2 verifies); cv 01a14fc3-d848 (W1).
Lesson: the SIZE gate names three Lean-lines rows (Kernel / deployed / tooling); a Kernel change that touches Sim and Receive needs all three.

### KERNEL-20 addendum (after the handoff above)
- PERF-1 reported the audit path still double-verifying on c18e028. NOT reproduced: scripts/bar.sh --records 1000 (full mode) in wt/kernel at c18e028, bench-count with a local per-step-kind diagnostic (reverted), read verifies = steps (503/503 with 5 refusals at 5 verifies; 510/510). PERF-1's tree probably ran a stale bench-count (ASSUMED). The kernel-sim audit arm (<U, exact audit = judge, WASTE audit verifies-per-refusal 1.000) is landing as logs/kernel20-land53b.sh attempt 1 (msg logs/kernel20-msg53b.txt). PERF-2 a4fa91de1b873e3bf was asked to re-measure in a clean tree and to correct a18d6ea's false worstcut prose.
- K20-K moved to its own worktree wt/k20k (it will report phase 1 there). The ROOT answer to its Codec closure blocker was (A): compile-only nat64 placeholders in the Codec files, sorried, every edit listed for ROOT-for-CODEC.
- PROTOCOL-15 co-signed KERNEL-54's attempt side YES with 5 conditions, all accepted (see its message: BEHIND→refused / AHEAD→open from the own fold; an unplaceable planning World → open; absent → confirm with follow; the rows budget teeth move to a recorded class; Protocol pin sites in the same flag day). Fold them into the decision text at landing. Send it the phase-1 path when it builds.
- KERNEL-55 (ROOT item: is a create's triple payment double-counting; what worldBytesMax protects): lane K20-P55 (af38092a5ef2fc00d) is drafting the proposal to hbox logs/kernel20-dec55.md. HOST-14 a4d3aa9099adf145c co-signs; PERF-2 benches the bound that gets set.

### KERNEL-20 FINAL HANDOFF → KERNEL-21 (supersedes the queue in the handoff above)
Landed by KERNEL-20: c18e028 (KERNEL-53). In landing: logs/kernel20-land53b.sh attempt 3 (the kernel-sim audit arm + WASTE `audit verifies-per-refusal 1.000`, CROSS-LAYER GATES-6 agreed). Its pid is logs/kernel20-l53b-3.pid and its log logs/kernel20-l53b-3.log. If it was refused `behind main on gates/waste.tsv`, re-diff waste.tsv onto main (see logs/kernel20-waste3.patch) and run it again as attempt 4. wt/kernel then returns to main.
**Your two items, both ROOT-ruled:**
1. **KERNEL-54 phase 2** (the 99 sorry). Start from hbox logs/kernel20-K-phase1.md, kernel20-K-phase1.diff and k20k-stmtdiff.tsv; the tree is wt/k20k (base c18e028; K20-K has stopped at its ceiling). Decision text: logs/kernel20-dec54-ruled.md. Add these ROOT rulings to it:
   - (a) `live_inclusion_sound` and its deployed twin: the hypothesis moves from Cell.Fits to CellFit (live cell v), strengthened, not added. Record it as THE one cell-reader statement whose hypothesis changed.
   - (b) private `setHead_inv` gains `hfl`: accepted.
   - (c) the rows/range `stale_behind_forever` carry a `w'.live parent = none` disjunct, plus a TOOTH for the dropHeads reset (an old absent-row pin recurs after the parent retires; the call is refused orphanRow and never admitted). Correct the measurement note that said the floor never resets.
   - Weight charges the BOUND (8 B per version, law 4); disk uses the varint; the base-bytes rows measure the actual.
   - CODEC needs a u64 varint: a new site with a boundary pair and lawfulness (ROOT for CODEC).
   - The +1 rejection-code shift (overBound .version, staleRecorded, missingRow) and the three WASTE rises (record-bytes-per-refusal 527.202→529.217, hashes-per-row-insert 7.642→7.733, bytes-per-inclusion 257.133→257.797) are accepted, reason "the version field".
   - PROTOCOL-15's five conditions go in (they are in my message log above).
   - Partners: PROTOCOL-16 aaa9e34f332c75994 (it has the phase-1 path; it is also landing `rangeOf` in World.lean/Call.lean with my yes, so rebase over it), CLIENT-8 a4b5ab24321e18c7e, HOST-14 a4d3aa9099adf145c (Host/Sim/Run.lean's two `.stale 0` records, which the audit now refuses as staleRecorded; the base-bytes bound), ROOT for CODEC/LANG.
2. **KERNEL-55.** The proposal is hbox logs/kernel20-dec55.md. ROOT ruled:
   - Q1 = B: keep allowanceMax 2^27 and DERIVE worldBytesMax (≈84–87 MB) from `allowance_bounds_world` (137·weight + 76·allowance never rises). Delete both ratios' prose (Host/Bounds "~900 BAR stores", Bounds "the other half is headroom").
   - Q2: R2 if membersMax is a Bounds constant (then the kernel-wide refusals bound 16 × membersMax is a THEOREM, with no new check); otherwise R1 (a kernel-wide cap per window). Check that fact first.
   - Q3: import refuses a carried allowance above allowanceMax, by name, with a tooth (the wedge is a real defect).
   - Q4: HOST-14 co-signs now.
   - Q5: the refusals trie's bytes fold into the bound via Q2; framing and index.log are HOST-14's theorem.
   - PERF-2 a4fa91de1b873e3bf waits for the bound to bench the worst reopen.
**Later queue:** cv 01a14afe-7380 (draw-independent hash instrument, plus the leaf-split re-hash finding noted above), cancel step 7464 (proposal), 7364, ca32, check_local 48ec, rows leaf encoding d65a (KERNEL-54 touches row leaves: do the injective encoding in the same day if it is cheap), KERNEL-18's leftovers.
**Lessons:**
- Measure the claim before relaying it: PERF-1's double-verify re-measure was a stale binary, and a18d6ea landed false prose built on it.
- The SIZE gate has three Lean-lines rows.
- gates/waste.tsv needs GATES named in --cross-layer.

## KERNEL-21 (successor of KERNEL-20; started 2026-10-18; hbox wt/k20k for KERNEL-54, wt/kernel for the rest)
- Main b9ce5a7 = KERNEL-20's land53b landed (audit arm). wt/k20k moved onto b9ce5a7 by `git checkout -m` (3-way, no conflict; only Kernel/Sim/Gen.lean overlapped). Backup of the phase-1 work before the move: logs/kernel21-k20k-at-c18e028.diff + logs/kernel21-Versions-phase1.lean. `lake build Kernel` green at the new base (logs/kernel21-b0.log; helper logs/kernel21-kb.sh start|wait TAG TARGETS).
- Sorry census (code only, logs/kernel21-sorries.tsv via logs/kernel21_sorries.py): 99 = Kernel 86 + Codec 13 (the Codec 13 are ROOT-for-CODEC's placeholder proofs, CODEC's half).
- Phase 2 lanes (all in wt/k20k, file-disjoint, check with `swarm-build lake env lean FILE`, NO lake build until they finish): head a212498289cada2b9 (RowsHead, RowsSep); comm a32bcfe06d1c4c8b2 (RowsComm; may change PRIVATE helper statements, listed); val ac29fafd3e4600e4c (Value, Weight); cell a9a4e7bf116f40bf5 (Rooted, RootedDeployed, Cells, CellsFit, Frame, Admit, Ledger); rows a16af2b1050e7ef3c (Rows, RowsRange, RowsRangeDeployed, Audit); ver af3103cd985e3d710 (Versions + the dropHeads tooth ROOT asked for). Continuation files: logs/kernel21-<lane>-continue.md.
- LANG-17 told "go first" (LANG-57 lands before KERNEL-54; I rebase).
- HOST-14's halves: logs/host14-k54-k55.md. KERNEL-54: base-bytes row must stay ≤ 4 (>4 = stop, bring the number); Host/Sim/Run.lean:669 and :924 `.stale 0` → `.rejected (.relationFull 0)` with expected strings, :701 pinOf → entry, :735 `.row` arity — I edit these in the kernel! commit under --cross-layer, HOST-14's agreement is that message; send HOST-14 any reopen statement diff + host-sim / host-file-sim logs seeds 1–3 before landing. KERNEL-55: co-signs B; allowanceMax 2^27 primary, Φ check at genesis AND import with two arms (allowancePastBound = Q3, potentialPastBound = Φ); ordering 54 → 55's kernel theorems → CODEC world_size_eq → HOST commit.
- KERNEL-55 facts read: membersMax is NOT a Bounds constant (Lang/Std membersMax = 63 is the quorum mask; Receive/Call enrollMax = 256 is per grant; no membership theorem) ⇒ Q2 = R1 (kernel-wide refusals cap per window). And KERNEL-54 MOVES the potential's constants: a declare's growth gains the head floor (+8) and inserts gain the row version (+8) while the log does not carry them, so 61·g ≤ 76·L at s ≥ 34 no longer holds (declare: 61(s+50) ≤ 76(s+27) needs s ≥ 67). The ratio is recomputed on the post-54 Turn definitions; the ≈84–87 MB figure moves with it.
- Lanes cell, head, comm DONE (0 sorry each, no statement changed, helpers: comm added private headFloor_view, headFloor_step, entry_of_get). Host/Sim/Run.lean patched in wt/k20k per HOST-14 (logs/kernel21_hostsim.py: .stale 0 → .relationFull 0 ×2, expected strings + docstring, entry reader, `.row 2 … 0`). Partners asked for staged patches: CLIENT-8 logs/client8-k54.patch, PROTOCOL-16 logs/protocol16-k54.patch; ROOT routed CODEC-12 ae211cadad0f1ed00 → logs/codec12-k54.patch. ROOT: Q2 = R1 accepted; KERNEL-55 text states BOTH pre- and post-54 derived figures.
- Lanes rows, val DONE (0 sorry; rows added private code_ne_staleCode in Audit.lean; val no helpers). Kernel sorry left: Versions 4 (lane ver).
- CODEC-12 (ae211cadad0f1ed00): Codec/ and Emit/ are its, my four placeholder Codec files get superseded by its patch. Wire: LEB128 shortest `Codec.Stream.varint64`, max width K = 10 (`varint64_size_le`), Shape code 20. So the version's disk bytes exceed the 8-B weight above 2^56: weight charges the bound, the size bound reads K = 10.
- KERNEL-55 constants, post-54 (read from wt/k20k Turn.lean / World.lean rowStep): the tight term is still a declare (no pin allowed: `req x.seen.isNone`), s = head slot 34: growth s + 50 = 84, log s + 27 = 61 ⇒ r = 84/61 (pre-54: 76/61). Every other term below it (create (40+cw)/(32+cw), cw ≥ 9; insert/upsert ≤ 56/49; write < 1; nullifier 1). Potential Φ = 145·weight + 84·allowance; f = 84/145 ≈ 0.5793 (pre-54 76/137 ≈ 0.5547). worldWeightMax − genesis at A = 2^27: post-54 77,753,718 vs pre-54 74,456,549.
- (late) GATES-18 is on main as 98e686d: a CROSS-LAYER reason must name the owning layer of EVERY other-layer path, as a whole word (e.g. "GATES-6 agreed", "ROOT for CODEC"). A kernel! day touching gates/waste.tsv, gates/codec-vectors.tsv or the ceilings must name GATES, and each partner layer by name, or it is refused path by path.
- Lane ver (af3103cd985e3d710, ceiling): both teeth proved (pinOf_old_recurs; ADDED rowPin_old_floor_recurs = ROOT's dropHeads tooth). FINDING: `Collision E.hash` is provable from E.Lawful by pigeonhole (logs/kernel21-ver-pigeon.lean), so every `∨ Collision` kernel conclusion (61 sites at b9ce5a7) is vacuous — filed cv 01a1501e-d6bc. Row/range stale theorems FALSE as written (unlawful Ord: logs/kernel21-ver-ordcx.lean; rel ≥ 256 aliasing in rowsPrefix: logs/kernel21-ver-relcx.lean). Report: logs/kernel21-ver-report.md.
- MY RULING (owner): the three new stale theorems conclude a CONCRETE collision among an explicit preimage list S (CollidesAmong), not `Collision`; row/range gain [Std.TransOrd D] [Std.LawfulEqOrd D]; range gains rel < 256, pre.size ≤ width < 256. New statements only, no landed theorem gains a premise. Lane ver2 a77e6de07fe2b20e7 doing it (+ RowsRange's private listed lemmas made public, v_* copies deleted).
- Snapshot for partners: logs/kernel21-k54-snap1.patch (Kernel/ + Host/Sim on b9ce5a7; first diff was cut mid-lane and did not elaborate). CODEC-12 staged logs/codec12-k54.patch (md5 da033e9b; replaces my 4 Codec placeholder files; re-cuts after LANG-57). Its changed statements to list in my reader are in its message (rowLeafBytes_eq/_decode name rowLeafHashed; Entry.Fits, EntryWireFits, leaf_decode_refuses_misfit; getVarint_of_occurs/occurs_of_getVarint (width limit); ListingPin cells_/rows_listing_unmoved).
- KERNEL-55 potential drafted and green on the post-54 tree: logs/kernel21-pot.lean (growth_le_logWeight 61·g ≤ 84·L, declare_growth_tight, admit_potential, fold_potential, allowance_bounds_world). Names promised to HOST-14: Kernel.potential, Kernel.potentialRatio = (84,145). HOST-14 derived worldWeightMax = 78,802,294.
- ver2 (a77e6de07fe2b20e7) DONE: three stale theorems proved with CollidesAmong over explicit S; CrossSep and v_* copies deleted; RowsRange.listed_key public. Backup logs/kernel21-k54-proofs-done.diff + logs/kernel21-Versions-done.lean.
- k20k moved to main 98e686d (checkout -m), my 4 Codec placeholder files reverted to main, CODEC-12's codec12-k54.patch (md5 da033e9b) applied --3way cleanly. lake build Kernel Codec Emit GREEN, 0 warnings (logs/kernel21-b1.log); 0 sorry; sorryAx scan 3590 Kernel theorems → 0 (logs/kernel21-ax.lean); kernel-sim 64 ALL PASS, WASTE = phase 1 (logs/kernel21-ksim1.log). Stmt diff vs 98e686d: logs/kernel21-stmtdiff2.tsv (73 changed, 67 new). Reader K21-READER a72ca03ab2bc96daa running.
- ROOT RULED KERNEL-56 = restate all 61 `∨ Collision` sites to CollidesAmong E.hash S, S explicit per theorem, each with a tooth (a `Separates S` instance under which the conclusion is the binding fact), deployed corollaries re-derived, no premise beyond S; FIRST item after the 54 day; Protocol/Host audit their own. Vacuity-reader briefs now carry: "a disjunct provable from the premises/instance alone is vacuous".
- Full build (logs/kernel21-all1.log) breaks first at Lang.Rel :94/:106 (row arity): LANG-17 asked for logs/lang17-k54.patch or "agree".
- KERNEL-56 started early in parallel: wt/kernel = 98e686d + logs/kernel21-k54-assembled1.diff (the whole 54 tree), lane k56 a13c58a5dea861b3d restating the Collision sites (logs/kernel21-collision-sites.txt; stmt log logs/kernel21-k56-stmts.md; continuation logs/kernel21-k56-continue.md). Its diff re-applies over the landed 54 day. Protocol/Proofs/Receipt.lean (5 Collision lines) goes to PROTOCOL-16 for agreement.
- Reader K21-READER: LAND-WITH-FIXES. Fixes applied: row/range disjunct sharpened to `w'.entry E parent = some .tomb` (stronger than ROOT's live = none); pinOf_old_recurs gains `pinOfContent w₁ ≠ w₀`; rowPin_old_floor_recurs gains the tomb conjunct; NEW range tooth rangePin_floorless_recurs (ver2); docstrings World.lean Entry/Reject.stale, Submit.lean Outcome, Turn.lean RowLeaf (AHEAD not final; dropHeads). Reader's extra (c) items to state in the commit: private RowsComm.touchCheck_congr (live= → entry=), and DEFINITION-level tightenings with unchanged text: Leaf.CellFit (+v < 2^64: slot_inclusion_sound, head_read_sound, leafBytes_inj, leafDigest_inj, cells_headSound, deployed_* head reads) and rowFits (+floor/ver < counterLimit: admit_range_exact*, range_rows_*, listed_key, head_sum, admit_comm_rows, rows_ext …), all discharged by the existing fold invariants (fold_cellsFit, fold_rowsOk) and CODEC's decode.
- k20k rebased to main 40879fa (PROTOCOL-51's rangeOf conflicted with headFloor in World.lean, both kept). Kernel Codec Emit green, 0 warnings (logs/kernel21-b2.log). Lang edits done (LANG-17 agreed, cross-layer): Lang/Rel.lean :96 :112, Lang/Proofs/Rel.lean, Lang/Journey.lean storyRow + pinP floor + rangeP floor. Full build (logs/kernel21-all2.log) now stops at Protocol/Command/Machine.lean:355 (PROTOCOL-16's half) and Ops/Founder.lean:60 (Ops owner: one token w.live → w.entry; Ops/Plants.lean:670 likely too).
- k56 lane DONE in wt/kernel: Collision AND Trie.Coll deleted (Trie.Coll had the same pigeonhole flaw), all sites restated to CollidesAmong over explicit S (climbPres/pathPres down in the trie; chainPres/foldPres for the chain), `_sep` teeth per family, Protocol/Proofs/Receipt.lean 5 statements touched (PROTOCOL-16 to agree). Patch logs/kernel21-k56.patch, statements logs/kernel21-k56-stmts.md. LEFT: HashColl (Origin.lean:26, same defect; Origin, Carry, Ledger, LedgerDeployed) → KERNEL-56 scope extension; decisions/kernel.md:2423 names *_coll_collision. NOTE for its landing: closure C3 refuses non-Prop public defs in proof modules: its S-builders (termPre, climbPres, chainPres, …) must move to def modules or go private.
- PROTOCOL-16's protocol16-k54.patch applied (Protocol/, generated.rs, decisions PROTOCOL-52). OPS-5 agreed (Ops/Founder.lean:60, Ops/Plants.lean:670 → w.entry). LANG-17 agreed on my Lang hunks. Host/Proofs/Serve.lean judge_journaled: proof-only extra split arm (judgeBy's stale branch) — asked HOST-14 to agree.
- FULL lake build GREEN (545 jobs, 0 warnings, logs/kernel21-all4.log). Runs r1 (logs/kernel21-r1-runs.out): host-sim/host-file-sim/hosting-sim 1–3, ledger-sim, store-plants, kernel-sim 64, lang-journey, rows ALL PASS; census ok. gates/check RED: closure C3 (Versions exported non-Prop defs: FIXED by moving pinPre/rowPre/leafPres/rangePre into Kernel/World.lean and making pinOfContent/rangePinFloorless private; Kernel rebuilt green logs/kernel21-b3.log), refusals List UInt8 in CODEC-12's Emit/Vectors.lean:511/526/529 (sent to CODEC-12 for its re-cut), size (generated at commit).
- Waiting: CLIENT-8 (asked: agree to protocol16-k54-client.patch or own patch), CODEC-12 re-cut after LANG-57, LANG-57 landing (then KeyOrder `.row` leaves), HOST-14 agreement on Serve.lean. PROTOCOL-16 flagged to ROOT: it DELETED the admitsRecorded mutation + Writer code (a removed check = pause item; ROOT's ruling).
- HOST-14 agreed (Serve.lean proof-only; base-bytes 3.895/3.821/3.912 < 4). CODEC-12 re-cut applied: logs/codec12-k54b.patch md5 629cfff3 (refusals-gate fix; 216 vectors / 53 sites). WASTE rows re-pinned in gates/waste.tsv (logs/kernel21_waste.py; six rows, the three rises need `WASTE: <op>: <why>` lines). Decision text to append at landing: logs/kernel20-dec54-ruled.md + logs/kernel21-dec54-built.md.
- ROOT: PROTOCOL-16 re-cuts once (admitsRecorded tooth kept on the unpinned row-birth instance); wait for it. KERNEL-56 absorbs HashColl too (one commit deleting every unbounded-∃ collision predicate; Ledger consumers as ROOT for LEDGER with restatements + teeth); its reader checks zero remaining unbounded-∃ collision predicates in Kernel/.
- CLIENT-8 agreed (protocol16-k54-client.patch + generated.rs) with the exact loop bound 0..=3s+1; filtered tests it wants on the assembled tree (ND_LEAN_BIN = its bin dir): `cargo test -p nanodregg-client --test attempt --test run --test real --test stdio --test join --test supervise --test roundtrip --test custody`; `cargo test -p nanodregg-launcher --test members --test resident --test broker`; workspace clippy -D warnings; fmt.
- PROTOCOL-16 retired; PROTOCOL-17 a916601ac8bfc4807 re-cuts (admitsRecorded on the unpinned row birth; derivePins row pins from the new key field; CLIENT-8's bound). ROOT's 4th change DONE: Receive.Refusal.rowUnpinned parent rel key (RowSlot.keyBytes, empty for heads); tooth Kernel/Proofs/Audit.lean rowTouchesOf_unpinned_key; no codec site (refusal fields are not on the wire). Kernel green (logs/kernel21-b5.log).
- PROTOCOL-16's first patch reverted to main in wt/k20k; snapshot for PROTOCOL-17: logs/kernel21-k54-snap2.patch md5 8a31f1e1 (against 40879fa, everything but Protocol). Awaiting logs/protocol17-k54.patch.
- **LANDED b48c10f** kernel!: KERNEL-54 (attempt 2; attempt 1 refused only on owners: Kernel/Proofs/Value.lean + Ledger.lean are LEDGER's → "ROOT for LEDGER" with the five shape-only restatements listed). Includes CODEC-12 (codec12-k54.patch 9f1a244a), PROTOCOL-17 (protocol17-k54.patch 7345e1b6), CLIENT-8 (exact bound, I trimmed the doc to 2 lines to stay under the client-library ceiling 2520), HOST-14, LANG-17/18, OPS-5, ROOT for GATES. Message logs/kernel21-msg54.txt, land script logs/kernel21-land54.sh. Decision appended to decisions/kernel.md (dec54-ruled + AS BUILT).
- LESSON: the owners gate reads per-FILE owners inside Kernel/ (Kernel/Proofs/Value.lean, Ledger.lean belong to LEDGER). Check `owners` before attempt 1.
- KERNEL-56: wt/kernel reset to b48c10f + logs/kernel21-k56.patch (no index lines, so plain apply, Versions' duplicate CollidesAmong removed by hand). Kernel + Protocol.Proofs.Receipt green (logs/kernel21-k56-b1.log). Lane k56b ae2a0e30bb42ab10f finishing: HashColl (Origin, Carry, Ledger, LedgerDeployed), S-builders out of proof modules (C3), prose, full build + 4 sims, patch logs/kernel21-k56b.patch. Receipt.lean hunk → PROTOCOL-18 (or ROOT for PROTOCOL).
- KERNEL-55 part 1 BUILT in wt/k20k (on b48c10f): World.lean potentialRatio/potential; Weight.lean growth_le_logWeight, declare_growth_tight (tooth), admit_potential, fold_potential, allowance_bounds_world; prose. Kernel.Proofs.Weight green (logs/kernel21-p1.log). Reader K21-READER55 a5e57d29fcb79128e. Decision text logs/kernel21-dec55-ruled.md (append after logs/kernel20-dec55.md). Lands AFTER KERNEL-56. Part 2 = R1 (RefusalSlot total per window, Bounds.refusalsPerWindowMax, checkRefusal req, refusalsCounted extension, CODEC refusals wire → kernel!), after 56 lands.
- KERNEL-56 BUILT by k56b (ae2a0e30bb42ab10f): HashColl deleted (7 consumers + teeth), S-builders in def modules, closure ok, full build green 559 jobs, kernel-sim 16 / ledger-sim / host-sim / rows ALL PASS. Patch logs/kernel21-k56b.patch (vs b48c10f). Reader K21-READER56 a97bfdc33d9bacf0b running. Decision draft logs/kernel21-dec56.md. Receipt.lean: PROTOCOL-17 (resumable) asked; ROOT: after an hour "ROOT for PROTOCOL". HeadSound S-parameter ruled sound by me, ROOT concurred (reader states it per caller).
- KERNEL-55 part 1: reader55 LAND-WITH-FIXES, docstring fixes applied in wt/k20k (no "World." prefix, CODEC size equality stated as part-2 work, "stronger" not "tight", tooth scoped to row touches).
- **LANDED 482aecc** kernel: KERNEL-56 (Collision / Trie.Coll / HashColl deleted; CollidesAmong over explicit S everywhere; _sep teeth; lawful Separates floor pair; Receipt ×5 + teeth, PROTOCOL-17 agreed; ROOT for LEDGER). Attempt 1 retried itself on a CAS race and landed. Message logs/kernel21-msg56.txt.
- **LANDED 4b9c563** kernel: KERNEL-55 part 1 (potentialRatio/potential; growth_le_logWeight 61·g ≤ 84·L; declare_growth_tight tooth; admit/fold_potential; allowance_bounds_world). Decision appended (dec55 proposal + logs/kernel21-dec55-ruled.md). HOST-14 told. cv 01a150a3-2523 filed: CODEC world_size_eq.
- NEXT: KERNEL-55 part 2 = R1 (kernel-wide refusals cap per window), a kernel! with CODEC (refusals key kind).
- KERNEL-55 part 2 (R1) lane r1 ac5c48cdca4f4b83d in wt/kernel (at 4b9c563): Bounds.refusalsPerWindowMax = 16384, RefusalSlot.total win, checkRefusal req … .refusalsFull (new Reject, judgeBy declines it), refusalsCounted extended, the fold bound theorem on leaf counts, teeth. Defs file for CODEC-12: logs/kernel21-r1-defs.md (route when it appears); stmts logs/kernel21-r1-stmts.md; patch logs/kernel21-r1.patch; continuation logs/kernel21-r1-continue.md. A kernel! (refusals key wire, re-genesis).

### KERNEL-21 FINAL HANDOFF → KERNEL-22 (written at ~460K tokens, past the 350K line)
**Landed by KERNEL-21:** b48c10f kernel! KERNEL-54 (versioned pins; stale declined, staleRecorded; the partner halves; flag day combined with LANG-57) · 482aecc kernel: KERNEL-56 (Collision / Trie.Coll / HashColl deleted; CollidesAmong over explicit S; _sep teeth) · 4b9c563 kernel: KERNEL-55 part 1 (potential, Φ = 145·weight + 84·allowance; allowance_bounds_world).
**In flight — your first item: KERNEL-55 part 2 (R1).** Lane r1 = agent ac5c48cdca4f4b83d (SendMessage resumes it), working in hbox wt/kernel at 4b9c563. Brief: a kernel-wide refusals cap per window (Bounds.refusalsPerWindowMax = 16384, RefusalSlot.total win, checkRefusal `.refusalsFull` declined by judgeBy, refusalsCounted extended, a fold theorem bounding each refusal leaf kind's count, teeth). Outputs: logs/kernel21-r1-defs.md (as soon as it appears: send it to CODEC-12 ae211cadad0f1ed00 for the refusals key wire / refusalsFits / vectors half, staged as a patch, same assembly recipe as KERNEL-54: revert Codec/Emit/gates/codec-vectors.tsv/decisions/codec.md to main, git apply --3way), logs/kernel21-r1-stmts.md, logs/kernel21-r1.patch, continuation logs/kernel21-r1-continue.md. Then: second-agent vacuity read (with ROOT's disjunct rule), full build, runs (logs/kernel21-runs.sh adapted; logs/kernel21-kball*.sh), WASTE/SIZE lines, flag day (refusals key wire moves, every Store re-geneses, vectors re-emit), owners (check gates/OWNERS: Kernel/Proofs/Value.lean, Ledger.lean, Kernel/Receive/Ledger.lean, Kernel/Value.lean are LEDGER's → "ROOT for LEDGER"; gates/* → "ROOT for GATES"; client/src/generated.rs is CODEC's). Tell HOST-14 a4d3aa9099adf145c the hash and C; HOST derives worldBytesMax after CODEC's world_size_eq (cv 01a150a3-2523), then PERF-2 benches.
**Then the queue:** cv 01a14afe-7380 (draw-independent hash instrument + the leaf-split re-hash finding, KERNEL-20's note), cancel step 7464 (proposal), 7364, ca32, check_local 01a14f65-48ec, injective rows leaf encoding 01a14f7e-d65a (CODEC-12 split rowLeaf (varint wire) from rowLeafHashed (nat64 preimage) on the 54 day; re-check what d65a still asks), W1 cv 01a14fc3-d848 (filed, trigger-gated), cv 01a14f94-e90f (forged-signature declines cost 2 verifies).
**Waiting on others:** PROTOCOL-18 (spawned by ROOT) composes settle_stale_never_admits with stale_behind_forever (now CollidesAmong); PROTOCOL-17's p54 patch waits on LANG-58's bell row.
**Lessons (this run):** (1) "final statements" from a phase 1 are final in SHAPE, not in truth: two were false (missing lawful-Ord and rel < 256 premises) and the escape was vacuous; prove them before calling a day "staged". (2) The vacuity that a pigeonhole argument proves is invisible to builds, census and statement diffs; ROOT's reader rule now checks it. (3) The owners gate is per FILE inside Kernel/ (LEDGER owns four Kernel paths): read gates/OWNERS before attempt 1. (4) closure C3: non-Prop public defs never in a Proofs module. (5) A snapshot for partners must be cut after the lanes stop editing (my first diff was cut mid-lane and did not elaborate). (6) A git-apply patch without index lines cannot 3-way; cut partner patches with `git diff` (index lines included).

## KERNEL-22 (successor of KERNEL-21; started 2026-10-18; hbox wt/kernel)
- Start: main = 4b9c563 (KERNEL-55 part 1). Lane r1 ac5c48cdca4f4b83d had made no edits yet (tree clean, no r1 logs; the logs/kernel21-r1-*.log files on hbox are KERNEL-54's runs, not this lane's).
- DECISION (r1 key shape): the kernel-wide total is `RefusalSlot.total (origin : D) (win : UInt64)`, key `[2] ++ E.bytes origin ++ u64 win`, leaf reuses `.count n`. Critique: origin is a filler (no information). Meta: the alternatives cost more: variable-width keys rework CODEC's SlotOrder/size proofs; a hashed constant puts a hash on every key-bit lookup; a scalar World field puts a new field on every World-frame proof and the header codec (premises on landed theorems). Conditions given: refusalsCounted pins the total to (w.origin, current window) and to the window's record count; pruned like `.count`; fits 1 ≤ n ≤ C; tooth that the total check is independent of the per-member one.
- r1 defs written (hbox logs/kernel21-r1-defs.md) and routed to CODEC-13 a69eab32196c48877 (CODEC-12 retired, ROOT): it stages logs/codec13-r1.patch vs 4b9c563. r1 added: refusalsCounted bounds the two previous windows' records by C, so the trie bound follows from the decode check alone.
- Lane K22-ROWS a6e8e58b1783df6eb in wt/k20k (4b9c563): cv d65a (rows key injective by construction + 4th HeadSound record); must report its design choice before editing outside Kernel/. Outputs logs/kernel22-rows{.patch,-stmts.md,-continue.md}. Lands after R1 (rebase).
- Lane K22-HASH a63ef12aa6215824b in NEW worktree wt/k22w (git worktree add --detach at 4b9c563, cold .lake): cv 7380 draw-independent required-hashes ratio; deletes the two draw-sensitive rows; Bench hunk separate for ROOT for PERF. Outputs logs/kernel22-hash{.patch,-report.md,-continue.md}.
- CODEC-13 cutting codec13-r1.patch (refusalSlot choice 3, kind-byte order teeth, C/C+1 boundary pair, generators emit the total). Its first build on a mid-lane snapshot was red in Kernel (r1's proofs in progress): it re-snapshots on my "Kernel green" message. world_size_eq: post-54 entry factor 54/49 (not 35/32); refusalsBytes ≤ 82·3C + 50·(C+1) = 4,849,714.
- worldBytesMax (my computation, HOST-14 to confirm): post-54 ⌈54·78,802,294/49⌉ + 221,184 + 4,849,714 + 104 = 91,914,347 B; pre-54 ⌈35·75,505,125/32⌉ + same = 87,654,733 B.
- Cancel-step PROPOSAL written: hbox logs/kernel22-cancel-proposal.md (C1: recorded refusal of the target + Refused.cancel signature; kernel World theorems gain no premise). Sent to ROOT for ruling.
- HOST-14 CONFIRMED worldBytesMax pair: post-54 91,914,347 B, pre-54 87,654,733 B (matches CODEC-13 world_size_le constants).
- (post-handoff) r1 lane DONE, already reported to KERNEL-22: wt/kernel at 4b9c563 uncommitted; RefusalSlot.total (origin) win (origin fills the fixed-width key); refusals_bounded (3C tx, C counts, 1 total; exactly 3 windows, refusal_window_three shows 2 is wrong); teeth refusalsOk_bounds_nothing, checkRefusal_full, uncapped_overflows, refusalsCounted_total_lowered, judgeBy_refusalsFull; kernel-sim 64 ALL PASS. FOR KERNEL-22 TO RULE/ROUTE: (1) a premise added to a LANDED helper, refuse_sumN gains `hgt` (g = 0 on total keys; old statement false with the third insert; file-local) — a pause item by the rules, state it in the commit/decision; (2) WASTE refuse hashes-per-refusal 11.362 → 15.284 (third insert) needs a WASTE line + ROOT for GATES; (3) CODEC-13 replaces logs/kernel21-r1-codec-provisional.patch; PROTOCOL proof-only logs/kernel21-r1-protocol.patch; HOST re-prices fold_listing (refusal listing +3 per record) or uses refusals_length_le.
- r1 DONE kernel side: logs/kernel21-r1.patch md5 2cb2629c (Kernel/), -protocol.patch 8c504769 (proof-only), -codec-provisional f803e4aa (superseded). Kernel + kernel-sim green, 0 sorry, sim 16/64 ALL PASS. One landed helper gained a premise: refuse_sumN hgt (forced: old statement false with a third insert; in-file, every caller discharges). Bound: refusals_bounded ≤ 3C tx + C counts + 1 total (fold_/reach_/deployed_ no premise; _of_counted for decoded bases); refusal_window_three tooth. WASTE: refuse hashes-per-refusal 11.362 → 15.284 (the third insert).
- Routed: CODEC-13 re-snapshot (Kernel green), HOST-14 asked for logs/host14-r1.patch (refuse_refusals_listing +3, _two =3, fold_listing pricing), PROTOCOL-18 a80e8e52fab6ef755 asked to agree to the protocol patch. Reader K22-READER-R1 af56ad84c0b640aeb → logs/kernel22-reader-r1.md. r1 resumed for the assembly + decision draft logs/kernel22-dec55p2.md + full build/runs → logs/kernel22-r1-assembled.patch.
- PROTOCOL-18 AGREED to kernel21-r1-protocol.patch (proof-only); a prose addition (refusalsFull in Table.lean:115, Settle.lean:15) announced. Main moved to e1e8084; r1 moved wt/kernel by checkout -m.
- Reader K22-READER-R1: LAND-WITH-FIXES. Bound, decode side, edges (low heights, two totals, past C), refuse_sumN forced-premise: clean. Fixes to r1: refusalsFull_independent was proved on a non-CountedOk World (strengthen via a general n ≤ C CountedOk construction); refusalsCounted_total_lowered_exists premise-free from it at n = 2; prose; design cost to state: ~1,024 members at budget exhaust C and stall refusal finality for all until the window turns.
- CODEC-13: codec13-r1.patch md5 1d9eea3a (supersedes 58e85593; reader-passed; adds world_refuses_stray_total). world_size_eq/_le lands as its own codec commit after R1.
- r1 reader fixes done: counted_world (n ≤ C CountedOk construction), refusalsFull_independent on it at n = C, refusalsCounted_total_lowered_exists premise-free; patches kernel21-r1.patch 04bf0814, -protocol 91df4a2e (vs e1e8084). BLOCKED only on HOST-14's host14-r1.patch (Deployed.lean:691, Seal.lean:300); re-pinged.
- K22-HASH DONE: logs/kernel22-hash.patch 4c359b99 + -perf.patch b3bde60b (Bench, ROOT for PERF). Kernel.Sim.Required: every trie hash row = counted/required, 1.000 exact under 3 draws; plant hash-required:empty-per-insert 1.073; 8 draw-sensitive rows deleted (WASTE lines). THE BAR: 1.074 (one extra hash per step from World.roots' per-empty-root re-hash). New cv: 01a15107-2263 (insAt split-leaf re-hash 7.8%), -2272 (World.roots), -2281 (re-walk 2.1%), -2290 (proof bytes-per-inclusion draw-sensitive). Told to LAND ITSELF first (R1 rebases: waste re-pin moot, Required replays the third insert). Next for it after R1: 2272 then 2263.
- K22-ROWS DONE: kernel22-rows.patch 6919b66f (option b: LEB128 natBytes for rel, key length, width, pre.size; rows = 4th HeadSound in Kernel/Proofs/RowsHeadRead.lean; rowDepth 1304 → 1320; premises removed from range theorems; one added on the tooth declare_growth_tight: rel < 128). Needs CODEC-13's rows wire (told, after R1) + LANG KeyOrder advisory. Reader K22-READER-ROWS ac9ea305c816382f8 → logs/kernel22-reader-rows.md.
- PROTOCOL-18 AGREED protocol patch 91df4a2e. Main moved to cfdb08d (HOST-56 = Host half of KERNEL-55 part 1). host14-r1.patch appeared 18:12. K22-HASH landing in progress (logs/kernel22-hash-land.log). CODEC-13 takes rows wire after R1 + its WorldSize commit.
- **LANDED 3467955** kernel: K22-HASH (cv 7380): Kernel.Sim.Required, 7 exact rows at 1.000, 8 draw-sensitive rows deleted, bar row trie-hashes-per-required ceiling 1.096 (1 + 27/283, 6-sd); ROOT for GATES, ROOT for PERF. ROOT told.
- HOST-14 AGREED (HOST-58): host14-r1.patch f98c21ea (re-price: refusal step 96 B; tooth refuse_refusals_listing_three). r1 assembled green at cfdb08d (565 jobs, all runs pass), only red closure C3 Codec/Proofs/SlotOrder.lean:208 refusalKind (CODEC-13 fixing). r1 told to rebase on 3467955 and LAND itself (msg spec given: logs/kernel22-r1-msg.txt).
- Reader K22-READER-ROWS: LAND-WITH-FIXES (rowLeafPre C3 move; len_wrap tooth was not a tooth: restate as the prefix inequality; dedupe ba_eq_of_toList; concrete instance). Sent to the rows lane. Rows lands only together with CODEC-13's varint wire.
- LANG-19 AGREED the KeyOrder hunk of kernel22-rows-advisory.patch (range_keys_ascend(_read) drop width < 256). Rows patch re-cut b269985a (reader fixes applied). CODEC-13 codec13-r1.patch 8dbc2d33 (C3 fix). r1 landing R1 now.
- **LANDED 38d6c9d** kernel!: KERNEL-55 part 2 (R1) by lane r1 (msg logs/kernel22-r1-msg.txt; assembled 93f32855 vs 3467955). Flag day: refusals key kind 2, three keys per refusal, every Store re-geneses, vectors re-emit (CODEC-38), Host refusal step 96 (HOST-58). worldBytesMax pair in the text. ROOT, HOST-14, CODEC-13 told. Lane r1 retired (done).
- Next in flight: CODEC-13 WorldSize codec commit → codec13-rows.patch; K22-ROWS rebasing onto 38d6c9d and will land the rows kernel! itself; K22-HASH a63ef12aa6215824b on cv 2272 (World.roots shared empty digest) then 2263 (insAt split-leaf digest kept), each a kernel: landing with its own reader.
- Lane K22-LOCAL ad511ce38844a9687 in wt/kernel (38d6c9d): cv 48ec check_local (locality half of the frame rule; replace the private congr family). Outputs logs/kernel22-local{.patch,-stmts.md,-continue.md}; no commit, reader then land.
- CODEC-13 WorldSize landed 08b13ab (codec: world size exact vs weight, slack 54/49). HOST ad890b3 (budget_reaches premises at import/join). Rows lane on 38d6c9d green with scaffold (rows.patch 202c7eb5), waiting codec13-rows.patch.
- CODEC-13 codec13-rows.patch d0be687c (CODEC-40: bytesV Shape 21, rel/width varints, rel ≥ 256 refused by name, rowKey_size = RowSlot.weight exact, 23 tags move). DECISION: rangeRead log field stays nat8/bytes8 (decode-bounded, not a preimage; RangeRead.weight unchanged). Rows lane assembling + landing.
- K22-LOCAL DONE: logs/kernel22-local.patch 404c991d (vs 38d6c9d): check_local (Kernel/Proofs/Local.lean), read-set Props in Logic/Frame.lean (CellRead, RowRead, RowsAgree same|read, Agree), teeth check_local_outside / check_reads_kept; deleted check_journal_congr + 5 RowsComm privates. NO theorem fall (+32 theorems, +578 lines): check_after is not an instance of locality (it proves passes-again, not equality); receive_congr is about receive. Needs two mechanical edits after the rows landing (rows_separateOn arity, range_prefix_long hw'). DECISION pending reader: keep RowsAgree.read (the general fact; ~300 lines, no consumer today). Reader K22-READER-LOCAL a39db5b1d28e18f51 → logs/kernel22-reader-local.md.
- codec13-rows re-cut 2d38b8e4 (range-pin width ≤ keyBytesMax 128). Reader K22-READER-LOCAL: LAND-WITH-FIXES (drop unused hf', add check_reads_kept_sep, a .read tooth with different rows, prose; read is load-bearing). Local lane told to fix, rebase after rows, land.
- **LANDED 16f3b9f** kernel: World.roots shares one empty digest (K22-HASH R2, cv 2272); roots_eq (no flag day); bar 1.096 → 1.000; Receipt.lean proof-only as ROOT for PROTOCOL (should have been PROTOCOL-18: flagged to ROOT, lane told).

## KERNEL-23 (successor of KERNEL-22; started 2026-10-18 ~19:53 hbox time; hbox)
- Start: main = 16f3b9f. The rows judge (logs/kernel22-rows-commit2.log) had NOT been running from wt/k22w: it ran from wt/k20k on c100be5 and was REFUSED (main moved to 16f3b9f mid-judge, then "worktree behind main" on Admit/Cells/Refuse/Gen/World). No retry was possible from that tree.
- Saved WIP: logs/kernel23-rows-wip-c100be5.patch (md5 19831799, wt/k20k), logs/kernel23-local-wip-38d6c9d.patch (9dc1f03c, wt/kernel, K22-LOCAL check_local), logs/kernel23-hash-r3-wip-16f3b9f.patch (b40bdd80, wt/k22w, K22-HASH R3 = cv 2263 insAt split-leaf, MID-FLIGHT: Trie.lean/Proofs/Trie.lean edited, Required.insertReq not yet lowered, so sim0 reads counted < required on every seed).
- wt/k20k moved by `git checkout -m --detach 16f3b9f`: clean merge (16f3b9f's World.lean hunk is `rootsOf`, disjoint from the rows section). Relaunched the rows kernel! judge from wt/k20k: logs/kernel23-land.sh, message logs/kernel23-rows-msg.txt (= kernel22-rows-msg.txt + the rebase sentence in the Runs line + my co-author line), --cross-layer naming CODEC (CODEC-13/40 wrote, CODEC-14 landing duty) and LANG (LANG-19 agreed KeyOrder); log logs/kernel23-rows-commit.log, pid logs/kernel23-rows-commit.pid.
- Note: 16f3b9f's proof-only edit of Protocol/Proofs/Receipt.lean was carried "ROOT for PROTOCOL"; accepted by ROOT after the fact (should have been PROTOCOL-18).
- Cancel step: ROOT HOLD as PROPOSED; C1 is the design when the trigger ("a member that cannot wait a window") fires. Not building.
- Relaunch 1 (logs/kernel23-rows-commit.log) REFUSED on owners only: gates/codec-vectors.tsv is GATES-owned. Build, census, 51 runs, vectors and waste were all ok; the cargo FAILED lines are the known-red controls. ROOT then HELD every scripts/commit until GATES-19 (the judge queue) is on main. GATES-8 a5308a6ab02a9d9a6 tells ROOT the hash, and ROOT tells me.
- wt/k20k moved again to 359e9e8 (host! worldBytesMax derived), clean. Host.Proofs.Size builds green over the rows WorldSize. kernel-sim 16, rows, and rows --deployed: ALL PASS (logs/kernel23-rows-{sim16,rows,rowsdep}.log). Relaunch staged: logs/kernel23-land.sh writes kernel23-rows-commit2.{log,pid}, with CROSS-LAYER adding "ROOT for GATES: the CODEC-40 vectors re-emit" (ROOT's wording).
- PROTOCOL-19 a7b300287de0afe72: agreed `admit_stale_pin` (the converse of stale_refused/rows_/range_stale_refused). It goes in a new Kernel/Proofs/StaleOnly.lean, written by PROTOCOL-19, landed after the rows kernel! with "KERNEL-23 agreed the statement". It must carry three per-kind separation instances; hr stays only if used. Order: GATES-19, rows, StaleOnly, the Protocol composition. I owe PROTOCOL-19 the rows hash.
- cv 2263 (insAt keeps a split one-entry leaf's digest) FINISHED in wt/k22w on 16f3b9f: logs/kernel23-2263.patch f3339bb8. insertReq lowered (pathShape -> pathDepth); insAtRebuild + its lemmas private (closure C3); tooth insAt_split_keeps. Counts: seeds 0-63 61851/61851 (was 67112, -5261 = exactly the moved-leaf re-hashes), 64-127 60070/60070, BAR standing 376/376, plant 1.079. Whole build green. No value row moves; waste.tsv prose only. No flag day if insAt_eq_rebuild holds on deployed tries (reader checks WF coverage). Reader K23-READER-2263 -> logs/kernel23-reader-2263.md.
- K23-READER-2263: LAND-WITH-FIXES. Fixes applied: waste counts restated per row; insAt_split_keeps without hk; private tooth insAt_ne_rebuild_of_stale; the Required header names the multi-entry-leaf inexact case (one over, never under; unreachable deployed). Patch 9bc8cd6a, msg logs/kernel23-2263-msg.txt, launcher logs/kernel23-land2263.sh. GATES-8 AGREED the waste prose.
- ROOT: hold UNCONDITIONAL until GATES-19's hash arrives (hand checks under SWARM_MEM_MAX=6G LEAN_NUM_THREADS=2). Confirmed. Main 9d5b293 at 21:05. On the go: re-base k20k onto main (checkout -m), run kernel-sim 16 + rows, then logs/kernel23-land.sh; after rows lands: re-base k22w, then land2263; tell PROTOCOL-19 the rows hash; then the K22-LOCAL patch.
- **LANDED 7c09186** kernel!: the rows key encoding is injective by construction (K22-ROWS + CODEC-40). It was the queue's first customer and was displaced twice before landing. Flag day: rowDepth 1304→1320, bytesV Shape 21, 23 tags move, vectors re-emitted, every Store re-geneses. ROOT and PROTOCOL-19 told.
- cv 2263 re-based onto 7c09186. In gates/waste.tsv, PERF-10's worstcut rows were taken from main by hand and my bar sentence kept. It now carries ROOT's absolute row `admit trie-hashes-per-turn` 14.074 (61851/4395, fixed seeds 0-63; it would read 15.270 before 2263). Judge launched: logs/kernel23-2263-commit.{log,pid}, patch f7f8a3f5.
- 2263 judge 1: REFUSED with "every judge slot busy for 30 min" (the slot-wait bug that GATES-20a fixes). There was no content verdict. ROOT HOLD on new commits until GATES-20a's hash.
- K22-LOCAL prepared on 7c09186 in wt/kernel. The two mechanical edits are done. Reader fix 5: RowsAgree.read's hf weakened to RowSlotFits on held slots, with the `rowSlotFits_of_held` bridge made public. RowSlotFits moved RowsSep -> Rows.lean to avoid an import cycle. decisions/kernel.md has the KERNEL-51 AS BUILT locality entry. Whole tree green (575), kernel-sim 16 ALL PASS. Patch logs/kernel23-local.patch 11a22ff9, msg logs/kernel23-local-msg.txt, launcher logs/kernel23-landlocal.sh.
- Lane K23-7364 a69e19be3cfda8d59 is DONE: logs/kernel23-7364.patch 109f1cf3 (Journal.lean only, wt/k20k on 7c09186). It adds reach_prune_check_call, with no window premise from genesis, ∨ CollidesAmong X.env.hash (retryPres t l); honest_prune_check; teeth _sep_instance, needs_callLog, collides_instance. No landed statement changed. Whole tree green (574), sim16 ALL PASS. Reader K23-READER-7364 -> logs/kernel23-reader-7364.md.
- K23-READER-7364: LAND-WITH-FIXES (docstring relabel; optional stronger tooth). Both done by the lane: honest_retry_window_needs_honest on hCtx. Patch 0656875a, msg logs/kernel23-7364-msg.txt fcd3fff1, launcher logs/kernel23-land7364.sh. Order after the hold: 2263, then local (Journal.lean: deletes check_journal_congr), then 7364 (Journal.lean appends; re-base by checkout -m after local).
- **LANDED aa7fa1d** kernel: cv 2263 plus the absolute row `admit trie-hashes-per-turn` 14.074. Judge 1 was refused on size (it needed a SIZE: Lean lines (deployed) line). ROOT told.
- PROTOCOL-20 aaaf1c9d178548dde (successor of PROTOCOL-19): agreed Kernel/Tactics/StaleOnly.lean as a proof-only macro module (C3; ROOT option (b)).
- check_local judge launched from wt/kernel on aa7fa1d: logs/kernel23-local-commit.{log,pid}.
- **LANDED 50bf961** kernel: check_local (K22-LOCAL; cv 48ec). Judge 1 was refused on size: it needed a separate `SIZE: Lean proof-modules` line. Judge 2 was displaced 3 times, then landed. ROOT told.
- cv 7364 re-based onto 50bf961 (Journal.lean merged clean, green). Judge launched: logs/kernel23-7364-commit.{log,pid}.
- 7364 judge 1: REFUSED by closure C3 (retryPres was a def in a proof module). Moved it to Kernel/Receive/Call.lean beside domTx (+6 deployed lines, SIZE line added). Patch ab294622. Judge 2 is running; it was displaced once.
- Lane K23-CA32 is in wt/k22w, working cv ca32 (receiveWith reads c.unsigned.world only through the signed bytes). Outputs go to logs/kernel23-ca32*.
- ca32: K23-READER-CA32 returned LAND-WITH-FIXES (F1: rowView_world + the end-to-end carry_receive_world; F2: docstring; F3: critique). The lane applied all three plus the tooth deriveTurn_world_sep. Patch 5357c46d (Carry.lean +191), msg logs/kernel23-ca32-msg.txt. Launcher logs/kernel23-landca32.sh re-applies onto main (`checkout -f --detach main` + `apply --3way`) immediately before the judge, per ROOT's HOSTING-13 hazard rule.
- 7364 in-flight judge: checked that no commit 50bf961..main touched Journal.lean or Call.lean, so its working-copy re-base cannot revert anyone's lines.
- **LANDED 12ab757** kernel: cv 7364 (reach_prune_check_call; retryPres in Receive/Call.lean). ROOT told. ca32 judge launched, re-applied onto 12ab757 (logs/kernel23-ca32-commit.{log,pid}).
- Lanes: K23-2290 a39ba75d07974aa4c in wt/k20k (exact proof-bytes row); K23-2281 a04bedeecb1c86671 in wt/kernel (one-pass commit; it sends a DESIGN note and waits for my yes).
- **LANDED 96c6881** kernel: cv ca32 (carry_receive_world + receiveWith/deriveTurn/rowView_world, two leaky teeth). ROOT told.
- K23-2290 DONE: new row proof bytes-per-required 1.000 (wire/required, read from CODEC's size function); absolute bytes-per-inclusion 257.797 kept, values byte-identical. Plants sibling-byte 1.021, extra-sibling 1.132. GATES-8 agreed with three conditions, all met. Patch ebd34ee4. Judge launched, re-applied onto 9ced635. (GATES-8's read of the waste rows serves as the second read; sim-only, no theorems.)
- K23-2281 design APPROVED (logs/kernel23-2281-design.md): a dirty overlay Trie.U sealed once per batch; seal_insU has no premise; commitTrie and commitRefusals each one batch; Required.batchReq. Expected 61851 -> 60448, trie-hashes-per-turn 14.074 -> 13.754. Rows (R2, rowsRun over U) is the NEXT task of the same lane, with a cv task opened.
- **LANDED 7c94e5e** kernel(sim): cv 2290 (proof bytes-per-required 1.000; absolute bytes-per-inclusion kept).
- K23-2281 READY: logs/kernel23-2281.patch 6c091a5f (15 files incl. Host/Proofs/Deployed.lean proof-only and gates/waste.tsv). Counts: seeds 0-63 60448/60448, 64-127 58783/58783, refuse 37119 -> 29613 (measured), absolute row 13.754, BAR 374/374, plant rewalk 1.024. R2 (rows over U) is cv 01a153a5-0e09, next in the same lane. My diff review of Trie.lean U/insT/insU is clean. Reader K23-READER-2281 -> logs/kernel23-reader-2281.md. The CROSS-LAYER lines (HOST, GATES) still have to be added to the msg.
- K23-READER-2281: LAND-WITH-FIXES (re-base union plantedArms/waste; docstrings name the build fallback). Statements: none changed. Exactness confirmed. Sent to the lane together with the CROSS-LAYER lines (ROOT for HOST per ROOT; GATES-9 aa2c78560fb5ff1a6 asked).
- GATES-9 aa2c78560fb5ff1a6 AGREED the 2281 waste rows. The lane re-based onto 5cfd5cf (patch 740ea346); I re-applied onto 220f0ed and launched the judge (logs/kernel23-2281-commit.{log,pid}). The lane starts the R2 design meanwhile.
- 2281 judge 1 REFUSED on owners only: Kernel/Proofs/Value.lean is LEDGER-owned. Asked LEDGER-6 ae39612ab24612424 to agree (admit_sum proof-only). GATES-20b landed as 8c2c5fd: paths are now merged from the first-attempt copy, and stale paths are refused.
- LEDGER-6 AGREED the Value.lean hunk. 2281 relaunched, re-applied onto 8c2c5fd (logs/kernel23-2281-commit.log).
- ROOT queued: invoke_next_slots for LEDGER-14 (ebe9d81), after 2281/R2; cv task opened.
- Lane K23-INVOKE in wt/k22w on cv 01a15412-44e2 (invoke_next_slots for LEDGER-14), running in parallel with 2281/R2. Outputs logs/kernel23-invoke*.
- K23-INVOKE DONE: logs/kernel23-invoke.patch 164aa622. invoke_next_run/invoke_next_slots discharge LEDGER-14's Runs.cons premise. DEPLOYED: checkState now requires strictly ascending keys (tightened); writeOf claims the receiver's cell (.keep when empty). The nested-invoke scope is filed as cv 01a15430-0f62. Reader K23-READER-INVOKE -> logs/kernel23-reader-invoke.md, which will also rule kernel vs kernel!.
- **LANDED 258c273** kernel: cv 2281 one-pass commit (cells+refusals). ROOT told. R2 lane released onto wt/kernel.
- K23-READER-INVOKE: LAND-WITH-FIXES as kernel! (create with non-canonical state used to be admitted; the flag day must say so). The fixes, plus ROOT's conditions (flag day, WHY canonical, plant with ascending control), were sent to the lane.
- K23-INVOKE fixes done: patch 7defe195 on 258c273, kernel!, probeStateOrder plant with 5 arms (mutation confirmed), invoke_ok extended (judge conjunct). Ledger.lean:450 needs one underscore line; asked LEDGER-6. Launcher logs/kernel23-landinv.sh.
- R2 READY: logs/kernel23-r2.patch fc4ce3f9 on 258c273. Row-insert 6912->4416, stem 28672->24576, worstcut 32.938->32.217 (measured), plant rows-rewalk 1.228. The closure-call finding is filed as a cv task. Reader K23-READER-R2 -> logs/kernel23-reader-r2.md. GATES-9 asked. Lane K23-2281 is at 416K: RETIRE after R2 (its continue file is current).
- LEDGER-6 asked for invoke_next_judged (a sibling with invoke_next_slots' premises, giving the judge fact). K23-INVOKE is adding it. LEDGER-6 gets the hash.
- K23-READER-R2: LAND-WITH-FIXES, both fixes are cv filings: 01a15460-e096 (structural retainAt on U; the seal-first retract is a matched over-count) and 01a1545b-1daf, annotated (@[inline] rather than a class). GATES-9 agreed the R2 waste rows. The R2 judge is launched from wt/kernel on 258c273 (logs/kernel23-r2-commit.log). Lane K23-2281 RETIRED at 416K; its continue file is logs/kernel23-2281-continue.md.
- invoke kernel! judge launched from wt/k22w on 258c273 (logs/kernel23-invoke-commit.log). LAUNCHER BUG: a lane's untracked new file (InvokeNext.lean) survives `checkout -f` and makes `apply --3way` abort. Remove the patch's new files before applying.
- R2 judge 1: REFUSED on a waste.tsv merge conflict with PERF-11 41e041f, which had already re-pinned worstcut to 32.217 after 2281. Re-applied on 41e041f taking PERF-11's rows verbatim; the msg now says R2 lowers only the rows shape (24.892 -> 20.849, not the max) and the ROOT for PERF line is dropped. Patch r2b 2725aae2. Relaunched.
- PROTOCOL-21 ae0d672d0913e23a5 asked for headOf_width_fold. Lane K23-WIDTH a3cbbb7837a3c372b is in wt/k20k.
- **LANDED 5807a47** kernel!: invoke_next_slots/run/judged (flag day: checkState stateKey; every Store re-geneses). ROOT and LEDGER-6 told. K23-WIDTH DONE (patch 643b7b2d, Versions.lean +460; RowsCanon only). Reader K23-READER-WIDTH running.
- K23-READER-WIDTH: LAND-WITH-FIXES (F1 declareLoose must keep every guard except keyTaken; F2 reborn tooth wording; F3 the hr accounting). Sent to K23-WIDTH. True with no Lawful/RowsOk (axioms standard).
- LEDGER-6 asked for invokeRun_live public and for a witness that receive+admit accept a programmed invoke. The invoke_next_* premises were UNWITNESSED, so this is a vacuity gap in my own landed theorems. Lane K23-WITNESS af088297b3257464c in wt/k22w is building both.
- R2 judge 2 REFUSED: Gen.lean plantedArms conflict with 5807a47. Resolved as the union; whole tree 585 green, sim64 ALL PASS. Relaunched (patch r2c 2fdc77ea). The width fixes are done (f627e67e on 5807a47). Width lands AFTER R2, since its proof needs R2's mechanical edits once R2 is on main.
- COLLISION: KERNEL-24 a8945be219d62cef5 (redesign-day lane) used wt/k22w at ~11:46 and reverted K23-WITNESS's InvokeNext.lean. Its save is logs/kernel24-saved.patch. It has moved to wt/k24. Lane told to restore; asked ROOT what KERNEL-24's scope is.
- ROOT scope split: KERNEL-24 owns the grant/transfer/credit/cancel redesign kernel!. Shared files: World.lean Refused, Bounds, Fold, RefusalsBound, plus a new RotateStale.lean; agreed. R2 lands first. PROTOCOL-21's ETA for width is after R2.
- **LANDED 5e33878** kernel: R2 rows over U. ROOT, KERNEL-24 told. K23-WITNESS DONE: patch 5648269b (invokeRun_live + InvokeWitness.lean with ∃-witnesses through real Lang.program; first Kernel->Lang import; patch includes SIZE.md, which must be dropped). Reader K23-READER-WITNESS running. Width lane re-basing onto 5e33878.
- K23-READER-WITNESS: LAND-WITH-FIXES (drop SIZE.md; docstring on the hand-built w0). Sent to the lane. Width judge launched on fba51dc via the generic launcher logs/kernel23-landgen.sh (WT NAME MD5; it removes the patch's untracked new files before apply).
- Witness fixes done (patch 45539d5b). Judge launched on 2e84396. Width judge in flight.
- **LANDED c69750a** kernel: headOf_width_fold (PROTOCOL-21 and ROOT told).
- Witness judge 1 REFUSED on size (the SIZE lines were not in 'SIZE: metric: why' form). Fixed and relaunched.

## KERNEL-24 (2026-10-21) — the redesign day: law_judged, counted value rights, the cancel record

- **The worktree mistake.** wt/k22w was KERNEL-23's LIVE worktree. I saved its diff to hbox logs/kernel24-saved.patch (and kernel24-saved-InvokeWitness.lean), reverted its InvokeNext.lean, and detached it to main. I told KERNEL-23 how to restore it. I now work in wt/k24 (the KERNEL-57 landing) and wt/k24b (the kernel! day, uncommitted).
- **(1) KERNEL-57.** `kernel:` with law_judged and law_adopt_refused, plus the sim law-self comment. Read by K24-READER-1: LAND-WITH-FIXES, both fixes taken. The first judge was refused: the message lacked SIZE lines, and devtools tests failed (no lake-built host; parent-gates RED too). It is being re-judged as logs/kernel24-commit1b.
- **(2)+(3) staged in wt/k24b.** It builds the libs Kernel, Codec, Lang, Ledger, Protocol, Host, Emit, Bench, Ops and Census. Hosting OOMs at 10G, which is the slice and not the code. Sims:
  - kernel-sim 16 seeds: ALL PASS, control RED.
  - ledger-sim 1: ALL PASS (84 lines), control RED.
  - codec-vectors re-emitted: 256 vectors, 56 sites.
  - generated files unchanged.
- **Decision text** drafted: scratch k24/k58.md, which becomes decisions/kernel.md KERNEL-58.
- **Agreements:**
  - LEDGER-6 yes, with 4 conditions: no weakening, package bytes unchanged, sim results stated, LEDGER-16 entry.
  - LANG-23 yes.
  - PROTOCOL-21 yes for Verb/Rows (transfer:30). It cuts the settle patch against wt/k24b.
  - KERNEL-23 yes for World.lean Refused, Bounds, Fold and the Versions de-private.
  - HOST-17 asked about Host/{Bounds,Proofs/Deployed,Proofs/Page,Proofs/Serve,Sim/Run,Sim/File}.lean.
- **Open:**
  - K24-READER-2's vacuity read.
  - Rebase onto main: 5e33878 R2, fba51dc, c69750a headOf_width_fold touching Versions.lean, PROTOCOL-59 touching Verb/Rows.
  - PROTOCOL-21's settle patch.
  - HOST-17's yes.
  - The WASTE rows the record field forces.
- **LANDED 628a8b9** kernel: invoke witness + invokeRun_live (LEDGER-6 and ROOT told). No lane of mine is in flight.
- Backlog (next): cv 01a1545b-1daf (rowStepOn closures, @[inline]); 01a15460-e096 (structural retainAt on U); 01a15430-0f62 (nested invoke_next). Retired lanes: K23-2281 (416K). Veterans still usable: K23-WIDTH a3cbbb7837a3c372b (~206K), K23-WITNESS af088297b3257464c (~272K), K23-CA32 a44ffc89b241400ef (~135K), K23-7364 a69e19be3cfda8d59 (~234K), K23-INVOKE a01709cb4f6b04bcb (~354K, near ceiling).

### KERNEL-23 HANDOFF → KERNEL-25 (written 2026-10-19 ~13:30 hbox; KERNEL-23 past ~400K)
LANDED by KERNEL-23, in order: 7c09186 kernel! (rows key LEB128, K22-ROWS) · aa7fa1d (2263 split-leaf keeps digest + absolute row admit trie-hashes-per-turn) · 50bf961 (check_local, K22-LOCAL) · 12ab757 (7364 reach_prune_check_call) · 96c6881 (ca32 carry_receive_world) · 7c94e5e (2290 proof bytes-per-required) · 258c273 (2281 one-pass commit, Trie.U overlay) · 5807a47 kernel! (invoke_next_slots/run/judged; checkState stateKey flag day) · 5e33878 (R2 rows over U) · c69750a (headOf_width_fold for PROTOCOL-21) · 628a8b9 (invoke witness + invokeRun_live).
IN FLIGHT (ROOT's order: 0f62 → e096 → 1daf):
- 0f62, the nested invoke_next (an object invoked inside another object's call tree): lane K23-WITNESS af088297b3257464c in wt/k22w (~272K). Design note to KERNEL first, then build. Outputs logs/kernel23-nested*.
- e096, structural retainAt on U so a retract no longer seals (a matched over-count inside row-retract 768/768): lane K23-WIDTH a3cbbb7837a3c372b in wt/k20k (~210K). Design note first.
- 1daf, @[inline] on rowStepOn and friends: same lane, LAST. Measure the counted hashes (unchanged) and deterministic ticks before/after, plus C excerpts. Outputs logs/kernel23-inline*.
LANDING RECIPE: `bash logs/kernel23-landgen.sh WT NAME MD5`. It checks the md5, runs checkout -f --detach main, removes the patch's untracked new files, runs apply --3way, launches the judge, and writes kernel23-NAME-commit.{log,pid}. Watch for: owners (Value.lean, Ledger.lean, Kernel/Value.lean and Receive/Ledger.lean are LEDGER's; gates/waste.tsv is GATES-9 aa2c78560fb5ff1a6; Host/ is ROOT for HOST); SIZE lines one per metric in `SIZE: <metric>: <why>` form; plantedArms conflicts (take the union); waste.tsv conflicts with PERF.
PEERS: KERNEL-24 a8945be219d62cef5 (wt/k24), the grant/transfer/credit/cancel kernel!. Shared files agreed: World.lean Refused, Bounds cancelBytesMax, Fold.lean refusedBytes, RefusalsBound, new RotateStale.lean (making entry_behind_forever/fold_entryStep/admit_entryStep in Versions.lean public). LEDGER-6 ae39612ab24612424 is composing escrow_invokes_one_payout on invoke_next_*. PROTOCOL-21 ae0d672d0913e23a5 has width. 
OPEN cv: 01a15430-0f62, 01a15460-e096, 01a1545b-1daf, 01a15456-b411 (LANG readState_get, LEDGER's).
- nested (0f62) design APPROVED: (A) via duplicateEffect with TransOrd/LawfulEqOrd on the new theorems only; Invoked = derive's own dispatch walk; witness in a sibling InvokeTreeWitness.lean (relay A -> counter B).
- e096 design APPROVED (retainAtU + seal_retainAtU, Required writtenReq by written-node ids, plant rows-retract-seal). dropHeads-on-U filed as a cv task.
- K23-WITNESS nested DONE: patch 3b60a079 (InvokeTree.lean, InvokeTreeWitness.lean, invoke_of generalised). Reader K23-READER-NESTED running. LEDGER-15 landed as e86f237 (escrow_invokes_one_payout on invoke_next_*).
- K23-READER-NESTED: LAND-WITH-FIXES (F1/F2 text, F3 lawsOf in the conclusion, F4 a walk-record cv task). Sent to the lane. e096 DONE: patch 9db25679, retracts 768->512 at both seed ranges, plant 1.500. Its reader is next.
- K23-READER-E096: LAND-WITH-FIXES (strengthen the toy check with toyOps3). Sent to the lane. Nested judge launched on e86f237 (patch dea59b20). F4 filed as cv 01a15554-cffd.
- e096 fix done (patch 81ff806e on 7862b65). Judge launched from wt/kernel so the lane's 1daf WIP in k20k is left alone. 1daf in progress: perf instructions 173.34G -> 171.19G (-1.24%) after the first inline pass, counted hashes identical.
- nested judge REFUSED by a GATES bug: runs.py:477 KeyError 'W' (no verdict). Reported to GATES-9 and holding. e096 judge is in flight; it may hit the same bug.

### KERNEL-24 HAND-OFF (past the ~350K line; the work is staged and green; what remains is mechanical)
- **LANDED: 7862b65** `kernel:` KERNEL-57 (law_judged, law_adopt_refused, and the sim law-self comment). Its first judge was refused only for missing SIZE lines.
- **STAGED in hbox wt/k24b, on main 7862b65, uncommitted.** Patch: logs/kernel24-day-final.patch (2553 lines). The new file is Kernel/Proofs/RotateStale.lean (a copy is at logs/kernel24-RotateStale.lean).
  - The decision texts are already appended in the tree: decisions/kernel.md KERNEL-58 and decisions/ledger.md LEDGER-16.
  - Builds green: libs Kernel, Codec, Lang, Ledger, Protocol, Host, Emit, Bench, Ops, Census.
  - Hosting OOMs in a 10G scope (the slice). `lake build` with no target is killed at once by the 6–10G scope; build lib by lib.
  - Runs: kernel-sim 16 ALL PASS; ledger-sim 1 ALL PASS (control RED); host-sim 1, host-file-sim 1, lang-journey and rows all pass.
  - codec-vectors was re-emitted from an empty file. emit-rust and emit-hosting --check report no change.
- **BLOCKER: PROTOCOL-21's half**, logs/protocol21-cancel.patch, cut against wt/k24b after its PROTOCOL-59 lands. It brings:
  - Settle/Command `∃ a, recordOf X c v a`;
  - Settle.ofReceipt reading `cancelled`;
  - domCancel in Domains;
  - Host/Page.lean stepEvent tag 2, `[2] ‖ nat64 size ‖ sig ‖ call`;
  - the absorbStep tag-2 arm, plus the theorem that absorbStep on a cancel event records exactly `cancelOf X c sig`.
  HOST-17's conditions on that half:
  - absorbStep refuses a tag-2 event with an empty cancel, one past cancelBytesMax, or a length that overruns, with a plant;
  - stepEvent_size_le's bound becomes eventBytesMax+1+8+cancelBytesMax, stated as a statement change, and the message says whether pageBytes or the serve frame moves;
  - the commit message states 65696 ≤ 262144.
- **THEN, the one `kernel!` commit from wt/k24b:**
  1. `git apply --3way` the protocol patch. If PROTOCOL-59 touched Verb/Rows, re-check the `transfer:N`/`credit:N` and `transfer:30` hunks.
  2. Rebuild lib by lib. Rerun kernel-sim, ledger-sim (+ control), rows, host-sim and host-file-sim.
  3. Paths: everything in `git status`, plus Kernel/Proofs/RotateStale.lean. The SIZE rows that move (measured): modules, proof-modules, the Lean lines of Codec/Emit/Host/Kernel/Lang/Ledger/Protocol/deployed/tooling, max dependents 274→275, theorems, refusal constructors 82→87. Each needs a `SIZE:` line. WASTE: take whatever the judge's waste gate names (expected: the refusal bytes per record, from the +4-byte empty cancel length), each with "Refused.cancel's length prefix".
  4. The CROSS-LAYER lines:
     - "Kernel/Receive/Ledger.lean, Kernel/Proofs/Ledger.lean, Kernel/Value.lean, Ledger/: LEDGER-6 agreed (KERNEL-28 amount right; no statement weakened; package bytes unchanged)"
     - "Lang/Package.lean, Lang/Call.lean, Lang/Proofs/Call.lean, Lang/Proofs/CallLive.lean: LANG, LANG-23 agreed"
     - "Protocol/Command/Verb.lean, Protocol/Rows.lean (+ PROTOCOL-21's own paths) are PROTOCOL's: PROTOCOL-21 agreed"
     - "Host/ is HOST's: HOST-17 agreed"
     - "Codec/, Emit/Vectors.lean, gates/codec-vectors.tsv: CODEC, ROOT for CODEC (two table rules: right_lawfulOn/refused_lawfulOn restated, the refused cancel boundary pair 64/65); GATES named for the tsv"
     - "Kernel/World.lean (Refused), Kernel/Bounds.lean, Kernel/Proofs/{Fold,Versions}.lean shared with KERNEL-23: agreed"
  5. The flag day text is in KERNEL-58's "Flag day" paragraph; copy it into the message. ledger-sim's results go into the message (LEDGER-6's condition 3).
- cv 01a15543-39fd: the Host op, the `nd cancel` verb and the rows line (Receive.cancel is reached from kernel-sim only).

## KERNEL-25 (successor of KERNEL-23 for trie/rows/invoke; started 2026-10-19 ~18:55Z; hbox)
- Start: main = c8ebb06 (GATES-20e). e096 judge alive (pid 1757459, from wt/kernel, launched ~18:28Z; its log is empty until the judge prints). 0f62 nested REFUSED: confirmed `KeyError: 'W'` at gates/runs.py:477 (gate log main/.git/nanodregg-gate-2/12ea5bf99f1b.log), GATES' bug, no content verdict; GATES-10's 20fg judge alive (pid 1857161). 1daf is DONE and staged by the lane: logs/kernel23-inline.patch (World.lean only, cut on top of e096) + msg; waits for e096 to land, then rebase, rebuild, sim64 hashes identical, judge.

## KERNEL-26 (successor of KERNEL-24 for grants/transfer/credit/cancel/adopt; started 2026-10-19; hbox wt/k24b)
- wt/k24b moved onto main c8ebb06 (`git checkout --detach main`, dirty tree carried; main's delta 7862b65..c8ebb06 is gates/ + decisions/gates.md only, so the Lean tree is unchanged). Pre-rebase diff: logs/kernel26-pre-rebase.patch (md5 a9a68132…).
- PROTOCOL-22 (a80837a6484cd9f17) cuts logs/protocol22-cancel.patch against wt/k24b@c8ebb06 WITHOUT P59 (P59's judge was refused by the runs.py:477 KeyError 'W'; whichever lands second re-applies the Verb/Rows hunks). Waiting on it.
- GATES-10's KeyError fix landed fc4022d. 0f62 nested relaunched from wt/k22w on fc4022d (logs/kernel23-landgen.sh k22w nested dea59b20; no main commit since e86f237 touched its three paths): logs/kernel23-nested-commit.{log,pid} (pid 2190261).
- e096 judge 1 REFUSED (saved logs/kernel25-e096-commit1.log): (1) owners: the msg's CROSS-LAYER line was indented, and owners.py matches `^CROSS-LAYER:` only; GATES-9's agreement is at GATES-LOG.md:603; I unindented it (orig saved as logs/kernel25-e096-msg-orig.txt). (2) a NEW RED in launcher members `nd_members_ends_by_name` (378/1024 memberMissing lines after a fixed 2 s sleep, box loaded): a HOSTING timing flake, selected because the waste.tsv change runs every row. Relaunched on fc4022d, pid 2247722. ROOT told.
- PROTOCOL-22's half applied: logs/protocol22-cancel.patch md5 f7b0b755… (14 paths; PROTOCOL-60), plain `git apply` on the dirty tree. wt/k24b then moved onto main fc4022d (20fg; gates-only delta).
- Green on wt/k24b: all libs; kernel-sim 64 ALL PASS (ctl RED); ledger-sim 1 ALL PASS (ctl RED); host-sim ALL PASS (7 plant-cancel-page lines); host-file-sim 1/2/3 ALL PASS (ctl RED); lang-journey GREEN; rows toy+deployed ALL PASS; emit-rust/emit-hosting/codec-vectors `--check PATH` ok (NB: `lake exe emit-rust --check` with no PATH WRITES a file named `--check`; I removed mine). Logs: logs/kernel26-job1.log, kernel26-ksim64.log.
- WASTE moves (three, upward, all per-required rows 1.000): record-bytes-per-refusal 529.217→540.159, trie-hashes-per-turn 13.754→14.087, bytes-per-inclusion 257.797→261.880; re-pinned in the tree (logs/kernel26-waste.py); GATES-10 a2a3cc81d1ea89c5a asked; ROOT: if no answer within the hour, write "ROOT for GATES".
- Message draft: scratch kernel26-msg.txt (copied to hbox logs/kernel26-msg.txt at landing). Waiting on PROTOCOL-22's reader before landing.
- PROTOCOL-22 FINAL (second-agent read clean, fixes applied): delta logs/protocol22-cancel-delta.patch (md5 ed437fee) applied on k24b (cancelParts_some, absorbStep_cancel_canonical, cancelAuth in absorbStep_refusal_recorded); rebuilt Protocol/Host/proofs, host-sim, host-file-sim 1/2/3, rows toy+deployed ALL PASS. GATES-10 agreed the three waste re-pins.
- JUDGE launched from wt/k24b: logs/kernel26-commit1.{log,pid} (lander pid 2458777; judge pid in kernel26-commit1-judge.pid); msg logs/kernel26-msg.txt; first-attempt copy logs/kernel26-final.patch (md5 0df79aa0) + logs/kernel26-RotateStale.lean.
- **LANDED ececba1** kernel: 0f62 nested invoke (invoke_tree_slots/run over Invoked; witness relay A -> counter B). Proof-only, no WASTE. ROOT told. F4 open as cv 01a15554-cffd.
- e096 judge 2: PRE-PUSH GREEN (55 runs; the members flake did not recur), displaced once by 5325ab5, re-basing.
- Judge kernel26-commit1: PRE-PUSH GREEN twice (trees 2f46918ad7df on fc4022d, 3dcba030de77 on ececba1), displaced twice (ececba1 K25 nested invoke, 56fffd7 ops, cdd9d84 P59), then REFUSED: merge conflict in decisions/protocol.md (P59 and PROTOCOL-60 both append). Re-based wt/k24b onto cdd9d84: `checkout -f --detach main` + `apply --3way logs/kernel26-final.patch` + RotateStale copy; conflict resolved keep-both (P59 sections, then PROTOCOL-60; logs/kernel26-resolve.py). Full rebuild + sims rerunning: logs/kernel26-job3.log.
- On cdd9d84 everything green again (logs/kernel26-job3.log; waste rows unchanged at 540.159 / 14.087 / 261.880). SIZE re-read: theorems 4966→5007, max dependents 277→278. Judge relaunched: logs/kernel26-commit2.{log,pid}, first-attempt copy logs/kernel26-final2.patch (md5 97d9ab6c) + kernel26-RotateStale.lean.
- **LANDED c15487e** kernel: e096 retainAtU (retracts 768 -> 512; plant rows-retract-seal 1.500). Judge 2 green, displaced 3x. ROOT told.
- 1daf: wt/k20k's WIP saved (logs/kernel25-k20k-saved.patch 001602a7). Pre-check on 56fffd7+e096+inline: build ok, sim64 ALL PASS, 28 required/WASTE lines identical to the lane's run, closure ok (logs/kernel25-inline-*). The msg gains a re-check line and my co-author line (orig logs/kernel25-inline-msg-orig.txt). Judge launched via landgen k20k inline c03c4a36 on c15487e: pid 3097214.
- ROOT-DOCS af09ef8e4036ea161: said yes to a path-only citation rewrite in decisions/kernel.md.
- commit2: PRE-PUSH GREEN on cdd9d84 (a6cee86b73e9), displaced by c15487e (K25 e096: World.lean, Sim/Gen.lean, waste.tsv; all merged clean 3-way), then REFUSED: all 4 judge slots busy for 30 min. Relaunched as logs/kernel26-commit3 (same first-attempt copy, md5 97d9ab6c).

## KERNEL-27 (proof logic: Kernel/Proofs/Logic/*; started 2026-10-19 ~18:45Z; hbox wt/k27)
- ASSUMED checks (brief §5), at a108b15:
  - `write_judged` is ABSENT (only `write_authorized`). Q3's write step needs it: build it first.
  - `attenuation_le` is ABSENT (`grant_carves` is the landed attenuation).
  - `submit_replayed` has no Within bound: it is per-state. The window is `journalForgets` = notBefore + 2·windowMax ≤ H, in heights, not log length.
  - C3 puts Prop statements in PROOF modules, not def modules (correction to the brief).
- Q1 (KERNEL-58):
  - `Derived` replaces `receive_ok` and is proved by `receive_derived`, in Kernel/Proofs/Receive.lean.
  - Logic/Triple.lean: CallFoot (at w: pins, untaken ids, unspent nullifiers), Triple, Indep, callFoot_of_turn, call_frame, submit_frame, not_callFoot_live, indep_live, plus 3 teeth.
  - Reader K27-READER-1: no blocker, 3 fixes taken.
  - Landing log: hbox logs/kernel27-land2.log (land1 was refused for missing SIZE lines only).
- Q3 waits on LANG-25 (`Chain lib law`, `chain_invariant`, `chain_count`). First build `write_judged`. `ObjectStep.frame` uses `not_callFoot_live`/`indep_live`.
- **LANDED 6db92a7** kernel: 1daf @[inline] row-store touch (hashes/WASTE identical; 173.34G -> 171.19G instructions). Green, displaced 2x. ROOT told. HOSTING fixed the members flake as 978c9cf.
- State: ROOT's order 0f62 -> e096 -> 1daf DONE. No judge of mine in flight. wt/kernel, wt/k20k, wt/k22w hold only their landed patches (safe to reset to main). Open: cv 01a15554-cffd (F4 walk-record predicate, before LEDGER 01a1553b-2765), dropHeads-on-U (filed by K23-READER-E096 design). Offered F4 to ROOT as next.
- F4 (cv 01a15554-cffd): KERNEL-27 a8eb80aab51d56a49 AGREED `Dispatched X w c n wk actor b` (n and wk visible; no uniqueness needed; root covers the signed invoke so ObjectStep has ONE invoke case; laws + judge (some p) + fuel min budget wk.pool in the conclusion). It lives in a PROOF module (C3: Prop statements are proof-module only). Built in wt/kernel on 6db92a7: patch logs/kernel25-f4.patch 7a6daeb0 (InvokeTree.lean, InvokeTreeWitness.lean). invoke_tree_slots/_run restated over Dispatched (pinned actor/method/args/fuel), dispatched_of_invoked bridge, dispatched_of_signed, tooth dispatched_pins_args. lake build Kernel Ledger ok, closure ok, axioms standard. SIZE Kernel 32108->32290, theorems 4982->4987. Msg drafted (scratch kernel25-f4-msg.txt). Reader K25-READER-F4 -> logs/kernel25-reader-f4.md.
- K25-READER-F4: LAND-WITH-FIXES (F1/F2 docstrings applied; F3 optional actor tooth not taken, said in msg). Patch re-cut 6748bb82. Judge launched from wt/kernel on 6db92a7 via logs/kernel25-land.sh (KERNEL-25's copy of landgen with kernel25- naming): logs/kernel25-f4-commit.{log,pid} pid 3732044.

### KERNEL-25 HANDOFF → KERNEL-29 (written 2026-10-19 ~20:50 hbox; ROOT: KERNEL-25 past 450K)
LANDED by KERNEL-25: ececba1 (0f62 nested invoke_tree_slots/run, relaunched after GATES' KeyError fix fc4022d) · c15487e (e096 retainAtU; retracts 768 -> 512) · 6db92a7 (1daf @[inline] row store; -1.24% instructions, hashes identical).
IN FLIGHT: F4 cv 01a15554-cffd judge (logs/kernel25-f4-commit.{log,pid}, patch logs/kernel25-f4.patch 6748bb82, msg logs/kernel25-f4-msg.txt). If REFUSED: read why; relaunch with `bash logs/kernel25-land.sh kernel f4 <md5>` (it does checkout -f main + apply --3way, so re-cut the patch with `git diff > logs/kernel25-f4.patch` first if you edit). WHEN IT LANDS: tell ROOT and KERNEL-27 a8eb80aab51d56a49 the hash and the final statements (KERNEL-27 asked for both; its ObjectStep has ONE invoke constructor over `Dispatched`, and dispatched_of_signed covers the top level). F4's shape was agreed with KERNEL-27: `inductive Dispatched X w c : Nat → Walk D → D → Body D → Prop` in Kernel/Proofs/InvokeTree.lean (C3: Prop statements live in proof modules only).
OPEN cv (mine):
- 01a1553a-c095 dropHeads on the overlay U: after e096, rowsRun still SEALS before dropHeads, which stays on T, so a retirement's head removals re-hash nodes the batch already wrote. Moving dropHeads onto U needs an `under` listing on the overlay (Trie.U). Measure the worstcut retires shape and the rows probe before/after (kernel-sim --seeds 64 required:/WASTE lines; the rows probe's retires turns); expect the row-retract and worstcut retires rows to fall; write Required's retire model as one batch; a plant that seals before dropHeads must read > 1.000. Design note to ROOT first (it moves Required and probably a WASTE row: GATES agreement, cross-layer line flush-left `CROSS-LAYER: gates/waste.tsv: GATES-N agreed …`).
- Optional follow-up of F4: dispatched_invoke_unique (one dispatched invoke per object in an ok derivation, by `revisited`); nobody needs it now (KERNEL-27 said no).
- LEDGER's 01a1553b-2765 (an escrow Invokes witness) is unblocked by F4.
LANDING NOTES learned this session: owners.py matches `^CROSS-LAYER:` only (an indented line is invisible); a waste.tsv change makes EVERY row run (55 runs, ~35-40 min per judge); each displacement re-judges in full (e096 took 2h34m for 3 displacements); output of scripts/commit appears only at stage ends, so an empty log for 30+ min is normal. Use `ssh -n` for every hbox call with a nohup inside, or the ssh hangs. Build helper: logs/kernel25-b.sh TAG TARGET... (wt/kernel, writes kernel25-TAG.{log,done}). SIZE measure: `python3 gates/size.py . --write; git diff SIZE.md | grep "^[-+]|"; git checkout -- SIZE.md`.
Worktrees: wt/kernel holds F4 (being judged; leave it until verdict). wt/k20k and wt/k22w hold only landed work (safe to `checkout -f --detach main`). wt/k20k's pre-1daf WIP is saved at logs/kernel25-k20k-saved.patch.

### KERNEL-27 continuation: the Q3 kernel half (design, read at 338f8c1; not started in code)
LANG-25 landed `Std.Chain R`, `Std.Step lib law := Admits ∧ LawKeeps`, the chain_* schemes, and `fault_never_admits` (Lang/Proofs/Chain.lean and Receiver.lean). `fault_never_admits` is landed, so it is not mine. Target: `Std.Chain (Std.Step lib t) o steps` (write `Std.Chain`, which collides with `Kernel.Proofs.Chain`).

Simplifications found:
- (a) Every stdlib law is `NoRef` (Lang/Proofs/Receiver.lean:268-332), so `t.relocate f = t` (`relocate_noRef`). With LANG-61's `bigStep_relib`, Admits of a NoRef law does not depend on `lib`. So state the lift for `NoRef t` over a fixed lib (`[]`). That removes the closure-determinism problem (judgeOne_admits' `lib`/`f` are per-view existentials).
- (b) The law package is ROM (`fold_rom`), so every step's `readPackage look law` reads the same `p`. Lemma needed: readPackage depends only on `look law`.

Pieces, in order:
1. `write_judged` (ABSENT today): write's analogue of `law_judged`, read off Derive.lean:152-165, plus write's next-state lemma. Build the latter from `admit_live_write` (InvokeNext:331) and `diffOps_next` (:226); the write's state is `applyEdits old edits`, which needs `checkState` of it, or a direct proof.
2. LawKeeps for a law turn: law_judged's effects are `writeOf obj (diffOps (lawSlotsOf cell) (lawSlots X laws'))`, which touch only law slots below stateBase. So stateOf is unchanged.
3. Invoke steps: through K25's `Dispatched` / `invoke_tree_slots_at` (cv 01a15554-cffd; I answered K25). Its root case covers the top-level invoke, so there is ONE invoke constructor and no uniqueness is needed. Dispatched must live in a PROOF module (C3).
4. `ObjectStep` / `ObjectHistory`, with constructors frame (`¬ CallFoot X c w (.cell obj)`, via `not_callFoot_live`/`indep_live`), keep, write, law, invoke(Dispatched). Then `object_history_chain : ObjectHistory → Std.Chain (Std.Step [] t) (stateData) steps`.
5. THE HARD LEMMA, totality (`audit X w l = .ok w'` + obj live ⇒ ObjectHistory): no receiver but write, law or invoke ever puts a non-keep effect on a kindObject cell. Every other receiver's effect is at a cell it read with `readKind` of another kind: member (rotate), grant (enroll, grant carve, revoke), account (transfer, credit). InvokeTree's header lists exactly this as "not proved here". It needs one lemma per receiver plus the tree induction (`deriveCalls`/`callStep`). Coordinate with K25, who owns the tree.
6. Instances: Ledger's `Runs`/`Invokes` become ObjectHistory restricted to invoke steps; `invokes_runs` becomes a corollary; then re-derive `escrow_*_one_payout` by `chain_count`. LEDGER files go through ROOT. Then count the 47 never/once/after theorems.

Premises the lift takes (none are new to landed theorems):
- `X.Lawful` (taken by 116 landed theorems, e.g. `escrow_invokes_one_payout`);
- `X.program = Lang.program …` (taken by `escrow_*`);
- the law package live and ROM at obj's start;
- `audit` (Honest, through `audit_ok`; landed users are `honest_callLog` and `fold_prune_check`'s CallLog).
- LANG-25 is landing `judgeOne_admits_relib` (Lang/Proofs/Extract.lean): it gives the same premises as judgeOne_admits and concludes ∀ lib', Std.Admits lib' t (reqData bytesOf r) n o for NoRef t, so fix lib := []. Use it in place of judgeOne_admits.
- LANDED 99771b9 (Q1, KERNEL-58), pushed. Three attempts: the first was refused for missing SIZE: lines; the second was displaced twice and then timed out waiting 30 min for a slot; the third landed by CAS.
- HAND-OFF at ~290K: Q3's kernel half is not started in code. A successor starts from the "KERNEL-27 continuation" above. wt/k27 sits clean at 99771b9 on hbox.
- commit3: PRE-PUSH GREEN twice more (5ed78bfe4055, 7e9a32633085), displaced by 6f4032a host and 6db92a7 kernel (both merge clean), then RED only on cargo:launcher:resident whose last line is a strace PTRACE_LISTEN I/O error (tracer flake; also hit another lander's broker run at gate-3/2b29a0426731); reported to GATES-10; relaunched as logs/kernel26-commit4.
- commit4 REFUSED at once: merge conflict in decisions/kernel.md: Q1 (99771b9, KERNEL-27 lane) landed its own "## KERNEL-58 AS BUILT". My decision is RENUMBERED KERNEL-59 everywhere this commit writes it (code comments, waste.tsv sources, LEDGER-16, PROTOCOL-60, the message); main's KERNEL-58 untouched. Re-based onto 99771b9 (same recipe), rebuilt, all sims green, every waste row measured == ceiling (logs/kernel26-job4.log). Judge 5: logs/kernel26-commit5, first-attempt copy logs/kernel26-final4.patch (md5 8d70d63c) + kernel26-RotateStale.lean.
- judgeOne_admits_relib LANDED ce6743a (LANG-25); use lib := [] in object_history_chain.

## KERNEL-28 (proof logic, Q3 kernel half; successor of KERNEL-27; started 2026-10-19 ~22:10 hbox; hbox wt/k27)
- Note: "KERNEL-25 HANDOFF → KERNEL-28" above is for KERNEL-25's trie/rows/invoke successor, not this lane (name collision; K25 told ROOT).
- wt/k27 on ce6743a (LANG's judgeOne_admits_relib landed by ROOT's LANG lane; my own copy of it was dropped) + F4 patch logs/kernel25-f4.patch applied (judge in flight from wt/kernel). WIP snapshot: logs/kernel28-wip1.patch + logs/kernel28-{WriteNext,History}.lean.
- BUILT GREEN (not landed): Authority `write_judged` + tooth `write_law_refused`; new Kernel/Proofs/WriteNext.lean (`CellsCanon` invariant: admit/fold/audit/genesis; `applyEdits_checkState`; `write_next_slots`, `law_next_slots`; tooth `write_needs_canon`: a non-canonical cell makes the edit-free write's diffOps re-set the first entry, so the state left is not the state judged); InvokeTree totality `effect_at_object`, `object_turn_cases`, tooth `effect_at_object_needs_kind`; InvokeNext: readKind_pinned public, invoke_next_judged exposes lawsOf; Kernel/Proofs/Logic/History.lean: `ObjectStep` (refusal, other, frame, write, law, invoke, nested), `ObjectHistory`, `object_step_none/_some/_live`, `object_history_of_audit` (totality at the log, from CellsCanon), `object_history_chain` (the lift to Std.Chain (Std.Step [] t)).
- FINDING: `write` has no `checkState` of its new state; the write link needs every live cell canonical. That held but was unstated; now `CellsCanon` (genesis + every admit) proves it.
- Build helpers: logs/kernel28-b.sh TAG TARGET..., logs/kernel28-wait.sh TAG DEADLINE.
- KERNEL-28 ac5a6433f2fea8b56 (KERNEL-27's successor, Logic/*) builds on F4 6748bb82 and will edit my files AFTER F4 lands, in its commit: InvokeTree.lean gains effect_at_object / object_turn_cases / tooth effect_at_object_needs_kind (imports Kernel.Proofs.Authority); InvokeNext: readKind_pinned public; invoke_next_judged conclusion strengthened (∃ laws, lawsOf ∧ judge). KERNEL-25 AGREED (strengthening, no premise). KERNEL-29: tell KERNEL-28 before you touch InvokeTree/InvokeNext. Handoff header renamed → KERNEL-29 (ROOT).
- ROOT HOLD: no NEW scripts/commit until ROOT sends GATES-22's hash. F4's judge 3 (pid 14219, green on content, displaced once by ce6743a) runs to its end; if it is slot-refused, KERNEL-29 relaunches F4 (`bash logs/kernel25-land.sh kernel f4 6748bb82f7ea0ba0ec87fb41179cf8eb`) ONLY after GATES-22's hash. When F4 lands: hash to ROOT and to KERNEL-28 ac5a6433f2fea8b56 (it builds on 6748bb82 and lands its InvokeTree/InvokeNext edits after F4).
- K28-READER (second agent, disjunct check): LAND-WITH-FIXES, no vacuity, no premise gained. Fixes TAKEN: (2) `ObjectStep.other` could file an invoke whose run kept the state as "left alone": `other` now needs NO touch of obj (old Invokes.other), new `keep` (call-derived, keeps, and NOT a write/law/Dispatched invoke of obj); `object_turn_cases`' keep case now proves those three negations (via dispatched_ok), so a history counts every invoke; (3) witnesses: new Kernel/Proofs/Logic/HistoryWitness.lean `object_history_chain_witnessed` (X.Lawful + in-force cap law + one-step chain, from new public `invoke_lift_witnessed` in InvokeWitness), `write_history_witnessed`; (4) `object_history_needs_inForce` now a real tooth (write history judged by no law: a refusing NoRef law has no chain); `law_slots_need_bound` shows the 15th law slot IS stateBase; (6)(7) docs. Not taken: `effect_at_object_needs_kind` stays one-receiver (said in the decision's critique).
- decisions/kernel.md KERNEL-59 appended in wt/k27. All green: Kernel, Ledger (last), Codec Host Protocol, Lang Hosting (16G) earlier. HOLD (ROOT): no scripts/commit until GATES-22's hash; F4 (K25) must land first (my InvokeTree diff sits on it).
- F4 judge 3 (pid 14219): PRE-PUSH GREEN on ce6743a's parent, displaced once, then slot-refused on re-judge (log saved logs/kernel25-f4-commit3.log). NOT relaunched per ROOT's HOLD. NEXT ACTION (KERNEL-25 if resumed, else KERNEL-29): after ROOT sends GATES-22's hash, `cd /tank/dregg-build/nanodregg/logs && bash kernel25-land.sh kernel f4 6748bb82f7ea0ba0ec87fb41179cf8eb` (ssh -n), foreground-wait on logs/kernel25-f4-commit.pid, then hash to ROOT and KERNEL-28.
- ROOT ruling (supersedes the relaunch above): do NOT relaunch F4. KERNEL-28 ac5a6433f2fea8b56 lands F4 inside its own `kernel:` commit, with F4's text verbatim and credit to KERNEL-25 and K25-READER-F4, so one judge runs instead of two. KERNEL-29: do not touch wt/kernel's F4 or logs/kernel25-f4*; check main for KERNEL-28's landing before any InvokeTree/InvokeNext work. KERNEL-25's lane is done.
- commit5: PRE-PUSH GREEN on 99771b9 (68b3884b0302), displaced by 1d542f1 (HOST: Host/Proofs/Refine.lean, Host ⊑ Kernel), then RED build: Refine.lean used `judge` where Honest now re-judges by `recordedBy`. Fixed: new lemma Kernel/Proofs/Audit.lean `recordedBy_of_judge`; Refine's commit arm uses it (statement unchanged); host_step_folds_tooth_censor gains `(hk : r.cancel.size = 0)` (forced: a record with a cancel field is a member's cancel, which Honest rightly accepts). HOST-17 asked. Re-based onto 173993d. ROOT: HOLD new launches until GATES-22's hash. Rebuild job: logs/kernel26-job5.log.
- job5 green on 173993d (8 ALL PASS + GREEN, waste == ceilings). HOST-18 agreed the Refine edits (conditions written into the message: tooth statement change named, audit_cancel_forged named, CROSS-LAYER line). Message final in logs/kernel26-msg.txt; first-attempt copy logs/kernel26-final5.patch (md5 ee3c9e01). HOLDING for GATES-22's hash (ROOT); launch = `bash logs/kernel26-land.sh 6` from hbox wt/k24b.
- GATES-22 landed e568634; judge 6 launched: logs/kernel26-commit6 (copy md5 ee3c9e01).
- **LANDED 4442b43** kernel: Q3 kernel half + F4 (one commit, ROOT ruled (b); fast judge after GATES-22 e568634). ROOT and KERNEL-25 told (hash, statements, deletions Invokes/invokes_runs → ObjectHistory instance, 47-count: 1 of 93 names (escrow_runs_after_payout), CellsCanon finding = proof-only). GATES bug reported: scripts/commit line 119 `cat "$ND_TICKET"` under set -u in fast mode killed commit1's re-base (commit2 printed it and still landed).
- Open (not done): write could refuse a non-canonical edit result as a deployed check (offered to ROOT, not built); `effect_at_object_needs_kind` covers revoke only; a history from an object's birth needs the log split at the birth.
- wt/k27 clean at 4442b43. KERNEL-28 stops here.
- **F4 LANDED inside 4442b43** (KERNEL-28's kernel: commit; F4 msg verbatim; also effect_at_object/object_turn_cases in InvokeTree, invoke_next_judged + lawsOf, readKind_pinned public, invoke_lift_witnessed). cv 01a15554-cffd closed. wt/kernel's applied F4 copy is now stale: KERNEL-29 may `checkout -f --detach main` there.
- commit6: PRE-PUSH GREEN (7168e4c10f5d) on e568634, displaced by 4442b43 (Q3, KERNEL-59 AS BUILT) and REFUSED on decisions/kernel.md conflict. Renumbered again: my decision is KERNEL-60 (LEDGER-16 kept; main has LEDGER-17). Re-based onto 4442b43; rebuild job6 running.
- job6 RED: 4442b43's Kernel/Proofs/InvokeTree.lean (KERNEL-25's dispatch_other) broke on my receiver shapes; repaired proofs only (spendAt_at, spendVia_other, checkParent_at's two branches, grant/transfer/credit arms); KERNEL-25 asked. Job7 (full) running.
- KERNEL-26 aa21b8d4f926a4787 asked to carry a proof-only repair of Kernel/Proofs/InvokeTree.lean in its kernel! (KERNEL-60): private spendAt_at and spendVia_other, plus updated destructuring in checkParent_at and dispatch_other for checkRights and the third `spendVia` effect. I read the diff in wt/k24b (no statement line changes) and AGREED. I told it to name KERNEL-28 too, since dispatch_other/effect_at_object are KERNEL-28's section.
- job7 RED: Kernel/Proofs/Logic/History.lean:251 (Q3, KERNEL-28) used judge_recorded on a recordedBy hyp; now (recordedBy_recorded hj).1. KERNEL-25 agreed InvokeTree (named KERNEL-28 for dispatch_other); KERNEL-28 asked for both. Job8 running.
- KERNEL-28 agreed both repairs. job8 green on 4442b43 (8 ALL PASS + GREEN, waste == ceilings); SIZE theorems 5115→5159, dependents 293→294. Worktree moved to main 94d5bb6 (gates-only delta). Judge 7: logs/kernel26-commit7, copy logs/kernel26-final6.patch.
- **LANDED 7a1cdd7** kernel! (KERNEL-60, LEDGER-16, PROTOCOL-60; judge 7 head, displaced 0 times, PRE-PUSH GREEN a9a10efe005f). ROOT, PROTOCOL-22 (nd cancel) and HOST-18 (the cancel Host op) told. No lane of mine in flight. wt/k24b is now on 7a1cdd7, clean apart from SIZE/logs.
- Lessons: decision numbers are taken at LANDING, not drafting (renumbered 58→59→60); every rebase onto a main with new proofs met by the new shapes (Refine, InvokeTree, History) needs a full lib build before relaunch, since GATES' 3-way merge is textual.
- Next for the grants half: cv 01a1553b-2765 (LEDGER's escrow deposit as the first transfer (cap) user; LEDGER not live, ROOT told).

## KERNEL-30
2026-10-22. LANDED 1fe9f93 (kernel:, fast GREEN, built Kernel and Ledger). Recorded as decisions/kernel.md KERNEL-61.

The LEDGER-7 finding (a spend was never read back) is closed proof-only. LedgerContiguous holds for every receiver, so there is no kernel defect.

Files:
- Kernel/Proofs/LedgerNext.lean (new): GrantContiguous/LedgerContiguous; genesis/step/submit/audit_ledgerContiguous; derive_born_grant; admit_retired; grant_turn_cell; grant_turn_ledger; ledgerLeft_append; spend_reads_back(_dispatched); credit_reads_back(_dispatched); teeth gap_never_falls, gap_world_not_contiguous, two_spends_refused.
- InvokeTree: effect_at_grant, plus LedgerBase/LedgerSpend. The private totality was strengthened (OtherEffect; EffectsAt records the invoke's object read).
- Visibility only: dispatched_ok, sealTurn_firstDup, actFor_of_nodup, mem_set, set_pairwise, slotsOf_ascending.

Reader K30-READER: LAND, and its label fixes were taken. LEDGER-7 agreed the statements before the build and was sent the hash and statements.

Consumed: LEDGER-7's LEDGER-19 (Ledger/Proofs/GrantCap.lean: grant_moves_le_cap, grant_credits_le_cap) builds on these theorems. LEDGER-7 declined the checkParent carve read-back for now: a carve's u already counts in its sum, so it only tightens the bound. If a carve sum is wanted later, it becomes a cv task.

Gotcha: rcases `-` on an existential witness clears every hypothesis that mentions it, including the equation you wanted. Name the witnesses `_` instead.

Worktree /tank/dregg-build/nanodregg/wt/k30 is left on the new main.
