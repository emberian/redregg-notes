# STORE-ROOT log (continuation file) — started 2026-10-14
Lane: STORE-ROOT (Claude). Item: SINS-LEDGER §1 D3/D5/D6/D9 — nothing keeps the world root.
Plan: (1) persist the tree in the checkpoint; (2) compress the tree (default-subtree SMT / Patricia); (3) the session's tree is the only one.

## events
- start: read SAFETY-BLOCK, SINS-LEDGER §1, PERF-FIX-LOG. Next: mirror refs (next?), source read for design.
- lane tree hbox:/tank/dregg-build/claude-lanes/store-root/src, branch store-root @ 5b7cae0d (lane/perf-fix tip = the floor;
  mirror has no `next` yet; 30a5009a is NOT an ancestor of 5b7cae0d -> rebase onto next when INTEGRATOR publishes).
  .lake/build = full COPY of warm-7dea0626 (667M, no shared inodes); .lake/packages cp -al (never rebuilt).

## DESIGN (read at 5b7cae0d)

### What exists (READ)
- Spec today: `Theory.AuthMap.Scheme.root` (uncompressed, depth 256, empties table); world root `WorldRoot.deployedRoot es
  = deployed.root (slotsOf deployed.ix es)` (slot = LAST entry per 256-bit PATH). Cache `WorldRootCache.Tree` = same
  uncompressed tree: a leaf only at height 0, every insert 256 node hashes (`insertWrite_nodeHashes`).
- `Theory.AuthTrie` ALREADY IS the compressed trie (Jellyfish leaf-shortcut: 0 entries -> dig empty, 1 -> its leaf at the
  highest level where it is alone, >=2 -> branch(hash children)); `tree n es`, `climb`, `verify`, `verify_sound` (answer =
  lookup or `Collision dig`). Used by DurableIndex. NOT proved there: honest-opening completeness; incremental insert root.
- Root consumers: DurableCheckpointCodec.worldRoot (openSealed recompute), DurableReceiverCore RootCache/RootsExact
  (+ injective flag, writeAllFresh?, fallback rebuild `else deployedRoot entries` in DurableServed:791, :1031, Core:1038,
  :1350), NativeHostCodec (world_opening at deployed), ReceiptContinuity (`opens`: deployed.verify of the SYSTEM slot with
  EXACTLY 256 siblings; Rust native/resource-client/src/receipt_continuity.rs checks a sibling bound), ReceiptContinuityIO
  (siblings read off the cached tree), WorldRoot binding theory (rootOf_binds etc., only WorldRoot-internal),
  HostRefinesWorldCore (doc only), Host/WorldRootBench.

### Order: (2) compress BEFORE (1) persist
Persisting the 256-level tree = ~cells*246 nodes (~8 MB at 1000 cells) in every checkpoint, deleted one commit later.
Compressed first, then the node table is ~2*cells digests. Same end state, no throwaway format.

### (2) the world root = AuthTrie over the KEY map (one theory, one definition)
- Spec: `deployedRoot es := AuthTrie.tree worldDig 256 (AuthTrie.entries deployedIx (canon es))`, canon = last value per KEY.
  `worldDig : NodeIn Key Digest Digest -> Digest` = cSHAKE256 "DREGG.WORLD-ROOT/v2" over a tagged injective encoding
  (empty [0] / leaf 1::keyBytes++digest / branch 2::l++r); `Collision worldDig -> cSHAKE collision` (as deployedIx_collision).
  Theorem tree_perm: `tree` is invariant under List.Perm (no WF needed) => deployedRoot depends only on `lastVal es`
  (order-free UNCONDITIONALLY). That deletes RootsExact.injective / KeysInjective / writeAllFresh? / every fallback
  rebuild (`if injective then cache else deployedRoot entries`): an index collision (2 keys, one 256-bit path) is just
  a `clash` node at height 0 whose digest is what `tree` gives (dig empty), so the cache equals the spec there too.
- Cache: `Trie = empty | leaf (rest : List Bool) (k,v) | branch d l r | clash (List (K x V))`; `Inv n t` (lengths,
  d = dig(branch (digest l) (digest r)), branch holds >=2 entries, keys nodup); `toEntries`; theorems
  digest_eq (Inv -> digest t = tree n (toEntries t)), insert_inv, insert_perm (toEntries (insert t e) ~ upsertKey ..),
  build (bulk, one hash per branch+leaf: same recursion as `tree`) = spec. Insert cost = the leaf's depth (~log2 n),
  not 256. RootCache = {trie, inv}; RootsExact becomes a Prop (`toEntries ~ canon es`): no runtime `entries` list (D4).
