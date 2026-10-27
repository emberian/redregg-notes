# FAERIE-FINDINGS

Landed `e4b38672` on nanodregg main (prose only: nothing re-emits, no format changed). Touched Lean modules rebuilt green (Kernel.Bounds/Turn/World/Receive.Call/Receive.Follow/Sim/Sim.Gen, Protocol.Table/Proofs.Table/Command.*/Head, Host.Follow, Lang.Claim). PROTOCOL-82 is on main; its rename of the Spec claim (decision 6) is not.

## Language (SPEC-DOCS "mine")
| # | result |
|---|---|
| 1 Surface lacks holes; grammar omissions | held: LANG-SURFACE (Lang/Surface, Read, Print) |
| 2 `ob (check P)` cannot check a contextual package | not filed, not fixed (code behaviour; no existing task found); LANG-SURFACE may cover it |
| 3 Lang/Claim.lean docstring | fixed at Lang/Claim.lean |
| 4 law/guard ticks unmetered | filed 01a17d72-9404 |
| 5 holeDerivationMoved name | filed 01a17d72-9427 |
| 6 selectHole docstring overstates | filed 01a17d72-943a (Lang/Contextual held by CTX-5) |
| 7 no top claim for holes over history | filed 01a17d72-944d |
| 8 only methods edit rows | statement of fact, nothing to fix |

## Kernel
| # | result |
|---|---|
| 1 chainNext roots | fixed Kernel/World.lean |
| 2 World.refusals field | fixed Kernel/World.lean |
| 3 refusalCount/Total "height H" | fixed Kernel/World.lean |
| 4 born ids | fixed Kernel/Turn.lean, Kernel/World.lean `bornId` |
| 5 World.credit | fixed Kernel/Receive/Call.lean |
| 6 lawDenied | fixed Kernel/Receive/Call.lean |
| 7 Right.observe | fixed Kernel/Receive/Call.lean |
| 8 overBound event, two bounds | fixed as a docstring on `Bound.event` (Kernel/Bounds.lean); a second constructor is not added |
| 9 Verdict.name collisions | filed 01a17d72-9462 |
| 10 root grant on unowned cell; account asset not a well | filed 01a17d72-9475 |
| 11 KERNEL-54 staleRecorded/auditRefusal | fixed (correction note in decisions/kernel.md; HOST-78 deleted them) |
| 12 KERNEL-66 Audit.lean | fixed (correction note, decisions/kernel.md) |
| 13 two KERNEL-76 | fixed: the row-touch entry is now KERNEL-78 (nothing referenced it); 72 and 74 stay unused |
| 14 MEMBER revoke | already fixed by 992ec055 |
| 15 OVERVIEW duplicate | already fixed by 992ec055 |
| 16 Sim.nameOf | fixed Kernel/Sim.lean, Kernel/Sim/Gen.lean |

## Protocol
| # | result |
|---|---|
| F1 "nd decides nothing" | fixed docs/MEMBER.md and client/src/lib.rs: say which open attempt an argv resumes and whether a refused resumed attempt is planned again. (decisions/client.md:712 left as history.) Spec claim for at-most-once: filed in 01a17d72-94c4 |
| F2 operation table receivers | fixed Protocol/Table.lean (submit=Receive.judge, lookup=World.journalAt, log=Host.Page.kept, header says no gate reads them) and docs/reference/protocol.md |
| F3 signShapes / start / "possession proof" | Spec/* held by SPEC-4; filed 01a17d72-94c4 |
| F4 Fork.lean header | Spec/* held; filed 01a17d72-94c4 (PROTOCOL-83 lands the rename) |
| F5 three comparison paths | filed 01a17d72-9488 |
| F6 cancel exceeds step bound | filed 01a17d72-949b; the "four other steps" docstring fixed to five in Protocol/Table.lean |
| F7 page absorbed onto moved World | filed 01a17d72-94af |
| F8 sync step count | fixed comment in Protocol/Command/Verb.lean |
| F9 nine docstrings | all fixed (Exit.behind, custodyPhase [already fixed on main by another landing; kept theirs], Machine header init and resume_rederives, Head.lean certified heads, Authority.none, Verb.receipt, Verb.adopt, Host/Follow wrongSocket) |
| F10 stale docs | fixed docs/MEMBER.md (planMoved, nd decides); OVERVIEW already fixed |
| F11 undecided points | filed 01a17d72-94d7 and 01a17d72-94c4 (health receipts and HeadOf/validity/unequal positions in the first) |

Existing tasks overlapping and not duplicated: 01a17ac1-5204, 01a17d57-5546, 01a17a38-9855, 01a17d16-e71d.
Not touched: Spec/*, Lang/Surface|Read|Print, Lang/Contextual/*, Hosting/Resident/*, README "One program".
Worktree `~/nd-land/faerie-findings` (own .lake copy, 1.5G) remains.
