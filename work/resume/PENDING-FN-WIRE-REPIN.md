# PENDING (next free slot, Sonnet is enough): re-pin Mini to fn's certified wire grammar on fn DEV
SUPERSEDED TARGET: pin fn root d420a2b5e2b3db18be134ba5a503160da84a31c3 instead: 211503 octets, BLAKE3 d00558d008108f98b0fcbc96c0ead68e3fc2c92076974f17f1c00463cf9324a5, 1028 vectors (mini-contract-3 slice 2, merging to fn dev). Older: fn dev 7e542c054 (81688 octets).
Adds the consumer FNCT families (mini-contract-3) and M4 store-identity; details in fn lanedumps/mini-contract.md.
Do: vendor the file byte-identical into protocol/fn/wire-grammar.json; update Compiler/FnWirePinned.lean pin (Lean BLAKE3), the
vector counts, Mini's grammar copies (fncu.cursor) and scripts/check-fn-wire.sh; every vector must agree; report disagreements
with the exact case (relay to fn). Then (opus or the same lane) consume store-identity in the fn-direct pin (M4) and retire any
remaining hand parsers of the new consumer families. Build on hbox slot-2.
