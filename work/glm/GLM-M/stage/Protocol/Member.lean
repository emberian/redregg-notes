/-
# Protocol.Member — the member surface, as one table

Every act the kernel admits (`Body`'s constructors, the head acts, the cancel, the adoption) and
every verb of the one command language, each with the `nd` form that reaches it, the page's form,
the test that proves a member reaches it, and the refusal names a member can see from it.
`docs/MEMBER.md`'s table is `Emit.Member`'s output from `rows`, checked at every convergence
(`gates/generated.tsv`); the theorems below are the build's own check, so the table cannot go
stale: a `Body` constructor without a row breaks `body_row`, a verb without a row breaks
`verb_row` (`#eval`-free: both are discharged by computation, at every `lake build`).

The one act with no member path is named here, not hidden: `carry`, the operator's export and
import of a World's state (KERNEL-29; `Host.Carry`). A member meets a carried World as an
invitation to it (`nd adopt`), never as the carry itself.
-/
import Kernel.Receive.Call
import Protocol.Command.Verb

namespace Nanodregg.Protocol.Member

/-- One row of the member surface: an act, and every way a member reaches it. -/
structure Row where
  /-- the act's name: `Body`'s constructor (`act`), or one of `named` (the protocol acts and the
  verbs that sign nothing) -/
  act : String
  /-- the `nd` form (the page's terminal takes the same words, without the `nd`) -/
  nd : String
  /-- how the page reaches it, where that is not simply typing the same words -/
  page : String
  /-- the row (an in-process journey of `Protocol.Rows`) or the client test that proves a member
  reaches it, or what the Machine lacks -/
  proof : String
  /-- refusal names a member can see from it (the act's own, not the shared wrongWorld,
  unknownKey, badSignature, stale, overPrice) -/
  refusals : String

/-- The table, one row per act. -/
def rows : List Row := [
  ⟨"enroll", "nd enroll TOKEN", "a hosted tab: init, then the guest-book enrols the token",
    "rows journey, invite; client tests join.rs",
    "badPossession, enrollSpent, unrooted, rightTarget, grantWidens"⟩,
  ⟨"rotate", "nd rotate", "typed (a member's own key change)", "row rotate; client tests custody.rs, roundtrip.rs",
    "notPrecommitted"⟩,
  ⟨"install", "nd install TEXT", "typed; the demos install the shipped packages",
    "rows journey, laws; client tests doc.rs", "badPackage, program"⟩,
  ⟨"create", "nd create [STATE LAW...] or nd create --pkg PKG STATE LAW...", "typed; the demos birth objects",
    "rows journey; client tests doc.rs, pin.rs", "lawDenied, stateKey, tooManyLaws, missingCell, idTaken"⟩,
  ⟨"createOf", "nd create --of TEXT STATE LAW...", "typed",
    "client tests createof.rs; a method's own createOf call is reached by invoke (the page's creator demo)",
    "badPackage, program"⟩,
  ⟨"write", "nd write OBJ K VALUE [--via GRANT]", "typed; the demos write slots",
    "rows journey; client tests real.rs", "noGrant, hasMethods, lawDenied, unpinned, stateKey"⟩,
  ⟨"law", "nd law OBJ LAW... [--via GRANT]", "typed", "row laws", "tooManyLaws, lawDenied, hasMethods, noGrant"⟩,
  ⟨"invoke", "nd invoke OBJ METHOD ARGS [--range REL K [PREFIX]] [--pin [OBJ/]REL KEY]... [--via GRANT]",
    "typed; the demos invoke methods", "rows use, rangeInvoke; client tests pin.rs, doc.rs",
    "noMethods, program, overTicks, overPrice, rowUnpinned, rangeUnpinned"⟩,
  ⟨"grant", "nd grant TARGET or ACCOUNT or world MEMBER or anyone RIGHTS [--via PARENT]",
    "typed; the demos share objects", "rows journey; client tests real.rs, pin.rs",
    "grantTarget, grantRight, grantWidens, unrooted, rightTarget, grantTooDeep, enrollSpent"⟩,
  ⟨"retire", "nd retire CELL", "typed; a demo retires a grant, another a shared object",
    "client tests pin.rs, doc.rs (no row yet)", "notOwner, valueRemains, lawDenied, rowsRemain, noGrant"⟩,
  ⟨"issue", "nd issue CAP", "typed", "rows pay, well", "overflow"⟩,
  ⟨"account", "nd account ASSET [--owner OWNER]", "typed", "rows pay, well", "idTaken, badAccount"⟩,
  ⟨"transfer", "nd transfer SRC DST AMOUNT [--via GRANT] [--once HEX]", "typed",
    "rows pay, well, bounty; the once key's attempt in client tests run.rs",
    "transferSpent, spent, belowFloor, zeroAmount, sameAccount, assetMismatch, overflow, notWell, noGrant, badAccount, badOnce"⟩,
  ⟨"credit", "nd credit WELL ACCT AMOUNT [--via GRANT]", "typed", "row well",
    "creditSpent, notIssuer, notWell, belowFloor, zeroAmount"⟩,
  ⟨"attest", "nd sync --attest", "typed", "row fork",
    "ahead; the checker's side: badAttestation, otherWorld, badHeadSignature, notMember, staleKey"⟩,
  ⟨"post", "nd sync --post OBJ", "typed", "rows selfHead, selfHeadPage",
    "noMethods, program; a follow that reads the post: forkedSelfPost"⟩,
  ⟨"cancel", "nd cancel CALL", "typed; a caught scene cancels its loose call",
    "rows cancel, cancelLie, cancelForged", "cancelled, outsideWindow, refusedFinal, committed, hostContradicted, cancelForged"⟩,
  ⟨"adopt", "nd adopt INVITE KEY (bare: nd adopt KEY_FILE, the kept invitation)",
    "typed only: the page's join is the thick path (host join); no thin-joiner scene yet",
    "rows thin, thinStale, seal, basePin, beforeLog; client tests join.rs",
    "badPage, pageMismatch, notAtGenesis, notBehind, wrongWorld, noBase, certified"⟩,
  ⟨"read", "nd read OBJ [KEY=VALUE...] or nd read OBJ ? or nd read OBJ REL K [PREFIX]",
    "typed; every object window reads the object", "rows describe, state, range; client tests real.rs, pin.rs",
    "unpinned, missingCell, wrongKind, expect, rowUnpinned, rangeTooLong"⟩,
  ⟨"sync", "nd sync [--to STEPS:CHAIN] [--check ATTEST]", "typed; a hosted tab's first command is sync",
    "rows fork, coldCatchUp", "forkedWorld, ahead, unreached, behind, chainMismatch, pageTooLong, eventMismatch, pageIo"⟩,
  ⟨"receipt", "nd receipt CALL", "typed; the attempt store's confirm runs it",
    "rows receipt, settle", "badCall, badToken"⟩,
  ⟨"health", "nd receipt --health [MEMBER]", "typed; the meter strip under every command", "row health",
    "badDigest"⟩,
  ⟨"invite", "nd invite [INPUT] (bare: the kept genesis input)", "typed", "row invite; client tests doc.rs, join.rs",
    "noBase, baseMismatch"⟩,
  ⟨"init", "nd init SPONSOR", "typed; a hosted tab runs it as it joins", "rows journey, invite; client tests join.rs",
    "badDigest"⟩,
  ⟨"join", "nd --join KEY_FILE INVITATION STORE /ABS/HOST", "the join-hosted form; the join HEX paste",
    "client tests join.rs", "the host's INVITE_REFUSED (an invitation the sponsor did not sign)"⟩,
  ⟨"genesis", "none: the operator founds the World (host genesis); the member's side is nd --join and init",
    "the founding form (Re-genesis); a hosted tab joins world.json's invitation", "row journey; client tests join.rs",
    "usage, badToken"⟩,
  ⟨"carry", "none: the operator carries a World's state across Worlds (host export, host import; RUNBOOK §5). A member meets the carried World as an invitation to it (nd adopt), never as the carry",
    "none", "row carry (the operator drives it)",
    "the operator's carryMismatch, wrongWorld; the member's beforeLog, wrongWorld"⟩
]

/-- The act a body is: its constructor's word (`Rows.Loopback.kindName`'s words). -/
def act : Body Nat → String
  | .enroll .. => "enroll" | .rotate .. => "rotate" | .install .. => "install"
  | .create .. => "create" | .createOf .. => "createOf" | .write .. => "write" | .law .. => "law"
  | .invoke .. => "invoke" | .grant .. => "grant" | .retire .. => "retire"
  | .issue .. => "issue" | .account .. => "account" | .transfer .. => "transfer" | .credit .. => "credit"

/-- The acts that are not `Body` constructors: protocol acts, and the verbs that sign no call. -/
def named : List String :=
  ["attest", "post", "cancel", "adopt", "read", "sync", "receipt", "health", "invite", "init",
   "join", "genesis", "carry"]

/-- **Every act the kernel admits has a row**: each `Body` constructor's word is a row's act. A
constructor added to `Body` without a row fails here, at every build. -/
theorem body_row (b : Body Nat) : (rows.map Row.act).contains (act b) := by
  cases b <;> rfl

/-- **Every verb of the one command language has a row**: each verb's word begins some row's `nd`
form. A verb added to `Verb.all` without a row fails here, at every build. -/
theorem verb_row : Verb.all.all (fun v => rows.any (fun r => r.nd.startsWith v.word)) := by
  decide

/-- Every row's act is a `Body` constructor's word or one of `named`: no row names an act nothing
reaches. -/
theorem rows_known : rows.all (fun r =>
    (["enroll", "rotate", "install", "create", "createOf", "write", "law", "invoke", "grant",
      "retire", "issue", "account", "transfer", "credit"] ++ named).contains r.act) := by
  decide

end Nanodregg.Protocol.Member
