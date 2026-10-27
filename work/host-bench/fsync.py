import os, fcntl, time, sys
d = sys.argv[1]
def run(size, reps=30):
    p = os.path.join(d, f"f{size}")
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    buf = b"x" * size
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter_ns(); os.write(fd, buf); fcntl.fcntl(fd, fcntl.F_FULLFSYNC); ts.append(time.perf_counter_ns() - t0)
    os.close(fd); os.unlink(p)
    ts.sort(); return ts[0]//1000, ts[len(ts)//2]//1000
for s in (100, 290060):
    print("fsync", s, "best/median us", run(s))
