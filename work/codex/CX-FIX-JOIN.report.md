# CX-FIX-JOIN report

2026-10-23 LANDED 00ed907 on nanodregg main, pushed to origin (scripts/commit FAST GREEN; built Protocol Host Hosting Bench rows host-sim host bench-* host-file-sim; decls ok).
  Subject: protocol: adopt's genesis check is "a World a genesis builds", not "no cell" (PROTOCOL-67).

2026-10-23 MEASURED (hbox wt/fixjoin at 43484ab, logs /tank/dregg-build/nanodregg/logs/fixjoin/run1.log):
  join.rs:278 panicked: left "refused notAtGenesis\n", right "refused notBehind\n". The thin joiner C's
  `nd adopt KEY` was refused by the new atGenesis check at `start`. Of d23091d's three changes it is (2), the adopt check, alone.

2026-10-23 READ (Protocol/Command/Machine.lean, Kernel/Receive/Follow.lean): HOSTING-43 defined
  atGenesis w := steps = 0 AND trie = .empty. A real follow never holds an empty World: genesisWorld inserts
  each founder's member cell and root grant at step 0, and a joiner's Store is that World. So the check
  refused EVERY honest adopt. It could not be satisfied on the honest path. The CHECK was wrong, not the test.
  The test stays unchanged.

2026-10-23 FIX (PROTOCOL-67, decisions/protocol.md; a pointer in HOSTING-43's sentence in decisions/hosting.md):
  atGenesis w := steps = 0 AND every trie entry is a live member or grant cell (genesisLeaf). It is still
  checked at start AND at phase 7 (HOSTING-43's time-of-check fix is kept). A step-0 World holding an object,
  a tomb or a spent nullifier is still refused. Theorems in Protocol/Proofs/FollowHead.lean:
  genesisWorld_atGenesis (every genesis World passes, so the check can be satisfied), atGenesis_object
  (replaces atGenesis_live: an accepted World holds no live object; no Canon premise), insertAll_toList.
  step_packageAt's statement is unchanged. Axioms: propext, Classical.choice, Quot.sound.

2026-10-23 MEASURED (logs/fixjoin/run2-{join,foreign,pin}.log): cargo test -p nanodregg-client --test join /
  --test foreign / --test pin each 1/1 ok. join includes D's adopt of the sealed base. Red control: run1.log
  (the same test at 43484ab).

2026-10-23 INFERRED / open: the next convergence must confirm cargo:client:join green. Rows, census and clippy
  were not run (fast judge). Residual named in PROTOCOL-67's critique: the check accepts any step-0 member/grant
  World. It does not require the founders of THIS World's inputs, because follow's Self does not carry the
  inputs. That case is reachable only through a Store that follow did not build.
