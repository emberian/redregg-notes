# DEPUTY-KERNEL continuation (written by DEPUTY-KERNEL itself, 2026-10-07 evening)

Supersedes DEPUTY-KERNEL-CONTINUATION-20261007.md. Running log: DEPUTY-KERNEL-STATUS-20261006.md (tail = newest).
Rules: DEPUTIES-20261006.md amendments; queue/README.txt.

## Routing (ids)
- MERGE-KEEPER: a41926dfb4ce97d3d (address by id; "MERGE-KEEPER" does not resolve). RETIRED, never message:
  a7d2124b6a09fa293, a6ac8c6c04f9b7d97.
- DEPUTY-PLATFORM: aed11e1555308dbcb (a4b57de3 retired). DEPUTY-OB-ENG: a7ce8f0f4cba1d908. ROOT: "main".
- Retired workers (never message; a message wakes them): a05080ba, abc2735a, adfa8411, a3ca8f60, a7c778c2,
  a1ff4ff3, aceeeb0d, a0793682, a1c9ff86, acf817bb.
- Shared remote burst2-a:/srv/git/minidregg.git is AUTHORITATIVE (GitHub is a mirror).

## ROOT rulings in force (burn)
- Keep replacing only for check-gap work (KN2-TRIE line). Row E: no more replacements tonight; remaining row E in cv
  for Ember: (b) 01a1180e-7140 paying upgrades/publish, (c) 01a1180e-715b seats signature-first (DoS),
  01a1180e-7175 postage only covers root load, 01a117cd-8596 (OB-ENG ruled C: cache entry replay per pin per turn).
- Birth port after trie B only if KN2-TRIE-C has room (<~300K); else it waits.
- Briefs narrow: exact files + theorem names, no re-census.

## WIND-DOWN STATE (ROOT, ~late 10-07; usage walls)
- All workers told to stop at a safe point, push, write continuation. No new spawns.
- main=green=cfdaf64d. next=68f78d23 (b31 = kn2-trie-b1, index/trie-v2 flag day; keeper regens fixture then gates).
  b30 (kn2-coproc-census) clears the b28 token-census red.
- KN2-TRIE-C a640a84085ac8ab63: B1 queued/picked; B2 approved by ROOT (evidence: forged-opening plants vs deployed
  digest for new families; per-name successor lines for old index removal); its continuation CONTINUATION-xi.txt
  (scratchpad/kn2-store-open/). Then doc-history (lane/kn2-doc-history3 a47b4f45, rebased + probe seed fix; DECISION
  queue as-is per compiled timings work/burn/STORE-COMPILED-TIMINGS.md; cv 01a1186d-687d), then birth (morning).
- MY OWN OPEN ITEM: ResearchWip drift (ROOT): 5 modules fail at cfdaf64d on the ground API change —
  Kernel.NativeCurrentMemberKey (also imported by NativeCurrentMemberKeyIO), Compiler.PortableJointCustodyIO,
  Kernel.JointReservationFunding, Kernel.RoomReleaseCurrent (<- RoomReleaseAuthority),
  Kernel.PortableHomeTransferAdmission (<- PortableHomeTransferReceiver). Port if live research else delete with import
  lines; then add ResearchWip to scripts-elab roots (check-scripts-elab.sh SCRIPTS_ELAB_ROOTS). Lane burst2-a
  kdk-replay branch lane/kn2-researchwip (no edits yet; a survey build was running).
- BURN-MUTATE (a49d5a831607517f3) final list pending: act only on survivors that also survive journeys; route Seat* to
  OB-ENG, Pay* ours; file cv. Interim: work/burn/interim1-kernel-survivors.txt.
- PORT-B retired: lane/kn2-port-b2 reconcile cv 01a118de-3019. PORT-D retired: doc-history above.
- All 45 unpushed kernel-lane branches archived on shared remote as lane/archive-<host>-<lane>-<branch>.

## Active worker (superseded by wind-down above)
- KN2-TRIE-C a640a84085ac8ab63 (opus): trie sub-range B (design scratchpad/kn2-store-open/TRIE-B-DESIGN.txt; my
  rulings recorded in its CONTINUATION-x + my message: presence keyed by subject, touched dropped, who bounded
  4096/65536 refused `limit`, withheld-leaf plant; backlinks hash order; transclusion backlinks on D w/ completeness
  theorem; last-write-per-cell w/ drop+re-add plant; since/tail deferred w/ cv + ratchet note; epoch index/trie-v2).
  Split B1 (families/rows/model/audit/flag day) then B2 (pages/queries/controller+fleet/deletions/plants). It spawned
  ONE implementer sub-agent; told no more. Then birth port (cv 01a11791-5c66 probes) only if room.

