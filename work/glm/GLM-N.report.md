# GLM-N report — LANG-111: the hole check bounds its printed lists

2026-10-27 lane start. Job: LANG-109 proved `package_prints_contextual` under two premises the
wire does not give (each hole's context and each candidate's supports at `listMax − 1`); make
`HoleROM.check` refuse both past `Read.listMax` by name, prove `check_context_le` and
`check_supports_le`, restate `package_prints_contextual` without the premises, a journey row,
spec §3.6 + appendix, decision LANG-111. Base d13fb79 (origin/main at lane start).

2026-10-27 reach read before editing: `HoleRefusal`/`HoleROM.check`/`checkContextual` and
`HoleRefusal.wire` (Lang/LiveHoles.lean); the LANG-109 chain `holeROM_prints` → `holes_prints` →
`package_prints_contextual` and the three `repeat' split`/`rename_i` proofs that unfold the check
(holeCheck_printable, holeCheck_facts in PrintWire; holeROM_check_code in Proofs/LiveHoles); the
reader's `listMax` (Lang/Read.lean: `Wire.rowMax + 2` = 258) and the printer's hole forms
(`(context T…)`, `(supports pin…)` — the +1 is the head word); `holeSite` (Resident, catch-all —
new refusals need no site); `Std.HoleRefusal` (a different type); Emit (no hole refusal name in
any input or `.rs`, so nothing re-emits); Emit/Vectors' hole fixture and the stdlib's generated
hole (both far under the bound); the journey (`boundaryRows` in Lang/Journey/Contextual.lean,
registered as `contextual-checks` via ContextualWire).

2026-10-27 edits written whole before any build (METHOD rule 1): two constructors + two check
clauses + two wire arms in LiveHoles; `check_context_le`/`check_supports_le` (position-independent
`assumption` proofs) + the restatement + two rename_i adjustments in PrintWire; one rename_i in
Proofs/LiveHoles; three journey rows (258 refused by name / 257 checks / 258 supports refused);
spec §3.6 rule + items 3 and 5; appendix bounds row + names row; LANG-111 in decisions/lang.md.
