# COST-MODEL log
- 2026-10-14 start; reading safety block + logs
- ROOT steer: WASTE MODEL not budget; files docs/WASTE-MODEL.md, scripts/gates/check-waste-model. Lane hbox claude-lanes/cost-model/src branch cost-model @ next 0125b224
- 18:30 gate script + table + fixture + workload.sh marker + merge-gate row written (uncommitted); self-test PASS; judge srw-after GREEN; plant phase.invoke ceiling 1500 -> RED observed. cshake-bench: 128 instr/B bulk (1.918 G / 15 MB raw).
- 18:50 COMMIT d670d30a on lane cost-model (base next 0125b224), pushed mirror lane/cost-model. GitHub from hbox: no key -> ROOT pushes.
  Files: docs/WASTE-MODEL.md, docs/waste-model.tsv, scripts/gates/check-waste-model, waste-model-{decisions.txt,fixture.tsv},
  scripts/perf/workload.sh (perf.t0 + perfCounting raw), merge-gate-checks row waste-model.
  First verdict: judge /tmp/srw-after (fffb817f) GREEN, all wall rows UNCONFIGURED (run not quiet); hints to lower ceilings when STORE-ROOT lands.
  Plants observed: phase.invoke ceiling 1500 -> RED; ratchet HEAD with certify 238.2->300 undecided -> RED; gate next HEAD PASS (first landing).
  Measure tables: hbox cost-model/w/measure-{before,after}.tsv. cshake-bench run outputs cost-model/w/.
  OPEN: births row under perf stat (lane/births-row) so landings are judged; J measurement; profile op 2 from a file-path Host.
