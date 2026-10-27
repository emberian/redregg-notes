# PERF-CODEC log (continuation file) — started 2026-10-14
Lane: PERF-CODEC (Claude). Front: codec layer only (Compiler/Tower256ConcreteBackend.lean, stream/frame codecs, Kernel/*Codec*.lean).
Lane tree (hbox): /tank/dregg-build/claude-lanes/perf-codec/src, branch perf-codec from lane/perf-fix a16e2f1b → push lane/perf-codec.
.lake: full private copy (cp -a, not -al) of perf-fix/src/.lake (build 746M + packages) — no shared inodes.

## events
- start: item J read at source. fixedStream.decodePrefix `if enough : width ≤ octets.length` (Tower256ConcreteBackend.lean:310).
  Users: Kernel/ObjectiveActivity recordWire (4 digest256 + phase await heights), sourceWire, awaitWire; DurableIndex keys (65-byte buffers, negligible).
  decodeBytesPrefix already has the same fix (@[csimp] decodeBytesPrefix_eq_decodeBytesPrefixTR) — fixedStream is the twin that missed it.
- edit 1: fixedDecodePrefixTR (splitAt + check on the taken prefix) + fixedStreamTR + @[csimp] fixedStream_eq_fixedStreamTR; fixedStream body untouched.
- codec-bench (Host/CodecBench.lean, exe codec-bench): decodeRecord on one awaiting record, N times; perf stat instructions:u, taskset -c 20.
  baseline 33075-octet record x500: 8.740 G (~17.5 M/decode, ~530 instr/octet).
- J MEASURED: d25a20e8 (bench bdd337d1). 2355o x2000 3.607->3.403 G (-5.6%); 8499o x2000 9.723->9.040 (-7.0%); 33075o x500 8.740->8.087 (-7.5%).
  The length walks were a minor share. Profile after J (perf dwarf): List.hasDecEq 38% incl (the strict decoder's `encode v = bytes`
  through the derived List UInt8 DecidableEq: closure call per octet, non-tail recursion), dec_ref 21%, splitAt+reverse (payload takes) 11%,
  re-encode appendTR ~7-12%. pushed lane/perf-codec.
- shape 2 (edit, building): ResourceBirthCodec.bytesEqual MOVED to Tower256ConcreteBackend (one copy; 4 callers renamed); @[csimp] bytesEqual
  twins on Framed.decode (durable log records), DurableReceiverCodec.decode (image), StoreCodec.decodePayload, ObjectiveActivity.decodeRecord.
  ~40 other `encode v = bytes` sites exist (grep list in transcript): NOT touched; the global fix is an instance change (DESIGN, below).
- shape 2 COMMITTED 0029ce9e (pushed). codec-bench after J -> after 2: 2355o 3.403->2.858 G (-16.0%); 8499o 9.040->7.093 (-21.5%);
  33075o 8.087->6.196 (-23.4%), wall 1590->772 ms. Net of fixed setup (~0.26 G), per 33075-octet decode 16.94 M -> 15.64 (J) -> 11.88 M.
  Remaining profile: dec_ref/free/malloc (List churn), splitAt+reverseAux (payload takes), re-encode appendTR.
- candidate chain launched: perf-codec/cand.sh candidate (umbrella ub.sh -> host -> consent -> rust -> pack), PID perf-codec/cand.pid,
  status perf-codec/cand-candidate.status, logs perf-codec/logs/cand-candidate-*.
- same J shape found in Compiler/FnWireGrammar.decode (w ≤ xs.length at uint/bytes/enum/tagArm/sized + (xs.drop w).length for declared
  lengths: O(fields·n), while decodeWithin's doc claims linear work). Off the deployed path (no Host/Kernel import). Twin decodeTR +
  decodeTR_eq (induction on Grammar) + @[csimp] elaborated green in scratch (perf-codec/scratch/fnwire-tr.lean); commit AFTER pack
  (pack refuses a compiled-input change after the host build).
- umbrella (scripts/lane/ub.sh @0029ce9e): every module green EXCEPT two orphan modules, neither touched by this lane or PERF-FIX, neither
  imported by minidregg-host (exe built): Kernel/NativeCurrentMemberKey.lean:42 (calls NativeHostReplay.verifyLoaded with a Durable where a
  DurableHistoryReader.Reader is now expected; stale since the verifyLoaded signature change) and Host/PrivateCircuitPlanFixture.lean:23
  (`toJson` unknown: missing `open Lean`). AxiomCensus green (none on sorry). Not fixed here (outside the codec front); reported to ROOT.
  Candidate continues: perf-codec/cand-rest.sh (host -> consent -> rust -> pack).

## DESIGN (not done here: each changes a type theorems mention)
- D-CURSOR. A ByteArray cursor for the decoder hot loop cannot be attached by @[csimp] without a type change: the decoder IS the
  `StreamCodec.decodePrefix : List UInt8 → Option (α × List UInt8)` field, and its law `decodePrefix_encode` is stated over List.
  A cursor needs a new field (e.g. `decodeAt : ByteArray → Nat → Option (α × Nat)` with a law tying it to decodePrefix on
  `bytes.toList.drop i`), which changes the StreamCodec structure every codec instance and every codec theorem mentions. And the
  decoded VALUES are `Bytes = List UInt8` (record inputs, checkpoints, payloads), so a cursor would still materialize lists; the
  splitAt (2 allocations/octet) would drop to 1, nothing more. The real gain is Bytes = ByteArray in the types (ledger D8, global).
- D-MATCH. The strict decoders still RE-ENCODE the whole value and compare it to the input (after shape 2 the compare is cheap;
  the re-encode's allocations remain, ~1/3 of a decode). Two ways out: (a) a `matches : α → List UInt8 → Option (List UInt8)`
  field that walks the input against the value without building the encoding (a StreamCodec field again: type change); or
  (b) prove each strict codec CANONICAL (decodePrefix bytes = some (v, r) → encode v ++ r = bytes) so the check is a theorem and
  the executable can skip it via @[csimp]. (b) changes no type but needs canonicity of StreamCodec.nat (it accepts high zero
  digits today: NOT canonical, so the check is load-bearing there) — i.e. a wire change to make `nat` canonical first.
- ~40 more `encode v = bytes` strict sites (Compiler/*Codec*, PolicyRecordCodec, NockProgramCodec, PortableHomeTransferCodec,
  GenericSimplex*, JointBackendPartyCodec, Host/*Authoring ...) still compile to List.hasDecEq / List.beq. Shape 2 covered the
  four on the Objective/durable path. The one-line global fix (a high-priority `DecidableEq (List UInt8)` instance via bytesEqual)
  would change the instance inside every downstream statement that decides byte equality: a term-level statement change, so not here.
- candidate perf-codec/candidate @0029ce9e (host sha 28b2ef82…; baseline perf-fix/candidate @a16e2f1b host fbcfb2e3…).
- rows on perf-codec/candidate: journey PASS, call PASS (63), send PASS (192), objectrecord PASS (39). (perf-codec/rows-J/)
- c92e4ea1 FnWire shape committed+pushed (NOT in the candidate; Host.FnOutcome/Host.Main import FnWire, so it IS on the host path).
  check-fn-wire.sh PASS. FnWire family + Host.Main build green.
- kn2-store-bench (1000-byte cells, no fixed fields) perf-fix bench-after1 vs this lane: cold full open 512 rec 161-164 -> 145-150 ms,
  open+append 191-222 -> 171-176 ms; whole run 86.61 -> 86.26 G instr (the run is dominated by growth, not decode).
- workload N=32 M=32 K=16 (instr:u per phase, box loaded, PERF_UNDER_LOAD=1): run-to-run spread is ~±10% (polling scales with wall):
  before(a16e2f1b) births 2313 G updates 2262; after run1 2533 / 2583 (box busier), after run2 2113 / 2142. Two more interleaved
  pairs running (perf-codec/pairs.sh, pairs.pid) before quoting a number.
- WORKLOAD VERDICT (N=32 M=32 K=16, instr:u, interleaved pairs on the same box, before = perf-fix/candidate a16e2f1b, after = 0029ce9e):
  pair3 births 2021.9 -> 2034.9 G, updates 2080.0 -> 2100.5; pair4 births 2021.2 -> 1982.3, updates 2143.8 -> 2078.8;
  reads 843.9/863.0 -> 851.4/854.3; judgment 210.5/205.4 -> 216.2/207.8. NO MEASURABLE CHANGE (within the ~±2% pair spread;
  unpaired runs spread ±10% with load). The codec decode is not a material share of a birth at this point; the micro gain (-30% per
  record decode) is real but decodes are a small fraction of the per-request instructions (which are dominated by the items A/B/C/D work
  and the ~0.38 G per spawned Host). Raw: perf-codec/wl-J-{before,after}{,2,3,4}.out, /tmp/pcw-J-*.
- shape 3 (edit, building): decodeBytesPrefixTR / fixedDecodePrefixTR take the prefix by List.take (compiled takeTR: array, then one
  cell per octet) instead of splitAt (reversed prefix + reverse: two cells per octet + a freed list).
- shape 3 MEASURED WORSE, REVERTED (never committed): List.take (takeTR: Array push + toList) instead of splitAt in the two executable
  twins: codec-bench 2355o 2.858 -> 2.997 G (+4.9%), 8499o 7.093 -> 7.579 (+6.8%), 33075o 6.196 -> 6.648 (+7.3%). splitAt's cons+reverse
  on mimalloc's small-object path beats the array round trip. splitAt stays.
- final verification: umbrella at HEAD c92e4ea1 running (scripts/lane/ub.sh umbrella-c92e4ea1 -> src/build-logs/umbrella-c92e4ea1.log,
  perf-codec/logs/ub-final.out; PID perf-codec/build.pid). Expected: green but the two pre-existing orphan reds.
- FINAL: umbrella at HEAD c92e4ea1: everything green except the same two pre-existing orphans (Host.PrivateCircuitPlanFixture,
  Kernel.NativeCurrentMemberKey); AxiomCensus green, none on sorry. .lake in perf-codec/src matches HEAD.
  Branch lane/perf-codec = c92e4ea1 (bdd337d1 bench, d25a20e8 J, 0029ce9e bytesEqual strict decoders, c92e4ea1 FnWire), pushed.
  Candidate perf-codec/candidate is @0029ce9e (no FnWire). Untracked in the tree: scripts/perf/ (copied from lane/perf-workload d37eee80
  for the workload runs; not committed), build-logs/, .minidregg-native-snapshot.