- Openings: `Trie.open k` -> AuthTrie.Opening (siblings top-down, terminal); prove completeness (honest opening verifies)
  -- the cv-task gap AuthTrie names. ReceiptContinuity.opens: AuthTrie.verify; "exactly 256 siblings" -> "<= 256".
  NativeHostCodec world_opening restated over AuthTrie. Rust receipt_continuity.rs: check the bound/JSON shape.
- Old: Scheme.root stays for the OTHER trees (Selvage/PlanBinding/AuthMapCellRoot use it); WorldRoot's uncompressed
  world-root path (deployed Scheme as world root, sparse eval, WorldRootCache.Tree, Good, deployedEmpties) DELETED.
- Breaks: the deployed root VALUE (every receipt worldRoot, checkpoint root) -> re-genesis; StoreEpoch moves via the
  checkpoint/world-root codec tag in PersistedCodecTags; old Stores refuse by epoch.

### (3) the session's tree is the only one
Read NativeHostSession/NativeHostLight/Host/Main session paths: openHead for a session request must reuse the session's
Opening (cache) and never rebuild. (Design after (2) lands; PERF-FIX-4 already removed confirm cold opens.)

### (1) persist the node table -- PAUSE-LIST QUESTION for ROOT before landing
Today openSealed RECOMPUTES the root from the body and refuses `rootMismatch` unconditionally; downstream the cache
carries a proof (Inv) that its digests are the hashes of its children. Zero-hash open = trusting MAC'd stored digests:
the unconditional "opened root = worldRoot body" becomes conditional on the MAC (the honest-sealer premise, same class
as the checkpoint STATE's existing trust, DATAMODEL §6 Q1). That is a check moving from recomputed to MAC-trusted =
pause item 2 ("anything that weakens a check"). After (2) the tree term at open is ~(cells branches + cells leaves)
hashes, the same order as the MAC's own body hash and the per-cell rootBytes hashing, so (1) buys <=~1/3 of open
hashing. Will measure after (2) and ask ROOT with numbers. Non-weakening part of (1) that can land regardless: none
found (verifying a stored node = hashing it).
- ROOT ruling: (a) base on main 30a5009a (mirror `next` stale) -> branch store-root = 50137af0 = merge of lane/perf-fix
  5b7cae0d onto 30a5009a (30a5009a is 7dea0626 + pipeline/perf scripts only; disjoint). (b) Checkpoint = ONE change owned
  by TURN-LOG (World: cells map, root-tree node table, spent, height, chain; one MAC, one tag). MY deliverable for (1):
  the node table's named sub-codec + lazy/MAC'd verification + theorems (opened root = fold of entries; tampered table
  refused by name) for TURN-LOG's module to import; I do NOT bump DurableCheckpointCodec's tag. (2) and (3) now, in
  parallel. Send TURN-LOG (via ROOT) the exact field/encoding within the day.
- 13:10 Theory/AuthTrieCache.lean (910 lines, compiles, axioms std): tree_perm; Trie (empty/leaf rest/branch d/clash) +
  Inv + entries; digest_eq; build/build_inv/build_entries; insert/insert_entries (Perm upsert)/insert_inv; lastVal,
  canon, root (last value per KEY), root_congr (order-free, no premise); Cache {trie, inv, paths, nodup} with Holds
  (Prop, no runtime entries list), digest_eq, build_holds, insert_holds, insertAll_holds; Trie.opening, opening_climb,
  opening_leaf, opening_present; Cache.opening_complete (AuthTrie's open cv-task gap: honest opening verifies, under
  PathsInjective). Scratch copy: scratchpad sr/AuthTrieCache.lean; lane copy src/Theory/AuthTrieCache.lean (uncommitted).
- 13:40 COMMIT cda83ad6 (on 50137af0) theory(authtrie): Theory/AuthTrieCache.lean + Theory.lean import. Built
  (`lake build Theory.AuthTrieCache` green), import boundary OK (Batteries import replaced by Mathlib.Data.List.Perm.Basic).
  Pushed mirror lane/store-root AND GitHub lane/store-root (hbox has no GitHub key: relayed from the Mac's
  /Users/ember/workbox/mini-unified-push-20261003 via `git fetch hbox:... ; git push github`).
- NODE-TABLE ENCODING for TURN-LOG (sent to ROOT): pre-order over Trie; per node a tag byte:
  0 empty | 1 leaf: digest(32) ++ ixBytes(32, the key's full 256-bit index, so no ix hash on open) ++ keyBytes k
  (prefix-free) ++ value digest(32) | 2 branch: digest(32) ++ left ++ right | 3 clash: nat count ++ (keyBytes ++ value)*.
  Leaf depth = position in the pre-order; rest bits = ixBytes bits dropped by depth. Decode O(nodes), zero hashes.
  Field name in the World checkpoint: `rootTree : List UInt8` (or the decoded Trie via a StreamCodec `trieStream`).

## CONTINUATION (context ~265K at 13:45: successor starts HERE)
State: lane hbox /tank/dregg-build/claude-lanes/store-root/src, branch store-root = cda83ad6. Build wrapper
`w/lb.sh <name> <targets..>` (nohup, pid file w/<name>.pid, status w/<name>.status, log w/<name>.log; swarm-build +
taskset 0-3 because loadavg ~30). Check a single file: `lake env lean <file>` (PATH=$HOME/.elan/bin:$PATH).
Theory API (Minidregg.Theory.AuthTrie): Trie, Trie.{digest,entries,Inv,build,insert,opening}, root dig bitsOf L es,
root_congr, lastVal(+_append,_snoc), canon, Cache dig bitsOf L {trie,inv,paths,nodup}, Cache.{digest,Holds,build,
build_holds,insert,insert_holds,insertAll,insertAll_holds,opening,opening_complete,PathsInjective}, Holds.congr.
NEXT, in order:
 a. Trie.leaf should CACHE its digest (leaf (d) rest k v, Inv: d = dig (.leaf k v)): otherwise every insert re-hashes
    leaf siblings (doubles per-insert hashes). Small Inv/proof edit in AuthTrieCache.
 b. Kernel/WorldRoot.lean: add worldNodeBytes (tagged injective: 0 | 1::keyBytes++digest | 2::l++r), worldDig =
    cSHAKE "DREGG.WORLD-ROOT/v2"; worldDig_collision (Collision -> cSHAKE collision, like deployedIx_collision);
    deployedIx_length; `deployedRoot es := AuthTrie.root worldDig deployedIx 256 es`. Rewrite the generic world
    section (rootOf/entries/lookup_entries/eq_of_lookups/RootBinding/rootOf_binds/rootOf_eq_exhibits_collision/
    resume_sound_rootOf + toy poles) over (dig, ix, L) with key-lastVal reads (lookup_entries needs NO IndexInjective
    now); needs a new theorem tree_inj (WF both, equal tree -> kv-perm or Collision) -> root_inj (lastVal equal or
    Collision). Delete deployed Scheme world-root use, deployedTable, old deployedRoot_eq, entryRoot_deployed,
    sparse world path if unused (Assurance uses its own sparseRoot - check).
 c. Kernel/WorldRootCache.lean: replace uncompressed Tree/Good/insertWrite with `abbrev DeployedCache :=
    AuthTrie.Cache worldDig deployedIx 256`; deployedOf = Cache.build; deployedWrite = Cache.insert.
 d. Compiler/DurableReceiverCore.lean (STATE-AT's file; tell ROOT): RootCache := DeployedCache; RootsExact cache es :=
    cache.Holds es (Prop); delete injective flag, injectiveCheck, fresh, writeAllFresh?, KeysInjective path, every
    `if injective then cache.root else deployedRoot entries` fallback (Core:1038,:1350; DurableServed:791,:1031);
    RootsExact.advance = insertAll + Holds.congr via lastVal_append; RootCache.root_eq via Cache.digest_eq.
    Ask ROOT whether to move RootCache out of DurableReceiverCore into WorldRootCache (ownership).
 e. ReceiptContinuity.opens: AuthTrie.verify worldDig deployedIx root .system (some leaf) opening (siblings <= 256);
    ReceiptContinuityIO: siblings/terminal from Cache.opening (JSON: terminal now needed for absence; for the system
    slot it is always leaf .system); Rust native/resource-client/src/receipt_continuity.rs sibling bound (<=256, variable).
 f. NativeHostCodec.cell_opens restated via Cache.opening_complete on Cache.build.
 g. Bump the world-root/receipt codec tag in Compiler/PersistedCodecTags.lean (NOT DurableCheckpointCodec's: TURN-LOG
    owns that) -> StoreEpoch moves; re-genesis. Then umbrella build (Host.Main), candidate (perf-fix/p4/cand.sh recipe),
    rows journey/call/send/objectrecord/growth, workload N=32 M=32 K=16 + kn2-store-bench CREATES=1 128/256/1024.
 h. (3) session-held tree; (1) node-table sub-codec for TURN-LOG (encoding above) + PAUSE QUESTION below.
PAUSE QUESTION (pending ROOT): a zero-hash open trusts MAC'd stored branch digests instead of recomputing (today
openSealed recomputes and refuses rootMismatch unconditionally; Inv on the cache would become an honest-sealer premise).
- 11:55 STORE-ROOT-2 start. (a) COMMIT 043f2e39 leaves carry digest (mkLeaf, expand reuses). pushed mirror+GitHub. check script w/chk.sh <file>.
- STORE-ROOT-2 working set (uncommitted on hbox lane tree, local copies in my scratchpad sr2/ + sr2/f/): AuthTrieCache +lastVal_isSome/
  cons/map, lookup_canon, wf_canon, root_lastVal_eq (binding: equal roots -> equal lastVals or Collision), paths_nodup,
  opening_terminal, opening_length. WorldRoot REWRITTEN over AuthTrie (Scheme/sparse/slotsOf/entryRoot DELETED; worldDig =
  cSHAKE WORLD-ROOT/v2 over nodeBytes 0|1 key++digest|2 l++r, emptyDigest constant; deployedRoot = AuthTrie.root worldDig
  deployedIx 256; deployedRoot_binds premise-free up to cSHAKE collision; RootBinding carrier = per-key honest-opening reads;
  toy poles at constant hash). WorldRootCache REWRITTEN: RootCache := AuthTrie.Cache worldDig deployedIx 256, RootsExact = Holds
  (Prop), advance = insertAll, opening_complete. DurableReceiverCore: RootCache/RootsExact/injectiveCheck/writeAllFresh?/fallbacks
  DELETED (moved to WorldRootCache per ROOT ruling 2); Sigma -> PSigma (×'). DurableServed: both fallbacks gone. ReceiptContinuity
  opens = AuthTrie.verify (terminal leaf .system), opens_sound restated (or cSHAKE collision); ReceiptContinuityIO
  cachedSiblings -> systemSiblings (+ systemSiblings_open completeness). NativeHostCodec cell_opens restated via
  Cache.opening_complete. Rust: receipt_continuity.rs already bounds siblings <= 256 and calls the Lean verifier: no change;
  hiding.rs is the per-CELL store root (STORE.ROOT/v2), untouched by the world root: no change needed.
  Umbrella build running: hbox w/umb.{pid,status,log} (pid 3321052).
- STEP g plan: rename PersistedCodecTags.world_root_v1 -> world_root_v2 "DREGG.WORLD-ROOT/v2" and make
  WorldRoot.worldCustomization READ that tag (no parallel literal); schema-refs digest moves -> StoreEpoch moves -> old Stores refuse
  naming schema-refs. Then objective gate: scripts/check-objective-proofs.sh proofs --draft 50137af0..HEAD, review, --pin (as 5b7cae0d).
- 14:xx umbrella (b..f) GREEN except Compiler.PersistedCodecTagCensus (registry still had world_root_v1: exactly step g). Step g
  applied (world_root_v2 registered; WorldRoot.worldCustomization READS it). Rebuild w/umb2 (via with-lean-slot, per ROOT).
- BEFORE bench (kn2-store-bench at 5b7cae0d built in store-root/before/src from a copy of perf-fix's .lake; w/bench-before;
  CREATES=1, perf --no-scale, taskset 8-11), instr:u core / open / light open / grown:
  128: 52.09 G, open 289 ms, light 271, grown 1462 ms | 256: 103.54 G, 679, 533, 2481 | 1024: 428.85 G, 2608, 2193, 14219 |
  4096: 2147.13 G, 13898, 9152, 265262 ms.  Files hbox store-root/w/bench-before-<n>.{out,csv}.
- ROOT ruling FINAL: NO persisted root node table (open recomputes; a stored copy does no work). Step (1) DROPPED. Remaining: wire-in + ConsentAnchor + tag, Rust bound, session-held cache (3), completeness, measurements.
- COMMITS b..g: 86fabb9e dbe6940e 248ef538 3b6ea9ce 6e12f8ca fffb817f (umbrella green at fffb817f incl census, ConsentAnchor,
  kn2-store-bench). Pushed mirror + GitHub lane/store-root = fffb817f. Reported to ROOT.
- AFTER bench (w/bench-after = lane .lake kn2-store-bench at fffb817f): 128: 10.86 G, open 33 ms, light 15, grown 547 |
  256: 22.05 G, 74, 32, 1388 | 1024: 101.23 G, 359, 168, 6574 | 4096 running.
- Candidate: w/cand.sh cand-1 (pid w/cand-1.pid, status w/cand-cand-1.status) -> store-root/cand-1. Before candidate =
  perf-fix/cand-M (tree = 5b7cae0d). NEXT: workload same-pass (cand-M then cand-1, N=32 M=32 K=16), rows journey/call/send/
  objectrecord/growth via perf-fix/run-rows.sh, objective-proofs ratchet (check-objective-proofs.sh proofs --draft cda83ad6..HEAD).
- STEP (3) READ: sessions already keep the trie across requests (NativeHostSession.refresh -> extendFrom -> Loaded.replay/extend
  advance; Light.refresh -> Opening.extend passes opening.roots). Remaining full evaluations: pastWitness / Served.ofStateAt (past
  states, STATE-AT's), Main bench lines. No code change for (3).
- AFTER 4096: 666.98 G (before 2147.13), open 2961 ms (13898), light 852 (9152), grown 69003 ms (265262). cand-1 waiting on lean slot.
- WORKLOAD same pass (cand-M=5b7cae0d tree -> cand-1=fffb817f; N=32 M=32 K=16, perf --no-scale, under load; both rc=1 ONLY
  for the 180 s wall bound, phases failed: none), instructions:u: genesis 17.75->10.50 G, setup 97.00->74.46, births
  1393.92->940.40, updates 1207.29->395.26, reads 694.55->180.60, checkpoint 21.77->7.88, judgment 114.14->44.66, reopen
  23.89->6.52. Total wall 600.4->318.9 s. Files hbox store-root/w/wl-{before,after}.out, /tmp/srw-{before,after}.
- RATCHET: proofs --draft 50137af0..HEAD: 5184 changes (128 removed, 39 restated, 5017 redefined / 23 roots), 0 unattributed;
  reasons by w/ledger.py (removed -> named successor or obsolete), appended to scripts/gates/objective-contract-changes.txt;
  --pin running (w/pin.{pid,log,status}). Rows on cand-1 running (w/rows-1).
- COMMIT h 81269fd3 ratchet pin (40751 rows). Pushed mirror+GitHub (GitHub warns objective-contract-changes.txt is 60.43 MB > 50 MB). Rows journey/call/send/objectrecord PASS on cand-1; growth running.
- ROWS cand-1: journey PASS, call PASS, send PASS, objectrecord PASS; growth FAIL (load 23-40): at 1000 write p50 3.141 s
  p99 10.271 s max 31.618 s, reopen 7.633 s, certify p50 1.02 s. Prior lanes' growth also FAILS under load (PERF-FIX-3:
  control a16e2f1b max 11.74 p99 8.01 p50 2.78). The max 31.6 s is NOT SETTLED: same-pass control running
  (w/growth2.sh: cand-M then cand-1, w/growth2.{pid,status}, w/rows-g{M,1}).
- REBASE onto next 0125b224: worktree store-root/rb (branch store-root-rb); code commits a..g applied clean
  (8417f7ea..30a080a6; theory 5417cfb7); gates commit SKIPPED (manifests regenerate on the rebased tree). .lake = cp -a build +
  cp -al packages from src. Build w/rb.{pid,log,status} via lean slot. NEXT on rb: ratchet --draft 0125b224..HEAD + pin; then
  fold openSealedRooted when next v2 (state-at) lands.

## CONTINUATION (STORE-ROOT-2, end of session ~17:30)
lane/store-root (mirror + GitHub) = 81269fd3 (on 50137af0): a 043f2e39, b 86fabb9e, c dbe6940e, d 248ef538, e 3b6ea9ce,
f 6e12f8ca, g fffb817f, h 81269fd3 (ratchet pin). Step (1) DROPPED (ROOT). Step (3) needs no code (sessions carry the trie).
IN FLIGHT (PID files in hbox store-root/w): rb.pid = rebased umbrella in worktree store-root/rb (branch store-root-rb on next
0125b224, waiting for a lean slot); growth2.pid = growth control (cand-M then cand-1).
NEXT: (1) rb green -> in rb: check-objective-proofs.sh proofs --draft 0125b224..HEAD, ledger reasons via w/ledger.py
(same mapping), append, --pin, commit; push rb HEAD as lane/store-root (force: it is a rebase; tell ROOT). (2) read
w/growth2.status + rows-g{M,1}/results.tsv: same-pass growth verdict. (3) when next v2 (state-at d951d57a) lands: rebase again,
delete DurableCheckpointCodec.openSealedRooted (+_eq/_ok); STATE-AT's keptAt calls openSealedWith with RootCache.build and
reads built.1.root (one open). (4) GitHub warns objective-contract-changes.txt is 60 MB.
