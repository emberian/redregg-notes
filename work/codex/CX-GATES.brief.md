Name: CX-GATES (run 3). READ FIRST /Users/ember/dev/redregg/work/codex/CX-GATES.run2.report.md (your runs 1–2: 20m/census/leak/20n/20o landed) and
/Users/ember/dev/redregg/work/codex/CX-P7.report.md's "ASK: GATES STALE-PATH FALSE POSITIVE" (the last such line) with its diagnostic
logs/CX-P7-run4-stale-diagnostic.log on hbox. THE DEFECT (GATES-20b's stale-path guard, gates/rebase.py): when a recent commit (e86f237,
LEDGER's escrow_link_bites) ADDED a theorem and the candidate (P7's port) retains that theorem byte-identical but elsewhere in the file,
the replay appends the addition at EOF, sees two declarations, and classifies the candidate as LACKING it (`lacks=True`): a false `stale
path` refusal of a semantics-preserving port (merge exit 0; working declarations 1; replay declarations 2; the old statement byte-identical).
FIX FORWARD in gates/rebase.py: a retained declaration (byte-identical statement present anywhere in the candidate's copy) is NOT lacked;
the duplicate-addition replay must not count as a lack; keep the guard's real teeth (a landing that truly removes a recent commit's added
declaration is still refused `stale path`; plant it: remove escrow_link_bites in a scratch copy → refused). PLANTS: (1) the real P7 case
from the diagnostic (retained theorem moved) → must PASS the guard; (2) the true-removal case → refused; (3) the existing GATES-20b plant
(a stale working copy erasing another lane's lines) still refused. Rule 16: plant inputs from the real source/log. Land as `gates:` (full
judge) through scripts/commit from wt/gates (rebase onto main's tip; detached, PID file logs/CX-GATES-stale-land1.pid; full-deadline
sleeps; never stop a judge). Report the hash with the words "stale detector" in the commit subject (CX-P7 polls for it). DONE.
