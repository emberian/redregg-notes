#!/bin/sh
# runact.sh N : run the activity driver on burst-e2e, wait, print red rows
ssh ember@152.236.4.24 "cd /srv/lanes/rollup/src && nohup sh -c 'python3 native/resource-client/objective-activity-native-acceptance.py --bin /srv/lanes/rollup/bin --root /srv/lanes/rollup/run-$1 > /srv/lanes/rollup/act-$1.log 2>&1; echo rc=\$? >> /srv/lanes/rollup/act-$1.log' > /dev/null 2>&1 &"
sleep 5
ssh ember@152.236.4.24 "until grep -a -q '^rc=' /srv/lanes/rollup/act-$1.log; do sleep 10; done; grep -a -n 'MISMATCH\|Traceback\|FAILED\|^rc=' /srv/lanes/rollup/act-$1.log | cut -c1-260; wc -l /srv/lanes/rollup/act-$1.log; tail -3 /srv/lanes/rollup/act-$1.log | cut -c1-220"
