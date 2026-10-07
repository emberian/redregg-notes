# FOREMAN STATUS (agent a27b385ccfd998741), wound down 2026-10-04 ~21:15Z (box clock)
Role: owns scheduling of NEW work for the Mini swarm; board = work/WORKBOARD-20261005.md (only the foreman edits it).
Worker rules: work/WORKER-BRIEF-20261005.txt + work/FOREMAN-WORKER-ADDENDUM-20261005.txt (items 12-14: slot-1/2 only <=24G,
slot-mk never, Rust-only cargo outside slots at 12G when load<24, P0 first).

## State at wind-down
- 21 workers were running; each was sent WINDDOWN-20261005.txt (commit, -wip, QUEUED, bundle to persvati
  claude-lanes/bundles/<id>.bundle, STATUS with reasons, stop). Their ids are in the board's last column.
- Queued by workers (most in merge batch c13): W09, W11, W13 (9f68674b dropped per root), W14, W16, W17, W20, W23,
  W24, W25, W26, W27 parts 1 and 4a, W06 part 1, W02 (check its STATUS).
- Parked veterans: W25 aa37fea229c1b322e (W25b after W17 + W34 land), W09/W34 a9643d08084c60cac (W09b after SEATS-NATIVE),
  W16 ade46c51035d02a3f (m3 mutant not run), W13 a22f0e172f19c264a (retired: 600K tokens).
- hbox-held lane sources (W2.F SPK, W2.G MPC, W2.B traffic, rewriter W1.15) were relayed read-only to /srv/relay-hbox on
  every burst box and persvati claude-lanes/relay-hbox/.

## Decisions and their reasons
- Dispatch is gated by BUILD SLOTS, not cores. Measured 20:47Z: about 10 flock waiters per f4, and flock is not FIFO. So keep
  build-active lanes at about 2x the slot count. Burn at nice 19 counts toward total load (root's target is 18-22 total).
- slot-3 was my request to PIPELINE-INFRA, made because I counted only non-burn work. ROOT withdrew it (amendment 4).
- Rust-only cargo runs outside the slots (addendum 13). They need no Lean slot, and taking them out of the queue lets Lean builds through.
- Veterans get the next quest in their own context (W09->W34, W26->W18->OB4, W23->W35, W24->W40, W20->W43, W11->W38,
  W06->W06b, W13->W14, W17->OB2-finish).
- Root rulings relayed: W27 channel keys = design B (all pairs always, ratchet, scheduled rekey every R epochs, PRF view tags
  with random decoys); W06 consent = Host serves the log (no tenant reads mini-core files; the MAC key stays in custody);
  fn TLS = PQ-only with a named pqGroupUnavailable refusal, b19f863c held until fn confirms a host.

## Open with the root
- RULED 21:20Z (not yet relayed, because W06b had already wound down): op 155 = option (1), served only to an ENROLLED member's
  signed request, every serve logged, exposure stated in the op docs + FRIENDS.md. Relay it to adbc03adcc479977e first thing on
  resume. New P0 row PLAN-SCOPED REPLAY (the thin-peer selective witness producer) is on the board.
- OB1 finding (a9950fd7a6f67f840): the elaborator alone does not preserve meaning (`let y: Bool = 5 in true == y` -> 5);
  OB1 restated the theorem as preservation for well-typed sources under an independent surface typing. Its design is in its STATUS.
- b19f863c waits on fn confirming a host with OpenSSL >= 3.5.

## Next step on resume (see the board's RESUME PLAN)
1. Read worker STATUS files and MERGE-QUEUE LANDED/BOUNCED. 2. Dispatch W42 (P0 opus, persvati/hbox slot). 3. Resume the P0 OB rows,
with Lean-heavy ones on the persvati/hbox slots. 4. Resume the others. 5. By 13:00Z every row has a persvati bundle + STATUS
(the boxes die at 15:55Z). Load check helper: scratchpad boxload.sh (top split by nice); boxes log load to ~/load.log every 30 s.
