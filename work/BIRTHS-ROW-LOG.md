# BIRTHS-ROW log (continuation)
- 16:30 lane cloned hbox /tank/dregg-build/claude-lanes/births-row/src, branch lane/births-row from next 0125b224.
- Finding: landing.sh flips a `pending` row to REQUIRED the moment it appears in results.tsv (ROOT 10-14). Brief wants births "required when green at main" -> needs a pending variant that flips only once main's baseline has it PASS.
- Plan: workload.py --births-only (genesis, setup, births, reopen); row_births in journey-rows; growth only under PIPELINE_NIGHTLY=1; plant JOURNEY_PLANT_BIRTHS=bar-1ms.
- 20:53 births N=64 on set 7ffd6524 (next) via lane runner --source-tree: FAIL. create p50 5224 p99 12309 max 12309 ms; resource p50 6822 p99 13282 ms; reopen 7691 ms; 68 cells, 138 records, Store 2,060,288 B; wall 885 s; load 23.46->23.22. Evidence /tank/dregg-build/claude-lanes/births-row/journeys/7ffd6524*/
- 20:55 plant JOURNEY_PLANT_BIRTHS=bar-1ms N=8: FAIL by name (create p99 2647 ms > 1 ms bar; resource p99 4898 ms > 1 ms bar). Same N=8 is under the real bar (create p50 2257). Evidence .../journeys-plant/
- Observation (not diagnosed): create p50 2.26 s at N=8 (26 records) vs 5.22 s at N=64 (138 records), same load ~23-25: per-birth cost grows with history.
- landing.sh judge tested on fixtures: births FAIL with main baseline absent -> pending, not counted, LANDABLE; main baseline PASS -> NEW RED + NOT MET, exit 1.
- commit c385f359 on lane/births-row, pushed to hbox mirror. GitHub push from hbox: no key (Permission denied) -> ROOT pushes.
