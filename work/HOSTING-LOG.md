# HOSTING-LOG — BUILD-HOSTING continuation (updated 2026-10-17, after the hbox cutover)

Brief: ~/dev/redregg/work/nanodregg-scout/ASSEMBLY-hosting.md §6. Charter: hbox main /tank/dregg-build/nanodregg/main.
Work ONLY on hbox: /tank/dregg-build/nanodregg/wt/hosting; scripts/commit there; builds `swarm-build …`.
Mac scratch: use .../scratchpad/hosting-lane/ ONLY (the shared scratchpad's `hb/` was overwritten by another
agent). Write edit scripts locally, scp to /tank/dregg-build/nanodregg/logs/hosting-*.py, run there (avoid
remote heredocs: zsh mangles backticks/quotes). Mac worktree deleted.

## Landed (main)
- 7b6b7f5 lifecycle package + theorems + hosting-sim. 6525ea1 sim SEED + ALL PASS. 4651d21 text re-emit
  (LANG ID-1 changed reqTy). 5339a3a Plan + Controller decisions (6 vacuity holes fixed).
- 6095c5b HOSTING-5 half: package on LANG Std (machine/stepTo/pkgOf), `last` deleted, methods remove0/start1/stop2,
  owner law interim on Std.lawOf; Proofs.Deployed.invoke_slots (native_decide) on the real slot path.
  Worktree clean after it (check `git status`).
- 66f665d decisions: ProgramOutside (CLIENT 6278ab8) closes the symlink hole. 6577e82 HOSTING-5 DONE:
  owner law + field deleted (KERNEL-25 be98647), state {entry16, kind17, phase18}, seed (kind, entry),
  G7 expects noGrant, Controller.touchedIds for Host.Tail (c722b05).
## Waiting on
- CODEC-2 (a5db8dcb963c5d57d): Codec.Path.clean/join/split, .u32/.path/.paths fields, Codec.Tagged,
  emit-rust --hosting hosting/src/generated.rs. I write Hosting/Wire.lean (actionCases, eventCases,
  Refusal.all/code, Hosting.Bounds.{frameMax,pathComponentsMax,pathsMax,grainsMax}); must not import
  Controller (so Action/Verdict types may need to move to a module Wire can import). Then delete my
  `clean` for Codec.Path.clean. Codes: action launch1 kill2 refuse3; event started1 exited2.
- HOST-5 LANDED Host.Tail c722b05: Tail.open dir keys Cadence.deployed Deployed.world Deployed.recorder.mark
  Deployed.tailStep; Tail.await (rounds × tailPollMs 50); key = STORE/key 32 bytes (Host.Cli readKey).
  Controller exe = Tail.open → reconcile over all cells → loop await → touchedIds → reconcile → frames (waits CODEC).
- CLIENT-2 (a1612c507f0ff2b93) answered: Linux branch already real (0590c0f) via /usr/local/libexec/nd-bwrap
  (AppArmor profile; NEVER /usr/bin/bwrap by hand; launch only through nanodregg_sandbox::command); /proc
  dropped from the floor (a grain needing it fails at launch: send CLIENT the path). ProgramOutside
  refusal landing (sha to come) — our plan's program pkg/<entry> lies under read pkgDir, so it passes;
  plant: symlinked entry pointing outside must refuse at launch. Policy.connect only when a row needs it.
- LANG-3 (adc11001c5ad34e55): Lang/Print.lean replaces Hosting/Text.lean (delete mine then).
- PROTOCOL-4 handed off (facts in PROTOCOL-LOG.md addenda); PROTOCOL-5 writes the grain row once the `create --pkg PKG --state TEXT` verb exists. NOTE: LANG's Read.readData already landed (8c5db14) — tell PROTOCOL-5 if it waits on it.
## Next
grain-launch (hosting/ crate, own [workspace], sandbox by path) once frames exist; physical plant on
hbox bwrap: probe grain writes vol OK, neighbour world EPERM, unconfined control proves non-vacuity,
plan with worlds/ read must turn it red. Then resident plan (needs connect + nd --stdio) and Broker
Lean core + World lease (HOSTING-7 of the assembly); NO provider-key file until ROOT confirms ruling.
Owed theorem: dirOf (hex) injective. Labels lowercase (case-insensitive FS) not yet refused.

## FOR HOSTING-2 (successor) — exact next work (written by BUILD-HOSTING at its context ceiling, 10-17)
State: main has HOSTING through 6577e82; the grain row PASSes (PROTOCOL-5 a4cd717157c6d458e, 92c0ad9; re-run after 6577e82).
hbox wt/hosting is clean. Read decisions/hosting.md HOSTING-0..7 first.

### 1. Hosting/Wire.lean (def module; MUST NOT import Hosting.Controller — the emitter imports it)
CODEC-2 (a5db8dcb963c5d57d) promised these names (confirm on main before use; it sends the sha):
- `Codec.Path.clean (c : ByteArray) : Bool` (= our `Hosting.clean`: nonempty, ≤ `Codec.Path.componentMax`=64,
  not "."/"..", no 47/0, over `c.data.toList`, @[csimp] Array loop). Then DELETE `Hosting.clean`/`componentMax`
  in Hosting/Plan.lean and restate `plan_components_clean`, `lits_clean`, `plan_refuses_*` over it.
- `Codec.Path.join : List ByteArray → ByteArray`, `Codec.Path.split`, `split_join`, `join_split`.
- `Codec.Layout` (Codec/Layout.lean, ON MAIN): `Field = byte | u64 | bytes | list | oneOf name cases`,
  plus new `.u32 name`, `.path name` (value `{p : List ByteArray // ∀ c ∈ p, Path.clean c}`, refused
  `rejected … "path/badComponent"`), `.paths name` (u32 count ‖ path*); `Layout.codec max fits`, `Layout.codec_lawful`.
- `Codec.Tagged := List (String × UInt8 × Layout)`, `Tagged.codec max fits`, `Tagged.codec_lawful` (`badTag`).
- Emitter: `lake exe emit-rust --hosting hosting/src/generated.rs`, reading EXACTLY
  `Hosting.Wire.actionCases`, `Hosting.Wire.eventCases`,
  `Hosting.Bounds.{frameMax, pathComponentsMax, pathsMax, grainsMax}` (grainsMax = 256, today in Hosting/Plan.lean;
  move into a `Hosting/Bounds.lean` the Wire module can import), and `Refusal.all` / `Refusal.code`
  (pattern: CustodyRefusal). Refusal = labelUnclean idUnclean entryUnclean malformedGrain crashLoop residentUnsupported.
Our codes (agreed): actionCases launch=1 (grain bytes, Plan as program:path, read/write/exec/connect/hidden:paths),
kill=2 (grain), refuse=3 (grain, why: oneOf Refusal); eventCases started=1 (grain), exited=2 (grain, status:u32, atMs:u64).
Action/Verdict/Plan types: Wire needs Plan (Hosting.Plan is fine to import); Action/Verdict live in Controller —
either move them to Wire or have Wire describe them by layout only and give a conversion with a round-trip
theorem from Layout.codec_lawful (no hand byte code; law 2/3).

### 2. Controller exe (`hosting-controller STORE LABEL`, deployed Lean, a lean_exe whose root holds only main)
Host.Tail (HOST-5 a7950cd8b77873a7e, c722b05, namespace Nanodregg.Host):
  `Tail.open dir keys Cadence.deployed Deployed.world Deployed.recorder.mark Deployed.tailStep : IO (Except (StoreFault F) (Tail W × File))`
  `Tail.await keys c step seg t rounds` (sleeps Host.tailPollMs = 50 between empty reads; deadline = rounds × 50)
  keys = `Keys.ofKey key Host.Deployed.shapes`, key = the 32 bytes of STORE/key (as Host.Cli's readKey).
Loop: open → reconcile over every live cell id of the World (once, O(store) at start; page by grainsMax) →
await → `Controller.touchedIds Deployed.env turns` → reconcile → write Action frames to stdout; read event
frames on stdin into `Live` (memory only). pkgId = `Controller.lifecycleId Deployed.env` bytes. `now` = the
launcher's atMs. Every loop sleeps and has a deadline; the ONE unbounded loop is the top-level one (law 4).

### 3. hosting/ crate, bin grain-launch (std only; own `[workspace]`; dep `nanodregg_sandbox` by path ../sandbox;
CARGO_TARGET_DIR=hosting/target gitignored; SIZE: Rust lines)
Reads Action frames (generated.rs) from the controller's stdout, `sandbox::command(policy, program, [])`
with every Plan path joined onto the operator's hosting root (a CLI arg, absolute), writes started/exited
frames. Decides nothing: a decode refusal ends the run by name; `ConfineError` (ProgramOutside, Exposed …)
is reported as an exit, never a fallback. Mechanism on hbox: /usr/local/libexec/nd-bwrap (CLIENT-2;
never /usr/bin/bwrap). /proc is NOT in the Linux floor; a grain needing it fails — send CLIENT-2 the path.
PID file for every child it starts; kill only by that PID.

### 4. The EPERM plant (a launcher integration test, hbox, filtered: `cargo test -p hosting --test eperm`)
Layout in a temp root under the crate's target dir: worlds/w1/{store,members,grains/<hexA>/{pkg,vol}},
worlds/w2/grains/<hexB>/vol/secret. The plan comes from LEAN (run `hosting-controller` or a Lean
`hosting-plan` dev exe over a World with one running grain), never built by hand in Rust. Probe grain =
grain-launch's own `--probe VOL VICTIM` mode (Rust std works under bwrap on Linux; C is refused by
closure C8). The probe must print:
  vol-write OK; neighbour-write EPERM; neighbour-read EPERM; pkg-write EPERM; store-read EPERM (worlds/w1/store).
