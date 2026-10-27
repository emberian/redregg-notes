# FAERIE-TWINS: nanodregg commit a03855ed (pushed to main)

| item | result |
|---|---|
| conforms_opt (and conforms_empty) | folded: one public theorem in Lang/Proofs/StdActivityMonitor.lean (optD form); StdOffer's copy deleted. Only two copies existed, not three. Built green incl. StdOfferFuse, StdOfferEscrow. |
| hex helpers | partial: Lang.LiveHoles.hexDigit deleted, calls Lang.Print.hexDigit. No hex helpers remain in Codec/ except Digest.toHex. Skipped: Protocol/Command/Text (own layer, proofs unfold UInt8 form), Hosting/Broker Json.hexDigit/hexVal, Hosting/Reply.hexVal, Lang/Read.hexVal. They differ in type (UInt8/Char/Nat) and folding them changes proof statements or layering. |
| Hosting line splitters | already: a single Resident.splitLines |
| textMax vs answerBounds | already: textMax is derived from Lang.Bell.answerBounds |
| rangeRowTy/pointRecTy | skipped: lives in Lang/Package.lean (off limits) |
| Host.Deployed vs Check callsOf | folded: Host.Check.callsOf renamed turnCalls (Lang.callsOf is the other) |
| Expr serializers | already: certificate, decls and JournalExpr are gone |
| Kernel dup detectors, Lang closed/live twins | skipped as instructed |
| Ticks/Lifetime, core_append | already folded (single Ticks, single core_append) |

Built green: Lang.LiveHoles Host.Check Lang.Proofs.StdActivityMonitor StdOffer StdOfferFuse StdOfferEscrow (157 jobs). Rebased onto moved main before push without a rebuild.
