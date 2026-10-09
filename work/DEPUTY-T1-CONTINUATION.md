# DEPUTY-T1 continuation (2026-10-08 06:15Z)
STATE: DONE. lane/t1-train = e0a8ba21a39d92b470cc331fd16ea0408f608b1f in /srv/git/minidregg.git (burst3-a). The gate was red=0 in a fresh lane (t1-gate3, logs /srv/lanes/t1-gate3/logs/gate-t1d.*). ROOT pushes it to GitHub main. I did not push.
Full record: redregg/work/CXO-EXPERIMENT-1.md (measurements, 8 cxo bugs, recommendation: do not scale until the polling, sandbox-service, scope and continuous-integration fixes land; those go to the hub's builder).
Workers: all retired (t1-collector, t1-meter, t1-retry, t1-mergefix, t1-mergefix2).
Leftovers on burst3-a, all created by this deputy, kept so they can be inspected:
- lanes /srv/lanes/t1-{collector,retry,meter,gate,gate2,gate3};
- /srv/lanes/t1-retry/{jbin,target-journey};
- ~/deputy-t1 (bare repo, train clone, old/new collector scans, ledger-append.txt, widen.py, pipe/).
They are safe to delete once ROOT has pushed.
Open items for others:
- /srv/pipeline/scripts/merge-gate-checks.sh on burst3-a still has the old row order; the next advance-base installs the fixed copy from the tip.
- hbox and persvati ports may carry the same scripts-elab ordering bug.
- The scope trap was never exercised; the next experiment needs a trap the item actually requires.
