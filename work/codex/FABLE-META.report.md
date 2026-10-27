# FABLE-META — generators as nano objects (axis 1, METAPROGRAMMING): report and continuation

Worker: FABLE-META (Claude Fable 5.1). Repo: `~/dev/nanodregg` (mirror). hbox worktree:
`/tank/dregg-build/nanodregg/wt/fable-meta` (branch fable-meta from ad90a47; warm .lake copied from wt/fable-ctx by cp -a, no shared inodes).
Local editing worktree: this session's scratchpad `wt-meta`. Design: `redregg/work/promo/DESIGN-META.md`.

## Dated lines

- 2026-10-26 READ: FRONTIER-AXES, VERDICT-20261024, TOPLEVEL-SPEC whole, HOLISTIC-LANG whole, DESIGN-CTX §0-1, DESIGN-TRUST §0,
  Lang/{Term,Ty,Eval,Package,Program,Call,Std,StdHead,StdActivity,HoleSyntax,Bell,Surface(parts),Wire(parts)}.lean, Codec/Tree.lean,
  Kernel/Receive/{Call,Derive}.lean, Kernel/Proofs/{Tree,Ledger(parts),InvokeTree(parts)}.lean, Lang/Proofs/{Call,CallLive,CallTeeth,
  MethodRun,StdOffer(take_run_sound),StdHead(head)}.lean, Lang/Journey/{Head,Main}.lean, decisions/lang.md titles + LANG-80..82.
- MEASURED: `Body.callable` excludes install; `install` receiver takes no authority (Derive.lean:107-111); the package wire is
  concatenative (Codec/Tree.lean); `grep -rho "(calls [^)]*)" world/` names only transfer; no Rust prim table (`grep lenLe client/` empty).
- DESIGN written: DESIGN-META.md (a generator = a package whose method returns `install BYTES`; the receipt is the Turn; hygiene =
  closed de Bruijn; rung 0 tonight (constant generator, Std.headGenerator, cell-id equality with headPackageId), rung 1 = three codec
  primitives + one package-wire flag day, rung 2 = lists; the one wrongness: bytes are not a type of code).
- FILES I TOUCH (landing 1): Kernel/Receive/Call.lean (Body.callable), Kernel/Proofs/Ledger.lean (tree_zeroBorn case),
  Kernel/Proofs/Generated.lean (new), Lang/Package.lean (callArms), Lang/Call.lean, Lang/Proofs/{Call,CallLive,CallTeeth}.lean,
  Lang/StdGen.lean (new), Lang/Proofs/StdGen.lean (new), Lang/Journey/Gen.lean (new), Lang/Journey/Main.lean, decisions/{lang,kernel}.md.
  FABLE-CTX: I do not touch Lang/StdHole.lean, LiveHoles, the fuse. FABLE-TRUST: I do not touch Std.head's LAW or Protocol.
ROOT (real 10-26 05:10Z): /Users/ember/dev/redregg/work/codex/FRONTIER-BOARD.md collects every axis's verdict, landed hash and shared need in one page; read it before a decision that touches another axis; ROOT keeps it current.
- BUILT (hbox wt/fable-meta at ad90a47, warm .lake): whole tree GREEN (764 jobs); `lake exe lang-journey` GREEN with GN0–GN5:
  GN1 the generate Turn bears ONE cell whose id == Protocol.Foreign.headPackageId (Std.head as an installed object, byte for byte, as one
  digest); GN3 a second generation `rejected idTaken`; GN4 one-byte generator refused `program decode lang/package-version/5` at the
  nested install, nothing born, World unchanged; GN5 `noMethod nope`. Theorems: Kernel `tree_package_checked` (new module
  Kernel/Proofs/Generated.lean), Lang `generate_run_sound` (Lang/Proofs/StdGen.lean), `install_reads` tooth.
- PLANT (restored, cmp-verified): install receiver without checkInstall → Lean RED first at Kernel.Proofs.Rooted:384; journey RED on every
  install-check row (L6, LV1, LV2, LI2, LD1, LD2, LC6, LC7, …).
