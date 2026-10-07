#!/bin/sh
# usage: waitlog.sh host logpath  -- blocks until rc= line, prints errors
ssh ember@$1 "until grep -q '^rc=' $2; do sleep 15; done; grep -n 'error\|^rc=' $2 | cut -c1-300 | head -60"
