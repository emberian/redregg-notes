Name: CX-READER-KERNEL. READ-ONLY adversarial reader: no worktree edits, no landing. CX-KERNEL (a Codex worker, dead now) built
cv 01a15849-3ae0 (the trie-binding theorem) and 01a1553a-c095 (dropHeads on the overlay U) in /tank/dregg-build/nanodregg/wt/cxkernel
(detached at 2b6e5e1); its patch is hbox /tank/dregg-build/nanodregg/logs/cxkernel-ready.patch (SHA256 02e082ef…, 35,268 bytes; paths in
logs/cxkernel-changed.txt; message logs/cxkernel-message.txt; its own disjunct read in /Users/ember/dev/redregg/work/codex/CX-KERNEL.report.md
and decisions KERNEL-62/63 in the worktree's decisions/kernel.md). CHARTER law 6: every theorem statement is read by a second agent
before it lands. You are that agent. READ the new theorem STATEMENTS in Kernel/Proofs/{TrieBinding,RowsOverlay}.lean and
Kernel/TrieBinding.lean (in the worktree) with the DISJUNCT CHECK: for each disjunct of each conclusion, is it provable from the
premises alone or from the instance alone (a 32-byte digest, an unbounded preimage, a Lawful env)? `∨ Collision` with an unbounded ∃ is
ALWAYS vacuous; the sound form is `CollidesAmong hash S` over an EXPLICIT finite list the theorem builds (KERNEL-56's shape: copy its
sites to compare). Check: `root_binds`/`_sep`/`deployed_trie_root_binds`/`deployed_rows_root_binds` (is root equality forced by
Canon/Fits? is the collision list explicit and finite? does `_sep` really remove the escape?); `takeListU_seal`/`underU_seal`/
`dropHeadsU_seal` (does `rowsRun_eq` keep its statement byte-for-byte? `git diff` it); the premise question (does ANY landed theorem
gain a hypothesis? grep every changed theorem signature against main's); the teeth (cxkernel-binding-tooth-red.log,
cxkernel-plant-heads-red.log: read them whole; is the mutation real?). Verify the build claim yourself ONCE: `SWARM_MEM_MAX=6G
LEAN_NUM_THREADS=2 swarm-build lake build Kernel` in the worktree, tee'd (it is warm; minutes). VERDICT to your REPORT: LAND /
LAND-WITH-FIXES (each fix exact: file, line, old → new) / REFUSE (why, by statement). Write `DONE` when the verdict is written.
