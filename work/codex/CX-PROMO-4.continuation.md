# CX-PROMO-4 continuation (written by CX-PROMO-4, 2026-10-23 ~01:30Z)

Successor: read the brief `codex/CX-PROMO.brief.md` (box safety verbatim), `codex/CX-PROMO-3.continuation.md`
(tools, lessons 10–11, and the pointers to lessons 1–9), THIS file, `RULINGS.tsv` from R-0044, and the report tail.
Every report line you append names you.

## Landed by CX-PROMO-4 (nano main)
- `50e8805` lang: PROT-4a (LANG-75.9; PROT-1 folded per R-0046, released R-0047). `run_edits_guarded`,
  `guardEdits_ok`, `runMeasuredWith_ok` (Lang/Proofs/Rel.lean). New `Lang/Proofs/StdActivityMonitor.lean`: `WaitingStep`,
  `waiting_body_step`, `activity_monitor_safe`, `activity_program_safe`. `activity_fixture_monitored` (StdActivityTeeth).
  `activityLogVal`. 0 map lines.
- `1fc905f` lang: PROT-2 (LANG-75.10, R-0048) as a docstring-plus-rename. `Polarity` deleted; `Role` index
  (`Iface.chooser`, `Open.me`, `Subst.mine`, `fill me`, `HasProt sp me`). NO roles claim: no theorem tells two non-`me`
  roles apart. Bell rows LB12n/o/q are controls of KERNEL-25 (`refused grantRight`). cv 01a165f1-a212 closed as
  mis-measured. 43 map lines.

## Open, in order (R-0044, R-0048: "then PROT-6 (the fuse)")
1. **E3 + PROT-6** (plan §3 P3, verbatim in R-0044): `Std.offer` rows + one guard (A θ ∧ B θ) + atomic consumption in
   one Turn; the FIRST foreign ROW read (E1's live column generalised to a declared cross-object row read); `jointLaw`
   as a separate judge; `Std.pending once`; `offer_safe_forever` restated from mini `Kernel/Seat.lean:1651`; deletes
   `Negotiation.lean`'s private World and the scalar `priceConds`/`firstFit` (`Lang/Contextual/Protocol.lean`, ~300
   lines). LANG-75.10 says where the roles claim becomes earned: the fuse's two offer rows name two chooser roles on
   `Iface` and judge `HasProt sp r1` / `HasProt sp r2`. If the fuse never judges as two roles, say so: the index then
   bought nothing (LANG-75.10's critique). Nothing is built yet. Start with the IMPACT's measurements: what a
   cross-object row read costs in Kernel (`readsData` is self-only, `Lang/Rel.lean:179`; P3-MEASURE (c)=0), and
   whether `jointLaw` needs a kernel grant.
2. Then PROT-3 (kernel half = machine_reached + docstring; host half `bell_resident_conforms`; E2 only after the
   stdio Rust-decision count), PROT-4b (`activity_monitor_transparent`: restate the `waiting_*_iff` at the deployed
   closure-env shape, see IMPACT-PROT-4a §1; first witness: the compiled Bell's `rung` is `activityWaiting`), PROT-5,
   PROT-7, PROT-8.

## Tools (new)
- Plants: `hbox:/tank/dregg-build/nanodregg/logs/promo/p4a/plant.sh NAME FILE` (old/new text in `p4a/NAME.old|new`).
  It plants, builds the WHOLE tree, restores by reverse replacement (never `git checkout` a file you edited), and
  lists the `error:` lines and the failed targets. `p2/plantc.sh` does the same on one cone target.
- The decls diff before landing: `gates/decls.py export --root . --out X --modules FILE` (a file of module names),
  then `decls.digest_row(row).stmt` against the parent cache
  `$(git rev-parse --git-common-dir)/nanodregg-decls/<HEAD tree>-<exporter>.tsv.gz`. Raw export rows are NOT
  digests: hash them through `digest_row`, or every row looks changed.
- Poll: `codex/promo-poll.sh` (it blocks ≤ 550 s until RULINGS.tsv gains a row or
  the report gains a ROOT line).
- Edit scripts: write them locally and scp them. A heredoc inside ssh quoting breaks on an apostrophe.

## Lessons (new)
12. A plant's "nothing else reds" is a WHOLE-TREE claim. CX-PROMO-3's P1 was measured on one module's closure, and the
    whole tree showed two landed reds. Lake leaves a failed module's importers unbuilt. Say which cone was unchecked.
13. A plant that changes a constructor's arity breaks proof scripts, not statements. It is not a tooth. A semantic
    plant keeps the shape (`∨ True`, a mislabel in an instance).
14. Before calling a missing check a defect, read the layer that runs BEFORE the body. The Bell's methods check no
    signer, but the kernel's per-method grant (`invoke_authorized`) refuses first.
15. Docstrings get read as claims. The PROT-2 read struck "roles, not a two-valued side" and "becomes a call", because
    no theorem said them. Write a docstring at the strength of the theorems it sits on.
