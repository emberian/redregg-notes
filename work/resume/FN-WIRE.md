# FN-WIRE (a09e2ea1b3ec8a5cc) -- resume note
Where it was: "BLAKE3 matches all 35 official vectors. Now the fncu cursor module." (earlier: "Proofs are clean."). Mission: Lean interpreter of fn's wire grammar (fn lane/mini-contract@5329b38cb specs/wire-grammar.json) + two round-trip theorems + BLAKE3 + pinned loader + CI row + replace fncu hand-parser.
Lane: persvati ~/workbox/claude-lanes/fn-wire/src (persvati), branch lane/fn-wire @ec53f8c2 (base 3b709c87; its 2 commits = the fn boundary commits already landed on main as 7ba967b3/1637417d). Uncommitted/untracked: Compiler/Blake3.lean, Blake3Kat.lean, FnWireFncu.lean, FnWireGrammar.lean (+ others; scratch/ dir).
WIP branch: lane/fn-wire-wip @3142e858 (6 files, +2060). Note: persvati lane had no `github` remote; I fetched refs/remotes/github/main (66e3c5b5) into this repo from ../agreement/src (refs only).
Builds: no build log in the lane (logs/ empty); results reported by the agent in-transcript only (proofs clean, BLAKE3 35/35 KAT vectors via scratch run). Treat as UNVERIFIED in the lane tree: compile first.
Main since pause: 20 landings since 3b709c87 (fn boundary landed; pins moved: lean-build-surfaces.json, host-closure.pin will conflict).
Bundles: persvati:/home/ember/workbox/claude-lanes/bundles/fn-wire.bundle (prereq 3b709c87; contains -wip), scholar-fn.bundle in lane dir.
Next step: `git rebase github/main` on lane/fn-wire-wip (or checkout it), finish the fncu cursor module + pinned-file module + CI row, `lake env lean` each new module, regenerate pins.

Written by FAIRY-RESUME 2026-10-04 ~18:40Z. main = github/main 66e3c5b5 (== burst-gate /srv/warm-base/src; umbrella green: /srv/warm-base/logs/green-66e3c5b5.log rc=0 18:21Z). Pause was ~18:00Z (usage wall). Boxes die 2026-10-05T15:55Z. Bundles are THIN (need prereq on main).

## VERIFIED by FAIRY-FIX 2026-10-04 ~18:55Z (burst-gate, lane /srv/lanes/fairy-fnwire, branch lane/fairy-fnwire @ d69ab3f4 + the 6 untracked files from persvati fn-wire/src copied verbatim, uncommitted)
GREEN. lane-check, in dependency order, all rc=0, no error/warning output (logs: burst-gate:/srv/lanes/fairy-fnwire/logs/FnWire*.log):
Compiler/Blake3.lean, Blake3Kat.lean (native_decide + #assert_compiled, 35 official vectors + fn trailers), FnWireGrammar.lean, FnWireJson.lean, FnWireRoundTrip.lean (axiom-pinned: decode_encode, encode_decode, decodeAll_*), FnWireFncu.lean (imports Kernel.FnConsumerScope; #assert_axioms clean). No sorry.
Not found / not yet written: a CI row or script, Compiler.FnWirePinned (the pinned loader named in Blake3Kat's docstring), the fncu hand-parser replacement; no lakefile/pins/surfaces entry for the 6 modules (lean-build-surfaces.json will need them).
Vector run (no script exists; scratch driver burst-gate:/srv/lanes/fairy-fnwire/RunWg.lean calls FnWire.checkDoc): fn lane/mini-contract:specs/wire-grammar.json (1e38bb67a) -> `OK families=3 accepted=31 refused=218` = all 249 vectors agree (the 5329b38cb version has only 10). Planted fault (a vector's `consumed` 97->98) -> `RED ... consumed 97, the file says 98`.
Remaining for this lane: pinned-file module + CI row + surfaces/closure pins + replace fncu hand-parser, then queue.

## VISIT (VISIT-B, 2026-10-04 ~19:20Z; main d27d1cad)
VERDICT: READY.
- Verified: persvati lane/fn-wire-wip 3142e858 = the 6 new modules only; its 2 base commits LANDED (48cf51f0=7ba967b3, ec53f8c2=1637417d by patch-id). The 6 files in burst-gate:/srv/lanes/fairy-fnwire/src are byte-identical to 3142e858 (sha256).
- Prepared: branch lane/fn-wire-visit @f5bdcaa5 in burst-gate:/srv/lanes/fairy-fnwire/src = main d27d1cad + one WIP commit of the 6 files. Main moved d69ab3f4..d27d1cad by scripts only (deploy/candidate, scripts/pipeline), no Lean, so FAIRY-FIX's lane-check green (6 modules) and the 249-vector run stand; not re-run (VERIFY-ONCE).
- Still stale: Blake3Kat.lean:71 docstring cites fn 5329b38cb; FnWireGrammar.lean:6-7 promises a vendored protocol/fn/wire-grammar.json that does not exist yet; Compiler.FnWirePinned (named in Blake3Kat and FnWireFncu docs) is not written.
- Next 1-2 h (burst-gate; lane-check single files, one slot only for the final closure build): vendor fn lane/mini-contract@1e38bb67a specs/wire-grammar.json (47340 octets, BLAKE3 68a681bf...047c) as protocol/fn/wire-grammar.json; write FnWirePinned (digest check with the Lean BLAKE3 + all 249 vectors, planted-fault red); CI row; umbrella imports + surfaces/closure pins; then the fncu hand-parser replacement; queue. The scratch driver burst-gate:/srv/lanes/fairy-fnwire/RunWg.lean is the vector-run template.
- Dependencies: none blocking. FN-DIRECT consumes its decoders (FN-DIRECT uses Host.FnOutcome until then).
