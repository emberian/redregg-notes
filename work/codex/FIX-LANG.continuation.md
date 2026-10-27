# FIX-LANG continuation (2026-10-24 ~14:00Z) — all five cards LANDED; what is left

Landed: e82f74d (LANG-78), a77f3d8 (LANG-79), 167d21b (LANG-80), a1575fd (LANG-81), 0829f4e (LANG-82).
Report: /Users/ember/dev/redregg/work/codex/FIX-LANG.report.md. Build box: hbox wt/promo (now at 0829f4e).
Lessons: a `lang!` landing takes ~70 min per full judge and is displaced by fast landers (twice each time);
the decls map lines are only reported at the end — collect them from the gate log
(`grep "add the line" <gate log> | sed 's/.*add the line: //' | sort -u`, drop `Demo.*` synthetic lines); since
a306536 an edited DEFINITION body also needs a RESTATES-MEANING line; proof modules may not export defs (C3).

Left (optional tails from the brief):
- B4 rows to their exact refusal names: Lang/Journey/OfferEscrow.lean LE5 (`startsWith "refused"`); Journey.lean
  L6 (`refused program` → `illTyped`), LH8b/LH11b (drop the unreachable `notChooser` arm; fix LH11b's comment),
  P8.2 / P8-deadline (disjunctions), Journey/Contextual.lean management-* (`!= "ok"`), LC8 (substring
  `"arguments:"`), Journey/Head.lean HD5 (no steps-mismatch arm).
- B3 comments: Lang/Proofs/StdOffer.lean:2, :11-12 and take_iff_compliant's docstring (matcher), take_resolve
  `{pair, theta}` → `{keys, pair, theta}`; Lang/Proofs/StdOfferEscrow.lean:14-16; Lang/Proofs/LiveHoles.lean:15;
  StdOfferFuse jointLaw_sound docstring; Std.lean:129-136 (KERNEL-25 built); Eval.lean:21-22; Wire.lean:20-26 (tag
  `hole 18`). Docstring-only commits are plain commits under R-0069 (3).
