# TRANSPORT-LOG — BUILD-TRANSPORT, DISSOLVED 2026-10-17

Temporary lane (ASSEMBLY-transport-consent §6, ~/dev/redregg/work/nanodregg-scout/). It owned no
path; it landed D1–D7 into the owners' paths with their review, and dissolves here. hbox worktree
/tank/dregg-build/nanodregg/wt/transport is clean at main; the Mac worktree was removed.

## Landed (all on hbox main, pre-push GREEN)
| D | sha | what | reviewed by |
|---|---|---|---|
| D4 | 9f2373e, 463200a, 99b5cbc | genesis image (one origin frame, base after it); rows use it; open refuses `foreignSegment` (HOST-18; was: a foreign seg.log TRUNCATED as a torn tail) | HOST-4 agreed |
| — | 9eb73b8 | PROTOCOL-4's wip batch landed for it (Attempt.next, replyMsMax, custody results) | ROOT order |
| D5 | 664e812, 44c82fc | PROTOCOL-22 close vocabulary (Status.closed, CloseReason, idle/frame/replyWrite ms, peerConnectionsMax); CLIENT-14 mux (one writer per conn, idle only with nothing in flight, named closes, reply backstop) | CLIENT-2 (5 conditions) |
| D5+ | 2a9d5a4, abb87b2, f5be21f | PROTOCOL-23 hang-up (child wire byte 255, ack by name, peerLeft); Host acks (handle/follow/refuseQueued); mux hangs up every end | PROTOCOL-5, HOST-5 |
| D6 | 4973105 | `attach/` crate: nd-attach (CLIENT-12 B), per-session cap freed by hang-ups, every end named | ROOT ruling; CLIENT-2 owns it now |
| owed | 229c719 | one reply per request frame on its own conn (replies_conns, served_conns, uncertain_conns) | HOST-5 |
| D7 | 4c327a7, 51036b4 | HOST-26: thin pins under their own string `base-digest/v1` (thin itself was PROTOCOL's a02b35c / HOST's 483ce14) | — |
| D1+D2 | 9e91ede | done by KERNEL-5 (KERNEL-24): World.origin, Unsigned.world, wrongWorld, origin-keyed founder ids | — |
| D3 | 3cae578, d5d7266 | PROTOCOL-29: Envelope.world first, wrongWorld first, v3; Self.world (replaces plan's w.origin placeholder); Thin wrongWorld; row wrongWorldRead | PROTOCOL-6 |

## Handed to owners (nothing of these is TRANSPORT's any more)
- **PROTOCOL-6** (abd8f012f13228e0b): the INVITATION format carrying (label, nonce, founders) so a
  member derives the origin itself (today copied by hand; HOST's `host genesis --nonce`), and the
  D7 sponsor-signed pin with an `attesterNotMember` cross-check; both are TOFU until it exists.
- **KERNEL-6** (aa36c7021124d8bdb) / CODEC: `Env.bytes` injective as a stated Ctx property — the
  missing step for "the envelope signature binds the world bytes" (PROTOCOL-29 critique).
- **HOST-6** (a59922b2afa99acbc): that `serve` sends exactly the arrays `served_conns` /
  `uncertain_conns` speak about is read off IO code, not a theorem; HOST-18's critique: a divergent
  copy of OUR segment past the base still reads torn up to frameMax (32 MiB) — nobody has
  questioned `recordBytesMax`.
- **CLIENT-2** (a1612c507f0ff2b93): nd-attach under a real sshd forced command; the three mux
  deadlines (30 s / 30 s / 120 s) and peerConnectionsMax 8 are unmeasured over a real WAN ssh; the
  cross-session cap is a declared absence (CLIENT-12).
- **Ember**: D8 — per-cell blinding stays a declared absence pending the KEY-CUSTODY ruling (scout C2's
  three required corrections are in the assembly §1).

## Lessons (for the next lane)
- On hbox, write scripts and messages locally and scp them: heredocs through ssh break on
  apostrophes and zsh eats backticks (it ate code spans in three docstrings this session).
- A 3-way rebase helper must fail LOUDLY: 4c327a7 landed conflict markers because its output went
  to /dev/null (now: transport-rebase.sh exits 1 on any conflict; GATES e9d06c3 refuses markers).
- Run every test that drives the thing you changed, not only its own file: f5be21f's hang-ups broke
  the python stand-in children in other client tests (CLIENT-2 fixed in c6e4abf).
- Decision numbers collide between parallel writers twice in one day (HOST-25, PROTOCOL-28): read
  the file at main right before naming one.
