#!/bin/sh
# sign.sh HEX -> Ed25519 signature hex under RFC 8032 TEST 1's PUBLISHED secret (a test vector, not a key)
set -eu
d=$(mktemp -d "$PWD/sign.XXXXXX")
printf '302e020100300506032b657004220420%s' 9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60 | xxd -r -p > "$d/k.der"
printf '%s' "$1" | xxd -r -p > "$d/m"
/opt/homebrew/bin/openssl pkeyutl -sign -inkey "$d/k.der" -keyform DER -rawin -in "$d/m" | xxd -p | tr -d '\n'
rm -r "$d"