CONTROL: the same probe run UNCONFINED (plain Command) must get OK on neighbour-write — proves the denials
are not vacuous (assert the control's OK before reading the confined verdicts).
PLANTS (each must turn the test red by name): (a) a Plan with `worlds/` added to `read` ⇒ neighbour-read OK
(or Exposed refusal) ⇒ red; (b) a symlinked pkg/<entry> pointing outside ⇒ ProgramOutside at launch.
Then the grain row's physical half becomes an `.exe` row (ASSEMBLY HOSTING-11), with PROTOCOL-5.

### After
Resident plan (two processes; needs CLIENT `Policy.connect`, landed only when a row needs it, and `nd --stdio`),
broker Lean core + World lease (ASSEMBLY HOSTING-7; NO provider-key file until ROOT confirms KEY-CUSTODY:
Ember's ruling = the operator holds provider keys, resident calls through the broker). Owed: `dirOf` injective;
labels lowercase (case-insensitive FS) refused by name; delete Hosting/Text.lean when LANG's Lang/Print.lean lands.

## HOSTING-2 (a357cdb9a860f3cde, from 2026-10-17 15:45Z)
Scratch: Mac .../scratchpad/hosting-lane/ ; hbox logs/hosting-lane-* (commit logs, pid files, plants' .orig copies).
- e1c3ca4 Hosting/Wire.lean (HOSTING-8): Plan/Refusal/LaunchFailure/Verdict/Action/Report; actionCases
  launch1 kill2 refuse3, reportCases started1 exited2 failed3 (NOT "eventCases": Hosting.Event is the lifecycle's);
  Bounds.frameMax 4096 (one bound: frame + every field), grainsMax. Hosting.clean/componentMax and Plan.connect
  deleted. Proofs.Wire: codec_lawful x2, actionOf_wire, reportOf_wire, decode_encodeAction, launch_fields (names
  ↔ plan fields), plan_roles, planned_launch_encodes. Vacuity read: 3 holes fixed.
- e1bbaff (HOSTING-9): labelOk (a-z0-9-) for label AND idHex; labels_fold_injective, plan_disjoint,
  dirOf_injective (Lang.Print.hex), reconcile_distinct_deployed; Text.lean deleted (LANG-5 615e452); oneOf fields
  grainRefusal / launchFailure (CODEC-2's ask). CODEC-2 lands emit-hosting + read_frame/write_frame on it.
- LANG is LANG-5 a0ace030eb5525250 (round-trip theorem coming: then lifecycle_text_reads may become a corollary).
Next: controller exe (pure Run.step + IO loop over Host.Tail.next, reports via a dedicated stdin task), then the
hosting/ crate grain-launch, then the EPERM test.
- 4777611 (HOSTING-10) hosting-controller STORE LABEL: Hosting/Loop.lean pure `step` (absorb reports of KNOWN
  grains only → decide roundIds once, paged → afterOne marks launches running → prune to running ∨ qualifies);
  Hosting/Cli.lean IO loop (Tail.open; round 0 over allIds; Tail.next + drained reports per round; Exit names).
  Proofs.Loop: step_decides/launch_sound/kill_complete(all 4 cases)/launch_complete/launch_marks, remember_has,
  returning_complete, absorb_stranger, step_kept, step_one_per_grain(_deployed). hosting-sim G17 runs step.
- 42bfe6d (HOSTING-11) launcher/ crate (NOT hosting/: case collision; OWNERS swapped, generated.rs CODEC-owned,
  charter phrase): bin grain-launch ROOT LABEL PIDS CONTROLLER [ARG..], bin probe; Lean exe hosting-drive (one
  Lean-planned launch, test driver). launcher/tests/isolation.rs 3/3 on hbox: control all ok; confined vol ok,
  neighbour ENOENT x2, pkg EROFS, store ENOENT; plants exposed / programOutside. Build/test with
  CARGO_TARGET_DIR=/tank/dregg-build/nanodregg/logs/hosting-lane-target (lane-private), filtered `--test isolation`.
  Not in standing yet (asked GATES-2 aedb775dc4517c504).

### FOR HOSTING-3 (successor) — written by HOSTING-2 at ~400K, 2026-10-17
Agent ids now: LANG-6 a0e14827e8b076d95, CODEC-3 a5c03e9649c328e52, KERNEL-6 aa36c7021124d8bdb (at ceiling →
KERNEL-7), GATES-2 aedb775dc4517c504. Check hbox logs/ROLES.txt.
Owed / waiting:
1. KERNEL-7 lands `fold_frame : World.fold E w ts = .ok w' → c ∉ touchedIds ts → w'.entry E c = w.entry E c`
   with the World port (KERNEL-23). Then: (a) state the controller's batch soundness over it (a cell not in
   touchedIds keeps its decision); (b) the port DELETES `w.cells`: replace `Loop.allIds w := w.cells.keys` with
   `w.trie.toList.filterMap fun p => match p.1 with | .cell c => some c | .nullifier _ => none` (O(store), start
   only; routing order — sort if order matters; it does not for step). World readers will take E (`w.live E i`):
   Controller.reconcile / Loop / proofs re-thread E.
2. LANG-6 owes `hex_injective` (from Lang.Proofs.Print.unhex_hexChars); then delete my local dirOf_injective
   lemmas (Hosting/Proofs/Controller.lean: digit_inj, byte_inj, hexL, hexL_inj) and use it.
3. lifecycle_text_reads → corollary of Lang.Proofs.Print.readPackage_checked (2a3285e) with ifaces = [];
   still needs `(Print.package lifecycle).isSome` and the check result as instances (one compiled fact may
   remain); goal: drop or shrink the native_decide allow row in gates/axioms-allow.tsv.
4. Broker (ASSEMBLY HOSTING-7) + provider-key file: KEY-CUSTODY CONFIRMED by Ember 10-17 — the OPERATOR
   holds provider keys; the resident calls through the broker; no key ever reaches the resident. First
   deliverable per charter: "the broker's first refusal by name with no key reaching the resident". Design in
   decisions/hosting.md first (both critiques); Lean decides (lease, refusals), Rust (launcher/ second bin,
   `keybroker`) moves bytes; key file custody checks like CLIENT's custody (mode/owner).
5. Resident plan: waits on CLIENT `Policy.connect` (only when a row needs it) and `nd --stdio`.
6. Grain row's physical half as an .exe row (ASSEMBLY HOSTING-11) with PROTOCOL-6 abd8f012f13228e0b.
Commit hygiene learned: scripts/commit refuses "worktree behind main" when another layer touched your file
(KERNEL edited Hosting/Controller.lean once): `git diff --binary > logs/x.patch; git checkout -- <dirs>;
git checkout --detach main; git apply --3way logs/x.patch; git reset -q`. SIZE lines must match the gate's
exact metric names (e.g. 'SIZE: max dependents of a non-foundation module: <why>'). A def in a Proofs
module is refused (closure C3); a theorem in a def module must be private.
- UPDATE (after the handoff text above): LANG-6 landed `Lang.Print.hex_injective` / `hexChars_injective` /
  `hexChars_lower` / `hexChars_digit` at f9ccb37 (Lang/Proofs/Print.lean). Item 2 is unblocked: dirOf_injective
  = hex_injective ∘ (String.toByteArray_inj, already used); delete digit_inj/byte_inj/hexL/hexL_inj. Also prove
  `dirOf_labelOk : labelOk (dirOf b) = true` (for b.size ≤ 32) from hexChars_lower, so the Plan.lean:42 docstring
  claim ("dirOf's lowercase hex is") is a theorem and the controller's plans never hit idUnclean. LANG-6 warns:
  its next landing changes Read fuel (Read.need = nesting depth, new Read.listMax; Print.fits checks width) —
  re-run hosting-sim G0 and lifecycle_text_reads after it.
- UPDATE: GATES-2 23a1f31 — the isolation test is now a standing tooth: gates/runs.tsv row
  `cargo:launcher:isolation	hosting-drive	exit 0`, run by standing.sh every run and by pre-push when launcher/
  or hosting-drive's import closure changes (ND_LEAN_BIN = the tree's bin). Plant verified by GATES-2. The
  HOSTING-11 CRITIQUE line "not a standing tooth until GATES runs it" is now stale: update it in decisions/hosting.md.

## HOSTING-3 (a514a92b544a85557, from 2026-10-17 19:50Z)
Scratch: Mac .../scratchpad/hosting-lane/ (h3-*.py edit scripts, msgN.txt); hbox logs/hosting-lane-* .
- ca798ba: lifecycle_text_reads = readPackage_checked at the lifecycle (∃ p s form), lifecycle_prints +
  lifecycle_encodes decide +kernel; both allow rows deleted (GATES-2 agreed); dirOf_injective = hex_injective;
  HOSTING-11 stale critique fixed; HOSTING-0 law-6 amendment dissolved. Reader a76c8e54c22da8406 ACCEPT.
- Note: `swarm-build lake build Hosting.Proofs.X` in wt/hosting is fast (warm); use it before scripts/commit.
- Next: HOSTING-12 broker design (decisions first), then stage 1.
- UPDATE: KERNEL-7 (ac9b1fb8228590424) carries the mechanical Hosting/ edits in its KERNEL-23 flag day (E threaded
  through reconcile/Loop/proofs, allIds = w.cellIds (trie order, tombs included), Cli uses X.env and the tail's
  (Turn, root) pairs). HOSTING-2 said OK after reading the diff. Item 1(b) above is therefore done by KERNEL-7;
  item 1(a) (fold_frame-based batch soundness) stays yours when its sha arrives. Merging bytesOf into E is yours, later.
- (in flight) HOSTING-12 broker stage 1 Lean half in wt/hosting (untracked Hosting/Broker*.lean,
  Proofs/Broker.lean; lakefile + runs.tsv row hosting-broker; decisions HOSTING-12). Reader
  a5494fcc5eb38c127 found 3 holes, fixed; re-read pending. Plants script: hbox logs/hosting-lane-plants.sh
  (7 plants, all red). Smoke: logs/hosting-lane-smoke.py (python frames → hosting-broker --drive).
  Commit msg: Mac scratch hosting-lane/msg2.txt.
- Also staged: Hosting/Proofs/Frame.lean (fold_frame, decide_frame over KERNEL-7 7c43273 admit_frame):
  HOSTING-10's owed batch frame; land separately after the read.
- Next asks: CODEC-3 emit broker frames → launcher/src/broker_generated.rs (families ask/request/verdict/
  answer, FRAME_MAX 131072); CLIENT custody `read_private` shared (needs CLIENT-3 via ROOT) so keybroker
  does not twin client/src/fsx.rs.
- 06edf05 LANDED: HOSTING-12 broker stage 1 Lean half (Broker, BrokerWire, BrokerCli, exe hosting-broker
  --drive T0 R=WINDOWMS:CAP:MAXTOK:MODEL/SLOT/PRICE[+..]; Proofs.Broker; specs private in proofs (List UInt8
  refused in def modules)). Reader a5494fcc5eb38c127 ACCEPT (2 passes).
- e15813f LANDED: Proofs/Frame.lean fold_frame/decide_frame.
- Asked CODEC-3 (a5c03e9649c328e52): launcher/src/broker_generated.rs from Hosting.BrokerWire 4 families.
  Asked ROOT: CLIENT-3 to move fsx read_private into sandbox crate (public, length range) for keybroker.
  keybroker Rust waits on both. Then: launcher/tests/broker.rs (resident stand-in; refusals by name; canary
  key never in resident bytes; 0644 key file stops by name; requestTooLarge instance).
- 570adfe LANDED: dirOf_labelOk + labelOk_of + reconcile_labels_deployed (Proofs/Controller section DirLabel).
- CODEC-3 landed 2d05802: launcher/src/broker_generated.rs (emit-broker). CODEC is now CODEC-4 aaba467e9c60e21bc
  (told: ask already done). OWNERS row for broker_generated.rs → CODEC: ask GATES-2 (not yet asked).
- CLIENT-3 aae5c92a4d1999133 moving read_private → nanodregg_sandbox::custody::read_private(path, RangeInclusive)
  Refused = Link|NotRegular|Owner|Mode|Length|Io; I agreed to its launcher/Cargo.lock cross-layer. Waiting on sha.
- Drafted (Mac scratch hosting-lane/): keybroker.rs (launcher/src/bin), broker_test.rs (launcher/tests/broker.rs),
  BrokerCli.lean argv now `hosting-broker T0 --drive SPECS` (keybroker passes T0 first). Need: lib.rs
  `pub mod broker_generated;`, Cargo.toml [[bin]] keybroker + zeroize =1.8.2 dep, runs.tsv row
  `cargo:launcher:broker	hosting-broker	exit 0` (GATES format, SHARED file), decisions HOSTING-12 Rust half.
- cc4f6fe + 0c86537 LANDED: keybroker (launcher/src/bin/keybroker.rs) + launcher/tests/broker.rs (standing row
  cargo:launcher:broker, 3/3); hosting-broker argv `T0 --drive SPEC`. 0c86537 = fix forward: Unix socket path
  >107 B in judge slot target dir (sockets now in $TMPDIR/kb<pid><name>, symlinked). Reported fail-open to GATES-2
  (new red row counted PRE-EXISTING). Rust plants script: hbox logs/hosting-lane-rplants.sh (3 plants red).
- Agreed: LANG-7 (ac6dbe9957c6ff484) lang! day edits Hosting/Proofs/Package+Deployed + re-emits world/grain/Lifecycle
  (asked: method_no_calls over all cases; re-run hosting-sim; message names lifecycleId re-emit). CODEC-4 may add
  launcher/tests/path_vectors.rs + row (cross-layer agreed).
- NEXT (HOSTING-12 stage 2): world/hosting/Allowance package (Lean-generated text, G0-style gate in hosting-sim),
  hosting-broker STORE mode via Host.Tail (like Hosting/Cli.lean), allowanceAmbiguous refusal, owner = operator
  member id check; key-slot set passed to decider (critique: keyMissing after charge). Then resident plan (blocked).

### FOR HOSTING-4 (successor) — written by HOSTING-3 at ~430K, 2026-10-17
Main has HOSTING through 0c86537. wt/hosting is clean and detached at main (check `git status`).
Read decisions/hosting.md HOSTING-12 in full first: the broker design, its theorems, the reader holes and the critiques.
Open, in order:
1. HOSTING-12 stage 2: the allowance comes from the World.
   - (a) A `world/hosting/Allowance` LANG package, generated in Lean like Hosting/Package.lean. Its state is
     {resident bytes, windowMs, cap, maxTokens, models list}. The owner is the operator and KERNEL-25 gates
     writes. The text comes from Lean.Print, with a G0-style byte gate in hosting-sim and a text-reads theorem
     through readPackage_checked (the lifecycle pattern).
   - (b) A `hosting-broker T0 STORE OPERATOR` mode that follows the Store through Host.Tail, as Hosting/Cli.lean
     does. It builds the entries from allowance objects whose KERNEL owner is OPERATOR. Two allowance objects
     for one resident are refused `allowanceAmbiguous`, which is a new Broker.Refusal case: that is a frame
     change, so ask CODEC-4 to re-emit broker_generated.rs.
   - (c) A changed allowance is a new budget (HOSTING-12 premise). Decide whether a changed windowMs restarts
     the meter at the forfeited window.
   - (d) Pass the set of key slots keybroker holds to the decider at start, so that keyMissing is refused
     before any charge. This closes HOSTING-12's critique.
   - Then delete the `--drive` mode (law 1: one input source) and move the test to a Store fixture.
2. Resident plan (HOSTING-6 of the assembly). It still waits on CLIENT `Policy.connect` (CLIENT-3
   aae5c92a4d1999133) and `nd --stdio`. The resident's plan must `connect` to its broker socket and must hide
   the key file.
3. TLS for upstream: decide it at stage 2 (critique). Either an operator-run terminator or a dependency in the
   key-holding process.
4. The grain row's physical half as an .exe row (ASSEMBLY HOSTING-11), with PROTOCOL-6.
5. Owed theorem: a grant's verdict always encodes (today the decider exits `unencodable`, which fails safe).
Watch for: LANG-7's lang! day re-ids the lifecycle (it makes the Hosting/Proofs edits, and I agreed). After it
lands, re-run hosting-sim and check that lifecycle_prints and lifecycle_text_reads build.
Hygiene learned:
- A new runs.tsv row that is RED on its own commit is labelled PRE-EXISTING and lands. Grep the judge log
  for `run <row> : ok` (reported to GATES-2).
- A Unix socket path is at most 107 bytes. Judge slot target dirs are deeper than that.
- Plants that leave a process running must fail by a deadline, never hang.
- In a def module, `List UInt8` is refused and so is a public theorem. Put specs as private defs in the Proofs
  module.
Agent ids: LANG-7 ac6dbe9957c6ff484, CODEC-4 aaba467e9c60e21bc, CLIENT-3 aae5c92a4d1999133, GATES-2
aedb775dc4517c504, KERNEL-7 ac9b1fb8228590424, LEDGER-2 afd32f4b9d6e68d3e. Reader used: a5494fcc5eb38c127.
ROOT ruling (10-17): stage 2 next. When stage 2 produces a row that needs Policy.connect, tell PROTOCOL-6
(abd8f012f13228e0b) for the row and CLIENT-3 (aae5c92a4d1999133) for the allowance. GATES-2 has the
PRE-EXISTING-new-row hole as its top item.
- GATES-2 closed the PRE-EXISTING-new-row hole in 0f4a2ae: the parent tree now runs only the rows in its own table, so a new row that goes red is NEW RED and pre-push refuses it. A new row's verdict in the summary can be trusted again.

## HOSTING-4 (a005898b332a67387, from 2026-10-18 00:55Z)
Scratch: Mac .../b3795e84-.../scratchpad/hosting-lane/ ; hbox logs/hosting4-* .
- Design taken (HOSTING-13, to write): an allowance is ONE meter = (resident, model): {resident, model, keySlot,
  microPerKTok, windowMs, cap, maxTokens, revoked}. LANG has no list type, and a fixed-arity model array is worse.
  The resident's total spend is the sum of its caps. KERNEL refuses `write` on a programmed object (hasMethods), so the
  package has methods `revoke` (permanent) and `set` (keeps model/resident/revoked) and NO laws. Ambiguity = two
  unrevoked operator-owned allowances for the same (resident, model); the operator resolves it with revoke.
  Entry.resident = dirOf(resident grain id), the socket name. Broker.follow: an unchanged (resident, allowance) keeps
  its meter, and a changed or new one opens spent to cap at max(now, last) (rule (c)). Broker.keys = keybroker's
  slots, so keyMissing is refused before any charge (d).
- Asked CODEC-4 for permission to carry the emit-broker re-emit cross-layer (allowanceAmbiguous = code 15). Told LANG-7.
- f6e0fe2 LANDED (HOSTING-13): allowance package + Broker one-meter/follow/keys/ambiguity; vacuity reader
  ad64d8383bcb4c821 ACCEPT on its 2nd pass (4 holes + 1 residue fixed); 11 Lean plants + 1 Rust plant red
  (scripts: hbox logs/hosting4-plants*.sh, hosting4-moved.sh, hosting4-swap.sh, hosting4-rplant.sh). CODEC-5 told.
- Stage 2b IN FLIGHT (wt/hosting, uncommitted): Allow.readAt/update + Proofs.Allowance mem_update/update_start/
  update_tracks (via fold_frame), built green; Hosting/BrokerCli.lean is now STORE mode ONLY
  (`hosting-broker T0 SLOTS STORE OPERATOR`, catchUp ≤ drainMax reads then `behind`, refresh = update + follow per
  ask), and it builds. --drive is DELETED in it. Drafts in Mac scratch hosting-lane/src: keybroker.rs
  (argv KEYS SOCKDIR PIDS UPSTREAM STORE OPERATOR RESIDENTS DECIDER; decider policy read=[STORE]) and
  tests/broker.rs (a World::genesis real-Store helper: nd --init/--keys, host genesis, supervise_host serve,
  nd install/create/invoke; residents 01,02; the live set → overSpend, revoke → grant on a). These are NOT yet on hbox.
  BLOCKED ON CLIENT-3's devtools crate (ROOT ruling): nanodregg_devtools::{repo, lean_bin, nd, nd_supervise,
  Supervisor::hold, supervise_host(nd_supervise, sock, hide, store, args)}. I agreed to its launcher/Cargo.toml
  [workspace] removal and Cargo.lock deletion. When it lands: add the dev-dep, switch isolation.rs and broker.rs
  lean_bin to devtools, ask GATES-2 to make the runs.tsv row `cargo:launcher:broker hosting-broker,host`, write
  HOSTING-14 in decisions, get a vacuity read, run the plants (update drops the touched filter; refresh skips the follow).
  Unverified: whether `nd install` prints `id <pkg hex>`.
- 659639d LANDED (HOSTING-14): STORE-mode hosting-broker; --drive deleted; Allow.absorb/update + tracking and fold
  theorems; real-Store broker test via devtools (CLIENT-17 cb6df3f); runs row hosting-broker,host. Reader ACCEPT
  on its 2nd pass. cv task 01a14a5f-c476 = decode→World.Canon theorem (CODEC/HOST), premise (i).
  Smoke on a real Store: hbox logs/hosting4-smoke.py (uses logs/hosting4-client-target nd binaries).
- NEXT (told ROOT): (1) theorem: a grant's verdict always encodes (HOSTING-12 owed); (2) TLS-for-upstream decision;
  (3) the resident plan (Policy.connect with CLIENT-3, nd --stdio); (4) the grain row's physical half with PROTOCOL-6.
- 5f03823 LANDED: step_encodes + grant_cap (verdicts always encode; `unencodable` unreachable).
- cv 01a14a5f-c476 (opened World is Canon): CODEC-5 landed Codec.Deployed.world_get_canon + Stream.refine_get_inner /
  product_get_fst (7db0597). HOST-8 a7b51f5a41be70521 is landing Host.openWith_world + Base.read_decode with HOST-28
  (sha to come). Then write the corollary in Hosting/Proofs: openWith_world → Base.read_decode → refine_get_inner →
  product_get_fst → world_get_canon → fold_canon (step = (tailStep w r).map Prod.fst; foldlM) ⇒ t.world.Canon. Then
  close the cv task with the theorem name. NOTE: Tail.open = openWith over IO readers (that is code, not a theorem).
- HOSTING-15 TLS — ROOT RULED (10-18): rustls =0.23.40 + ring =0.17.14 (no fetched pure-Rust provider), in the TCB
  table as "trusted, unverified; swapped only for a verified provider". Anchors are operator DATA:
  `keybroker KEYS ANCHORS …`, read with custody checks (regular, no symlink, owner = euid, not g/o-writable; 0644 ok),
  refusing anchorsMissing / anchorsMalformed by name. deploy/ emits the prod anchors from pinned webpki-root-certs, with a
  generated.tsv-style byte check (OPS-2 a493aca8608fbc234 owns this). HOSTING-15 must state that editing the anchor
  file widens trust and that the emitted-vs-crate check is what detects it. The hostname comes from a Lean model→provider
  table and is carried in the grant frame (the grant gains `host`: a CODEC-5 afad87333c5b8a98a re-emit). UPSTREAM stays
  the dial address, with SNI and verification on Lean's host. No custom verifier. Refusals tlsCertificate / tlsHostname /
  tlsProtocol (+ noProvider from Lean). Test: its own CA (rcgen dev-dep), and the canary over real TLS is the success
  control. Plants: an untrusted cert, a hostname mismatch. Plan: Lean first (providerOf "claude-" prefix → anthropic
  host api.anthropic.com; teeth/sim/test models renamed claude-*; step_encodes gains the host field), then keybroker
  rustls, then the test. Ask CLIENT-3 for custody::read_public (do not twin it in keybroker).

### FOR HOSTING-5 (successor) — written by HOSTING-4 at ~450K, 2026-10-18
Main has HOSTING through 5f03823. Read decisions/hosting.md HOSTING-12, -13 and -14 first. wt/hosting is clean
(`git checkout --detach main` before editing). NOTHING is in flight: HOSTING-15 has not started. Lane scratch:
hbox logs/hosting4-* (plants: hosting4-plants*.sh, -moved, -swap, -born, -rplant; smoke over a real Store:
hosting4-smoke.py using logs/hosting4-client-target nd binaries; plant helper hosting4-plant.py) and Mac
.../b3795e84-.../scratchpad/hosting-lane/.
Landed by HOSTING-4: f6e0fe2 (HOSTING-13 allowances in the World: one meter per (resident, model), package
world/hosting/Allowance with methods revoke/set and no law, follow, keys, allowanceAmbiguous), 659639d (HOSTING-14
STORE-mode broker `hosting-broker T0 SLOTS STORE OPERATOR`, --drive deleted, the broker test on a real Store via
devtools), 5f03823 (step_encodes). The vacuity reader ad64d8383bcb4c821 has context on all three.

1. HOSTING-15, TLS for keybroker's upstream. ROOT RULED (10-18); build exactly this, decision first (CRITIQUE + META):
   - The crypto is rustls =0.23.40 with the ring =0.17.14 provider (in the hbox cargo cache; do NOT fetch rustcrypto).
     Add it to the TCB table beside SHA-512 as "trusted, unverified; swapped only for a verified provider". TLS is in
     the TCB by trust (a platform fact, law 2 table), not by proof. There is no OpenSSL and no custom verifier. rustls
     has no renegotiation. SNI and hostname verification are on.
   - Anchors are operator DATA: `keybroker KEYS ANCHORS SOCKDIR PIDS UPSTREAM STORE OPERATOR RESIDENTS DECIDER`.
     keybroker reads ANCHORS (PEM) under custody checks: regular file, no symlink, owner = euid, not group- or
     world-writable (0644 ok). It refuses anchorsMissing / anchorsMalformed by name at start. I asked CLIENT-3 for
     `nanodregg_sandbox::custody::read_public(path, range)` (same Refused enum) so the checks are not twinned; that
     answer is pending. deploy/ emits the production anchors from the pinned webpki-root-certs (cache has 1.0.8/1.0.9),
     with a generated.tsv-style byte check against the crate. OPS-2 a493aca8608fbc234 owns the emit and the check
     (asked; proposed path deploy/units/tls-anchors.pem; pending). HOSTING-15 must say: an operator who edits the
     anchor file widens trust, and the emitted-vs-crate check is what detects it.
   - The hostname comes from a Lean model→provider table (`providerOf`, e.g. the prefix "claude-" → Anthropic,
     host api.anthropic.com; an unknown model is refused `noProvider`), never from the resident's ask. The grant frame
     gains `host`: a Broker.Refusal/Verdict frame change, so CODEC-5 afad87333c5b8a98a re-emits broker_generated.rs (or
     agrees that you carry `lake exe emit-broker` cross-layer, as CODEC-4 did). Update step_encodes for the
     extra field. The teeth, the sim's Allowance journey and the Rust test use model "m"/"n"/"a"; rename them to
     claude-* and fix the fixed numbers (accumulate_tooth's 83, the keyMissing tooth).
   - UPSTREAM stays the operator's dial address. SNI and verification use Lean's host, so a misrouted dial fails
     verification. The HTTP Host header becomes Lean's host.
   - New wire refusals: tlsCertificate, tlsHostname, tlsProtocol (append codes 16+, plus noProvider). Map rustls'
     errors (NotValidForName → tlsHostname; UnknownIssuer and other certificate errors → tlsCertificate; everything
     else → tlsProtocol; a dial failure stays upstreamFailed). Never relay upstream text.
   - Test (launcher/tests/broker.rs): its own CA via the rcgen dev-dep (cache has 0.14.8; use its ring feature),
     a fake upstream on rustls ServerConfig with a cert for api.anthropic.com signed by the test CA, and the test
     passes that CA as ANCHORS. CONTROL: the canary over real TLS (the key reaches the fake upstream; no resident
     byte holds it). PLANTS, each red by name: a self-signed (untrusted) server cert → tlsCertificate; a cert for
     another hostname → tlsHostname. Keep the existing plants green/red as before.
2. cv 01a14a5f-c476: prove the World `Tail.open` returns is `World.Canon`, then close the task with the theorem name.
   Pieces: HOST-8 a7b51f5a41be70521 is landing `Host.openWith_world` (Host/Proofs/Backup.lean: the opened world =
   `rs.foldlM step b.world` with `Base.read … = .ok (b, …)`) and `Base.read_decode` with its HOST-28 commit. Neither
   sha has arrived yet. CODEC-5 landed 7db0597: `Codec.Deployed.world_get_canon` (world.get at any offset → Canon +
   leaves fit), `Codec.Stream.refine_get_inner`, `product_get_fst`. The chain is Base.read_decode → unfold decode to
   get at 0 → refine_get_inner → product_get_fst → world_get_canon → KERNEL fold_canon over foldlM of
   `(tailStep w r).map Prod.fst` (each record's runRooted = fold: Hosting/Proofs/Allowance runRooted_fold /
   stepTurns_fold). State it over openWith_world, and note in HOSTING-14 that `Tail.open` runs that openWith
   over IO readers, which is code. That discharges premise (i) of HOSTING-14 and the controller's round 0
   (allIds_complete / start_tracks are already stated under Canon).
3. The resident plan (HOSTING-6 of the assembly) waits on CLIENT `Policy.connect` (ask CLIENT-3 when a row needs
   it) and `nd --stdio`. The resident's plan must `connect` to SOCKDIR/<dirOf grain id>.sock (Entry.resident =
   dirOf of the allowance's resident = the resident grain's World id) and hide the key file. Open question for
   stage 3: keybroker's RESIDENTS is still an operator argument, and deriving sockets from the World is undecided.
4. The grain row's physical half as an .exe row (ASSEMBLY HOSTING-11), with PROTOCOL-6 abd8f012f13228e0b. Now that
   devtools exists, the controller can be driven on a real Store exactly as broker.rs does (host genesis/serve/
   follow + nd install world/grain/Lifecycle + create + invoke start), with grain-launch under it. PROTOCOL-6
   advised registering it as a cargo:launcher:<test> row naming host.
Hygiene learned:
- Remote python with quotes breaks in ssh '…'. Write scripts locally and scp them (logs/hosting4-*.py).
- Before applying a patch, `git checkout -- PATHS` restores from the INDEX. After `git apply --3way` your edits are
  staged, so check `git diff --cached`.
- scripts/commit wants a SIZE line for every metric that rose. A Prop def in a def module is refused (C3): put
  specs as private defs in the Proofs module. Run `cargo fmt -p nanodregg-launcher` before committing.
- Cargo rows run under the root workspace (GATES-2): a new dependency ships with its Cargo.lock change.
Agent ids: CODEC-5 afad87333c5b8a98a, LANG-8 a4b6bc659ce41e2d9, HOST-8 a7b51f5a41be70521, CLIENT-3
aae5c92a4d1999133, PROTOCOL-6 abd8f012f13228e0b, OPS-2 a493aca8608fbc234, GATES-2 aedb775dc4517c504, LEDGER-2
afd32f4b9d6e68d3e, vacuity reader VACUITY-READER-H4 ad64d8383bcb4c821. Check hbox logs/ROLES.txt.
- UPDATE (after the handoff): OPS-2 agreed on the anchors. The path is `deploy/tls/anchors.pem` (NOT deploy/units).
  Format: concatenated PEM CERTIFICATE blocks, one per `webpki_root_certs::TLS_SERVER_ROOT_CERTS` entry in the
  crate's order, base64 at 64 columns, LF. Pin `webpki-root-certs = "=1.0.9"`. The emitter is a Rust bin
  `emit-anchors [--check] PATH` in a new workspace member deploy/anchors. It waits on GATES letting a generated.tsv row
  name a cargo bin (so a hand edit of the .pem is red on every commit). OPS-2 sends the sha. keybroker's ANCHORS =
  that file's installed path.
- UPDATE: CLIENT-3 landed `nanodregg_sandbox::custody::read_public(path, range)` at 0c17301 (CLIENT-18). It refuses a
  symlink, a non-regular file, an owner ≠ euid, a length out of range, any g/o write bit, and setuid/setgid/sticky.
  0644/0444/0600 pass, and the same Refused enum is used. A root-owned system bundle is refused (by design: it is the
  operator's file). The parent directory is NOT checked (flagged to ROOT). Use it for keybroker's ANCHORS.
- FYI (LEDGER-3 a11788b66fe43f571): world/escrow/Escrow is LEDGER's shipped text (7c6c7e1, ledger-sim E0 gate). It is not HOSTING's. Nothing to do.
- UPDATE: CLIENT-19 eb0ec6a (ROOT ruling). read_private, read_public and check_private_dir now apply sshd StrictModes
  to every ancestor directory (owner euid or root, no g/o write), refused `Dir(path)`; /tmp and group-writable
  /tank paths are refused. keybroker names it `keyFileDir` (CLIENT carried this cross-layer). Tests must use
  devtools::scratch(name)/mkdirs ($ND_SCRATCH, else ~/.cache/nd-t, 0700), and the launcher broker test already does.
  OWED by HOSTING-5: the broker test leaves directories behind in ~/.cache/nd-t, so clean them up (remove only what the test
  created). The ANCHORS file must also live under a StrictModes-clean path, both in deploy and in the test.

## HOSTING-5 (a16c2e5b494aa5e26, from 2026-10-18 06:35Z)
Scratch: Mac .../b3795e84-.../scratchpad/hosting-lane/h5/ ; hbox logs/hosting5-* (plants: hosting5-plants.py
(Rust, args = plant names), hosting5-lplants.py (Lean); outputs hosting5-plants*.out).
- 0eb0803 LANDED HOSTING-15 (TLS): Lean providers/providerOf/noProvider + grant host; keybroker
  `KEYS ANCHORS SOCKDIR PIDS UPSTREAM STORE OPERATOR RESIDENTS DECIDER`, rustls 0.23.40/ring, TLS1.3 only,
  anchors via custody::read_public (CLIENT-18/19 incl. dir chain), tls* refusals; test own CA (rcgen), canary
  over real TLS, plants (untrusted, hostname, TLS1.2-only server, no close_notify) red. Reader ACCEPT pass 2.
  gates/tcb.tsv CREATED (ROOT ruling) + OWNERS SHARED; GATES-3 a34016a287bafcb63 writes the gate + untrusted/
  rustls-webpki rows; CLIENT-3, CODEC-6 a7dcb3be86813ca52 add theirs. SPKI pin follow-up = cv 01a14a7d-55c3.
  OPS-2 has the argv (installed layout /etc/nd/keybroker/{anchors.pem,provider.key}, user nd).
- NEXT: Canon corollary (cv 01a14a5f-c476): draft at hbox logs/hosting5-Open.lean (Hosting/Proofs/Open.lean),
  pieces cited: Host.openWith_world + Base.read_decode (6b89d6f), Codec.Stream.refine_get_inner/product_get_fst,
  Codec.Deployed.world_get_canon, stepTurns_fold, fold_canon. Agents now: HOST-9 aa03e59965e1f9ec4, CODEC-6
  a7dcb3be86813ca52, LANG-9 ae7c1ef24d42d1286, GATES-3 a34016a287bafcb63.
- 26b8074 LANDED: Hosting/Proofs/Open.lean open_world_canon (HOSTING-14 premise (i) discharged); cv 01a14a5f-c476
  DONE; satisfiability witness follow-up cv 01a14a8a-ffa6 (native_decide over a small sealed base).
- HOSTING-16 (OPS-2's ask: keybroker exit table) built in wt/hosting: Hosting/BrokerExit.lean (DeciderExit 0/70-78,
  KeybrokerExit 80-100,102,103; 101 = Rust panic avoided), Proofs/BrokerExit.lean, BrokerCli Exit.kind/code, Emit/Broker
  emits keybroker_exit (CODEC-6 agreed, cross-layer), keybroker.rs exits from it (decider code passed through),
  test asserts codes. Plants red (3 Lean). Vacuity read requested from ad64d8383bcb4c821.
- 12ce0ff LANDED HOSTING-16 (keybroker exit table; OPS-2's blocker). Reader ACCEPT pass 2.

### FOR HOSTING-6 (successor) — written by HOSTING-5 at ~380K, 2026-10-18
Main has HOSTING through 12ce0ff. wt/hosting is clean (run `git checkout --detach main` before editing). NOTHING is in
flight. Read decisions/hosting.md HOSTING-15 and -16 first. Lane scratch is hbox logs/hosting5-*:
- plants: hosting5-plants.py (Rust; argv = plant names; restores keybroker.rs from hosting5-kb.orig.rs) and
  hosting5-lplants.py (Lean);
- outputs: *.out.
Landed by HOSTING-5:
- 0eb0803 HOSTING-15: TLS. Lean's providers table names the host; keybroker takes KEYS ANCHORS …; rustls 0.23.40 on
  ring, TLS 1.3 only; the anchors go through custody::read_public; refusals tls*; gates/tcb.tsv created.
- 26b8074: open_world_canon (cv 01a14a5f-c476 DONE).
- 12ce0ff HOSTING-16: the exit tables.
Open follow-ups (cv):
- 01a14a7d-55c3: SPKI pin set, tlsPin, in addition to the chain check (ROOT: not v0).
- 01a14a8a-ffa6: a native_decide closed witness that open_world_canon's premise is satisfiable.
Reader residues, not holes:
- HOSTING-16: only one decider code (io 78) is exercised, so a second case (store 76 via a corrupted Store) would
  pin the pass-through fully.
- HOST-9 is told that readKey throws on a missing key file (so that end is named io, not store).
- HOSTING-15: a keybroker that ADDED bundled roots to its store is review-guarded, not test-guarded.
Waiting on others:
- OPS-2 a493aca8608fbc234 renders the keybroker unit from DeciderExit/KeybrokerExit.codesOf (it has the argv and
  the layout /etc/nd/keybroker, user nd, and ExecStartPre emit-anchors --check). It will move SOCKDIR when stage 3
  names a sandbox-reachable one.
- GATES-3 a34016a287bafcb63: the tcb.tsv gate, plus the untrusted/rustls-webpki rows (owner HOSTING).
- CLIENT-3 and CODEC-6 add their tcb rows.
NEXT, in order:
1. Resident plan (stage 3). The need is a launcher cargo test, not a Protocol row. Protocol rows are `.members`
   nd drives, and PROTOCOL-6 advised `cargo:launcher:<test>` rows naming their Lean exes.
   - The test: the controller launches a grain whose kind is resident; its plan lets it connect to
     SOCKDIR/<dirOf grain id>.sock; it asks keybroker and gets a grant from the fake TLS upstream; it cannot read the
     key file. That needs CLIENT `Policy.connect` (CLIENT-3 aae5c92a4d1999133 builds it when a row needs it, so send
     them this test as the need) and `nd --stdio`.
   - Note: on Linux, connect() to a socket inode on a ro bind works (IS_RDONLY does not gate sockets), but the
     sandbox policy should name it explicitly.
   - Open question: keybroker's RESIDENTS is still an operator argument. Should the sockets be derived from the World?
   - LANG-35 (3ed84fc): an install now needs its import closure pinned (`unpinned`). This touches hand installs in tests.
2. The grain row's physical half: a cargo:launcher test driving the controller on a real Store (as broker.rs does:
   host genesis/serve + nd install world/grain/Lifecycle + create + invoke start), with grain-launch under it.
Agents (check ROLES.txt):
- CODEC-6 a7dcb3be86813ca52, HOST-9 aa03e59965e1f9ec4, LANG-10 a712e8c509a3bb0e0, GATES-3 a34016a287bafcb63
- CLIENT-3 aae5c92a4d1999133, PROTOCOL-6 abd8f012f13228e0b, OPS-2 a493aca8608fbc234
- VACUITY-READER-H4 ad64d8383bcb4c821 (it has context on HOSTING-13..16)
Hygiene:
- scripts/commit wants a SIZE line for EVERY metric that rose, including 'Lean lines (Emit)', the tooling line, and
  'max dependents …'.
- C3 refuses any def/abbrev exported from a Proofs module: inline it, or make it private and keep it out of
  public statements.
- Python edit scripts run inside ssh with an unquoted heredoc turn `\\n` into a real newline. scp script files
  instead.
- cargo fmt reflows assert_eq! lines, so re-fetch a file before anchoring an edit on it.
- (after the handoff) OPS-2 landed the keybroker unit at 11a9c97: deploy/units/linux/nd-keybroker.service, rendered
  from the BrokerExit tables. Prevent = 70 71 72 73 75 76 78 80-100 103 104; 74/77/102 and a 101 panic restart.
  EXITS.md holds an operator sentence per end, so a NEW BrokerExit end needs its EXITS.md arm (cross-layer,
  pre-agreed with OPS). Its sockets are 0600 under UMask=0077 in /run/nd-keybroker/sock, so only `nd` can connect.
  Stage 3 owes OPS-2: the uid/group grains connect as, and where SOCKDIR must sit; OPS-2 re-renders. Not yet run
  under systemd on any box.
  OPS-2 residue: the ExecStartPre `emit-anchors --check` failure is NOT covered by RestartPreventExitStatus, so a bad
  installed anchors file retries until the start limit (5 in 120 s), named in the journal each time. Running the unit
  under systemd is OPS-3's (burst5-a is still up; one window, after INTEGRATOR-6 and Ember agree; OPS-LOG ## OPS-3).

## HOSTING-6 (a6d3ac11df77ce1c5, from 2026-10-18)
Scratch: Mac .../b3795e84-.../scratchpad/hosting-lane/h6/ ; hbox logs/hosting6-* .
- HOSTING-17 DRAFTED (wt/hosting decisions/hosting.md, uncommitted; copy hbox logs/hosting6-h17.md): two uids
  (nd = host serve + keybroker; NEW nd-hosted = grain-launch, controller, grains); SOCKDIR /run/nd-broker (tmpfiles
  `d /run/nd-broker 2710 nd nd-hosted -`, NOT RuntimeDirectory); socket SOCKDIR/<dirOf id>/broker.sock 0660
  nd:nd-hosted, per-resident dir 02710 (the sandbox binds the DIR so a broker restart needs no relaunch);
  keybroker `sockDir` exit + SO_PEERCRED gid check → wire `peerRefused` (code 20); Policy.connect rule (euid+0600
  OR other-owner+group=egid+0660; ConnectNotSocket/Link/Mode/Owner, Dir). Asked ROOT (custody: widens connect
  nd → group nd-hosted). FOR OPS-3: §7 of HOSTING-17 is the unit change list. Open for OPS/HOST: controller's Store
  read as nd-hosted (recommend a host follow as nd-hosted).
- PROTOCOL-7 ab1b7e29205360b2c sent a resident-row NEED; I returned it amended (R1..R6 + plants a..d). On its
  "agreed" I send it to CLIENT-3. RESIDENTS-from-World = HOSTING-18 (after the first resident row).
- HOST-9: HOST-33 landed ff60a08 (re-geneses every Store; broker.rs makes fresh Stores per run, so unaffected).
  HOST-9 queued "readKey on a missing key file = named StoreFault" as its next item. WHEN THAT LANDS,
  launcher/tests/broker.rs's pass-through case (empty STORE) will end `store` (76), not `io` (78): flip
  `decider_exit::IO` to `decider_exit::STORE` and its comment in the same commit (HOST-9 is told to cross-layer it or ping you).
- ROOT APPROVED HOSTING-17 with 5 conditions (peer uid+gid; residue + cv 01a14aad-fc83 per-grain uids; StrictModes
  check of SOCKDIR + each <r>; connectMax=2; controller on its own nd-hosted follower Store) + §8 placement (CLIENT-20).
  LANDED 62b346d (HOSTING-17), bcf1d67 (§8), 5561a3a (LaunchFailure +9 connect cases 8-16, generated.rs re-emit,
  CODEC-6 agreed; CODEC-6 also agreed I carry emit-broker).
- IN FLIGHT (wt/hosting, uncommitted, built green): BrokerWire peerRefused=20, BrokerExit sockDir=105, Ops/Units
  (sockDir EXITS arm; argv +${ND_PEER}, SOCKDIR /run/nd-broker, RuntimeDirectory nd-keybroker only: ROOT YES, flag
  `--cross-layer "Ops/Units.lean: nd-keybroker argv gains ${ND_PEER}, SOCKDIR /run/nd-broker, RuntimeDirectory
  nd-keybroker (OPS-2's standing agreement; OPS-3 informed)"`), deploy/units + broker_generated.rs re-emitted.
  Rust drafts: hbox logs/hosting6-kb.rs (keybroker: PEER argv, socket_paths, bind 0660, peer_cred check) and
  logs/hosting6-br.rs (broker.rs: rendered-argv helper from the emitted unit = ROOT condition; sockdir test; peer
  test). BLOCKED on CLIENT-3's custody::check_shared_dir + custody::peer_cred + Policy.connect (same commit).
  OPS-3 spawned by ROOT with §7; RUNBOOK §2a still names /run/nd-keybroker/sock (OPS-3's).
- LANDED 45b1394 (keybroker HOSTING-17 half: PEER argv, SOCKDIR/<r>/broker.sock 0660, sockDir 105, peerRefused 20,
  broker test runs keybroker from the RENDERED unit argv = ROOT's condition; Ops/Units argv carried cross-layer,
  ROOT yes) and fe3f83d (resident plan: Plan.connect, connectOf, residentUnsupported DELETED, launch frame connect,
  grain-launch ROOT BROKER LABEL PIDS CONTROLLER + rootsOverlap; plan_connect_own/disjoint/clean,
  planned_resident_encodes; isolation.rs a_resident_reaches_its_own_broker_socket_and_nothing_else = reader H4's
  hole 1; hole 2 = cv 01a14ad0-ae99 HOSTING-18). CLIENT-3 landed Policy.connect + check_shared_dir + peer_cred 64c89e0.
- ROOT ruled the hosted follower (B): host.sock stays nd-only; hosted follower socket under setgid
  /run/nd-follow/<id>/ (02710 nd-hosted:nd), nd-supervise 0660 (CLIENT-3 adds), client nd (as nd) drives it.
  Principle "the trusted side initiates to the less-trusted side" — written into HOSTING-17 §7 in the HOSTING-19 commit.

### FOR HOSTING-7 (successor) — written by HOSTING-6 at ~390K, 2026-10-18
LANDED 8be4026 (nothing in flight; wt/hosting clean apart from untracked-nothing): HOSTING-19 grain-launch/controller
exit tables — Hosting/LaunchExit.lean (ControllerExit 0,106-115; LaunchExit 116-127, all < 128), Proofs/LaunchExit,
Cli Exit.kind, Emit/Hosting emits launch_exit/controller_exit, generated.rs re-emitted, grain-launch main maps ends
(controller pass-through, ≥128 → controllerSignaled), isolation test grain_launch_exits_..., gates/runs.tsv
isolation row + hosting-controller, decisions HOSTING-19 + §7 follower addendum. Vacuity read asked of
ad64d8383bcb4c821. If HOSTING-6 did not land it, land it: paths Emit/Hosting.lean Hosting/Cli.lean
Hosting/LaunchExit.lean Hosting/Proofs/LaunchExit.lean launcher/src/bin/grain-launch.rs launcher/src/generated.rs
launcher/tests/isolation.rs gates/runs.tsv decisions/hosting.md; --cross-layer for generated.rs (CODEC-6/7
standing agreement for unedited emit-hosting) and Emit/Hosting.lean (CODEC's: needs CODEC-7 a96227257cb8e3c92's yes
— ASK FIRST); SIZE lines for every risen metric. Then send OPS-3 a63176c79bbcb74dc the sha (it renders
nd-grain-launch@ from codesOf).
NEXT, in order:
1. The resident ROW `cargo:launcher:resident` (PROTOCOL-7 ab1b7e29205360b2c agreed the need: R1..R6 + plants a..e,
   see the amended need in this session's messages; PROTOCOL-7 reviews the test). Real Store as broker.rs
   (World::genesis — factor broker.rs helpers into launcher/tests/common/), install world/grain/Lifecycle +
   world/hosting/Allowance, create a grain `(record (entry "probe") (kind resident) (phase installed))`, allowance
   resident #<grain id hex>, invoke start; keybroker with RESIDENTS = dirOf id (64 hex), SOCKDIR = a SHORT scratch
   (sun_path: SOCKDIR ≤ 30 bytes; isolation.rs uses `i<pid base36>`), PEER = uid; grain-launch over the real
   hosting-controller; the probe (launcher/src/bin/probe.rs: ops read/write/connect/list) must also be able to ASK
   (an Ask frame over the socket) — extend it. R1: assert the launch's connect path from grain-launch/controller
   output, not computed in Rust (consider a grain-launch stderr line per launch naming its connect paths).
   Plant (d): restart keybroker mid-row (by its PID file), ask again: granted (the directory bind).
2. The grain row's physical half `cargo:launcher:grain` (PROTOCOL-7 agreed): real Store, create + invoke start,
   process under the planned policy, operator stop ends it, grantee stop refused grantRight and the process lives;
   plant: a controller ignoring stop is red at the stop step.
3. HOSTING-18 (cv 01a14ad0-ae99): keybroker's sockets from the World; delete RESIDENTS.
4. cv 01a14a8a-ffa6 (open_world_canon satisfiability witness), cv 01a14a7d-55c3 (SPKI pins, tlsPin, plant).
5. CLIENT-3 aae5c92a4d1999133 builds `nd --stdio` when told its shape (for the full two-process resident).
Agents: ROOT main; OPS-3 a63176c79bbcb74dc; CLIENT-3 aae5c92a4d1999133; PROTOCOL-7 ab1b7e29205360b2c; CODEC-7
a96227257cb8e3c92 (CODEC-6 a7dcb3be86813ca52 agreed the emit carries); LANG-11 ac74cc733b391d27a (digest lang! day
re-emits world/grain/Lifecycle + Allowance, type-only edits to Hosting under cross-layer; I said keep resident/entry
bytes); HOST-10 a466e00c707f4b7be; VACUITY-READER-H4 ad64d8383bcb4c821 (context on HOSTING-13..19).
cv: 01a14aad-fc83 per-grain uids (trigger: first multi-principal deployment); 01a14ad0-ae99 HOSTING-18.
Hygiene: python edit scripts with quotes/apostrophes MUST be scp'd (an ssh heredoc broke twice). Plant scripts:
hbox logs/hosting6-plants.py (keybroker), -rplants.py (resident), -lplants.py (plan Lean), -lep.py (exits).
- HOSTING-19 LANDED 8be4026 after reader H4's holes: (1) reportPipe masked a fatal controller end -> fixed (bounded
  wait, pass-through), test via hosting-drive --exit-after-launch (109), but the plant (wait removed) stayed green 3/3:
  review-guarded, stated; (2) the <128 guard unexercised, stated. CODEC-7 agreed Emit/Hosting. OPS-3 has the sha.
  HOSTING-6 stopped at ~410K with nothing in flight.
- (after stop) LANG-11 landed 1b831da (digest lang! day): world/grain/Lifecycle + world/hosting/Allowance re-emitted,
  package ids changed; type-only edits to Hosting/Proofs/Allowance (seed_state over digestOf) and Proofs/Package;
  hosting-sim ALL PASS. HOST-10 a466e00c707f4b7be has my yes for `.store f.name` → `.store f.text` in BrokerCli/Cli
  (HOST-35) on condition it flips broker.rs's empty-store expectation IO → STORE and runs both launcher rows.
  Tests install packages from the texts, so no hard-coded ids to chase; check after rebasing.

## HOSTING-7 (spawned by ROOT 2026-10-18; CLIENT-LOG names it a8d9d17a1910bbe3b)
Scratch: Mac .../b3795e84-.../scratchpad/hosting-lane/h7/new/ (my edited copies, the source of truth for the uploads);
hbox logs/hosting7-rplants.py (+ .out): plants a-f.
- Resident need text: hbox logs/protocol7-resident-need.md (Mac redregg/work/RESIDENT-ROW-NEED.md).
- ROOT RULED HOSTING-20 (nd --stdio member socket): nd --stdio as nd under nd-supervise --group nd-hosted --peer UID,
  member ws worlds/<l>/members/<dirOf>, /run/nd-member/<dirOf>/nd.sock 0660 in 02710 nd:nd-hosted, TYPED MEMBER root
  (grain-launch ROOT BROKER MEMBER, rootsOverlap pairwise), confined (write member ws, connect host.sock+follow).
  Surface: STDIO_VERBS (PROTOCOL-7 emits) else notOnSurface; noRotation; argv only. NO `install <path` form exists
  (corrected). CLIENT-3 builds it, sends sha. THEN HOSTING owes: Plan typed connect roots, grain-launch MEMBER arg,
  re-emit, row second socket.
- BUILT, green, in wt/hosting (uncommitted, at main e285406): HOSTING-21 resident row (resident.rs, common/mod.rs,
  probe ask/wait, grain-launch connect line, keybroker 0600 when PEER==own uid (ROOT ok), runs.tsv row, broker.rs on
  common). Plants a-f all red. Sent to PROTOCOL-7 for review and VACUITY-READER-H4 for a read. Land after both.
- Facts learned: the follow Store only advances when nd drives it (`nd sync` after each invoke); plans HIDE
  worlds/<l>/members, so it must exist or every launch is pathMissing → crashLoop.
- LANDED b3c3d67 (ETXTBSY flake: place_exe via `cp`, stress test, plant red 3/3), 113537f (HOSTING-21 resident row),
  c2019b9 (HOSTING-22 grain row; PROTOCOL-7 cross-ref 1db64e8). PROTOCOL-7 retired-ish (~370K, PROTOCOL-8 next).
- BUILT, green, wt/hosting uncommitted: HOSTING-23 (deciderMechanism 79 / controllerMechanism 67: pass through only
  codes in emitted ALL; byteModule emits ALL for every table, CODEC-7 agreed) + HOSTING-24 (layoutHidden +
  plan_hidden_layout, LAYOUT_HIDDEN, grain-launch layoutMissing 68). Patch hbox logs/hosting7-mech.patch, msg
  logs/hosting7-msg3.txt. Waiting OPS-3 yes + reader H4. Paths: Emit/Rust.lean Emit/Hosting.lean Hosting/BrokerExit.lean
  Hosting/LaunchExit.lean Hosting/Plan.lean Hosting/Proofs/Plan.lean Ops/Units.lean client/src/generated.rs
  deploy/units/{EXITS.md,linux/nd-grain-launch@.service,linux/nd-keybroker.service} launcher/src/bin/{grain-launch,keybroker}.rs
  launcher/src/{generated,broker_generated}.rs launcher/tests/{broker,isolation}.rs launcher/tests/common/mod.rs
  decisions/hosting.md. Cross-layer: Emit/* + generated (CODEC-7), Ops/Units + deploy/units (OPS-3), client/src/generated.rs.
- LESSON: an unquoted heredoc inside ssh '...' runs backticks (mangled a Lean comment). scp scripts.
- NEXT after that: HOSTING-18 (RESIDENTS from World), MEMBER root after CLIENT-3's nd --stdio, canon witness, SPKI pins.
- LANDED a487504 HOSTING-23/24 (deciderMechanism 79, controllerMechanism 67, layoutMissing 68; byteModule ALL;
  LAYOUT_HIDDEN + plan_hidden_layout; ≥128 = signaled, reader H4's hole fixed). OPS-3 told (fixes its live rows N/O).

### FOR HOSTING-8 (successor) — written by HOSTING-7, 2026-10-18
main has HOSTING through a487504; wt/hosting clean (git checkout --detach main before editing). Nothing in flight.
Landed by HOSTING-7: b3c3d67 (ETXTBSY), 113537f (HOSTING-21 resident row + keybroker 0600-when-PEER-is-own + HOSTING-20
ROOT ruling recorded), c2019b9 (HOSTING-22 grain row), a487504 (HOSTING-23/24).
Harness: launcher/tests/common/mod.rs holds World (genesis_following = follower Store at a path; follower() = a
member's own follower Store; install; allowance; grant/genesis_args), keybroker argv from the unit (argv/argv_with,
start_residents), grain_launch_rendered (from nd-grain-launch@.service), Logged (stderr collector + PID file),
Short/Gone scratch guards, until (deadline = hang), place_exe (cp: never fs::copy an exe you then run), verdicts.
Probe ops: read write connect list ask wait (appends per line; probe.recv = bytes received).
Facts: the follower Store moves only when nd drives it (`nd sync` after each invoke); worlds/<l>/members must exist
(now layoutMissing at start). Plant script: hbox logs/hosting7-rplants.py (env PLANT_OUT, PLANT_TESTS; plants a-h, m1-m5).
NEXT, in order:
1. HOSTING-18 (cv 01a14ad0-ae99). FINDING (read, not yet a decision): the Lean side is ALREADY consistent — the
   decider names each allowance by Controller.dirOf(resident) (Allowance.allowanceOf) and compares it with the
   socket name keybroker puts in the decide frame; plans connect to dirOf(grain id). So the residual is that
   RESIDENTS (operator argv) is a second copy of a World fact: a resident grain not listed has no socket (its launch
   is pathMissing → crashLoop), and a listed name that is no resident grain gets a socket nobody may connect to.
   Right design (delete RESIDENTS, CLAUDE.md "prefer deleting"): the decider computes the resident set from the World
   (lifecycle objects of kind resident, dirOf of id) and keybroker binds/unbinds from it. Hard part: the socket must
   exist BEFORE the controller's launch resolves Policy.connect (else pathMissing, then crashLoop within 5 fast
   relaunches). Options to weigh: (a) the decider pushes resident-set frames on catch-up (keybroker reads decider
   stdout on its own thread; today it is request/response under one Mutex); (b) keybroker binds on a grain's BIRTH
   (installed) so the start Turn comes later — still racy for create+start back-to-back; (c) the controller refuses
   to launch a resident whose allowance… (it cannot see sockets). Argue in decisions/hosting.md, ask ROOT if it
   changes who may connect (it does not widen: same per-resident sockets). Ops/Units drops ${ND_RESIDENTS} (OPS).
2. MEMBER root (HOSTING-20) after CLIENT-3 lands nd --stdio (+ nd-supervise --peer): Plan typed connect roots,
   grain-launch ROOT BROKER MEMBER, pairwise rootsOverlap, re-emit, resident row's second socket.
3. cv 01a14a8a-ffa6 (open_world_canon satisfiability witness), cv 01a14a7d-55c3 (SPKI pins, tlsPin, plant).
Agents: ROOT main; OPS-3 a63176c79bbcb74dc; CLIENT-3 aae5c92a4d1999133; CODEC-7 a96227257cb8e3c92; LANG-12
aa6fec46b5067cd28; PROTOCOL-7 ab1b7e29205360b2c (~370K, PROTOCOL-8 next); VACUITY-READER-H4 ad64d8383bcb4c821 (at
~350K; found the ≥128 hole — a fresh reader may be needed).
- LANDED d7c9d95: broker.rs peer test's CONTROL has its own upstream (HOST-11 found a window-boundary race: the control's ask could be granted and reach the refused peers' shared upstream). Plant p-peer-unchecked red.

## HOSTING-8 (aa823e7641b7b6082, from 2026-10-19 11:31Z)
Scratch: Mac .../777a29c9-.../scratchpad/h8/ (edited copies, msg25.txt, hosting8-plants.py); h8b/ (HOSTING-26 drafts).
hbox logs/hosting8-* (plants hosting8-plants.py [names as argv], .out; commit logs; patches h25*.patch);
lane cargo target logs/hosting8-target (its tmp/ iso-* are mine to clear).
- LANG-16 a528bfa435823b2e1 landed the resident's package world/resident/Bell(.ob) at 00c9e20 (state only:
  answer open pending resident ring ringer = slots 0..5; methods answer 0 close 1 open 2 ring 3; law bell).
  ROOT RULED PROTOCOL-48 (option b): `read OBJ` prints a programmed object's state through Lang.Print, routed
  to PROTOCOL-13 a8b9027b0e85da990 (LANG-16 reviews). Until it lands HOSTING-27 gates only on the raw pending slot.
- LANDED b9cd50f HOSTING-25: typed plan socket fields broker/member (connect deleted), memberOf = [<id>, nd.sock]
  under MEMBER root; grain-launch ROOT BROKER MEMBER LABEL PIDS CONTROLLER; pairwise rootsOverlap; foreignPath 69
  (frame path/socket not the grain's own); Proofs: plan_sockets_*, grainOf_named, launch_named,
  reconcile_launch_named (VACUITY-READER-H8 a496ca6a7ba681a8b found the grainOf hole). Resident row: World::member
  (nd --init-hosted, enroll, observe grant, follower, nd-supervise nd --stdio 0600 one-uid), probe `nd` op
  (client frame code; launcher now depends on nanodregg-client). GATES-6's leak fix (Tree Drop) inside.
  World serves host.sock at run/host.sock (alone in its dir). OPS-5 a5d4126a74c378ee7 owes RUNBOOK §2b,
  deploy/live/broker.sh $R/member, and the per-resident member unit (shape sent).
- Facts: hbox wt .lake must have `host` rebuilt after main moves (a stale host answers badPackage on install);
  nd-supervise refuses a child with nothing hidden (CLIENT-8); a connect grant exposes the socket's whole dir.
- NEXT: HOSTING-26 (ruled (A)): delete ND_RESIDENTS; Track.update generic (Allowance + residents), decider
  reports the resident set (lifecycle cells kind resident, phase ≠ removed, dirOf) on a `residents` request;
  keybroker polls each tick, binds new / unbinds removed; decide refuses `notResident` for a name not in the set;
  theorem: every launch's broker socket is in the set (with tracking exactness); race (start before keybroker
  learns birth → pathMissing) named + planted; DeciderExit for > residentsMax; Ops/Units drops ${ND_RESIDENTS}.
- LANDED 43ab42a HOSTING-26 (reader H8b ACCEPT on its 2nd pass after 4 holes; plants q1-q7, r1, r2 red): Track.lean (generic
  follower), Controller.residentOf, BrokerWire residents request/verdict + notResident 21 + residentsMax 1024,
  Broker.admit, DeciderExit residentsPastBound 7, BrokerCli follows grains, keybroker polls every 200 ms and
  binds/unbinds; proofs launch_served/launch_resident/residents_encode/admit_*; plants q1-q7 red
  (logs/hosting8-plants26.py/.out); tests: broker.rs sockets_follow_the_worlds_resident_grains, World::r1/r2
  real resident grains, short_dir SOCKDIR, resident.rs race plant (keybroker down → `<c> failed pathMissing`).
  OPS-5 AGREED the Ops/Units edits (argv w/o ND_RESIDENTS, residentsPastBound sentence); OPS-5 lands the
  RUNBOOK keybroker.env sentence after the hash. Decision draft: Mac scratch h8b/h26.md (append to decisions).
  Vacuity reader VACUITY-READER-H8b af1b467d6e38c73d5.

### FOR HOSTING-9 (successor) — written by HOSTING-8 at ~540K (past the 350K mark; stopped after HOSTING-26)
State: main has HOSTING through 43ab42a (HOSTING-26); wt/hosting clean apart from what scripts/commit moved. PROTOCOL-48 LANDED
7932cb3: `read OBJ` on a programmed object prints ONE line, the state through Lang.Print.data
(`(record (answer "...") (open true) (pending false) (resident #…) (ring "...") (ringer #…))`).
`read OBJ I=V` still compares raw slot bytes (V an argv word: the data encoding; bool true = byte 0x01).
1. HOSTING-27, the REAL resident (THE BAR's "hosted Hermes" IS this process; say so). Design points found:
   - A new bin (launcher crate, `resident`), run as pkg/resident under grain-launch, no argv/env (sandbox
     clears both): it reads a config file beside itself (pkg/resident.conf: `object HEX`, `broker PATH`,
     `member PATH`, `model NAME`, `ticks N`), written by the operator with the package. Sockets are the
     plan's (BROKER/<g>/broker.sock, MEMBER/<g>/nd.sock), the same absolute paths inside bwrap.
   - Loop with bounded ticks (sleep between, no wall-clock verdict): `read OBJ ?` once → method indices by
     LABEL (answer, ring) from `method I LABEL ARGTYPE` lines (never hard-coded); each tick `read OBJ`;
     act only when pending (gate: `read OBJ 2=\x01`-style expectation, raw slot, or the printed line).
   - TWIN TRAPS, unresolved, decide before coding: (a) reading the ring text out of the printed record
     line in Rust is a reader of Lang's text; (b) writing `(record (text "…"))` needs Lang string escaping;
     (c) extracting the model's reply from the provider's JSON body is a JSON parser. Options weighed:
     pass the whole printed state line to the model as context (no parse); restrict the written reply to a
     charset needing no escaping (documented filter); and have the LEAN broker extract the reply text
     (Broker has a proven Json.str/unstr) so keybroker's Answer carries text, not the provider body — that is
     a HOSTING-12/15 wire change (CODEC re-emit) and the cleanest; propose it as part of HOSTING-27/28 to ROOT.
   - Package: world/resident/Bell.ob (LANG-16, 00c9e20): slots answer0 open1 pending2 resident3 ring4 ringer5;
     methods answer0 close1 open2 ring3; law bell (birth not rung; invoke never changes resident).
     The resident's member = World::member (HOSTING-25 harness); operator grants it invoke:<answer> + observe
     on the bell; a ringer member rings.
   - Test: cargo row (resident.rs or its own resident_bell.rs): real host, fake upstream answering an
     Anthropic-shaped body; mutations: resident writes without a grant (noGrant), writes another object
     (refused), calls the broker without the fence (connect outside plan → ENOENT), plus a canary.
2. HOSTING-28 PROPOSED (design only; ROOT rules; Ember supplies the key): the provider's SPKI pin (sha256 of
   SubjectPublicKeyInfo) as a build-time Lean constant in Broker.providers (per provider, a SET to allow
   rotation), carried in the grant frame or emitted as a Rust const; keybroker checks the leaf (or chain)
   SPKI after rustls verification; mismatch → new refusal `pinMismatch`; plant: a CA-valid cert with another
   key → pinMismatch; control: the pinned test key passes. cv 01a14a7d-55c3. Before ANY real key.
3. Member socket ordering (OPS-5 asked): proposal = one long-lived nd-side server per World that binds each
   resident's member socket from the World (like keybroker now), replacing per-resident nd-member@ units;
   OPS-5 deletes nd-member@ if adopted. Needs CLIENT (nd-supervise multi-socket or a new small server) — a
   decision with CLIENT/ROOT.
Agents: ROOT main; OPS-5 a5d4126a74c378ee7; LANG-16 a528bfa435823b2e1; PROTOCOL-13 a8b9027b0e85da990;
GATES-6 a55f38eda9d00894a; readers VACUITY-READER-H8 a496ca6a7ba681a8b, -H8b af1b467d6e38c73d5.
Hygiene: rebuild `host` in wt/.lake after main moves (stale host → badPackage); nd-supervise needs a --hide;
Short/short_dir for every socket root (≤30 bytes); dir(name) needs a letter in common::dir's table.
- LANG-16 (after LANG-56 4e81a85): Lang.Print shows a byte string as "text" only when every char is plain,
  else #hex; read the Bell line with Lang.Read.readData at the state type — never split by hand. For the
  Rust resident that means: get the Lean side to decode (a Lean resident-helper exe, or the broker), or a
  documented charset filter on what is written; do not write a Rust reader of Lang text.
- HOST-13 a55e9ab90683e7922 has my yes for a one-arm edit to Proofs/Allowance stepTurns_fold (HOST-49).
- HOSTING-8 STOPPED at ~575K after HOSTING-26 (nothing in flight). HOSTING-27/28 not started: see FOR HOSTING-9.
- (after stop) OPS-5 c32a36a: RUNBOOK §2a for HOSTING-26. KNOWN RED: deploy/live/broker.sh row G waits for
  $R/broker/01/broker.sock, which no longer exists (keybroker serves only resident grains the Store holds, and
  live-calls' genesis makes none). Fix: live-calls creates a resident grain; broker.sh derives $sock from its
  dirOf. Needs a box window; OPS-5 offered to ROOT. A box-run harness, not a standing row.

## HOSTING-9 (spawned by ROOT 2026-10-19; successor of HOSTING-8)
Scratch: Mac .../777a29c9-.../scratchpad/h9/ (edited copies, h2829.md decision, msg2829.txt, hosting9-plants.py).
hbox logs/hosting9-* (plants .out/-l6/2/3, commit logs, msg); lane cargo target still logs/hosting8-target.
- ROOT RULINGS 10-19: HOSTING-28 = P2 (pins operator DATA like ANCHORS, LEAF SPKI only, production file emitted from
  Lean + gated, EMPTY, fail closed, never handshake the provider; anchors narrowed same day). HOSTING-27 socket C:
  YES (Host/c/sock.c + Host/Sock.lean, HOST-13 agreed with conditions: connect honours timeout, EINTR retried,
  read max=0 refused, sun_path length refused by name, MSG_NOSIGNAL, tcb row, HOST-numbered decision in
  decisions/host.md co-signed by HOST-13, show HOST-13 the diff first). grain-launch passes plan paths as argv
  (theorem or reordering plant). No IO.appPath. resident.conf = ONE Lang data value read by Lang.Read.readData.
- HOSTING-29 + 28 built (one hosting!): Hosting/Reply.lean (JSON reply reader over ByteArray+index, law 3 — a
  List UInt8 draft was refused by gates/refusals.py; C3 refuses public defs in proof modules), Proofs.Broker
  reply_printed + unstr_str over the deployed reader, Proofs/Reply teeth; keybroker PINS + leaf_pin + reply
  round trip; emit-anchors 7 of 121 roots (crt.sh provenance); emit-pins + deploy/tls/pins (empty);
  KeybrokerExit pins 140-148 (106-115 are ControllerExit's: Proofs.LaunchExit caught it). VACUITY-READER-H9
  (a5c8d1b61469c30bc) ACCEPT after 9 holes closed. OPS-5 + GATES-6 agreed the cross-layer paths. First judge
  RED (C3, List UInt8, LaunchExit code clash) — fixed. GATES-6's broker flake (interleaved stderr) fixed in it.
- HOSTING-30 PROPOSED written: /Users/ember/dev/redregg/work/HOSTING-30-MEMBER-SERVER.md (CLIENT need §4;
  open question: per-member follower vs one shared follower).
- LANDED 9df02da HOSTING-29 + HOSTING-28 (pre-push GREEN after three RED judges: C3/List UInt8/LaunchExit clash, then a set_option linter override and the renamed tooling SIZE metric; main moved twice — logs/hosting9-land.sh carries the edits onto main and execs scripts/commit in one step). Pins exits are 140-148. Plants final: logs/hosting9-plants3.out (+plants4); l2 deleted as a plant because field's duplicate filter was dead once members refuses repeats everywhere (field is now find?).

### FOR HOSTING-10 (successor) — written by HOSTING-9 at ~480K (past the 350K mark; stopped after 9df02da)
State: HOSTING-28+29 landed 9df02da. HOSTING-27 NOT started in code; every ruling for it is in hand:
1. HOSTING-27, the REAL resident (THE BAR's "hosted Hermes" IS this process; say so in the decision). ROOT-ruled shape:
   - a `lean_exe resident` (Hosting/Resident/*.lean, own cone; root module holds only main, C7; lakefile + runs.tsv rows
     need GATES-6's yes — they gave the same for emit-pins in minutes).
   - SOCKETS: Host/c/sock.c + Host/Sock.lean (HOST-13 a55e9ab90683e7922 AGREED with conditions — quote them: externs in
     Host/Sock.lean; connect honours the timeout (non-blocking connect + poll, or a documented AF_UNIX note); read
     timeout = the named error "timeout"; EINTR retried, never reported; nd_conn_read refuses max=0 so empty = EOF only;
     path length checked against sun_path, overlong refused BY NAME before copying; MSG_NOSIGNAL (never SIGPIPE);
     gates/tcb.tsv row; contracts tested by name: EOF, timeout, overlong path, peer closing mid-write; the decision is a
     HOST-numbered entry in decisions/host.md, co-signed HOST-13, saying Host's serve may adopt it later; SHOW HOST-13
     THE DIFF before landing). Also: gates/native-allow.tsv row for Host.Sock, and SIZE-CEILING lines for
     `native (extern/implemented_by)` (9) and `C lines` (159), both at their ceilings now.
   - NO IO.appPath (absent under bwrap). grain-launch passes the plan's paths as argv, field for field (read dirs, write
     dirs, broker sockets, member sockets, each joined onto its root) — ROOT wants a theorem or a reordering plant
     refused. The rest of the config is ONE Lang data value in pkg/resident.conf read by Lang.Read.readData at a fixed
     record type (bell object, model, maxTokens, system text).
   - Loop: `read OBJ ?` once → method index of `answer` by label (Protocol's describe reader, never hard-coded);
     each tick `read OBJ` → the ONE printed line → Lang.Read.readData at the state row → pending? ring text →
     Wire.encodeAsk (one message, the ring text) on the broker socket → Wire.decodeAnswer → `invoke OBJ <answer>
     (record (text "…"))` printed by Lang.Print.data at the arg type. Bell needs text 1..2000 bytes: truncate at a UTF-8
     boundary; an empty reply / a refusal / a status → answer a fixed short text naming it (e.g. `(refused overSpend)`)
     so a pending ring is answered exactly once and never re-asked (each ask costs the meter). Member frames: Protocol
     commandLayout/commandReplyLayout + the frame header (probe.rs's `nd` op is the Rust picture of the wire).
   - Test (cargo:launcher:resident or a new resident_bell.rs): real host, World::member as the resident, a ringer
     member, the Bell package (world/resident/Bell.ob) installed and an object created with resident = the resident's
     member; fake upstream answering ANTHROPIC_BODY-style; founder rings, resident answers, founder reads. Mutations:
     answering when not pending (unrung), as a non-resident (notResident), writing another object (noGrant), asking
     the broker off its fence (ENOENT). Real upstream only after Ember supplies a key (never in a test).
2. HOSTING-30 PROPOSED is written: /Users/ember/dev/redregg/work/HOSTING-30-MEMBER-SERVER.md (sent to ROOT). Waiting on
   CLIENT-8 for the follow question (per-member follower vs shared). OPS-5 knows nd-member@ stays until then.
3. OPS-5 a5d4126a74c378ee7 owes, after the 28/29 hash: broker.sh installs $R/etc/pins (empty), RUNBOOK §2a (pins, rotation
   recipe, pinMismatch 23, narrowed anchors, reply shape) — text from decisions/hosting.md HOSTING-28/29.
Facts learned: gates/refusals.py refuses `List UInt8` in def-modules (law 3) and set_option maxHeartbeats; closure C3
refuses public defs in proof modules; ControllerExit owns 106-115, KeybrokerExit pins 140-148 (Proofs.LaunchExit checks keybroker codes against
it); after main moves, rebuild hosting-controller/-drive/-broker AND host in wt/.lake (stale = shapeMismatch / badPackage);
`ssh hbox 'nohup …&'` needs `< /dev/null` or ssh hangs; the kernel reduces the ByteArray reader fine (teeth ~seconds).
Readers: VACUITY-READER-H9 a5c8d1b61469c30bc (knows Reply.lean). Agents: ROOT main; HOST-13; OPS-5; GATES-6 a55f38eda9d00894a.

## HOSTING-10 (spawned by ROOT 2026-10-19; successor of HOSTING-9)
Scratch: Mac .../777a29c9-.../scratchpad/h10/ (edited copies; host52.md = HOST-52 draft). hbox logs/hosting10-* (patch, sock log,
helper .py). Cargo target: logs/hosting8-target.
- Landing 1 (host:, HOST-52) STAGED, uncommitted in wt/hosting: Host/c/sock.c (145 lines; nd_unix_connect / nd_conn_write_all /
  nd_conn_read; poll + CLOCK_MONOTONIC deadline per call; named errors timeout pathNul pathTooLong readMaxZero readMaxPastBound),
  Host/Sock.lean (+ Conn.stream : IO.FS.Stream so Host.readExact reads a socket), Host/Sim/Sock(+Main) = host-sock-probe,
  launcher/tests/sock.rs = cargo:launcher:sock GREEN (EOF, timeout, max0, overlong, mid-write EPIPE, absent, full backlog, echo control);
  file.c io_errno → shared nd_io_errno; gate rows (tcb, native-allow, runs x2), ceilings native 12 / C lines 304; rustix dev-dep.
  HOST-14 a4d3aa9099adf145c reading it (ROOT added: backlog plant — done; EINTR: stated reason, no handler in these exes).
- CLIENT-8 a4b5ab24321e18c7e: I said YES to nd-members in launcher/ (residents.rs, bin/nd-members.rs, tests/members.rs, lib.rs
  `pub mod residents;`, Cargo.toml bin + rustix process, MembersExit 150-159 in Hosting/BrokerExit.lean + proofs). ROOT ruled (A):
  one follower per resident; MEMBERS/<name>/follow one-line 0600 file — the resident row/RUNBOOK adopt it when it lands.
- LANDED da0593e HOST-52 (host:, Host.Sock; HOST-14 LAND after F1-F6; 6 attempts lost to CAS races / behind-main;
  logs/hosting10-reland1.sh = carry-and-exec helper). HOST-14 measured: Lean runtime ignores SIGPIPE, catches 7/11/33.
- Landing 2 (hosting!, HOSTING-27) launched via logs/hosting10-reland2.sh (log hosting10-commit2.log). Resident:
  Hosting/Resident/{Args,Bell,Sockets,Run,Main}.lean + Proofs/Resident.lean (15+ theorems), plan_argv in launcher,
  row cargo:launcher:resident_bell GREEN. Facts learned: invoke needs `--via GRANT` (conf field grant); a grant
  lacking the right is `grantRight`, not noGrant; nd --stdio renders every method-check refusal as `refused program`
  (PROTOCOL-15 took it: cv 01a15039-0a62), so deliver judges refusals by re-reading the bell's state.
  VACUITY-READER-H10 a03299b1d149d4bc2 (2 passes; knows Run.lean). PERF-2 told: one round = ring + answer = 2 writes.
- LANDED 0e4d57f HOSTING-27 (hosting!, 2 attempts). decisions/hosting.md HOSTING-27 has critique + meta-critique + the
  reader's verdicts. wt/hosting is clean apart from what scripts/commit moved.

### FOR HOSTING-11 (successor) — written by HOSTING-10, 2026-10-19
State: main has HOST-52 (da0593e) + HOSTING-27 (0e4d57f). Nothing in flight.
Open, in order:
1. HOSTING-30 (per-World member server): CLIENT-8 a4b5ab24321e18c7e is building nd-members in launcher/ (my YES; MembersExit
   150-159). ROOT ruled (A): one follower per resident, MEMBERS/<name>/follow 0600 file. When it lands, move
   cargo:launcher:resident(_bell) onto nd-members and drop World::member's per-test nd-supervise.
2. HOSTING-27 critique items: a theorem over Run.tick's effect order (intent keep -> ask -> answer keep -> deliver);
   a ring nonce in Bell's state (LANG) for a true ring identity; when PROTOCOL's cv 01a15039-0a62 lands
   (`refused program REASON`), log/name the reason in deliver (still judge by state).
3. THE BAR v2 (PERF-2 a4fa91de1b873e3bf): round = ring + answer (2 writes), tick 1 s; a shorter tick or a
   notification is a HOSTING change if PERF asks.
Facts: invoke needs --via GRANT; grant without the right = grantRight; Lean runtime ignores SIGPIPE and catches 7/11/33;
scripts/commit races: use a carry-and-exec helper (logs/hosting10-reland{1,2}.sh) and nohup it as its own command
(not inside a && chain, or ssh hangs). GATES-18: a CROSS-LAYER reason must name each foreign path's owner layer.
4. LANG-58 (coming from LANG-18): the Bell becomes a queue of rings (cv 01a14ece-43f1; relation `rings` keyed n). I told
   LANG-17 what the resident needs: answer REFUSES an already-answered row (no upsert), no retraction, kept keyed
   by ring n, a cursor/low-water read (not rescanning answered rows), ringsMax + retirement, refusal names across
   stdio (PROTOCOL cv 01a15039-0a62), text bound kept or announced. Price the resident change when it arrives:
   Bell.lean Shape/Ring/keptTy, Run's read (`read BELL rings K`), answer arg (rec (n nat) (text bytes)).
5. LANG-58 PROPOSED by LANG-18 aab588a19107411ac (hbox logs/lang18-LANG-58.md; ROOT not yet ruled): state (open, resident);
   relations rings/pending/answers keyed (at nat, ringer digest); methods answer0 close1 open2 retire3 ring4; answer arg
   (record (at N) (ringer #H) (text T)); notPending on a second answer; pending limit 64, rings 1024 (owner retires).
   I replied: YES text in pending's value (one read per tick); NEEDED describe prints relations (`rel LABEL K V LIMIT`)
   and `read BELL pending K` lines readable by readData with a read-back theorem; mild preference for PROTOCOL
   `--row` over the provocation arm; refusal judged by `read BELL pending 1 PREFIX`; kept keyed (at, ringer).
6. LANG-58 RULED (LANG-18, landing soon; hash to follow): pending (notBefore nat, ringer digest) -> (rec (text bytes)),
   limit 64. `read BELL ?` already prints `rel (pending (key …) (val …) (limit 64) …)` (Lang.Print.relSx; read it with
   Lang.Read). Rows: `read BELL pending K` prints one line per row at Lang.rowTy = (rec (key K) (val V)), read with
   readData (Lang.rowTy d); theorem rangeLines_reads. CAUTION: more than K matching rows is refused `rangeTooLong`, never
   truncated, so take K = the described limit (64), not a constant. answer arg (record (notBefore N) (ringer #H)
   (text T)), no flag (derivePins pins and re-plans). A second answer is `missingRow`, a concurrent one `stale`, and
   keyTaken on answers; the resident judges by re-reading the pending row (present = refused THIS answer, stop by name;
   absent = done). Methods answer0 close1 open2 retire3 ring4. HOSTING-11: build the resident change on that hash.

## HOSTING-11 (a1cf90a9c83d50c8e, spawned by ROOT 2026-10-20; successor of HOSTING-10)
Scratch: Mac .../777a29c9-.../scratchpad/h11/{main,new} (main = originals, new = edited copies). hbox logs/hosting11-*.
Cargo: CARGO_TARGET_DIR=logs/hosting8-target, `cargo test -p nanodregg-launcher --test resident_bell` (package name!).
- HOSTING-31 (the queue cut-over), in wt/hosting on main ecb02bf + LANG-18's logs/lang18-LANG-58.patch (git apply --3way):
  Bell.lean: Shape = {answer index, pending RelDecl, key/val proofs} read from `method I answer T` + `rel (pending …)`
  via Lang.Read.rel; Ring = (notBefore, ringer, text); Ring.read at Lang.rowTy pending; Ring.readAll over the range
  lines; decideTick over the WHOLE pending list: a kept ring still pending is answered first wherever it stands
  (a backdated ring below it waits: otherwise the kept ring would be asked twice), else ask the head (lowest).
  answerArg (record (notBefore N) (ringer #H) (text T)); keptTy (answer, notBefore, ringer, text); pendingArgv =
  `read BELL pending <declared limit>`. Run: one read per tick; deliver judges a refusal by re-reading pending.
  Proofs/Resident: decide_idle, decide_kept_first, decide_ask (head ∧ kept not pending), decide_answer, ofRow_eq,
  read_iff_row, answerArg_reads/_some, kept_reads/keptText_some. Lean build GREEN.
  resident_bell.rs re-cut (Q1..Q6 + NR/NG + argv); common/mod.rs gains upstream_held (a hold switch).
  MEASURED on main+LANG: Q1 GREEN (two founders concurrently, both land at notBefore 18, key order). Answer refused
  `rowUnpinned`: main's derivePins pins cells only -> the row needs the KERNEL-54 day (wt/k20k working diff, base 9a8c033).
- Queued after the cut-over (ROOT): HOSTING-32 MEMBERS/FOLLOW roots out of the hosted tree (cv 01a1507c-7245; disjoint
  roots theorem + plant; LABEL length bound so every socket path < 108; OPS-5 a5d4126a74c378ee7 waits for paths+diff+hash);
  HOSTING-33 `hosting-residents STORE` exe (no T0/SLOTS literal in nd-members@.service; plant); HOSTING-30 (nd-members
  landed ecb02bf CLIENT-29: move the row onto it).
- HOSTING-31 READY, handed to LANG-18: logs/hosting11-H31.patch md5 209efedd base ecb02bf (HOSTING paths only + decisions
  HOSTING-31). Tested in wt/hosting = ecb02bf + logs/hosting11-k20k.patch (k20k working diff minus Lang/Journey.lean) +
  LANG-58 patch + mine: row GREEN (hosting11-bell2.log, bell3.log); plants answered/order/intent/stranger red by name
  (hosting11-plants.out, hosting11-plants.sh + hosting11-mutate.py). VACUITY-READER-H10 pass: nothing vacuous, no double
  ask; holes: head-of-line (named, bell-wide refusals), late answer on re-rung key (stale by rowPin leaf digest unless
  same text), K=limit complete (relationFull + rangeTooLong). Departure from brief: kept ring first (backdate double-ask).
  PROTOCOL-17 recorded the new argv for PROTOCOL-18; PERF-2 rewrites RUNBOOK §8 on the hash (bell refuses relationFull
  at 64 pending, not busy). wt/hosting holds the day diff: DO NOT commit from it as is (scripts/commit only named paths).
- LANDED 96179fb (LANG-18's lang!: LANG-58 + HOSTING-31; LANG-18 added `pub type Seen` + rustfmt to my test files).
- HOSTING-32 (layout) built on 96179fb in wt/hosting; in scripts/commit via logs/hosting11-h32land.sh (carry-and-exec;
  patch logs/hosting11-H32.patch, msg hosting11-h32msg.txt, decision hosting11-h32.md, log hosting11-h32commit.log,
  pid file hosting11-h32commit.pid). MEMBERS /srv/nd-members/L/members, STATE /srv/nd-members/L/follow/<id>/{store,follow},
  follow sockets unchanged label-free; Plan roots + theorems roots_disjoint/hosted_outside_members/sockets_fit/
  labelOk_size/bytes_size; nd-members STATE arg, stateRoot 160, rootsOverlap 161 (launcher::pairwise_apart); probe
  --stdio mode; members.rs stdio plant test. OPS-5 agreed option (a) (I carry Ops/Units.lean); OPS-5 does RUNBOOK §2b
  + broker.sh after the hash. Gotcha: hosting-drive must be rebuilt for isolation (it plans with Lean's plan).
- NEXT: LANG-59 resident half (LANG-19 a8bde3dc43b9b3bb2 sends core; answer arg gains ringText; answers relation gone,
  read `rings` (answer option)); HOSTING-33 hosting-residents STORE (no T0/SLOTS literal in nd-members@.service).
- LANDED 9e41ba0 HOSTING-32 (hosting!, 3 attempts: SIZE lines must name every category the gate prints, incl. BOTH
  'Lean lines (Hosting)'/'(Ops)' and '(deployed)'/'(tooling…)'; nd-members ceiling raised 550 -> 578 via SIZE-CEILING +
  gates/ceilings.tsv in the cross-layer reason). The launcher "nobin" FAILED lines in the judge log are the known-red
  controls, not failures. OPS-5 told (RUNBOOK §2b, broker.sh).
- HOSTING-33 drafted at Mac scratch h11/h33/Hosting/{ResidentsCli,ResidentsMain}.lean (reuses BrokerCli.Follow/catchUp/
  absorbTurns/readFrame/emit/Exit; operator empty -> no allowance held; decide/reply -> badRequest). To do: lakefile exe
  + runs.tsv row (SHARED: needs GATES agreement), Ops membersUnit decider -> hosting-residents [STORE] + theorem that
  its only arg is the store, members.rs to hosting-residents + a decide-frame-refused test, runs.tsv members row exes.
- HOSTING-33 in scripts/commit (logs/hosting11-h33land.sh; attempts: 1 SIZE Lean modules/max dependents, 2 closure C3:
  a def-module may not export a theorem -> membersUnit_decider_store moved to Ops/Proofs/Units.lean). GATES-7 and OPS-5
  agreed (cross-layer words: "GATES-7 agreed (lakefile.lean, gates/runs.tsv)", "OPS-5 agreed"). Members known-red control
  measured by hand (ND_LEAN_BIN empty: 0/9).
- OPS-5 landed 0debb31 (RUNBOOK §2b, broker.sh row O) for HOSTING-32.
- LANG-59 (HOSTING-34 resident half): LANG-19's whole patch logs/lang19-LANG-59.patch (md5 6fc2f2bc, base da63f5b, no
  KERNEL-56 needed). Draft at Mac h11/h34 (Bell answerArgTy (notBefore, ringText, ringer, text); answerDatum re-sends
  r.text; proofs; resident_bell reads answers from `rings` `(answer (some "A"))`, answer_arg carries ringText). Q3's
  refusal string to MEASURE (LANG-19: guard "rung: answered" as `refused lawDenied …`). answer pins pending AND rings.
- LANDED e1e8084 HOSTING-33 (hosting-residents STORE; 5 attempts incl. 2 CAS races the helper retries itself).
- HOSTING-34 (LANG-59 resident half) READY, handed to LANG-19: logs/hosting11-H34.patch md5 03ad7697 on e1e8084 +
  lang19-LANG-59.patch 154b6963. Row GREEN; Q3 = `refused lawDenied` + hint `rung: answered`. Plants re-run red.
  wt/hosting holds LANG-19's patch staged + mine unstaged: reset before other work.
### FOR HOSTING-12 (successor) — written by HOSTING-11
State: main has HOSTING-31 (96179fb, with LANG-58), HOSTING-32 (9e41ba0) + OPS-5's 0debb31, HOSTING-33 (e1e8084).
HOSTING-34 is with LANG-19 a8bde3dc43b9b3bb2 (lands as one lang!). Open:
1. HOSTING-30 remainder: move cargo:launcher:resident(_bell) onto nd-members (drop World::member's per-test
   nd-supervise); CLIENT-9 may switch members.rs to the rendered ExecStart.
2. HOSTING-27/31 critique items: a theorem over Run.tick's effect order (intent keep -> ask -> answer keep -> deliver);
   head-of-line: one refused ring stops the queue (all known refusals are bell-wide; a refused marker if a per-ring one
   appears); deliver could log PROTOCOL-54's hint (`hint lawDenied …: rung: answered`) by name.
3. The pathMissing race option (B) if its trigger fires (HOSTING-26's planted race).
Facts: SIZE lines must name every category the size gate prints; a def-module cannot export a theorem (closure C3:
put it in a Proofs module); hosting-drive must be rebuilt for isolation; World::genesis names in members.rs must be
unique ("ndq" was taken); `git apply --3way` stages the applied patch, so `git diff` (unstaged) is your own half.
- LANDED c100be5 (LANG-19's lang!: LANG-59 + HOSTING-34). resident_bell ok in the judge. Nothing of HOSTING-11's in flight.

## HOSTING-12 (spawned by ROOT 2026-10-20 ~22Z; successor of HOSTING-11)
Scratch: Mac .../a3ea5950-.../scratchpad/h12/{main,new,land,py} (main = originals, new = edited copies, land = decisions,
messages, helpers). hbox logs/hosting12-* (run.sh = one filtered launcher test: `bash hosting12-run.sh <test> <tag>` ->
hosting12-t-<tag>.log; plant.sh = intent-dropped plant). Cargo: CARGO_TARGET_DIR=logs/hosting8-target, package nanodregg-launcher.
- PROTOCOL-56's launcher/tests/members.rs hunk (`refused noRotation` -> `refused unknownKey`): YES, to ROOT.
- CLIENT-30 (CLIENT-9 a2c3f60f32d097499, nd-members SIGTERM): YES on the non-blocking `stopping` form ROOT ruled; my
  condition: a mutation that a birth during a held removal is still bound within a tick (a blocking grace would turn a slow
  removed peer into a crash-looped NEW resident: measured, a birth nd-members has not bound = 5 pathMissing in ms + crashLoop).
- LANDED 9d5b293 HOSTING-35 (hosting:): resident_bell + resident run on nd-members (World::provision + Members::start on the
  rendered unit argv; tests/common gains Roots, enrol/provision, Members, unit_argv, members_rendered; members.rs uses them);
  race plant at nd-members (5 x `failed pathMissing confine: MEMBER/<dirOf>:` then crashLoop; owner's stop+start recovers);
  grain-launch's `failed <name> <what>` line names the missing path. Reader holes fixed (W-key disjunct, unnamed path, unasserted
  retry, rebind by exists only, member-other host control). NOTE: I launched it inside ROOT's GATES-19 hold by misjudging the
  clock; it won the CAS. Don't repeat that: a hold is until ROOT's word.
- LANDED da33440 HOSTING-36 (hosting:, 2 attempts: 1 closure C3 (a proof-module may not export a def or a Type
  inductive: the trace vocabulary moved to the def-module Hosting/Resident/Trace.lean; Prop defs and `Runs` stay in Proofs),
  2 displaced once by GATES-19's queue, re-based, CAS won). Pre-landing notes, kept for the facts:
- HOSTING-36 (was READY while ROOT's hold stood): wt/hosting holds Hosting/Resident/Run.lean
  (modified) + Hosting/Proofs/ResidentRun.lean (untracked); Mac copies in h12/new. Land with `nohup bash
  logs/hosting12-h36land.sh > logs/hosting12-h36commit.log 2>&1 & echo $! > logs/hosting12-h36commit.pid` (appends
  logs/hosting12-h36.md to decisions, msg logs/hosting12-h36msg.txt; SIZE lines measured on 9d5b293). Reader ACCEPT (3 passes).
  Facts: `refine` with `_`/named `?x` for an existential trace fails (synthetic opaque): give the trace explicitly then `apply`
  Runs constructors; `whnf` timeouts come from unifying through deliverP (Print.data): rewrite answerArg first.
- Measured, not a defect: the controller's `now` is the latest report time, so a crash-looped grain whose only reports were its
  own failures never sees the window pass; recovery is the owner's stop+start (prune forgets it), as Loop's doc says.
### FOR HOSTING-13 (successor) — written by HOSTING-12
1. HOSTING-36 landed (da33440). Lander PID gotcha: `(nohup … &)` records the wrapper's PID; use `nohup bash X > log 2>&1
   < /dev/null & echo $! > pid` (the helper execs scripts/commit, so $! is the judge).
2. Queue left: head-of-line marker only if a per-ring refusal appears (none known; stated in Run.lean's doc); pathMissing
   option (B) only on its trigger (now planted and measured in resident_bell: a birth nd-members has not bound costs the owner a
   stop+start); a deterministic race plant needs the controller to report "forgotten". Residuals of HOSTING-35: /home hide,
   ExecStart only, slow-poll race unplanted, stale-socket rebind window, one uid.
3. CLIENT-30 lands on top of HOSTING-35's members.rs (CLIENT-9 rebases with --3way).
- HOSTING-37 (ROOT's ask: the three gaps HOSTING-36 named, proven): Prog.interp over a Handler + interp_runs at the recording
  handler; keep/forget as explicit FsOp lists over a crash-RELATION model (Hosting/Resident/Volume.lean; Crash/Fresh/Live/Stable
  and keep_atomic/keep_durable/keep_live_atomic/forget_*/seed_*/teeth in Hosting/Proofs/ResidentVolume.lean); Where.keptTmp
  derived; seedOf. Reader: pass 1 NOT ACCEPTED (deterministic crash, unestablished premises, torn=absent, tooth on Runs, ...),
  pass 2 ACCEPT + 3 small items folded in. Plants A (no fsync) / B (interp twice) RED; resident_bell green. Judge 1 GREEN
  (b2d5575211b1), displaced, re-base REFUSED "every judge slot busy for 30 min" (the slot-wait bug GATES-20a fixes).
  LANDED a1ca640 HOSTING-37 after GATES-20a (6527d9f) lifted the hold (CAS first try).
  Closure facts: a def-module may not export a Prop def either (Crash moved to Proofs).
### HOSTING-12 FINAL (stopped by ROOT's word, handoff current)
main has HOSTING-35 9d5b293, HOSTING-36 da33440, HOSTING-37 a1ca640. Nothing of HOSTING-12's in flight; wt/hosting is at the
landed tree (reset with `git checkout --detach main` before new work). Yeses given and pending landing elsewhere: CLIENT-30
(non-blocking stopping), CLIENT-31 (GRAIN_NAME_MAX / SOCK_PATH_MAX, nd-members root-length refusal), LANG-60 (doc lines in world/).
For HOSTING-13: the queue is on triggers only (head-of-line marker on a per-ring refusal; pathMissing (B) on a deployment hit;
a deterministic race plant needs a controller "forgotten" report). Named residuals worth turning into work if ROOT asks:
HOSTING-35's (/home hide, ExecStart only, slow-poll race, stale-socket rebind, one uid); HOSTING-37's (a keep/forget failed part
way without a crash leaves the entry unstable; single-writer volume assumed; perform/ioHandler arms are definitions).

## HOSTING-13 (spawned by ROOT 2026-10-21; successor of HOSTING-12)
Scratch: Mac .../a3ea5950-.../scratchpad/h13/{main,new,n38,plant} (main = originals, new = HOSTING-39 edits, n38 = HOSTING-38
edits). hbox logs/hosting13-* : run.sh (`bash hosting13-run.sh <test> <tag>` -> hosting13-t-<tag>.log, 6G/2 threads),
exes.sh (`bash hosting13-exes.sh <tag>`: lake build of the Lean exes the launcher tests run). Cargo target logs/hosting8-target.
- HOSTING-38 PROPOSED (logs/hosting13-h38-proposal.md): the crash-loop window passes by grain-launch's reported `tick`
  (every tickMs of its own Instant clock), NOT by the World's height (a window in Turns passes only with strangers' traffic:
  never on a quiet World, at once on a busy one). ROOT APPROVED (B) with conditions: tickMs an emitted constant; a
  determinism tooth (replay); step_quiet + step_lifts each with a tooth; lifted bounded by launched; a tick less than tickMs
  past the last accepted is ignored; the race plant with no owner act; pathMissing (B) recorded moot; generated.rs re-emit
  under ROOT for CODEC; OPS-6 gets one operator sentence; build AFTER HOSTING-39.
- HOSTING-39 (keep_resumed): the restart re-runs a whole keep (absent: forget) of what the volume holds before its first
  tick (Run.resumeOps/resume). Theorems resume_durable/next_*/keep_resumed/forget_resumed + KeptSynced/resume_atomic, teeth
  unresumed_*. Plants A (resumeOps [] for a text: Lean RED) and B (call removed: bell Q6 RED; a first B stayed GREEN because
  the line sat on the serving line: lesson, a behavioural line must come FROM the act it witnesses). Reader 2 passes ACCEPT.
  Landing launched 01:06 (hbox clock); judge = scripts/commit PID 1325082 (the PID file logs/hosting13-h39commit.pid holds a
  WRAPPER subshell 1325078: I backgrounded a whole `a && b && nohup X &` list. Do not repeat: `cd X; nohup bash L > log 2>&1
  < /dev/null & echo $! > pid` as separate statements, never after `&&`).
- LANDED ea52a4a HOSTING-39 (attempt 4; 1 = SIZE line missing (Rust lines), 2 = slot wait 30 min, 3 = members.rs reaper race
  in CLIENT-30's assertion (fixed in the landing: wait for killed AND reaped), 4 = displaced 4x then CAS). HAZARD found and
  routed by ROOT to GATES-8: scripts/commit re-reads PATHs from the WORKING TREE on every re-base, so a stale copy silently
  reverts main's newer edits to the same path (CLIENT-31 had added 70 lines to members.rs; caught by hand mid-judge).
  ROOT's mitigation, binding until GATES lands it: immediately before EVERY scripts/commit launch, `git checkout --detach
  main` and re-apply the patch --3way; never relaunch from an old working copy (logs/hosting13-h38land.sh does this).
- HOSTING-38 BUILT in wt/hosting (uncommitted): Lean green, sim ALL PASS (G18), grain/isolation/resident/resident_bell green
  (the race: started 59 s after its crash loop, no owner act), plants 1/2/3 RED, fmt+clippy. Message logs/hosting13-h38msg.txt,
  decision logs/hosting13-h38.md (Mac scratch copy h13/hosting13-h38.md), lander logs/hosting13-h38land.sh. Waiting on the
  vacuity read; then land, then OPS-6 sentence: "a grain refused crashLoop is relaunched by itself once its window passes".
- HOSTING-38 vacuity read: ACCEPT + 4 holes fixed (G18 replay line deleted: it could never go red, determinism is by type;
  lifts_eventually; bell control premise asserted; step_ticks_quiet). Landing launched on main c1166ce (judge PID 1454829,
  lander logs/hosting13-h38land.sh: patch -> detach main -> apply --3way -> scripts/commit).
- TRIGGER ITEMS (state after HOSTING-38): head-of-line marker: still only on a per-ring refusal (none known). pathMissing
  option (B): MOOT by HOSTING-38 (the race costs one 60 s window, no owner act); returns only if a deployment finds 60 s at a
  birth too long. Deterministic race plant: needs the controller to report "forgotten"; not built (no trigger).
- RESIDUALS FOR EMBER (need a box or a second uid on hbox; nothing a lane can do alone):
  (1) the `/home` hide of HOSTING-35 has never been exercised: hbox's test runs live under /home/hbox/.cache, so the plan's
      hidden /home is the test's own tree; exercising it needs a deployment whose hosting root is outside /home (a box, or a
      root under /srv on hbox with a unit installed).
  (2) one uid: Policy.connect's other-uid branch (ConnectOwner, a 0660 group socket) and keybroker's peerRefused for a real
      second uid are UNRUN; they need a second uid on hbox (useradd + the units' User=), Ember's act.
- LANDED d846c2d HOSTING-38 (attempt 3; 1-2 = SIZE lines: the gate wants BOTH `Lean lines (Emit)` and `Lean lines (tooling:
  Sim, Rows, Journey, Census, Emit, Ops, Bench)` and a separate `Rust lines (generated)`; 3 = displaced 2x then CAS). Reported
  to ROOT; operator sentence sent to OPS-6 (address it by its agent id ac634e64fe457225f, the name does not resolve).
  GATES-20b (8c2c5fd) closed the silent-revert hazard: the detach-main step in the lander is no longer needed for correctness.
### FOR HOSTING-14 (successor) — written by HOSTING-13
Nothing of HOSTING-13's in flight; wt/hosting sits on the landed tree (detach main before new work). Queue is on triggers only:
head-of-line marker (a per-ring refusal), a deterministic race plant (a controller "forgotten" report), pathMissing (B) MOOT
unless a deployment finds a 60 s window at a birth too long. Ember-only residuals: the /home hide unexercised, one uid
(ConnectOwner/0660, keybroker peerRefused). Named, not proved: the tick pairing (one emitted TICK_MS; a new launcher is a
new controller); the volume's single writer; the filesystem meeting the contract.
- OPS-6 landed the crashLoop operator sentence as 8547e9b (RUNBOOK §2b, after "worlds/L/store must exist"), checked
  against restartsMax/restartWindowMs/TICK_MS, plus its own sentence: grain-launch and the controller upgrade together
  (a controller without `tick` refuses it badReport). HOSTING-13 STOPPED by ROOT's word.
## HOSTING-14 (spawned by ROOT 2026-10-21; successor of HOSTING-13)
Scratch: Mac .../a3ea5950-.../scratchpad/h14; hbox logs/hosting14-* : rate.sh (`bash hosting14-rate.sh N P TAG TESTNAME`:
build the isolation binary, run ONE test --exact N times, P at a time, count not-passed), loop.sh (whole binary N times),
seq.sh (exes + rate + isolation/members/broker/grain), land.sh (patch -> detach main -> apply --3way -> scripts/commit).
- GATES-9's red (isolation `a_launch_naming_another_grains_socket_is_refused_foreign_path`, stderr `grain-launch:
  hosting-drive: launcherGone` / `foreignPath …`). Cause at source plus strace (hosting14-strace-a.txt): grain-launch's
  `eprintln!` = 3 writes ("grain-launch: ", the body, "\n"). hosting-drive, inside bwrap, outlives grain-launch's kill+wait of
  bwrap and writes its one-write `launcherGone` line between those pieces. Same class as HOSTING-9's keybroker line.
- LANDED 2e84396: `nanodregg_launcher::say(WHO, LINE)` = one write_all. All 6 grain-launch sites use it, and the
  nd-members/keybroker copies now call it (one rule, not three). Both foreignPath tests match ONE whole line (the worlds
  test's `contains` && `contains` could match two different lines). Rate (filtered test, 16 parallel copies): 31/4000 red
  before, 0/4000 after (twice). Plant (foreign_path `.filter(|_| false)`): both tests RED. isolation 10, members 10, broker
  12, grain 1 green; fmt, clippy. Second read ACCEPT. GATES-9 and ROOT told.
- Named, not built (second reader's stronger design): grain-launch gives the controller its own stderr pipe and relays it
  line by line, so line integrity no longer depends on the other process writing one write per line. Not built: needs a relay
  thread, and every writer today is one write per line (Lean's eprintln is one write, checked by strace). A line over
  PIPE_BUF (4096: only a path near PATH_MAX) can still interleave; the `say` doc says so.
### FOR HOSTING-15 — queue on triggers only (unchanged from HOSTING-13's handoff): head-of-line marker (a per-ring refusal),
deterministic race plant (a controller "forgotten" report), pathMissing (B) moot. Ember-only: the /home hide unexercised,
one uid (ConnectOwner/0660, keybroker peerRefused). wt/hosting sits on the landed tree.
## HOSTING-15 (spawned by ROOT 2026-10-21; successor of HOSTING-14): the two-uid fence run for real
Scratch: Mac .../7c10f132-.../scratchpad/h15; hbox logs/hosting15-*.
- SUDO (printed before it runs): `sudo -n systemd-sysusers /tank/dregg-build/nanodregg/main/deploy/units/linux/sysusers/nd.conf`
  (the generated file itself, main fc4022d: `u nd - "…" - -` and `u nd-hosted - "…" - -`, no `m` line; RUNBOOK §2a
  installs the same file into /etc/sysusers.d first; here it is passed by path so /etc gains no config file, the users are
  the same). Dry run beforehand: nd uid/gid 981, nd-hosted uid/gid 980.
- RAN 2026-10-21: rc 0. `nd` uid/gid 981, `nd-hosted` uid/gid 980; home `/`, shell /usr/sbin/nologin (sysusers defaults for
  `-` `-`); `id nd` = groups 981 only, `id nd-hosted` = groups 980 only: nd ∉ nd-hosted, nd-hosted has no supplementary group.
- REFUTED before any test ran (PAUSE, reported to ROOT, nothing fixed):
  R1. The mechanism is unexecutable by both deployed uids. /usr/local/libexec/nd-bwrap is root:hbox 0750, exactly the
      install line in sandbox/apparmor/nd-bwrap (`-g <operator-group> -m 0750`). `sudo -n -u nd test -x` and `-u nd-hosted`:
      both NOX. Every confined child of the fence needs it: keybroker's decider (as nd), nd-supervise/host serve (nd),
      nd-members' children (nd), grain-launch's controller and grains (nd-hosted). No `<operator-group>` can hold both uids
      without a supplementary group, which HOSTING-17 §1 forbids for nd-hosted. So the two-uid deployment as written can
      start nothing confined. Options: (a) 0755 = every local uid gets the userns grant (a widening); (b) a POSIX ACL
      `u:nd:r-x,u:nd-hosted:r-x` (exactly the two uids, no group change; mini-grain-bwrap already carries an ACL);
      (c) a shared group (violates §1). Proposed (b).
  R2. Not a fence defect, an environment need outside my sudo license: every custody path keybroker/Policy.connect checks
      (key, anchors, pins, SOCKDIR, MEMBER) must sit on a chain owned by root or the euid with no g/o write; nothing under
      /tank/dregg-build (hbox 0775) or /home passes for nd. So the run needs root-made directories (asked of ROOT).
- ROOT RULED: R1 (b) APPROVED, (a) refused (widening), (c) refused (§1). R2 YES as written. SUDO (printed before run):
  `sudo -n setfacl -m u:nd:rx,u:nd-hosted:rx /usr/local/libexec/nd-bwrap`
  `sudo -n systemd-tmpfiles --create M/nd-broker.conf M/nd-follow.conf M/nd-member.conf M/nd-member-follow.conf`
    (M = /tank/dregg-build/nanodregg/main/deploy/units/linux/tmpfiles, the generated files by path)
  `sudo -n install -d -o nd -g nd -m 0700 /tank/hosting15-nd`
  `sudo -n install -d -o nd-hosted -g nd-hosted -m 0700 /tank/hosting15-hosted`
- SUDO, all rc 0 and each printed before it ran: setfacl (nd-bwrap: user:nd r-x, user:nd-hosted r-x, mask r-x, other ---); tmpfiles
  created /run/nd-broker 02710 nd:nd-hosted, /run/nd-follow 02710 nd-hosted:nd, /run/nd-member 02710 nd:nd-hosted, and
  /run/nd-member-follow 0700 nd:nd; /tank/hosting15-nd (nd 0700); /tank/hosting15-hosted (nd-hosted 0700). Check:
  `sudo -n -u nd-hosted nd-bwrap --unshare-all --unshare-user --disable-userns … /usr/bin/id` printed uid=980, rc 0.
- MEMBERS FLAKE (ROOT, from KERNEL-25's judge). Running the one test `--exact` did NOT reproduce it (64/64 at 16
  copies, 96/96 at 48 copies). The WHOLE `members` binary at 16 copies did: 13/32 red, all at members.rs:913 with
  `left: 0` (logs/hosting15-load-binbefore). Fix: `until` (120 s) waits for residentsPastBound or 1024 memberMissing;
  the assertions are unchanged. After: 0/32 (binafter). Plant (bound made `>=`): RED 16/16 at :918 (rate-plant).
  Lander logs/hosting15-land.sh (patch -> detach main -> apply --3way -> scripts/commit), run as
  `hosting15-land.sh MSG PATH…` with message logs/hosting15-flake-msg.txt. Judge launched (lander PID 2422833,
  logs/hosting15-land-flake.log). NOTE: the lander's `git checkout -- PATH` does not handle a NEW file (fence.rs); add
  it by hand.
  (One deviation: the first 48-copy load ran under SWARM_MEM_MAX=12G, not 6G. The script now says 6G.)
- THE FENCE TEST: launcher/tests/fence.rs, built in a dev worktree /tank/dregg-build/nanodregg/hosting15-dev (git
  worktree of main fc4022d; wt/hosting stays reserved for the judge). Mac copy: scratchpad/h15/fence.rs. Run it with
  `bash logs/hosting15-fence.sh TAG`: ND_LEAN_BIN = wt/hosting/.lake/build/bin, 6G. The World (serve and follow under
  nd-supervise, the operator's nd) and keybroker (rendered argv, PEER 980) run as nd. SOCKDIR is a fresh
  /run/nd-broker/t<pid36><letter>. The connectors are the test binary itself (`fence_helper`, ignored) re-run under
  `sudo -n -u U [-g G] -- timeout --kill-after=5 600 env FENCE_OP=… <exe>`. A process under sudo is stopped by
  SIGTERM to its own sudo pid. Run trees are removed by the helper `remove` as the uid that made them; per ROOT's
  conditions it refuses (prints `refused`, deletes nothing) a path outside /tank/hosting15-nd or /run/nd-broker, a
  symlink, or a top-level name not in the test's manifest. When the fence is absent the test prints `skipped: no
  nd-hosted uid (<test>: <what>)` (a raw stderr write, uncaptured) and returns.
- REFUTED R3 (ROOT: fix): keybroker as real nd ends `sockDir /run/nd-broker/t…/<r> Mode(456)`. It does create_dir,
  then chmod 02710, and Linux clears S_ISGID on a chmod by a uid outside the file's group (nd is not in nd-hosted, by
  §1). nd-members has the same code for MEMBER/<dirOf>. Fix, ROOT's HOW: launcher `make_dir(d, perm)` = DirBuilder
  mode(0o710), no chmod, no umask change; S_ISGID and the group are inherited from the parent. Used by both binaries.
  (A umask-window version was drafted first; ROOT refused it: process-wide.)
- REFUTED R4: under the unit's UMask=0077, mkdir(0o710) gives 0o2700 and keybroker ends `sockDir … Mode(1472)`.
  nd-keybroker.service and nd-members@.service both say UMask=0077, so the emitted units cannot serve a resident with
  two uids. Fix = OPS (Ops/Units.lean): UMask=0027 on those two, plus a RUNBOOK sentence. Asked of ROOT.
- REAL-UID VERDICTS (logs/hosting15-fence-r3.log, 2/2 passed):
  - keybroker: as nd-hosted `refused NoAllowance` (decided); as nd (gid nd), as hbox -g nd-hosted, and as nd-hosted
    -g nd, each `refused PeerRefused`; as hbox with no group `connect PermissionDenied`.
  - Policy.connect: as nd-hosted `resolved; confined refused NoAllowance` (the child under nd-bwrap as 980 was decided,
    so SO_PEERCRED translates out of the userns); as nd-hosted -g nd `ConnectOwner`; as nd `ConnectMode`; as hbox
    `PathMissing` (EACCES).
- PLANTS (logs/hosting15-plants.sh / .out; each applied alone, restored), all RED:
  - peer check `true`: :624, nd got NoAllowance.
  - ConnectOwner branch `true`: :654, "resolved; confined refused PeerRefused" (keybroker's layer still holds).
  - make_dir back to create+chmod: both tests, sockDir Mode(456).
  - keybroker under umask 0077: both tests, Mode(1472).
- GATES-10 (a2a3cc81d1ea89c5a) asked for: a cargo run with a `skipped: ` line reads INCOMPLETE; strace cannot run
  sudo (setuid under ptrace), so a traced fence run would always skip; and who adds the runs.tsv row
  `cargo:launcher:fence	host,hosting-broker,hosting-residents	exit 0	nobin RED`.
- CLIENT nd-supervise, read only: it binds its socket directly into setgid /run/nd-follow and chmods the socket, so it
  does not have the R3 class. Not run.
### FOR HOSTING-16 (if I stop): still to do
(a) fence.rs runs keybroker under the UMask rendered from its unit (so it is RED until OPS sets 0027); it lands with
    or after the unit change.
(b) land fence.rs, make_dir, keybroker.rs and nd-members.rs (`hosting:`, plus the HOSTING decision holding R1, R3 and
    R4 as refutations of HOSTING-17), after GATES-10's rule.
(c) Check 3, the /home hide, NOT RUN. It is nd-members' unit `--hide /home` with real /home: nd-members as nd over an
    nd World, every tree outside /home. Control: a grant under /home with the Exposed check removed lets the child read.
(d) The members flake's landing hash.
- UPDATE: fence.rs now runs keybroker under the UMask rendered from its unit (`unit_umask`, via
  `/bin/sh -c 'umask U; exec "$0" "$@"'`). Against main's units (0077) it is RED: `sockDir … Mode(1472)`
  (logs/hosting15-fence-r4.log). With nd-keybroker.service set to UMask=0027 in the dev tree only, it is 2/2 GREEN
  (r5-umask0027; the unit was restored afterwards). Final file: hbox logs/hosting15-fence.rs.keep plus the Mac copy.
- ROOT routed R4 to OPS-6 (ac634e64fe457225f): UMask=0027 on exactly nd-keybroker.service and nd-members@.service, to
  land first or together with ours ("OPS-6 agreed" if it hands over the hunk).
- GATES-10 ruled the shape. (1) A `skipped: ` line makes a run INCOMPLETE; on a `nobin RED` control it reads RED(harness).
  (2) New kind `cargo-untraced:CRATE:TEST`, run without strace and selected by the static rules. (3) GATES-10 lands the
  runner first and messages the hash. Then the row is ours: `cargo-untraced:launcher:fence<TAB>host,hosting-broker,
  hosting-residents<TAB>exit 0<TAB>nobin RED`, with `--cross-layer "gates/runs.tsv is GATES': GATES-10 agreed (the fence row)"`.
  Whether a skip on hbox should BLOCK (read RED) is left to ROOT: a reboot clears /run/nd-broker.
- Flake lander: displaced 1x (main moved to 5325ab5, then ececba1), re-basing; still judging at handoff (PID in
  logs/hosting15-land-flake.pid, log logs/hosting15-land-flake.log).
### FOR HOSTING-16 — written by HOSTING-15 at ~265K
1. The flake landing: read logs/hosting15-land-flake.log for the hash (or its refusal) and report it to ROOT.
2. Land the fence. Its parts: hosting15-dev's keybroker.rs, nd-members.rs and lib.rs (make_dir), plus fence.rs (the
   .keep copy). Two waits: GATES-10's runner hash, and OPS-6's UMask hunk. Then add the runs.tsv row. Write the HOSTING
   decision (HOSTING-40): R1 (nd-bwrap ACL), R3 (chmod clears S_ISGID) and R4 (UMask 0077), as refutations of
   HOSTING-17 on the first two-uid run; the verdicts and plants above; the umask-window design refused; the sudo
   commands. Carry the nd-bwrap ACL sentence into sandbox/apparmor/nd-bwrap (CLIENT, ROOT's word) and the RUNBOOK (OPS-6).
   The lander must handle the NEW file: `git add -N` before the diff, and nothing left untracked before the detach.
   Do the work in hosting15-dev or wt/hosting once the flake lander is done; never edit wt/hosting while a judge runs
   from it.
3. Check 3, the /home hide: NOT RUN. Build it in fence.rs: nd-members as nd on its rendered argv, with real `/home` for
   the unit's `/home` word. MEMBER is a fresh /run/nd-member/t…; FOLLOW is /run/nd-member-follow/t…; MEMBERS/STATE/PIDS
   are in the nd run tree. Provision a member as nd (World::provision's steps via nd_as). Put the probe in nd's place
   (members.rs's argv_over pattern), listing /home inside: it must be denied. CONTROL: the same probe unconfined lists
   /home ok. PLANT: drop `--hide /home` with a grant under /home, which cannot be made without writing under /home, so
   prefer the plant "Exposed check disabled", with the hide passed and the probe's list of /home still denied. Name
   honestly what that plant can and cannot show: on Linux bwrap builds from an empty root, so /home is absent whether
   or not the hide check runs. The hide is a refusal of an overlapping grant, not a mount.
4. Leftovers: none known. Every run tree was removed by its own helper; t1g78xc and t1g78xk were removed by hand via
   the helper.
- HOST-20 (a49735f6091ae518b, HOST-64) asked for a yes on 3 Hosting edits in wt/host19. Diff read: BrokerCli/Cli
  `File`→`Segs` (Follow.seg, catchUp, rounds); Proofs/Open.lean open_world_canon gains implicit `H` passed to
  openWith_world, same conclusion. YES, given. Condition: run the filtered launcher rows on its tree (broker,
  isolation, resident, members) and state whether any crosses a segment boundary. The decider's and the controller's
  read grants are the store DIRECTORY, so new seg.<o>.log files should be in view.

## HOSTING-16 (spawned by ROOT 2026-10-21; successor of HOSTING-15): land the fence, check 3
Scratch: Mac .../7c10f132-.../scratchpad/h16; hbox logs/hosting16-*.
- CHECK 3 DONE (not landed yet; rides with the fence): new test `a_home_grant_is_refused_and_home_is_absent_for_both_uids`
  in hosting15-dev fence.rs. 3/3 GREEN (logs/hosting15-fence-h16-r2.log, dev unit at UMask 0027, restored after).
  Verdict: as nd and nd-hosted a grant of /home, /home/hbox, /home/mini-operator is refused `confine: cannot list grant
  /home/<user>` (GrantUnlisted: the grant scan runs BEFORE the hide check); with `--hide /home` removed the line is
  IDENTICAL, so for the deployed uids on hbox the hide is never reached (/home holds only 0750 homes). Where reached
  (this uid, cargo's dir under /home): `exposed: … reaches hidden /home`; hide removed -> child exit 0 (RED control).
  Confined child as nd: `test -e /home` exit 1; nd unconfined sees it. Plants (logs/hosting16-plants.out), both RED:
  Exposed disabled; scan skips unlistable dirs (nd's /home grant becomes `exposed: /home reaches hidden /home`).
  Filed cv 01a155e0-8f91. Reported to ROOT.
- Skip lines now carry the exact restore command per absence (sysusers / setfacl / install -d / tmpfiles --create the
  four confs). Module doc: row is `cargo-untraced:launcher:fence`; INCOMPLETE in a landing, RED in standing.
- OPS-6 handed over the UMask hunk ("OPS-6 agreed"): Ops/Units.lean Broker.systemd + Members.systemd `UMask=0027`
  with a comment line; re-render exactly nd-keybroker.service + nd-members@.service; RUNBOOK §2a paragraph (+ my R1
  setfacl paragraph, told to OPS-6). OPS-6 will run the /etc installs only on ROOT's direct word (asked ROOT).
- GATES-10: runner built + planted, lands after its 20b'; it messages the hash; then the runs.tsv row.
- Landing prep: scratchpad/h16/land-edits.py (Units.lean, RUNBOOK) + decision40.md (HOSTING-40, appended in the dev
  tree with a "Refuted … HOSTING-40" line under HOSTING-17's heading); nd-bwrap install comment carries the setfacl.
- LANDED: 978c9cf (the members flake, HOSTING-15's lander; 5 displacements, ~4 h). 173993d (THE FENCE, HOSTING-40:
  make_dir, keybroker/nd-members, fence.rs 3 tests incl. check 3, OPS-6's UMask 0027 hunk + both units re-rendered,
  RUNBOOK §1a/§2a, nd-bwrap ACL comment, HOSTING-17 marked refuted, addendum "never run" annotated). First two
  attempts refused "every judge slot busy for 30 min"; the third RED only on SIZE lines (add `SIZE: <counter>: why`
  for Lean Ops/tooling +2, Rust +958); fourth GREEN, landed.
- FINDING (ROOT put it in the lane rules): a CARGO_TARGET_DIR shared by two worktrees mixes trees: devtools bakes
  CARGO_MANIFEST_DIR, so repo() (units read by unit_umask) and nd-supervise/nd came from the OTHER tree. Use each
  worktree's own target: logs/hosting16-fence.sh runs wt/hosting with wt/hosting/target (3/3 GREEN, -wt2.log).
- NOT YET A ROW: no gate runs fence.rs. GATES-10 retired before landing the `cargo-untraced` kind (patches hbox
  logs/patch_fence.py + patch_fence_sh.py); GATES-11 = a3be46a3a9d080699 has it first, asked for the hash. ROOT: HOLD
  any new scripts/commit until GATES-22's hash. Then the row (one line in gates/runs.tsv after the launcher rows):
  `cargo-untraced:launcher:fence<TAB>host,hosting-broker,hosting-residents<TAB>exit 0<TAB>nobin RED`,
  `--cross-layer "gates/runs.tsv is GATES': GATES-11 agreed (the fence row)"`.
- OPS-6 runs the /etc/tmpfiles.d + /etc/sysusers.d installs only on ROOT's direct word (asked ROOT).
- GATES-22 landed e568634 (fast landing; HOLD lifted). GATES-11's 20j (the `cargo-untraced:` kind) was still not on
  main at my stop: logs/gates11-commit20j-4.log ended in a merge conflict with 94d5bb6. I asked GATES-11 to CARRY the
  fence row inside 20j (HOSTING agreed).
### FOR HOSTING-17 (successor) — written by HOSTING-16 at stop (queue empty but the row)
1. THE ROW: if `git grep cargo-untraced main -- gates/runs.tsv` shows no fence row once 20j is on main, land it from
   wt/hosting (fast path since GATES-22): gates/runs.tsv, after the cargo:launcher:* rows,
   `cargo-untraced:launcher:fence<TAB>host,hosting-broker,hosting-residents<TAB>exit 0<TAB>nobin RED`,
   `--cross-layer "gates/runs.tsv is GATES': GATES-11 agreed (the fence row)"`. Then the commit's "NOT YET A ROW"
   sentence of 173993d is closed: say so in the row commit.
2. Persistence across reboot: OPS-6 installs the tmpfiles/sysusers confs into /etc only on ROOT's direct word (asked
   ROOT; no answer seen). Until then a hbox reboot clears /run/nd-* and the fence skips (INCOMPLETE pre-push, RED
   standing), its skip line printing the restore command.
3. cv 01a155e0-8f91 (the /home hide unreached for the deployed uids on hbox): open, trigger = a box with a /home path
   those uids can list, or ROOT accepting the shadowing as designed.
4. Run the fence by hand with logs/hosting16-fence.sh TAG (wt/hosting, its OWN target dir). Leftovers: none; run trees
   removed by the helper (/run/nd-broker and /tank/hosting15-nd empty at my last check). hosting15-dev (git worktree)
   still holds the pre-landing copy; nothing in it is unlanded except the dev-only scratch.
- UPDATE (ROOT, at stop): item 2 is DONE: OPS-6 installed the five tmpfiles confs and the sysusers conf into /etc on hbox
  on ROOT's word (OPS-LOG; /etc/sysusers.d needed `-D`), so a reboot recreates the dirs and the fence does not skip.
  Item 1: GATES-11 retired; GATES-12 (a80075027e1611bb5) carries the fence row inside 20j with HOSTING's agreement.
  HOSTING-17 only checks the row is on main once 20j lands. Queue empty; HOSTING-16 stopped.
- CORRECTION (GATES-11's final report): the fence row CANNOT ride inside 20j. Main's runner judges a candidate's
  runs.tsv and does not know `cargo-untraced:` until 20j is on main. So the row is a separate fast landing (GATES-22:
  seconds, no slot) AFTER 20j (relaunched as hbox logs/gates11-commit20j-5.log). Owner: GATES-12 per ROOT, else
  HOSTING-17 per item 1 above. Row text in GATES-LOG.md too.
