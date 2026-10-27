Cross-World replay, reproduced (OPS, 2026-10-16, main 87c721e). ASSEMBLY-ops §0.3.
Run from a clone of nanodregg at 87c721e with `lake build host` done:
  U=$(lake env lean --run PATH/Replay.lean unsigned w); SIG=$(PATH/sign.sh $U)
  lake env lean --run PATH/Replay.lean check w w $SIG      # in-process, deployed Ctx
  host genesis storeA w $P1 $P2; host serve storeA < submit.frame   (and storeB)
Results: run.txt (in-process), host-run.txt (two real Stores, status byte 0, same turn digest d9b10451…).
Founder key = RFC 8032 TEST 1 public key; signature made by openssl from that vector's PUBLISHED secret.
