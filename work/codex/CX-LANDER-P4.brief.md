Name: CX-LANDER-P4. LANDER ONLY. The independent reader CX-READER-P4 already returned VERDICT: LAND for card P4 (33 statements) in hbox
/tank/dregg-build/nanodregg/wt/CX-P4 (its REPORT /Users/ember/dev/redregg/work/codex/CX-READER-P4.report.md, read whole: the verdict, the
changed paths, the drafted message path logs/CX-P4-message.txt). It then HELD its launch for 40+ minutes waiting for judge-slot benches
to stop, misreading rule 13: that rule forbids a 16G HAND build beside a bench; a landing through scripts/commit IS the judge, runs
under the judge's own slot discipline, and is launched regardless of bench activity. DO NOW: in the worktree, rebase onto main's tip
(main moved: 2b7bc39+; the decision append is append-only), run gates/check.py once (no 16G build; the fast path builds what it
reaches inside the judge), grep the message for placeholders, then launch scripts/commit detached (PID file logs/CX-LANDER-P4-land1.pid,
log logs/CX-LANDER-P4-land1.log), wait with full-deadline sleeps, never stop the judge; a refusal is read whole and fixed forward
(a displaced attempt re-bases itself). Report the hash, DONE.
