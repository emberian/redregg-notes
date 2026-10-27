# GUARDS log (continuation file) — started 2026-10-14
Lane: GUARDS (Claude). FOLLIES-20261014 §1: 4,392 #guard on next, no guard-discipline check in Mini.
Lane tree hbox:/tank/dregg-build/claude-lanes/guards/src, branch guards @ next 0125b224. git grep count 4414 (raw, incl. comments).

## events
- start: read SAFETY-BLOCK, Bread GUARD-DISCIPLINE.md + check-guard-discipline.py; Mini has Theory/AssertCompiled.lean + Theory/AxiomPin.lean.
  Plan: port as scripts/gates/check-guard-discipline.py (self-contained stripper + char literals), baseline scripts/gates/guard-discipline-baseline.txt,
  rows in merge-gate-checks.sh and local-gates.sh.
- RATCHET LANDED 1a5a52f4 (lane/guards on mirror; GitHub: hbox has no key -> ROOT). Ratchet 70.
  ⚑ FOLLIES count wrong: ~4,300 of "4,392" are `#guard_msgs (…) in #print axioms` exact axiom pins (not counted). Real: 70 #guard in 7 modules;
  Host closure holds only Compiler/NativeObservationCodec (4). Reported to ROOT. NEXT: convert all 70 (NativeObservationCodec first).
- conversions drafted (all 70) in lane tree, uncommitted: NativeObservationCodec (validBatch_iff ∀ + 4 kernel instances),
  NPHA (priorBounds_iff, priorReceiptMatches_iff, pinHeader_message/nullifier ∀, same_height_prefix_excludes_next ∀; prepare/fence/pin
  fixtures native_decide), WorldKindChecks (∀: toLawful_decode_encode_append, decodeDefinition_encode_append/_isSome_iff, Instance
  decode_encode + decode_encode_append, lower_unknown_field, lowerAll/prepare_eq_none_of_mem; instances kernel or native),
  KeyRotationInspectionChecks/CarryConfigurationChecks/LegacyStoreCarryChecks/probe-fn-portable-line native_decide.
  .lake/build = full cp -a of hyp-instances (at 0125b224), packages cp -al from warm-7dea0626.
  build b1 (run/b1.pid, run/b1.log) waiting on a lean slot.
- b1 (run/b1.log): NativeObservationCodec + NPHA GREEN (native_decide/#assert_compiled resolve transitively in NPHA). Fails fixed:
  CarryConfiguration/LegacyStoreCarry/WorldKindChecks lacked `import Theory.AssertCompiled` (added; import-boundary OK, host-closure OK 775);
  WorldKindChecks: `lower` ambiguous (-> WorldKindInstance.lower), decode_encode_append proof reworked (first|… fallbacks); decode_encode GREEN.
- b2 (run/b2.pid) 20:50: hbox in ZFS iowait 67% (txg_sync D, swap full); lean procs 8 s CPU in 33 min. Waiting.
- b2/b3 GREEN: all touched modules + Host Host.Main (EXIT=0), probe script elaborates. COMMITTED e22cdedc (lane/guards on mirror): 70 -> 0.
  77 theorems: 14 general (validBatch_iff; priorBounds_iff, priorReceiptMatches_iff, pinHeader_message/_nullifier, same_height_prefix_excludes_next;
  WorldKind: toLawful_decode_encode_append, decodeDefinition_encode_append/_isSome_iff, Instance decode_encode/_append, lower_unknown_field,
  lowerAll/prepare_eq_none_of_mem), 16 kernel instances, 47 compiled (40 library + 7 probe).
  Ratchet: empty gate-written ledger = green, missing = red (self-test arm). --rev HEAD PASS.
  OPEN (design note): the WorldKind ∀ facts live in Kernel/WorldKindChecks, not beside their defs (WorldKindInstance/WorldKindDescriptor/
  Tower256ConcreteBackend.StreamCodec); moving them = rebuild (Tower256 one = whole tree). Offered to ROOT.
  GitHub push: hbox has no key -> ROOT.
- FINAL: ROOT pushed e22cdedc to GitHub. Ruling: the WorldKind ∀ facts STAY in Kernel/WorldKindChecks for now; CODEC-SHAPES carries
  toLawful_decode_encode_append (and may carry the rest) to its natural home during its Tower256 canonical-codec flag day.
  Lane GUARDS done: ratchet 1a5a52f4 + conversions e22cdedc; Mini #guard population 0, gated (merge-gate + local-gates rows).
  Lane tree hbox:/tank/dregg-build/claude-lanes/guards/src left in place (.lake/build full copy ~1G; run/ logs b1-b3, probe).
