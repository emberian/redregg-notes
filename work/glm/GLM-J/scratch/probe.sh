#!/usr/bin/env bash
# GLM-J probe: does the real nd retire an object end to end? Two founders, real sockets.
set -euo pipefail
cd ~/nd-land/glm-j
R=/tmp/glmj-probe; rm -rf $R; mkdir -p $R/{holding,holding-b,stores}
chmod 700 $R/holding $R/holding-b
ND=target/debug/nd
HOST=.lake/build/bin/host
run() { # ws holding args...
  local ws=$1 holding=$2; shift 2
  ND_WORKSPACE=$ws ND_HOLDING=$holding ND_HOST_SOCK=$R/socks/host.sock ND_FOLLOW_SOCK=$ws/follow.sock $ND "$@"
}
out() { echo "--- $*"; }
$ND --init >/dev/null 2>&1 || true
ND_WORKSPACE=$R/ws ND_HOLDING=$R/holding $ND --init >/dev/null
ND_WORKSPACE=$R/ws-b ND_HOLDING=$R/holding-b $ND --init >/dev/null
AK=$(ND_WORKSPACE=$R/ws ND_HOLDING=$R/holding $ND --keys)
BK=$(ND_WORKSPACE=$R/ws-b ND_HOLDING=$R/holding-b $ND --keys)
KEYA=$(echo "$AK" | sed -n 's/^key //p'); NEXTA=$(echo "$AK" | sed -n 's/^next //p')
KEYB=$(echo "$BK" | sed -n 's/^key //p'); NEXTB=$(echo "$BK" | sed -n 's/^next //p')
out genesis
$HOST genesis $R/stores/W nano $KEYA $NEXTA $KEYB $NEXTB > $R/genesis.txt
cat $R/genesis.txt | head -4
M0=$(sed -n 's/^founder 0 member \([^ ]*\) grant .*/\1/p' $R/genesis.txt)
G0=$(sed -n 's/^founder 0 member [^ ]* grant \(.*\)/\1/p' $R/genesis.txt)
M1=$(sed -n 's/^founder 1 member \([^ ]*\) grant .*/\1/p' $R/genesis.txt)
G1=$(sed -n 's/^founder 1 member [^ ]* grant \(.*\)/\1/p' $R/genesis.txt)
mkdir -p $R/socks $R/ws $R/ws-b
$HOST serve $R/stores/W --retain 0 > $R/serve.log 2>&1 &
echo $! > $R/serve.pid
$HOST follow $R/stores/FA $M0 $G0 > $R/fa.log 2>&1 &
echo $! > $R/fa.pid
$HOST follow $R/stores/FB $M1 $G1 > $R/fb.log 2>&1 &
echo $! > $R/fb.pid
sleep 1.5
export ND_FOLLOW_SOCK=$R/ws/follow.sock
export ND_HOST_SOCK=$R/socks/host.sock
A() { ND_WORKSPACE=$R/ws ND_HOLDING=$R/holding $ND "$@"; }
B() { ND_WORKSPACE=$R/ws-b ND_HOLDING=$R/holding-b ND_FOLLOW_SOCK=$R/ws-b/follow.sock $ND "$@"; }
out "bob syncs"
B sync >/dev/null || B sync || true
out "alice creates a cell"
CELL=$(A create | sed -n 's/^id //p')
echo "cell $CELL"
A write $CELL 0 "hello" >/dev/null
out "bob (non-owner) retires: expect refused notOwner"
B retire $CELL || true
out "alice retires: expect success"
A retire $CELL || true
out "alice reads it: expect refused missingCell"
A read $CELL || true
out "alice retires again: expect refused missingCell"
A retire $CELL || true
out done
