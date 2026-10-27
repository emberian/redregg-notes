"""ASSEMBLY-perf ID-1 repro: the real `host serve` under nd-supervise's macOS FLOOR answers no frame.

usage: python3 -I perf-sandbox-hang-repro.py DIR MODE
  DIR  holds a copy of the `host` exe and a Store made by `DIR/host genesis DIR/store toy`
  MODE none | floor | sysctl | name:hw.ncpu[,more]   (prefix with LEAN_NUM_THREADS=4 to test the env fix)
The profile mirrors sandbox/src/lib.rs `platform` (macOS): program literal, FLOOR, the store as
read+write, file-read-metadata on every ancestor. Sends two 5-byte frames (unknown ops) and waits 3 s
for each reply. Ran 2026-10-16 on the HEAD host exe: none 0.3 ms, floor NO REPLY, sysctl 4.5 ms,
name:hw.ncpu 0.5 ms, floor + LEAN_NUM_THREADS=4 0.2 ms. Exit code is 0 in every mode (EOF still ends
the process), which is why nothing has noticed.
"""
import os, select, struct, subprocess, sys, time

W, mode = sys.argv[1], sys.argv[2]
meta, p = "", W
while p != "/":
    p = os.path.dirname(p)
    meta += f' (literal "{p}")'
prof = (f'(version 1)(deny default)(allow process-exec (literal "{W}/host"))'
        f'(allow file-read* (literal "{W}/host") (literal "/") (literal "/dev/urandom") (subpath "/usr/lib")'
        f' (subpath "/System/Volumes/Preboot/Cryptexes") (subpath "{W}/store"))'
        f'(allow file-read-metadata{meta} (literal "{W}"))(allow file-write* (subpath "{W}/store"))')
if mode == "sysctl":
    prof += "(allow sysctl-read)"
if mode.startswith("name:"):
    prof += "(allow sysctl-read " + " ".join(f'(sysctl-name "{n}")' for n in mode[5:].split(",")) + ")"
cmd = [f"{W}/host", "serve", f"{W}/store"]
if mode != "none":
    cmd = ["sandbox-exec", "-p", prof] + cmd
pr = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(0.3)
t = time.time()
for op in (0xFE, 3):
    pr.stdin.write(struct.pack("<IIB", 5, 7, op)); pr.stdin.flush()
    r, _, _ = select.select([pr.stdout], [], [], 3)
    if r:
        os.read(pr.stdout.fileno(), 64)
        print(mode, "op", op, "reply after", round((time.time() - t) * 1000, 1), "ms")
    else:
        print(mode, "op", op, "NO REPLY in 3 s")
pr.stdin.close()
print(mode, "rc", pr.wait(timeout=10))
