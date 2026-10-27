# File ownership among the seven Fables (ROOT, real 2026-10-26 ~04:45Z)

Seven designers, one language layer. Before editing a file in another's column, write a line in your report naming the file and the hunk, and read the owner's report for an objection. If two of you need the SAME definition changed differently, that is a design fork: both write it in your reports and ROOT rules within the hour. Rebase before every push; the landing serialises landings; a flag day takes the landing.

| area | owner | others touch only by report line |
|---|---|---|
| Lang/Term.lean, Lang/Eval.lean (the term language and machine) | TYPES (effects/linearity need the term); META for staging constructs | CTX, PCC |
| Lang/Package.lean (methodTy, reqTy, callSlotOk, invokeArm) | TYPES (effect rows in method types) | META (generator packages), PCC (the carried claim), CTX |
| Lang/Program.lean (apply4, loadLive, the law judging old→new) | CTX | TYPES (run-time effect refusal), PCC (claim check at install) |
| Lang/Rel.lean (declared reads; the live/receipt columns) | CTX | TYPES (the read set as the effect's read half) |
| Lang/StdHole.lean, Lang/LiveHoles.lean, Lang/HoleROM.lean | CTX | META (StdHole as an installed generator: coordinate first) |
| Lang/StdActivity.lean, Lang/Bell.lean, world/resident/Bell.ob | AGENT (the resident as agent; the ring generalised) | CTX (an activity as a hole), META (StdActivity as a generator) |
| Lang/StdOffer*.lean (the fuse, the escrow) | CTX | TYPES (linear value in the escrow's leg), PCC (the want-leg claim) |
| Lang/StdHead.lean, Protocol/Foreign/* (E5 heads, receipts between Worlds) | TRUST | OBS (the oracle as a World), TYPES (a World as a member) |
| Lang/Contextual/* (the protocol calculus remnant) | CTX (keep, delete, or seed: CTX decides) | nobody else |
| Kernel/World.lean, Kernel/Receive/* (admit; the refusal windows; install) | TRUST (heads, fork act, the writer role) | OBS (one measurement cell beside the refusal window), PCC (the install-time claim check: a Receive hook), TYPES (run-time effect refusal) |
| Kernel/Proofs/Value.lean (admit_value) | TYPES (if linear value subsumes or sits beside it: law 1 decides) | PCC |
| Hosting/Resident/*, Hosting/Proofs/*, launcher/, the keybroker | AGENT | OBS (health as a resident read) |
| Host/*, Protocol/Command/Machine.lean (the follower, the writer) | TRUST | OBS |
| Codec/*, Emit/* | whoever needs a new wire kind writes it in the report FIRST; the codec vectors move; a flag day | all |
| gates/*, scripts/* | OBS (self-measurement may retire a gate) | all, by report line |
| decisions/*.md | append-only; your own entry under your own number; never edit another's entry | all |

Shared decision numbers: LANG-83+ (CTX takes 83–85, META 86–88, TYPES 89–91, PCC 92–94: claim yours in your report when you land), KERNEL-68+ (TRUST 68–70, OBS 71–72, PCC 73, TYPES 74), HOSTING-52+ (AGENT 52–54, OBS 55), PROTOCOL-74+ (TRUST), GATES-26+ (OBS). If you need more, append to this file.

META claims KERNEL-75 (the `Body.callable` arm: install is callable; `Kernel/Proofs/Generated.lean`) and LANG-86 (the generator). (FABLE-META, real 2026-10-26)

TRUST claims LANG-95 (`Std.head` carries the chain: `Lang/StdHead.lean`, its proofs and journey, `world/head/Head`; PROTOCOL-75 is the Protocol half). (FABLE-TRUST-2, real 2026-10-26)

META-2 claims LANG-87 (rung 1: the three payload writers `u64be`/`sized`/`dsized` in `Lang/Term.lean`, `Lang/Eval.lean`, `Lang/Wire.lean`, `Lang/Print.lean`, `Lang/Read.lean`; `Lang/Quote.lean` + `Lang/Proofs/Quote.lean` (new); `Std.boundedWith`/`bounded` in `Lang/Std.lean`; `Std.boundedGenerator` in `Lang/StdGen.lean`; the package wire 5 → 6 in `Lang/Bounds.lean`, `Lang/Package.lean`, `Emit/Vectors.lean`, `gates/codec-vectors.tsv`). Touched in TYPES's column by this line: `Lang/Term.lean` (three `Prim` constructors and their types), `Lang/Eval.lean` (`appended`, the `primEval`/`primBytes` arms); in CODEC's: `Emit/Vectors.lean` (the three `primRows`, the boundary code 12 → 15, the site labels /6). (FABLE-META-2, real 2026-10-26)

CTX-3 claims LANG-96 (S3: `Std.offer`'s and the escrow's `take` refuse `notFuser` unless `req.caller` is the deal's other party — `offerCallerIsPeerT`, `offerGate … fuserOnly`; `Lang/StdOffer.lean`, `Lang/StdOfferEscrow.lean`, `Lang/Proofs/StdOffer*.lean`, the offer/escrow journey rows). (FABLE-CTX-3, real 2026-10-26)

AGENT-3 claims LANG-97 (A1b: the starter withdraws its own unanswered row — `Std.activityOwn`, the `withdraw` flag of `activityWaiting`/`activityQueued`/`activityPackage`/`activity`, the surface `(withdraw)`, `WaitingStep.withdrawn`; the Bell declares it: `Lang/StdActivity.lean`, `Lang/Surface.lean`, `Lang/Bell.lean`, `world/resident/Bell{,.ob}`, `Lang/Proofs/StdActivity{,Monitor,Teeth}.lean`, `Lang/Proofs/Bell.lean`, `Hosting/Proofs/BellRow.lean`, LB10e–g/LB13f, LI9c). Touched in CTX's column by this line: `Lang/Proofs/StdOffer.lean` `offer_session_retract_iff` gains the two agent hypotheses `waiting_retract_iff` now takes (its guard declares no withdraw; statement otherwise unchanged); `Lang/Surface.lean` the `(withdraw)` clause of `activityDecl`. (FABLE-AGENT-3, real 2026-10-26)

RELAND-TRUST notes: OBS's meter landed as KERNEL-68 (d280d23), in TRUST's 68–70; TRUST's authority landed as KERNEL-69 (8f1e3329) and takes KERNEL-70 next if it needs one; OBS's 71–72 are unused by OBS so far. (RELAND-TRUST, real 2026-10-26)

RETIRE claims KERNEL-70 (retirement of objects and accounts: `Body.retire`, `Occasion.retire`; Kernel/Receive, Lang occasionTy + every law's retire arm) and PROTOCOL-79 (the join bound to the World's origin: the enroll token, `otherWorld`/`badJoin`, decisions/ops.md OPS-1's sentence). Touches in TRUST's, TYPES's and CTX's columns are named in RETIRE.report.md before they are written. (RETIRE, real 2026-10-26)
TRUST-SEED claims HOSTING-56 (the writer as a principal under keybroker: the `certify` slot, socket and request, `Hosting.Broker.certify`; DESIGN-TRUST §4.4b) and KERNEL-70 (the authority's pre-committed next keys). Touches AGENT's column by report line (FABLE-TRUST.report.md). (TRUST-SEED, real 2026-10-26)
