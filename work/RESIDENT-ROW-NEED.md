# cargo:launcher:resident — the agreed NEED (PROTOCOL-7 + HOSTING-6, 2026-10-17; HOSTING-17)

runs.tsv: `cargo:launcher:resident	hosting-controller,hosting-broker,host	exit 0`
Shape: a Rust launcher test like broker.rs. Real Store (host genesis/serve under nd-supervise; nd install
world/grain/Lifecycle (+ Allowance); create a resident grain; invoke start). No wall-clock verdict: a deadline renders `hang`.
Layout: socket SOCKDIR/<dirOf id>/broker.sock (one directory per resident). BROKER = broker root, a new grain-launch
argument. On hbox one uid: the one-uid branch (socket euid-owned, exactly 0600).

R1  The controller (Lean) plans the launch; the plan's connect entry is EXACTLY [<dirOf id>, "broker.sock"] relative to
    BROKER. The test reads it from the plan / launch frame, never computes it in Rust.
R2  grain-launch resolves the policy: Policy.connect gets ONE socket path. lstat: a socket, no symlink, no other-bits;
    EITHER owned by euid at exactly 0600 (this row) OR another uid with group = egid at exactly 0660 (deployment).
    Every ancestor owned by root/euid/the socket's owner, no g/o write (CLIENT-19 Dir). Linux binds the socket's PARENT
    directory. Then launch.
R3  Inside, the resident connects, asks keybroker, gets the fake TLS upstream's status/body (a grant).
R4  Inside, the key file is ENOENT.
R5  Inside, resident 02's socket SOCKDIR/<02>/broker.sock (exists on the host) is ENOENT, and SOCKDIR itself as a listing.
R5b Inside, the listing of the bound directory is exactly ["broker.sock"].
R6  CONTROL: the canary key is in what the upstream received, and absent from every byte the resident received.
Refusals by name at resolve, before any process: a regular file at the path → ConnectNotSocket; a symlink →
ConnectLink; a 0666 socket → ConnectMode; a 0660 socket owned by euid → ConnectMode; a group-writable ancestor → Dir.
Declared UNRUN in the row text, with the reason (one uid on hbox): ConnectOwner, keybroker's peerRefused.
Plants, each red at a NAMED step, each run once to show it:
 (a) the policy binds SOCKDIR instead of SOCKDIR/<r> → R5 connects → red at R5;
 (b) the plan omits the connect entry → red at R3 (ENOENT or a named refusal);
 (c) the mode check skipped → the 0666 case launches → red at ConnectMode;
 (d) keybroker restarted mid-row (stop by its PID file, start a new one); the resident asks again and must be granted
     (a socket-file bind makes this red);
 (e) keybroker writes a second file into SOCKDIR/<r>/ → red at R5b.
Grain physical half `cargo:launcher:grain` (`hosting-controller,host	exit 0`): same real Store, create + invoke
start; the process runs under the planned policy; operator invoke stop ends it (named exit); the grantee's stop is
refused grantRight and the process stays alive. Plant: a controller that ignores stop → red at the stop step. It
restates m6grain's sandbox half; the Lean `grain` row's docstring names it (PROTOCOL adds the cross-reference).
PROTOCOL-7 reviews both tests before they land.