- OWNERSHIP: touched TRUST's column (Kernel/Receive/Call.lean: `Body.callable` + the notCallable docstring only) and TYPES's
  (Lang/Package.lean: `installArm` + one word in `callArms`'s doc + the arm in `callArms`); claimed KERNEL-75 in FABLE-OWNERSHIP.md.
  Decision entries: LANG-86, KERNEL-75 (appended; LANG-83 from CTX landed meanwhile and sits before mine after the 3-way merge).
- LANDING L1: main moved ad90a47 → 5fa281d (TRUST's PROTOCOL-74) while I built; carried the edits by `git apply -3` (conflicts: Journey/Main.lean
  session list and decisions/lang.md, both kept-both); `scripts/commit -F logs/fable-meta-L1.msg --cross-layer … <14 paths>` launched
  detached (PID file `wt/fable-meta/logs/fable-meta-land.pid`, log `logs/fable-meta-land.log`), fast judge (`lang:`).

## Continuation (rung 1 of DESIGN-META §3: parameters; a `lang!` package-wire flag day) — for the successor

Read DESIGN-META.md §3 and §6 first; then `Lang/Term.lean` (Prim), `Lang/Eval.lean` (primEval, primBytes,
primTicks), `Lang/Wire.lean` (primCode, packageVersion, `lang/package/5`), `Lang/Bounds.lean`
(packageWireVersion), `Lang/Proofs/{Sound,Cost,Wire,WireTeeth}.lean` (the per-primitive cases),
`gates/codec-vectors.tsv` (the refused-boundary rows that must flip), `Lang/Journey.lean` row LV.
1. Primitives (each a new `Prim` constructor, O(1) work, charged like its cousin): `len : bytes → nat`;
   `varint : nat → bytes → bytes` (= `Stream.putVarint n ++ b`; walks |b|, charged as `cat`); `be : nat → nat → bytes`
   (`w ∈ {4, 8}`, big-endian; any other width is a named fault `badWidth`, not `stuck`); `idBytes : digest → bytes`
   (the reverse of LANG-38's forbidden direction; sound: every digest in a run came from the World). `Prim.left/right/result`
   give the checker their types for free.
2. The flag day: `Bounds.packageWireVersion` 5 → 6; `lang/package/5` → `lang/package/6` (`packageCodec_label` fails the
   build otherwise); codec-vectors rows; every `.ob` fixture's bytes move by the version byte (same content), so
   `Protocol.Foreign.headPackageId` moves, the Bell's shipped core (`world/resident/Bell.core`? read LB0/LBw) re-emits,
   the devnet re-genesises; row LV keeps refusing version 5 by name. Say all of it in the commit (full judge).
3. `Lang/Quote.lean` (NEW): `packageTerm : Package → Term`, a nano term computing `encodePackage p` by `cat`/`varint`/
   `be` over literal fragments (the tree codec is concatenative: `tag ‖ varint |p| ‖ p ‖ varint n ‖ kids`, Codec/Tree.lean);
   theorem `eval_packageTerm : BigStep lib env (packageTerm p) (.ok (.bytes (encodePackage p)))` for `p` within bounds.
4. The first template generator: `Std.boundedGenerator S f` whose `generate (max : nat)` emits `bounded S f max`'s package
   bytes with `be 8 max` spliced at the literal; `generate_bounded_sound : run = [install (encodePackage (pkgOf … (bounded S f max)))]`.
   GN6–GN8 rows: generate at 100, create an object of the bore id, a write of 101 refused "f over 100".
5. Then structural generators wait for a bounded sequence type (axis 7, TYPES's column): coordinate before touching Ty.
Box safety: swarm-build always; never kill by pattern; a PID file or nothing; never git stash; never delete outside wt/fable-meta.
- LANDING attempts 1–4 REFUSED by the source gates, each fixed forward: (1) SIZE lines + a CROSS-LAYER naming LEDGER (`ROOT for LEDGER`, Kernel/Proofs/Ledger.lean);
  (2)(3) main moved under me twice (5fa281d TRUST, 1e8a2a0 PCC: both touched Lang/Journey/Main.lean's session line and appended decisions): a 3-way
  conflict on the same line is a conflict however I merge, so each relaunch re-detached wt/fable-meta at the new origin/main and re-applied my
  two hunks on main's copies; the decision entries now sit MID-FILE (LANG-86 before LANG-83, KERNEL-75 before the last KERNEL entry) so a
  concurrent append at the end no longer conflicts; (4) seven SIZE metrics rose (modules, proof-modules, lines per layer, max dependents): one
  `SIZE: <metric>: <why>` line each; (5) AXIOM-CENSUS red: `headGenerator_wire` by `native_decide` (nano's census admits no native_decide): deleted;
  the fact is GN0's row.
- **LANDED c82f171** (fast judge GREEN: decls ok with the 5 RESTATES-MEANING lines, census ok, 355 modules in the reach; pushed to origin).
  main was fab2875 (OBS) under it. hbox wt/fable-meta is detached at c82f171, clean; its `.lake` is warm at that tip (a successor can `cp -a` it).

## Closing state (2026-10-26)

- Landed: c82f171 = LANG-86 + KERNEL-75: `install` callable from an object; `Std.generatorOf` / `Std.headGenerator` (Std.head as an installed
  object, byte for byte: GN1's cell id == headPackageId); `tree_package_checked` (Kernel/Proofs/Generated.lean); `generate_run_sound`
  (Lang/Proofs/StdGen.lean); GN0–GN5 in lang-journey. Design: DESIGN-META.md (rung 0 built; rung 1 = three codec primitives + one
  package-wire flag day, priced in §3.3; rung 2 waits for lists; the one wrongness: bytes are not a type of code, §6).
- Not done: rung 1 (the continuation above). Open and named, not cards: `createOf` (generate-and-instantiate in one Turn, DESIGN-META §6.3);
  a quorum-gated generator (laws on a generator object); the signed-call composition of `tree_package_checked` over `derive` (13 cases).
- Local: this session's scratchpad `wt-meta` (a worktree of the mirror on branch `fable-meta`, stale edits; removable) and `fable-meta-L1.msg`.

# FABLE-META-2 (successor; rung 1) — dated lines

- 2026-10-26 ~06:00Z READ: this report whole, DESIGN-META whole, FRONTIER-BOARD (the wire ruling: version by LANDING ORDER), FABLE-OWNERSHIP;
  Lang/{Term,Eval,Wire,Bounds,Package(wire),Std(bounded,lawOf,At),StdGen,Quote?}.lean, Lang/Proofs/{Sound(primEval_sound),Cost,Wire(version),
  WireTeeth,LawMeaning,BigStep,StdGen,MethodRun,Extract(Means),Load(runSetup_spec),StdRun(sel_toVal),Receiver(NoRef)}.lean, Codec/{Tree,Varint,
  Stream}.lean + Codec/Proofs/{Tree,Varint,Stream}.lean (putD_node/kidsBytes/putVarint_eq/Lawful.put_eq), Emit/Vectors.lean (package site),
  Lang/Journey.lean (LV rows), Lang/Journey/Gen.lean, gates/decls.py header, gates/OWNERS, scripts/commit header.
- MEASURED: origin/main = c82f171 at start (my predecessor's landing is the tip; no wire bump landed yet, so I take 6 by the ruling, and
  re-number on rebase if CTX/TYPES/PCC land first). The mirror's checkout is stale at ad90a47; I work in a detached scratch worktree
  (`scratchpad/wt-meta2`) and ship patches to hbox wt/fable-meta by `git apply` (never rsync into the build tree).
- DESIGN CORRECTIONS (read off the code, before writing): (a) `Term.prim` is BINARY everywhere, so `len`/`idBytes` (unary) are shaped as
  buffer-first APPENDS equal to the codec's own `put`s: `u64be`, `sized`, `dsized` (one writer per scalar literal kind; bool by `ite`);
  `len`/`varint` dropped as unneeded by any template; raw `idBytes` refused (an id's bytes enter a byte string only as a codec payload).
  (b) The quoter is over OPEN terms: a free `var i` is a stage-1 parameter (cross-stage persistence); spec `Term.fill`. (c) `Std.bounded`'s
  refusal loses its decimal (`"{f} over the bound"`) — a nano generator cannot render a number and a differing law text would be a twin;
  `bounded S f max := boundedWith S f (natT max)`.
- BUILT (hbox wt/fable-meta, patch of origin/main c82f171, swarm-build 6–8G/2 threads, module by module): Lang.Proofs.Quote GREEN
  (`quotePackage_sound`: the quoted term appends exactly `encodePackage (fillPackage vals p)`; `noRef_quotePackage`); Lang.Proofs.StdGen
  GREEN (`generate_bounded_sound`: every admitted run of `boundedGenerator r f`'s `generate {max = m}` returns `[install B]` with
  `encodePackage (boundedPackage r f m) = some B`); Lang.Journey.Gen compiles (GN6–GN8 written). Whole tree + lang-journey + codec-vectors
  running (`logs/meta2-full.log`, PID file `logs/meta2-full.pid`).
- OWNERSHIP: TYPES's column touched (Lang/Term.lean: three `Prim` constructors + their types; Lang/Eval.lean: `appended`, the arms);
  CODEC's (Emit/Vectors.lean: primRows + boundary + labels); claimed LANG-87 in FABLE-OWNERSHIP.md. Decision entry LANG-87 placed MID-FILE
  (after LANG-86, before LANG-83). Lang/Journey/Main.lean UNTOUCHED (GN6–GN8 live in genRows).
- BUILT (hbox wt/fable-meta, whole tree GREEN at the second full build; `lake exe lang-journey` GREEN after `--write world/doc` re-emitted
  `world/doc/Section` — its text names package ids, which moved with the version byte; GN6: generate at 100 bears exactly the cell of
  `encodePackage (boundedPackage {n : nat} n 100)` (1442 bytes; the generator 2489 bytes); GN7 set 50 admitted; GN8 set 101 refused
  `lawDenied bounded: n over the bound`; LV1–LV3 refuse `lang/package-version/6`); `codec-vectors --write` then `--check` ok (291 vectors of
  59 sites: the package site +3 writer rows, boundary 12 → 15, every other package row's first byte 05 → 06, version site 06/05).
- LANDING L2 launched ~07:20Z: `scripts/commit -F logs/fable-meta-L2.msg <29 paths>` detached (PID file `wt/fable-meta/logs/fable-meta-L2-land.pid`,
  log `logs/fable-meta-L2-land.log`), FULL judge (`lang!:`), wire version 6 (origin/main still c82f171 at launch: no other bump landed; I
  re-number on rebase if one does). Message: 7 SIZE lines, 14 RESTATES-MEANING lines, 4 CROSS-LAYER lines (CODEC, GATES, ROOT for HOSTING,
  TYPES's column by the table).
- LANDING L2 attempt 1 REFUSED by the full judge (~08:35Z; log `logs/fable-meta-L2-land.attempt1.log`; gate log
  `main/.git/nanodregg-gate-2/23dc68860809.log`): build ok, census ok, vectors generated ok, cargo rows ok (the keybroker/hosted-uid
  failures are KNOWN-RED controls on main, not mine). Two reds, both fixed forward: (1) decls: nine undeclared restatements — five
  Lang.Proofs.Wire theorems whose STATEMENTS carry the label string (`lang/package-version/5` → 6), three StdTeeth teeth carrying the
  refusal text, and `Lang.Need.forgeStep` (a plant whose `match` over `Prim` gained arms: the body digest moves whenever Prim grows): nine
  RESTATES-MEANING lines; (2) waste: `worstcut-rows {reopen,audit}-trie-hashes-per-step` 20.184 → 20.187 (332038 vs 331983 hashes over
  16448 steps, +55): the version byte moved the installed Bell's package id, so the bench's base-World trie keys differ; raised with a
  `WASTE: worstcut-rows:` line and the rows' source notes (gates/waste.tsv, named in the GATES CROSS-LAYER line). LESSON for the next
  flag day: a wire bump's RESTATES list is the label string's every THEOREM, the version's every bench ceiling, and every `match` over
  the grown inductive — grep `lang/package-version/N` in Lang/Proofs and `.primR\|match .* Prim` in Lang/Sim before the first launch.
- Main moved under attempt 1: c4800fb (AGENT HOSTING, `hosting!`, wire still 5). Attempt 2 launched ~08:45Z (PID file
  `logs/fable-meta-L2-land.pid`, log `logs/fable-meta-L2-land.log`), 30 paths (+ gates/waste.tsv), still version 6; TYPES/PCC/TRUST
  full judges ahead in the slots.
- **LANDED 1bdd5ba0** (LANG-87, `lang!`, package wire 5 → 6; full judge GREEN: decls ok with 23 RESTATES-MEANING lines, census ok, runs ok
  (87 runs of 60 exes), generated files ok; "queue: head (displaced 1 times); landed by compare-and-swap"; pushed to origin). Rung 1 of
  DESIGN-META is built: three payload writers (`u64be`, `sized`, `dsized`), `Lang.Quote` + `quotePackage_sound`, `Std.boundedGenerator` +
  `generate_bounded_sound`, GN6–GN8. hbox wt/fable-meta is detached at 1bdd5ba0, clean, `.lake` warm there.
- L3 (LANG-88, `lang:` fast): `Std.ownerGenerator` — no argument; the output names the INVOKER (`agentParam = ⟨digest, get req "agent"⟩`,
  the `dsized` writer's deployed use); `Std.allowlistWith` (+ `allowlistLaw_one` rfl); `generate_owner_sound`; GN9–GN11 GREEN on hbox
  (B generates → the cell of `ownedPackage {n : nat} B`, 1613 bytes; A through a grant refused `owner: not on the allowlist`). Built
  green first try; journey exit 0. Launched ~09:40Z (PID file `logs/fable-meta-L3-land.pid`, log `logs/fable-meta-L3-land.log`).
- **LANDED c327ba13** (LANG-88, `lang:`, fast judge GREEN first attempt: decls ok with 0 map lines, census ok; "queue: fast; landed by
  compare-and-swap"). Two generators landed tonight: `Std.boundedGenerator` (an argument) and `Std.ownerGenerator` (the request).
- L4 (next, `lang:`): the owed refactor — `Std.templateGenerator A ps p` + ONE theorem `generate_template_sound` (any template generator's
  admitted run installs `encodePackage (fillPackage vals p)` under `Params`); `generate_bounded_sound` / `generate_owner_sound` become
  corollaries; the two 60-line copies go.
- L4 (LANG-88.1, `lang:` fast): `Std.templateMethod`/`templateGenerator A ps p doc` + `generate_template_sound` (the one theorem; its
  `hres` hypothesis — "generate resolves to its declared signature" — is `rfl` at any concrete argument type: `methodSig` decides
  `A.isData`/`pairNamed` by computation, which a variable `A` cannot); `generate_bounded_sound`/`generate_owner_sound` keep their
  statements as ten-line instances; two method defs + six per-generator lemmas deleted (DELETES lines), `boundedGenerator`/`ownerGenerator`
  RESTATES-MEANING (bodies now `templateGenerator …`, byte-identical packages: GN6–GN11 GREEN, lang-journey exit 0). Built green on hbox.
- **LANDED 74d42e77** (LANG-88.1, fast judge GREEN first attempt: decls ok with 10 map lines (8 DELETES, 2 RESTATES-MEANING)).

## Closing state (FABLE-META-2, 2026-10-26 ~10:30Z) — parked near the brief's threshold

- Landed tonight, in order: **1bdd5ba0** (LANG-87, `lang!`: package wire 5 → 6; `u64be`/`sized`/`dsized`; `Lang.Quote` +
  `quotePackage_sound`; `Std.boundedGenerator` + `generate_bounded_sound`; GN6–GN8; `Std.bounded`'s refusal is now `"{f} over the
  bound"`), **c327ba13** (LANG-88: `Std.ownerGenerator`, `generate_owner_sound`, GN9–GN11), **74d42e77** (LANG-88.1:
  `Std.templateGenerator`, `generate_template_sound`, the two theorems as instances). DESIGN-META §8 records all three.
- Other lanes landed under me (all re-based automatically): c4800fb AGENT `hosting!`, 9ccb6b6 + f70a5f9 TRUST. TYPES's LANG-89 and
  PCC's L2 (both wire bumps) were still in the judge slots when I parked: the next wire version is 7 (mine took 6).
- hbox `wt/fable-meta`: detached at 74d42e77, clean, `.lake` warm (a successor can `cp -a` it or build in it). Local scratch
  worktree removed. Logs of every attempt under `wt/fable-meta/logs/` (`fable-meta-L2-land.attempt1.log`, `-L2-land.log`,
  `-L3-land.log`, `-L4-land.log`, the journey logs `meta2-journey2.log`, `meta3-journey.log`, `meta4-journey.log`).
- Not done, named (not cards; the successor's choice by DESIGN-META §8's order): `createOf` (KERNEL arm; coordinate with TRUST-2 by
  report line before touching Kernel/Receive), a quorum-gated generator (a generator WITH state and laws), rung 2 over TYPES's
  `Ty.seq`; a `bytes`/`bool`-parameter template (a doc-parametrised generator) is the cheapest next instance of
  `generate_template_sound`.

## Continuation — for FABLE-META-3

Read first: DESIGN-META §8 (what rung 1 is and is not), this report's L2–L4 lines, then the code at nano `74d42e77`: `Lang/Quote.lean`
(the quoter; `Param`, `param`, `quoteTerm`, `quotePackage`), `Lang/Proofs/Quote.lean` (`Appends`, `quotePackage_sound`,
`noRef_quotePackage`), `Lang/StdGen.lean` (`templateMethod`, `templateGenerator`, `boundedPackageWith`, `ownedPackageWith`,
`maxParam`, `agentParam`), `Lang/Proofs/StdGen.lean` (`generate_template_sound` and its two instances: the shape every new generator
follows), `Lang/Journey/Gen.lean` (GN0–GN11; two founders B and A), `decisions/lang.md` LANG-87/88/88.1 (mid-file, after LANG-86).
Facts a successor must not relearn:
1. A new `Prim` is a package-wire flag day (a primitive code under term tag 7 turns a refused vectors row into a read one); the
   full judge wants, beyond SIZE lines: RESTATES-MEANING for every THEOREM whose statement carries the label string
   (`grep lang/package-version/N Lang/Proofs`), every `match` over `Prim` (`Lang/Sim/Need.lean forgeStep`), every tooth naming a
   changed refusal text; a `WASTE: worstcut-rows:` line (the installed Bell's id moves, +~55 trie hashes); `world/doc/Section`
   re-emitted by `lang-journey --write world/doc` (its text names package ids); `codec-vectors --write` then `--check`; CROSS-LAYER
   lines naming CODEC (Emit/), GATES (gates/*.tsv), ROOT for HOSTING (world/). The version is by landing order: take main's + 1 when
   the judge starts, re-number on rebase (`scratchpad/renumber.py` did it in one call; recreate: Bounds, Package, Proofs/Wire,
   Journey, Vectors labels, the decision text; re-draw the tsv).
2. `apply4_method`'s binder types must be passed explicitly (`(R := .record []) (S := genStateTy) (A := A) (Q := reqTy)`) when the
   argument type is a variable; `resolveMethod` is `rfl` only at a concrete argument type (`methodSig` decides `A.isData`), hence
   `generate_template_sound`'s `hres` hypothesis.
3. `putVarint` is well-founded recursion: a tooth over `sized`/`dsized` needs `decide +kernel`; `u64be` decides plainly.
4. `git checkout -- .` on the hbox worktree reverts regenerated files (the vectors table, `world/doc/Section`): keep them in the
   patch, or regenerate after every re-apply. Never rsync into the build tree; ship patches with `git apply`.
5. The landing queue: five full landers share four judge slots; a lander waits "in place" (an empty log for up to 4 h is normal:
   `fuser <common>/nanodregg-gate-K.flock` names the holders); a displaced lander re-bases and retries by itself.
The next card by the design: a quorum-gated generator (DESIGN-META §8 (b)) — a generator package with state
`{approvals, proposal, generated}` and the law `Std.quorum` over `generated`, whose `generate` method installs the quoted template
AND commits the proposal (`generated := v`, approvals reset): read `Std.quorumLaw`'s commit arm (Lang/Std.lean, the quorum section)
and Journey's LQ rows (the shared setting's propose/approve methods) first; the theorem is `generate_template_sound`'s shape with a
state-writing method (write a `templateMethodWith (newState : Term)` rather than a copy). Or `createOf` (§8 (a)) after a report
line to TRUST-2 naming the Kernel/Receive hunk.
Box safety (verbatim): swarm-build always (`SWARM_MEM_MAX=8G LEAN_NUM_THREADS=2` per module, 24G whole tree); never kill by
pattern — no `pkill -f`, no `pkill -x`, no `killall`, no `kill -u`; a PID file or nothing; never `git stash`; never run an unfiltered
`-p <crate>` test suite; never delete outside wt/fable-meta and this session's scratch.

# FABLE-META-3 (createOf, quorum-gated generator) — dated lines

- 2026-10-27 STATUS: BUILT, not landed. hbox `~/nd-land/meta` (based on origin 80c622a; rebases onto ≥ 6faa984 before landing). `Body.createOf` (KERNEL-76: install-if-absent then create, owned by the SIGNER, object born first; codec tag 13; every kernel tree theorem carries the case) + the typed Lang call arm `createOf {pkg, state : T}` (LANG-96; Call/CallLive/CallTeeth proofs green) + `Std.templateCreator`/`boundedCreator`, `make_template_sound`/`make_bounded_sound` green; GN12–GN17 written; testground `creator` demo + tour step written. `Std.quorumGenerator` + `generate_quorum_sound` + GN18–GN20 written (LANG-97), not yet built. Whole-tree build of the createOf reach running once. NEXT: rebase, journey + codec-vectors re-draw + testground gate, land createOf; then land the quorum generator; then the `code`-type note in DESIGN-META.
- 2026-10-27 **LANDED ee2f790f** (pushed by rule 1 from hbox `~/nd-land/meta`): KERNEL-77 + LANG-96 + LANG-99 in one commit. `Body.createOf` (tag 13; owner = signer; package reused when the signer pins it live, installed otherwise; object born first; `withBorn` view); the typed Lang arm `createOf {pkg, state : T}` with every call round-trip/liveness proof; `Std.templateCreator`/`boundedCreator` + `make_template_sound`/`make_bounded_sound`; `Std.quorumGenerator` + `generate_quorum_sound`; `derivePins` pins a live cell the derived Turn would bear (createOf reuse); GN12–GN20 green (lang-journey 1253 ok); kernel-sim 64 seeds ALL PASS; codec-vectors re-drawn (294). Numbers: KERNEL-76 and LANG-98 were taken by other lanes during the landing; mine are KERNEL-77 and LANG-99. Design: DESIGN-META §9 (built) and §10 (the `code` type note: `Ty.pkg I`, interfaces not terms).
- Landing friction: main moved five times; one scripts/commit run reached its rows and was refused only by `cargo-untraced:launcher:fence` (hosted-uid tests, the known environmental red) and `launcher:resident_bell` timing out at 600 s under load 92; I pushed by hand after rebuilding the merged tree and re-running lang-journey, kernel-sim and codec-vectors. FINDING for ROOT: `d422453` (testground lane) reverted `9f10566` (join consent) and `0cf39ad` (LANG-97 ringer withdraw) on main — a stale-tree revert; the join and LANG-97 later reappear partially (enroll is 5-field again at ee2f790f) — someone should check what of LANG-97 survives.
- Not done / next: the quorum law's own meaning theorem (`quorum_change_sound`, LANG-99's critique) so "installed only with k approvals" is one statement; rung 2 over a sequence type; `Ty.pkg I` per §10.
- Testground: kernel.wasm built from ee2f790f (4.57 MB, emcc 6.0.9); `node axes-run.mjs creator` OK (10 commands: alice's make bears her object + the package, bob's reuses it, alice refused noGrant on bob's object) and `generator` OK.

# FABLE-META-4 (the quorum's meaning, the interface a method produces, the claims demo) — dated lines

- 2026-10-27 **LANDED 655ff42e** (LANG-102): `Std.quorum_commit_attested` (Lang/Proofs/StdQuorum.lean). Along any `Chain (Step lib (quorumLaw …))` from a state with no approvals, over distinct members, a write or invoke that changes the guarded field to `ng` had `set ng` proposed, and at least k distinct members (a sublist of `ms`) each signed an earlier approval step of exactly `set ng`. One invariant, `Attested`, plus `bit_add_pow2` and `setMembers`. The cv card's one-step statement already existed (`quorum_change_needs_k`, general, since LANG-24); proving it again would have been a twin. `Std.quorumGenerator` is now a checked constructor (`Except StdRefusal Package`, refusing as `Std.quorum` does). Before, k = 0 installed with no approval and a repeated member held two bits. `quorumGeneratorOf` is the package. `generate_quorum_sound` also states the run's new state (`runMeasured_inv_slots`). `quorumGenerator_installs_attested` is LANG-99's composition as one theorem. Journey GN21 (`duplicateMember`, `badThreshold`). Whole tree built (849 jobs); lang-journey GREEN. Pushed by hand: the lander's only red was `rows --deployed` (600 s). Main had moved by docs only, plus a restore with no path in common; replayed with `git merge-tree`.
- 2026-10-27 **LANDED c17cf0f0** (LANG-103): the interface a method produces is a GRADE, `Effect.produces I`, not `Ty.pkg I`. The decision is in LANG-103 and DESIGN-META §11: no checkable introduction exists for a typed package value, because the quoter writes a bytes term the checker cannot see into. Install refuses `badProduces`. The run refuses `produces LABEL: lacks M` / `type M` / `extra M`. `runMeasured_produces` is the theorem. Wire: an absent `produces` encodes exactly as before, so no id moves and the version stays 10. A hand-written `Repr Effect` keeps the codec vectors' decoded meanings (295, ok). Restated: `readPackage_closedText` and `readPackage_package` take produced interfaces well-formed (from `checkFields_produces_wf`). `effects_prints` replaces three fixed-shape lemmas. Journey GN22 (admitted), GN23 (`produces generate: lacks reset`, nothing born), GN24 (`badProduces set`). Whole tree built (849 jobs); lang-journey GREEN. Pushed by hand: the lander's reds were `rows --deployed` (600 s), `cargo-untraced:launcher:fence` (hosted-uid, environmental) and `cargo:launcher:resident_bell` (600 s under load). META-3 hit the same three.
- Open from LANG-102/103 critiques: the witnesses are "earlier in the history", not "since the last reset" (the proof gives the stronger form; the statement does not); the produces check is at generation, not at the generator's install (needs rung 2's checker-visible quote); createOf's `T` is still not tied to `I` (iface carries no state type); the surface has no `produces` clause; a run decodes each produced package once more than the kernel does, unmetered.
- 2026-10-27 **LANDED 0f86881d** (testground; cv 01a17afc): the `claims` demo and its tour step (after the creator, before the meter). alice installs a package claiming `keeps le100 bounded` whose `write` arm skips the test: refused at install. `Kept` installs; `set 50` is admitted and `set 101` refused `lawDenied`. The texts are the journey's own, through `tg_text` (`kept`, `keptLeaky`). `Owned` moved to Lang/Journey/Owned.lean and `Kept`/`le100`/`boundedKeeps`/`leaky` to Lang/Journey/Kept.lean (same namespace), so the kernel prints them without linking the journey harness: importing the journey had grown kernel.wasm to 5.48 MB; with the split it is 4.65 MB (889 KB gzip). `node axes-run.mjs claims` GREEN (6 commands), `generator` GREEN; lang-journey GREEN. Pushed by hand: the lander's only red was `rows --deployed` (600 s). Not published to Pages (the testground lane's publish.sh).
- PARKED. Continuation: nothing in flight. Worktree hbox `~/nd-land/meta` at c17cf0f0 + the part-3 files (= 0f86881d's content); `git reset -q origin/main` to sync. Next for META, by the critiques: (1) rung 2's checker-visible `quote`, which makes `produces I` a static check at the generator's install and lets `Ty.pkg I` have an introduction; (2) a surface `(produces I)` clause; (3) state `quorum_commit_attested`'s witnesses as "since the last reset" (the invariant already gives it); (4) the inspector line in TESTGROUND.report.md.