## In flight at writing
- gate b28 on next 5b54d6de (row-e-d7, coproc, d7-authority 321290 derived). main=green=65181dbd.
- kn2-row-e-a queued (5b54d6de..d4b1c503): PLAN/v4 flag day; commit has NO successor lines though it deletes
  invoke frontEndPaid + Mail.empty: if ledger shows removed rows, I write reasons. Close cv 01a117cd-857b on landing.

## Landed today (closed cv): 01a1163e-62a7 neutral births; 01a11742-712b spent verifier unified.
## Open cv I hold: 01a11741-1af8 (AuthTrie verify_complete/insertRoot_eq unproved; incremental root probe-checked),
01a11794-cacd (plants), 01a11794-cab3 (trie B), 01a114aa-6780 (fleet ops), 01a117a6-ccc2 (IO.Process.output leak class),
01a1172e-43a0 (light carry), 01a1172e-43ba (consensus prefix suffix replay), 01a1172f-3ca5 (undisclosed operator vis).

## How I review / land my own fixes
Lane burst2-a:/srv/lanes/kdk-replay (private cache PIPELINE_LAKE_CACHE=/srv/lanes/kdk-replay/private-lake-cache;
lane-check / lake-slot). Edit via python scripts scp'd from scratchpad/kernel/ (zsh quoting over ssh is fragile).
Ledger reasons: keeper sends work/logs/bNN-removals-for-KERNEL.tsv; reply file *-REASONS-from-KERNEL.tsv
(`<name>\t<successor:|derivable:|obsolete:> ...`), successors must exist (private names OK since keeper 9fe4fd68).

## FINAL (after wind-down)
- green = main = cfdaf64d (b28-b30, 0 reds). next = 68f78d23 (b31 kn2-trie-b1) published, UNGATED; resume steps in
  MERGE-KEEPER-STATUS-20261007.txt (WIND-DOWN section). Keeper id a41926dfb4ce97d3d.
- KN2-TRIE-C STOPPED: scratchpad/kn2-store-open/CONTINUATION-xi.txt + B2-CONTINUATION.txt (implementer stopped before
  code; findings: family 7 needs a bounded rank-ordered walk for pages since readSubtrees reads whole subtrees; cursor
  edge decisions; successor theorems in a module off the exe-root path; PresenceIndex.cellsOf + LinkIndex.latestLinks
  must move before deleting the old modules). Pushed: lane/kn2-trie-b1 9f35b372, lane/kn2-trie-b2 (= b1, no code),
  lane/kn2-trie-b-wip d5226b3a, lane/kn2-coproc-census 395fcbc4. Order next: B2 -> doc-history -> birth.
- No kernel workers live.

## ResearchWip survey result (measured at cfdaf64d, burst2-a lane kdk-replay; no edits made)
Importer chains: NativeCurrentMemberKeyIO <- Host/CurrentRecipientVerifier.lean + ResearchWip; RoomReleaseAuthority <-
Kernel/RoomReleaseIntent.lean + ResearchWip; PortableHomeTransferReceiver <- ResearchWip only. (Check whether
Host/CurrentRecipientVerifier and Kernel/RoomReleaseIntent are themselves in any built target before deleting.)
First errors:
- Kernel/NativeCurrentMemberKey:42 type mismatch (verifyLoaded now takes a Reader) -> small port (Reader pattern 36fdf343).
- Compiler/PortableJointCustodyIO:21/57/89 type mismatch, implicit `reservation`, unsolved goals; :108 theorem rests on sorryAx.
- Kernel/JointReservationFunding:31 type mismatch; :45 theorem rests on sorryAx.
  -> both carry sorry-dependent theorems already: 10-03 swarm WIP; strong DELETE candidates.
- Kernel/RoomReleaseCurrent:30 Ground has two constructors (anonymous ⟨⟩), :69/:90 PreparedOn.authority gone, :84 unknown Recipient.
- Kernel/PortableHomeTransferAdmission:42-53 `ground` / ground.view.* unknown (half-ported in efbac239).
Then: add ResearchWip to SCRIPTS_ELAB_ROOTS (or its own gate row) so drift goes red.
