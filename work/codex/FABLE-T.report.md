# FABLE-T — typed nested-call arguments (cv 01a16679-198f): report and continuation

Worker: FABLE-T (Claude Fable 5.1). Repo: `~/dev/nanodregg` (mirror; origin github emberian/nanodregg).
hbox worktree: `/tank/dregg-build/nanodregg/wt/fable-t` (logs under its `logs/`; the landing's PID file
`logs/fable-t-land.pid`, log `logs/fable-t-land.log`). Local editing surface: this session's scratchpad
`wt2` (a git worktree of the mirror at 892647d with the L1 edits). Design: `redregg/work/promo/DESIGN-T.md`.

## Dated lines

- 2026-10-23 20:1xZ READ: IMPACT-PROT-6 §0.6/§3, READ-PROT-6b-grok whole, Lang/{Term,Package,Call,Program,
  Surface,StdOffer,StdOfferEscrow,Journey}.lean, Lang/Wire/Data.lean, Kernel/Receive/{Call,Derive,Authority},
  Lang/Proofs/{Call,CallLive,CallTeeth,Data,Extract,MethodRun,Provenance,Load,StdOffer,StdOfferFuse,StdOfferEscrow},
  Ledger/Proofs/{EscrowRun,EscrowWitness}, decisions/lang.md LANG-21/23/33/75.11/76, GATES-20t, RULINGS R-0069.
- 20:2xZ MEASURED: `grep -rho "(calls [^)]*)" world/` → `(calls (transfer))` ×3 and no-call rows only: NO deployed
  package declares an invoke slot. `git grep callsOf`: Host/Check.lean:98 and Hosting/Proofs/Allowance.lean:63 are
  homonyms (a journal decoder; a private test helper), not twins of Lang.callsOf.
- 20:3xZ READ (Authority.lean:49–61, Derive.lean:188): a nested call's `Req.principal` is the grant's ROOT ISSUER
  (the owner); the design's first idea (take refuses a root call by principal) is impossible; dropped.
- 20:4xZ DESIGN written: DESIGN-T.md (T1 runtime-encodes, not a Term encoder; price; consumer; plants; flag day;
  two landings L1 lang! / L2 lang:).
- 21:xxZ BUILT L1 in wt/fable-t: whole tree green (751 jobs); `lake exe lang-journey` GREEN (LC3 shows o5 received
  n = 4 composed by four relays; LC7 badMethod; LC8 callee refusal `arguments: decode truncated 8 4`).
- MEASURED decls diff (parent 892647d built in wt/fable-t-parent vs candidate, 25 modules): 54 RESTATES-MEANING,
  7 DELETES, 1 moved (Wire.dataTy), 49 added. Hypotheses gained: 1 (callData_isSome invoke clause).
- PLANTS (logs/fable-t-plant{1,2}-*.log): PT1 (slot handed no invoke arm) RED CallLive.callsOf_go_live,
  InvokeTreeWitness.c1_runA, journey RED (33) `calls: c0 args: no invoke arm`; PT2 (encoder dropped) RED
  Call.argsBytes_argsData/argsData_argsBytes, InvokeTreeWitness.c1_runA, journey RED (23) `arguments: decode …
  truncated 0 8` at the callees/takes. Both restored (cmp-verified).
- LANDING L1 attempt 1: REFUSED — main moved 892647d → e96c9a5 (2c3bb09 LANG-75.22 added Lang/Proofs/StdOfferEscrowFuse.lean
  consuming fuse_calls and renamed fuse_resolve → escrow_fuse_resolve; 506bf2c; e96c9a5); merge conflict in
  Lang/Proofs/StdOfferEscrow.lean. Rebased the local L1 commit onto e96c9a5, adapted StdOfferEscrowFuse to the typed
  deal; rebuilt (366 jobs), journey GREEN; decls diff now 55 RESTATES-MEANING / 7 DELETES.
- LANDING L1 attempt 2: `scripts/commit -F logs/fable-t-L1.msg --cross-layer … <25 paths>` launched detached; full judge
  (lang!). LANDED: e2eecce (pushed to origin after one displacement; the full judge ran twice).

