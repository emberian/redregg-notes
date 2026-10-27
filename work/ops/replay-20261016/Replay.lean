/-
OPS step 2 (ASSEMBLY-ops §0.3): does a call signed for one World admit in a re-genesised World
with the same NAME and founders? Deployed Ctx (Host.Deployed.X: CODEC codecs, cSHAKE256, Ed25519,
LANG's program). The founder key is RFC 8032 TEST 1's PUBLIC key (a published test vector; the
signature is made outside Lean by openssl from that vector's published secret).
  replay unsigned NAME          -> hex of the unsigned bytes to sign
  replay check NAME1 NAME2 SIG  -> submit the same call to genesis(NAME1) and genesis(NAME2);
                                   writes the host frame to ./submit.frame
-/
import Host.Deployed
import Host.Wire
import Protocol.Command.Text

open Nanodregg Nanodregg.Kernel Nanodregg.Kernel.Receive Nanodregg.Host Nanodregg.Host.Deployed

def hexb (s : String) : ByteArray := (Protocol.Text.ofHex s).getD ByteArray.empty
def pub1 : ByteArray := hexb "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a"
def pub2 : ByteArray := hexb "3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c"

def founders : List (ByteArray × D) := [(pub1, nextKeyDigest X pub2)]
def worldOf (name : String) : World D := Receive.genesis X name.toUTF8 allowanceMax founders

def unsignedFor (name : String) : Unsigned D :=
  let fid := founderId X name.toUTF8 0
  { member := fid, key := pub1, notBefore := 0, validUntil := 100,
    pins := [(fid, pinOf X.env ((worldOf name).live fid))], maxCharge := 1 <<< 40,
    body := .create none [] [] }

def verdict (w : World D) (c : Call D) : String :=
  match submit X w c with
  | .ok (t, w') => s!"ADMITTED height={w'.height} tx={(txIdOf X c).toHex} turn={(turnDigest X.env t).toHex}"
  | .error (.refused r) => s!"REFUSED {r.name}"
  | .error (.rejected r) => s!"REJECTED {repr r}"

def main : List String → IO UInt32
  | ["unsigned", name] => do
    IO.println (Protocol.Text.toHex (X.unsignedBytes (unsignedFor name))); return 0
  | ["check", n1, n2, sig] => do
    let c : Call D := { unsigned := unsignedFor n1, signature := hexb sig }
    let w1 := worldOf n1
    IO.println s!"world1 name={n1} chain={w1.chain.toHex}: {verdict w1 c}"
    match submit X w1 c with
    | .ok (_, w1') => IO.println s!"world1 again (journal holds it): {verdict w1' c}"
    | .error _ => pure ()
    let w2 := worldOf n2
    IO.println s!"world2 name={n2} chain={w2.chain.toHex}: {verdict w2 c}"
    IO.FS.writeBinFile "submit.frame"
      (encodeFrame { conn := 1, op := Protocol.Op.submit.code, payload := X.callBytes c })
    IO.println s!"founder0 member={(founderId X n1.toUTF8 0).toHex}"
    return 0
  | _ => do IO.eprintln "usage: replay unsigned NAME | replay check NAME1 NAME2 SIGHEX"; return 2