- L2 BUILT (not landed): the fuse as two objects. Local worktree `wt3` (scratchpad) = L1 + L2; hbox worktree
  `wt/fable-t2` (at e96c9a5 + the L2 files synced): `lake build Lang Ledger Kernel.Proofs.InvokeTreeWitness
  lang-journey` GREEN (366 jobs), `lake exe lang-journey` GREEN (LF1: X.fuse → Y.take, both offers gone, equal
  sessions; LE1: both legs moved). Whole-tree build GREEN (755 jobs). Plants PT3 (type error at generation: the package no longer checks; journey RED (2);
  callsFuse_means red) and PT4 (fuse_run_sound, noRef_fuse red; journey RED (5): LF1 admitted as half a fuse) done.
  decls map: 19 RESTATES-MEANING / 20 DELETES (in scratchpad `fable-t-L2.msg`). LANG-77 addendum written in wt3's
  decisions/lang.md. L1 landed e2eecce; wt3 rebased onto it (local commit 'L2 wip'); fable-t2 at e2eecce + L2: Lang/Ledger/journey GREEN.
  LANDING L2 attempt 1 REFUSED by closure C3 (a proof module exported `abbrev fuseOkEnv`): made private in both
  proof modules (duplicated, as the other env abbrevs are). LANDING L2 attempt 2 launched (`wt/fable-t2/logs/fable-t2-land.{pid,log}`),
  fast judge (lang:). LANDED e7c2b13 (decls: 39 map lines, 19 declared changes of meaning). cv task 01a16679-198f DONE with
  both hashes. (rebase
  wt3 onto the landed L1: `git -C wt3 rebase <L1 hash>`; the L1 commit in wt3 is the local b2668d1).
  Design notes that changed while building: `offerGuard` admits `invoke fuse` as a consumer; `takeArg` in
  Lang/Proofs/StdOffer.lean takes a `tail` so the take's tree lemmas serve the fuse's 4-field argument;
  `callSlotsOf_two (T U)`; `offer_fields`/`pair_shape`/`keys_shape`/`key_shape`/`offer_shape`/`escrow_fields`/
  `escrow_shape` made public; `EscrowLegMoved` takes the party's argument `ad`; `escrow_fuse_admitted` takes
  `hne : x' ≠ y'` (a fuse of an object with itself is `samePeer`-refused at run time; the theorem does not
  re-derive that).

## Closing state (2026-10-23, ~23:30Z)

- main: e7c2b13 (L2) on e2eecce (L1). Nothing of FABLE-T is unlanded.
- Validation debt per R-0069: L1 ran the FULL judge (lang!) twice (one displacement); L2 ran the FAST judge. The next
  convergence (`scripts/converge`) judges rows/benches/census for L2; the lang-journey was run green by hand on both.
- hbox worktrees left in place (as lanes do): `wt/fable-t` (L1 base, now at e2eecce), `wt/fable-t2` (L2, now at e7c2b13),
  `wt/fable-t-parent` (the decls parent export at e96c9a5). Each holds a ~0.8 GB `.lake`; removable by Ember when wanted.
- Open follow-ups (not cards yet): (a) `escrow_fuse_admitted` takes `hne : x' ≠ y'` which the dispatch could discharge
  (`revisited`); (b) K's trigger (the owner's root `take` is not a fuse) stands as LANG-75.11 left it; (c) a `bytes`-typed
  invoke slot can still forward opaque bytes — nothing deployed does; (d) the surface `(invoke T)` kind has no `.ob`
  package using it yet (Std.offer is Lean-emitted).

## Continuation (for a successor if this session parks) — superseded by the closing state above

1. If `logs/fable-t-land.log` shows a refusal: read it WHOLE and fix forward in wt/fable-t (the judge prints the map
   lines to paste if the RESTATES/DELETES lines are wrong; private names may need the user name instead of the
   `_private…` form). Re-run the same scripts/commit line (it is in the log head).
2. L2 (DESIGN-T §3): the fuse as two objects. `Lang/StdOffer.lean`: `offerFuseArg theta := {keys, pair, theta,
   via}`; `fuse` = `offerTakeTree` with a `done` that returns the take's two edits AND one call
   `invoke <peer> take {keys, pair, theta} budget via` (peer = `ite (deq req.self pair.a) pair.b pair.a`); method
   type `methodTy S (offerFuseArg theta) [offerCallTy theta] (offerTakeRows rels) E 2`; delete `offerFuseBody`'s
   matcher and the `x/y/viaX/viaY` fields. Escrow instance: fuse = escrow take's leg payment + the invoke (two call
   slots). Journeys LF/LE: no Z; B grants X `[invoke take]` on Y; A invokes `X.fuse`; LF7 becomes `peer: samePeer`.
   Proofs: `fuse_calls` → `fuse_run_sound` (model on `take_run_sound`/`take_core`); `fuse_tree`/`fuse_atomic`/
   `jointLaw_sound`/`invitation_once` over the two-object tree (x's rows from fuse_run_sound, y's from
   take_run_sound; one θ by `decodeData_eq_ok_iff`); `escrow_retract_moves_leg`'s fuse case now has a retract
   and a transfer. Plants PT3 (fuse sends `keys` where it sends `theta`) and PT4 (fuse drops its call). Land as
   `lang:` through scripts/commit from wt/fable-t after `git fetch && rebase` onto the landed L1.
3. Decision text for L2: a LANG-77 addendum ("L2 landed <hash>: the matcher deleted; fuse_run_sound; …"), and
   LANG-75.11's fork-M sentences pointed at it.
4. Close the cv task with the L1+L2 hashes: `cv task close 01a16679-198f --hash …` (check `cv task --help`).
