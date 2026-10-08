#!/usr/bin/env python3
"""cxo — Codex hub for Claude deputies. One resident process owns a private `codex app-server`,
the worker registry, events, jobs (builds, journeys, cargo, train checks), submit guards and the
rate-limit gate. Deputies use the CLI. Design: redregg/work/CODEX-ORCHESTRATION-DESIGN-20261008.md;
usage: README.md beside this file; experiment record: redregg/work/CXO-EXPERIMENT-1.md."""
import hashlib, asyncio, json, os, sys, time, sqlite3, re, fnmatch, subprocess, shlex, signal, itertools, tempfile

HOME = os.path.expanduser(os.environ.get("CXO_HOME", "~/.cxo"))
SOCK = os.environ.get("CXO_SOCK") or os.path.join(HOME, "hub.sock")
if len(SOCK) > 100:  # AF_UNIX path limit
    import hashlib
    SOCK = "/tmp/cxo-%d-%s.sock" % (os.getuid(), hashlib.sha1(HOME.encode()).hexdigest()[:10])
CODEX = os.environ.get("CXO_CODEX", "codex")
CODEX_HOME = os.environ.get("CXO_CODEX_HOME", os.path.join(HOME, "codex-home"))
DEFAULT_MODEL = os.environ.get("CXO_DEFAULT_MODEL", "gpt-6.1-sol")
DEFAULT_BUDGET = int(os.environ.get("CXO_DEFAULT_BUDGET", "12000000"))
BUILD_CMD = os.environ.get("CXO_BUILD_CMD", "swarm-build lake build {targets}")
CARGO_CMD = os.environ.get("CXO_CARGO_CMD", "swarm-build cargo {spec}")
BOX_ENV = os.environ.get("CXO_BOX_ENV", "/srv/pipeline/box.env")
FETCH_ARTIFACTS = os.environ.get("CXO_FETCH_ARTIFACTS", "/srv/pipeline/scripts/fetch-artifacts")
ARTIFACT_TIP = os.environ.get("CXO_ARTIFACT_TIP", "green")
UMBRELLA = os.environ.get("CXO_UMBRELLA", "Minidregg Host.Main:leanArts ObjectiveProofs").split()
SLOTS_CMD = os.environ.get("CXO_SLOTS_CMD", "slots --json")


def build_pool_size():
    """builds: CXO_MAX_BUILDS, else the box's lane-slot count from `slots --json` (list length, or lane_slots/total/slots/n), else 6."""
    if os.environ.get("CXO_MAX_BUILDS"):
        return int(os.environ["CXO_MAX_BUILDS"])
    try:
        o = json.loads(subprocess.run(shlex.split(SLOTS_CMD), capture_output=True, text=True, timeout=10).stdout)
        n = len(o) if isinstance(o, list) else next((o[k] if isinstance(o[k], int) else len(o[k]) for k in ("lane_slots", "total", "slots", "n") if k in o), 0)
        if n > 0:
            return n
    except Exception:
        pass
    return 6


def pool_sizes():
    """one pool per job kind: a long journey must never hold a build slot (CXO_MAX_JOBS no longer exists)."""
    return {"build": build_pool_size(), "journey": int(os.environ.get("CXO_MAX_JOURNEYS", "3")),
            "cargo": int(os.environ.get("CXO_MAX_CARGO", "2")), "train": int(os.environ.get("CXO_MAX_TRAIN", "1"))}
JOB_TIMEOUT = int(os.environ.get("CXO_JOB_TIMEOUT", "5400"))
PUSH_REMOTE = os.environ.get("CXO_PUSH_REMOTE", "")  # e.g. /srv/git/minidregg.git; empty = no push
PUSH_PREFIX = os.environ.get("CXO_PUSH_PREFIX", "lane/")  # the shared remote's pre-receive accepts lane/<name> only
MKLANE = os.environ.get("CXO_MKLANE", "/srv/warm-base/mk-lane.sh")
LANES = os.environ.get("PIPELINE_LANES", "/srv/lanes")
IGNORE = ["WORKLOG.md", ".minidregg-native-snapshot"]  # never staged, never scope-checked (hub's own notes; mk-lane's marker)
STALL_S, PIGGY_S = 900, 600
DEFAULT_PROTECT = ["Assurance/NativeAcceptedFixture*", "AxiomCensus*.lean", "TokenCensus*", "Theory/AxiomPin.lean",
                   "scripts/gates/*", "scripts/pipeline/*", ".github/*", "lakefile*", "lean-toolchain", "lake-manifest.json"]
GIT_ID = ["-c", "commit.gpgsign=false", "-c", "user.name=ember arlynx", "-c", "user.email=cmrx64@gmail.com"]
# E2-5: long work inside the sandbox is disguised polling (every note/idle turn re-sends the whole context). Refuse it via the
# exec-approval path (approvalPolicy "untrusted": every non-trivial command asks) and point at the hub-side tickets.
APPROVAL = os.environ.get("CXO_APPROVAL", "untrusted")
EXEC_CAP_S = int(os.environ.get("CXO_EXEC_CAP_S", "20"))   # an in-sandbox command running longer than this is flagged + steered
LONG_RX = re.compile(os.environ.get("CXO_LONG_RX", r"\blake\s+build\b|\bswarm-build\b|\bcargo\s+(build|test|run|check|clippy|bench)\b|"
                     r"\S*journeys?(?:\.d)?/\S+\.(?:sh|py)\b|objective-native-acceptance|check-objective-proofs|merge-gate-checks|check-scripts-elab|hyp-ledger|"
                     r"\bsleep\s+\d{2,}|\bwhile\s+(true|:|sleep)"))
CARGO_RX = re.compile(r"\bcargo\b")
NARRATE_N, NARRATE_M = int(os.environ.get("CXO_NARRATE_N", "4")), int(os.environ.get("CXO_NARRATE_MIN", "10"))
WAIT_TEXT = "END YOUR TURN NOW with no further actions. The result arrives as a new message. Never poll."

DEV_INSTR = """You are a Codex worker for a coordinating deputy, reached only through these tools:
- report(phase, note): call at start, after each milestone, and at least every 15 minutes. Its reply may carry deputy instructions; follow them.
- ask_deputy(question, default, must_wait): ask instead of guessing. If must_wait, END YOUR TURN right after; the answer arrives as a new message.
- request_build(targets): Lake builds in your lane, in a build slot, outside your sandbox. Single-file checks you may run yourself.
- request_journey(script, args): run a journey/acceptance script outside your sandbox (sockets allowed) with prebuilt base binaries.
- request_cargo(spec): a FILTERED cargo build/test outside your sandbox (network, memory containment).
- Every request_* returns a ticket; then END YOUR TURN. The result (exit code, log path, tail) arrives as a new message.
  Never poll build_status in a loop: each poll re-sends your whole context and costs as much as real work.
- submit(title, body, claims, waivers): the ONLY way to finish. The hub commits your working tree and checks it. Do not run git commit yourself.
Keep WORKLOG.md in the worktree root (never committed): decisions and why, assumptions, current state. A successor starts from it.
Forbidden: sorry/admit, new axioms, new native_decide, deleting or weakening a theorem/test/assertion, editing pins, fixtures,
gates or toolchain files, `|| true`, piping a build into tail, pkill -f, git stash, printing the environment, an unfiltered test suite.
If submit is refused, fix the findings and submit again, or ask_deputy. Ending a turn without submit (and with nothing pending) counts as a stall."""


def _fn(name, desc, props, req):
    return {"type": "function", "name": name, "description": desc,
            "inputSchema": {"type": "object", "properties": props, "required": req, "additionalProperties": False}}


S, B, ARR = {"type": "string"}, {"type": "boolean"}, {"type": "array", "items": {"type": "string"}}
TOOLS = [
    _fn("report", "Report progress to your deputy; returns any deputy instructions.", {"phase": S, "note": S}, ["phase", "note"]),
    _fn("ask_deputy", "Ask your deputy. Returns at once. must_wait=true: end your turn right after; the answer arrives as a new message.",
        {"question": S, "default": S, "must_wait": B}, ["question", "default", "must_wait"]),
    _fn("request_build", "Queue a Lake build of the targets in your lane (build slot, outside the sandbox). Returns a ticket; then END YOUR TURN.",
        {"targets": ARR, "allow_dirty": B}, ["targets"]),
    _fn("request_journey", "Run a journey/acceptance script from your lane outside the sandbox. In args, {bin} and {manifest} expand to the "
        "prebuilt base artifact set (unchanged Rust/Host binaries); for a Host you changed, request_build it first and pass its path. "
        "Returns a ticket; then END YOUR TURN.", {"script": S, "args": ARR}, ["script", "args"]),
    _fn("request_cargo", "Run a FILTERED cargo command outside the sandbox, e.g. 'test -p mini-client --test frames' or "
        "'build -p minidregg-host --bin x'. Tests need -p and a filter or --test. Returns a ticket; then END YOUR TURN.", {"spec": S, "allow_dirty": B}, ["spec"]),
    _fn("build_status", "Non-blocking status of a ticket. Do not call it in a loop; results are delivered to you.", {"ticket": S}, ["ticket"]),
    _fn("submit", "Finish: the hub commits your working tree and checks scope and weakening guards. waivers: 'rule:path reason' "
        "strings for deliberate deletions.", {"title": S, "body": S, "claims": ARR, "waivers": ARR}, ["title", "body", "claims", "waivers"]),
]

ADDED_RULES = [("sorry", r"\bsorry\b"), ("admit", r"\badmit\b"), ("axiom", r"^\s*(private\s+)?axiom\b"),
               ("native_decide", r"\bnative_decide\b"), ("heartbeats0", r"maxHeartbeats\s+0\b"), ("or-true", r"\|\|\s*true\b"),
               ("pipe-tail", r"\|\s*tail\b"), ("ignore-test", r"#\[ignore\]|\.skip\(|@pytest\.mark\.skip"), ("pkill-f", r"pkill\s+-f")]
REMOVED_RULES = [("del-theorem", r"^\s*(@\[[^\]]*\]\s*)?(private\s+|protected\s+)?(theorem|lemma|example)\b"),
                 ("del-assert", r"#assert_|\bassert(_eq|_ne)?!?\s*\(|#guard\b|#\[test\]|\bdef test_")]
WCOLS = {"build_cmd": "text", "umbrella": "text", "green_tree": "text", "unc": "int default 0", "reqs": "int default 0",
         "polls": "int default 0", "pending": "int default 0", "nopush": "int default 0", "declined": "int default 0",
         "unprot": "text"}  # unprot: json [[glob, added_to_allow]] one-shot protected-path approvals (cxo unprotect)
JCOLS = {"pid": "int", "note": "text"}  # pid: the job's process group (hub restart recovery); note: dirty-tree diff hash


DATA_FILE_RX = re.compile(r"\.(tsv|csv|json|jsonl|lock)$")  # pins, ledgers, emitted data: regenerated rows are not source edits


def parse_n(x):
    """token count: 15000000 | 15M | 1.5m"""
    x = str(x).strip()
    return int(float(x[:-1]) * 10**6) if x[-1:] in "Mm" else int(x)


def allow_vs_protect(allow, protect):
    """allow globs that a protect glob covers (the guard would revert the worker's edit): [(allow, protect)]"""
    return [(g, p) for g in allow for p in protect if g == p or fnmatch.fnmatch(g, p) or fnmatch.fnmatch(p, g)]


READERS = r"(cat|grep|rg|sed|head|tail|less|more|ls|git|wc|find|nl|awk|diff|echo|chmod|stat|cd|test|file|realpath|dirname|basename|" \
          r"printf|tee|xargs)$"
SHELLS = ("bash", "sh", "zsh")
PREFIX_WORDS = ("time", "nohup", "env", "exec", "command", "nice")


def _segments(cmd, depth=0):
    """quote-aware split of a shell line into command segments (token lists); `sh -c 'script'` is expanded in place."""
    lex = shlex.shlex(cmd.replace("\n", " ; "), posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    out, cur = [], []
    for t in lex:
        if t and set(t) <= set(";&|()\n"):
            out.append(cur); cur = []
        else:
            cur.append(t)
    out.append(cur)
    res = []
    for seg in out:
        while seg and re.match(r"^\w+=", seg[0]):  # FOO=1 cmd
            seg = seg[1:]
        if depth < 3 and len(seg) >= 3 and os.path.basename(seg[0]) in SHELLS and re.match(r"^-\w*c$", seg[1]):
            res += _segments(seg[2], depth + 1)
        elif seg:
            res.append(seg)
    return res


def _exec_words(seg):
    """the words in EXECUTION position: the first word, after time/env/..., and the script after an interpreter (not `bash -n`)."""
    while seg and os.path.basename(seg[0]) in PREFIX_WORDS:
        seg = seg[1:]
    if not seg:
        return None
    first = os.path.basename(seg[0])
    if re.match(READERS, first):
        return None
    if first in SHELLS + ("python", "python3"):
        rest = seg[1:]
        if rest and rest[0] in ("-n", "-m", "-c") and not (first in SHELLS and rest[0] == "-c"):
            return None  # bash -n / python3 -m py_compile: syntax checks, not runs
        rest = [x for x in rest if not x.startswith("-")]
        return rest[:1] and rest[0:1] + seg[seg.index(rest[0]) + 1:][:6]
    return seg


def exec_hint(cmd):
    """None if the command may run in the sandbox, else the refusal hint. A long-command name counts only in EXECUTION position
    (first word of a segment, or the script handed to bash/sh/python3), never as an argument to rg/grep/cat/sed/chmod/bash -n."""
    if not cmd:
        return None
    try:
        segs = _segments(cmd)
    except ValueError:
        segs = [cmd.split()]
    hit = None
    for seg in segs:
        ew = _exec_words(seg)
        if not ew:
            continue
        full = " ".join(ew)
        base = " ".join([os.path.basename(ew[0])] + list(ew[1:]))
        if LONG_RX.match(full) or LONG_RX.match(base):
            hit = full
            break
    if not hit:
        return None
    cmd = hit
    tool = "request_cargo" if CARGO_RX.search(cmd) else "request_build" if re.search(r"\blake\b|swarm-build", cmd) else "request_journey"
    return ("REFUSED by the hub: this command is long-running and must not run in your sandbox (each minute of waiting costs a full "
            "model request). Use %s(...) instead: it runs hub-side, returns a ticket, and the result arrives as a new message. "
            "Then END YOUR TURN; do not narrate or poll." % tool)


def now(): return time.time()
def ago(t): return "-" if not t else "%dm" % ((now() - t) // 60)
def git(cwd, *args, env=None):
    return subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True, text=True, env=env).stdout


def stage_pathspec():
    return ["--", "."] + [":(exclude)%s" % p for p in IGNORE]


def tree_id(wt):
    """the tree the worker would submit (excluding IGNORE), computed in a temp index: no side effects."""
    fd, idx = tempfile.mkstemp(prefix="cxo-idx-"); os.close(fd)
    env = dict(os.environ, GIT_INDEX_FILE=idx)
    try:
        git(wt, "read-tree", "HEAD", env=env)
        git(wt, "add", "-A", *stage_pathspec(), env=env)
        return git(wt, "write-tree", env=env).strip()
    finally:
        os.unlink(idx)


def dirty_info(wt):
    """(dirty, note): is the lane tree dirty (excluding IGNORE), and a note tying a job to the exact tree: HEAD, the tree id and the
    sha1 of the full diff against HEAD (untracked files included, via a temp index)."""
    fd, idx = tempfile.mkstemp(prefix="cxo-idx-"); os.close(fd)
    env = dict(os.environ, GIT_INDEX_FILE=idx)
    try:
        git(wt, "read-tree", "HEAD", env=env)
        git(wt, "add", "-A", *stage_pathspec(), env=env)
        tree = git(wt, "write-tree", env=env).strip()
        diff = subprocess.run(["git", "diff", "--cached", "HEAD"], cwd=wt, capture_output=True, env=env).stdout
    finally:
        os.unlink(idx)
    head = git(wt, "rev-parse", "HEAD").strip()
    dirty = bool(diff)
    return dirty, "%s head=%s tree=%s diff_sha1=%s" % ("DIRTY-TREE" if dirty else "clean-tree", head[:12], tree[:12], hashlib.sha1(diff).hexdigest())


# ---------------------------------------------------------------- hub
class Hub:
    def __init__(self):
        for d in ("", "wt", "logs", "jobs", "briefs"):
            os.makedirs(os.path.join(HOME, d), exist_ok=True)
        self.db = sqlite3.connect(os.path.join(HOME, "registry.sqlite"), isolation_level=None)
        self.db.executescript("""
        create table if not exists workers(name text, gen int, deputy text, model text, effort text, thread text, wt text,
          base text, state text, turn text, last_item real, last_report real, reports int default 0, tokens int default 0,
          nudges int default 0, stalled int default 0, budget int default 12000000, created real, retired real, allow text,
          protect text, sha text, primary key(name, gen));
        create table if not exists events(id integer primary key, ts real, deputy text, worker text, kind text, text text, seen int default 0);
        create table if not exists msgs(id integer primary key, name text, gen int, ts real, text text, delivered int default 0);
        create table if not exists jobs(ticket text primary key, name text, gen int, kind text, what text, status text, exit int,
          log text, t0 real, t1 real, tree text);
        create table if not exists trains(name text primary key, deputy text, wt text, green text, state text, last text);""")
        have = {r[1] for r in self.db.execute("pragma table_info(workers)")}
        for c, t in WCOLS.items():
            if c not in have:
                self.db.execute("alter table workers add column %s %s" % (c, t))
        have = {r[1] for r in self.db.execute("pragma table_info(jobs)")}
        for c, t in JCOLS.items():
            if c not in have:
                self.db.execute("alter table jobs add column %s %s" % (c, t))
        self.rid = itertools.count(1)
        self.pending = {}       # rpc id -> future
        self.execs = {}         # thread -> {item id: (command, t0)} in-sandbox commands now running
        self.cad = {}           # thread -> {"reports": [ts...], "art": ts, "flagged": bool} (E2-5 cadence guard)
        self.turn_flags = {}    # thread -> {"submit_tried": bool, "warned": set()}
        self.pool_n = pool_sizes()
        self.pool = {k: asyncio.Semaphore(n) for k, n in self.pool_n.items()}
        self.pool_run = {k: 0 for k in self.pool_n}
        self.job_rc = {}
        self.kill_grace = 10.0
        self.rate = None
        self.paused = False
        self.ev_signal = asyncio.Event()

    # ---- registry helpers
    def _row(self, r):
        row = r.fetchone()
        return dict(zip([c[0] for c in r.description], row)) if row else None

    def cur(self, name):
        return self._row(self.db.execute("select * from workers where name=? order by gen desc limit 1", (name,)))

    def by_thread(self, tid):
        return self._row(self.db.execute("select * from workers where thread=?", (tid,)))

    def upd(self, w, **kv):
        self.db.execute("update workers set %s where name=? and gen=?" % ",".join("%s=?" % k for k in kv),
                        list(kv.values()) + [w["name"], w["gen"]])
        w.update(kv)

    def event(self, w, kind, text, deputy=None):
        self.db.execute("insert into events(ts,deputy,worker,kind,text) values(?,?,?,?,?)",
                        (now(), deputy or (w["deputy"] if w else "-"), ("%s/g%d" % (w["name"], w["gen"])) if w else "-", kind, text))
        self.ev_signal.set()

    def artifact(self, w):
        c = self.cad.setdefault(w["thread"], {"reports": [], "art": 0, "flagged": False})
        c.update(reports=[], art=now(), flagged=False)

    def wlog(self, w, line):
        with open(os.path.join(HOME, "logs", "%s.g%d.log" % (w["name"], w["gen"])), "a") as f:
            f.write(time.strftime("%H:%M:%S ") + line.replace("\n", " ")[:400] + "\n")

    def live_names(self):
        return [r[0] for r in self.db.execute("select distinct name from workers").fetchall()]

    # ---- app-server
    async def start_codex(self):
        if not os.path.exists(os.path.join(CODEX_HOME, "auth.json")):
            raise SystemExit("no auth.json in %s (copy it; see README)" % CODEX_HOME)
        self.proc = await asyncio.create_subprocess_exec(CODEX, "app-server", "--listen", "stdio://",
            env=dict(os.environ, CODEX_HOME=CODEX_HOME), cwd=HOME, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE,
            stderr=open(os.path.join(HOME, "app-server.stderr"), "a"), limit=1 << 26)
        asyncio.ensure_future(self.reader())
        await self.rpc("initialize", {"clientInfo": {"name": "cxo", "title": "cxo hub", "version": "2"},
            "capabilities": {"experimentalApi": True, "optOutNotificationMethods": [
                "item/agentMessage/delta", "item/reasoning/textDelta", "item/reasoning/summaryTextDelta",
                "item/reasoning/summaryPartAdded", "item/commandExecution/outputDelta", "item/fileChange/outputDelta",
                "item/plan/delta", "command/exec/outputDelta"]}})
        self.send({"jsonrpc": "2.0", "method": "initialized"})
        self.rate = (await self.rpc("account/rateLimits/read", {})).get("result")
        for name in self.live_names():  # re-attach live workers after a hub restart
            w = self.cur(name)
            if w["state"] in ("RETIRED", "DEAD"):
                continue
            res = await self.rpc("thread/resume", {"threadId": w["thread"]})
            if "error" in res:
                self.upd(w, state="DEAD"); self.event(w, "DEAD", "resume failed: %s" % res["error"].get("message"))
            else:
                self.upd(w, turn=None, pending=0)
                self.event(w, "RESUMED", "hub restarted; worker idle, pending jobs lost. send it 'continue' if needed")

    def send(self, obj):
        self.proc.stdin.write((json.dumps(obj) + "\n").encode())

    async def rpc(self, method, params, timeout=120):
        i = next(self.rid)
        fut = asyncio.get_running_loop().create_future()
        self.pending[i] = fut
        self.send({"jsonrpc": "2.0", "id": i, "method": method, "params": params})
        try:
            return await asyncio.wait_for(fut, timeout)
        except asyncio.TimeoutError:
            return {"error": {"message": "timeout %s" % method}}
        finally:
            self.pending.pop(i, None)

    async def reader(self):
        while True:
            line = await self.proc.stdout.readline()
            if not line:
                for name in self.live_names():
                    w = self.cur(name)
                    if w["state"] not in ("RETIRED", "DEAD"):
                        self.event(w, "HUB_CODEX_EXIT", "app-server exited; restart the hub")
                return
            try:
                m = json.loads(line)
            except ValueError:
                continue
            if "method" in m and "id" in m:
                asyncio.ensure_future(self.on_request(m))
            elif "method" in m:
                try:
                    self.on_note(m["method"], m.get("params") or {})
                except Exception as e:  # never let one bad notification kill the reader
                    sys.stderr.write("note %s: %r\n" % (m["method"], e))
            elif m.get("id") in self.pending:
                self.pending[m["id"]].set_result(m)

    def on_note(self, meth, p):
        if meth == "account/rateLimits/updated":
            self.rate = self.rate or {}
            self.rate["rateLimits"] = p.get("rateLimits", p)
            return
        w = self.by_thread(p.get("threadId", "")) if p.get("threadId") else None
        if not w:
            return
        if meth == "turn/started":
            self.upd(w, turn=p["turn"]["id"], last_item=now(), stalled=0)
            self.turn_flags[w["thread"]] = {"submit_tried": False, "warned": set()}
        elif meth == "item/completed":
            self.upd(w, last_item=now())
            it = p.get("item", {})
            t = it.get("type")
            if t == "agentMessage":
                self.wlog(w, "say " + (it.get("text") or "")[:300])
            elif t == "commandExecution":
                self.execs.get(w["thread"], {}).pop(it.get("id"), None)
                self.wlog(w, "run [%s] %s" % (it.get("exitCode"), it.get("command")))
            elif t == "fileChange":
                self.artifact(w)
                self.wlog(w, "edit " + " ".join(os.path.relpath(c.get("path", "?"), w["wt"]) for c in it.get("changes", [])))
            elif t == "dynamicToolCall":
                self.wlog(w, "tool %s %s" % (it.get("tool"), json.dumps(it.get("arguments"))[:250]))
        elif meth == "item/started":
            self.upd(w, last_item=now())
            it = p.get("item", {})
            if it.get("type") == "commandExecution":
                self.execs.setdefault(w["thread"], {})[it.get("id")] = (it.get("command") or "", now())
        elif meth == "turn/diff/updated":
            self.check_protected_live(w, p.get("diff", ""))
        elif meth == "thread/tokenUsage/updated":
            tot = p["tokenUsage"]["total"]
            self.upd(w, tokens=tot["totalTokens"], reqs=w["reqs"] + 1,
                     unc=tot["inputTokens"] - tot.get("cachedInputTokens", 0) + tot["outputTokens"])
        elif meth == "error":
            e = p.get("error", {})
            info = e.get("codexErrorInfo")
            if isinstance(info, str) and "usage" in info.lower():
                self.paused = True
            if not p.get("willRetry"):
                self.event(w, "ERROR", "%s %s" % (info, e.get("message", "")[:200]))
        elif meth == "turn/completed":
            st = p["turn"].get("status")
            flags = self.turn_flags.pop(w["thread"], {"submit_tried": False})
            self.upd(w, turn=None)
            self.wlog(w, "turn end " + str(st))
            if w["state"] in ("RETIRED", "DEAD", "BUDGET"):
                return
            if st == "failed":
                self.event(w, "TURN_FAILED", json.dumps(p["turn"].get("error"))[:300])
            elif st == "interrupted":
                self.event(w, "INTERRUPTED", "turn interrupted; worker idle")
            elif w["state"] == "WORKING" and not w["pending"] and not flags["submit_tried"]:
                if w["sha"] and tree_id(w["wt"]) == git(w["wt"], "rev-parse", "HEAD^{tree}").strip():
                    self.upd(w, state="SUBMITTED")  # nothing changed since its last submit: idle, not stalled
                elif w["nudges"] < 1:
                    self.upd(w, nudges=w["nudges"] + 1)
                    asyncio.ensure_future(self.start_turn(w, "You ended your turn without calling submit and with nothing pending. "
                        "Either submit with evidence, or call ask_deputy(must_wait=true) with what blocks you and then end your turn."))
                else:
                    self.event(w, "NO_SUBMIT", "turn ended twice without submit; worker idle")

    def check_protected_live(self, w, diff):
        flags = self.turn_flags.get(w["thread"])
        if flags is None:
            return
        paths = set(re.findall(r"^diff --git a/(\S+) b/", diff, re.M))
        hit = [x for x in paths if any(fnmatch.fnmatch(x, g) for g in json.loads(w["protect"])) and x not in flags["warned"]
               and not any(fnmatch.fnmatch(x, g) for g, _ in json.loads(w["unprot"] or "[]"))]
        if hit and w["turn"]:
            flags["warned"].update(hit)
            msg = "STOP: you edited protected path(s) %s. Revert them now; protected files are not yours to change." % ", ".join(hit)
            asyncio.ensure_future(self.rpc("turn/steer", {"threadId": w["thread"], "expectedTurnId": w["turn"],
                                                          "input": [{"type": "text", "text": msg}]}))
            self.event(w, "GUARD", "protected edit steered: " + ", ".join(hit))

    async def on_request(self, m):
        meth, p, rid = m["method"], m.get("params") or {}, m["id"]
        if meth == "item/commandExecution/requestApproval":
            w = self.by_thread(p.get("threadId", ""))
            cmd = p.get("command") or ""
            hint = exec_hint(cmd)
            dec = "accept"
            if not w or w["state"] in ("RETIRED", "DEAD"):
                dec = "decline"
            elif hint:
                dec = "decline"
                self.upd(w, declined=(w["declined"] or 0) + 1)
                self.event(w, "EXEC_REFUSED", "long in-sandbox command refused: %s" % cmd[:140])
                self.wlog(w, "refused " + cmd)
                if w["turn"]:
                    asyncio.ensure_future(self.rpc("turn/steer", {"threadId": w["thread"], "expectedTurnId": w["turn"],
                                                                  "input": [{"type": "text", "text": "DEPUTY: " + hint}]}))
            self.send({"jsonrpc": "2.0", "id": rid, "result": {"decision": dec}})
            return
        if meth == "item/fileChange/requestApproval":  # edits are judged at submit by the guard, not here
            self.send({"jsonrpc": "2.0", "id": rid, "result": {"decision": "accept"}})
            return
        if meth != "item/tool/call":
            dec = "denied" if meth in ("applyPatchApproval", "execCommandApproval") else "decline"
            self.send({"jsonrpc": "2.0", "id": rid, "result": {"decision": dec}})
            return
        w = self.by_thread(p.get("threadId", ""))
        if not w or w["state"] in ("RETIRED", "DEAD") or self.cur(w["name"])["gen"] != w["gen"]:
            text, ok = "This worker generation is retired. Stop now and end your turn.", False
        else:
            fn = getattr(self, "tool_" + p.get("tool", ""), None)
            try:
                text, ok = await fn(w, p.get("arguments") or {}) if fn else ("unknown tool", False)
            except Exception as e:
                text, ok = "hub error in %s: %r" % (p.get("tool"), e), False
        self.send({"jsonrpc": "2.0", "id": rid, "result": {"success": ok, "contentItems": [{"type": "inputText", "text": text}]}})

    # ---- delivery: steer a live turn, else start one
    async def deliver(self, w, text):
        w = self.cur(w["name"]) if self.cur(w["name"])["gen"] == w["gen"] else None
        if not w or w["state"] in ("RETIRED", "DEAD"):
            return "ERR retired"
        if w["state"] in ("SUBMITTED", "WAITING_ASK", "WAITING_JOB") and not (w["state"] == "WAITING_JOB" and w["pending"]):
            self.upd(w, state="WORKING", nudges=0)
        if w["turn"]:
            r = await self.rpc("turn/steer", {"threadId": w["thread"], "expectedTurnId": w["turn"], "input": [{"type": "text", "text": text}]})
            if "error" not in r:
                return "steered"
            w = self.cur(w["name"])
            if w["turn"]:
                return "ERR steer: " + r["error"].get("message", "")
        err = await self.start_turn(w, text)
        return "ERR " + err if err else "turn started"

    # ---- worker tools
    def take_msgs(self, w):
        rows = self.db.execute("select id,text from msgs where name=? and gen=? and delivered=0 order by id", (w["name"], w["gen"])).fetchall()
        for i, _ in rows:
            self.db.execute("update msgs set delivered=1 where id=?", (i,))
        return [t for _, t in rows]

    async def tool_report(self, w, a):
        self.upd(w, last_report=now(), reports=w["reports"] + 1)
        ms = self.take_msgs(w)
        c = self.cad.setdefault(w["thread"], {"reports": [], "art": 0, "flagged": False})
        c["reports"] = [t for t in c["reports"] if t > now() - NARRATE_M * 60] + [now()]
        txt = ("DEPUTY: " + "\nDEPUTY: ".join(ms)) if ms else "ack"
        if len(c["reports"]) > NARRATE_N:
            if not c["flagged"]:
                c["flagged"] = True
                self.event(w, "NARRATING", "%d reports in %dm with no new artifact (jobs=%s req=%s); told to end its turn and wait" % (
                    len(c["reports"]), NARRATE_M, w["pending"], w["reqs"]))
            txt += ("\nHUB: you are narrating. %d reports in %d min and no new file change or job result; each report is a full-context "
                    "model request. END YOUR TURN NOW and wait for the job result (request_build/request_cargo/request_journey)." % (
                        len(c["reports"]), NARRATE_M))
        return txt, True

    async def tool_ask_deputy(self, w, a):
        q, d = a.get("question", ""), a.get("default", "")
        aid = "a%d" % next(self.rid)
        if a.get("must_wait"):
            self.upd(w, state="WAITING_ASK")
            self.event(w, "ASK", "%s %s Q: %s | default: %s" % (aid, w["name"], q, d))
            return "Question %s sent. %s" % (aid, WAIT_TEXT), True
        self.event(w, "NOTE", "%s Q(non-blocking): %s | default: %s" % (aid, q, d))
        return "noted; proceed with your default and record it in WORKLOG.md", True

    def new_job(self, w, kind, what, cmd, tree=None, note=None):
        tk = "%s%d" % (kind[0], int(now() * 1000) % 1000000000)
        log = os.path.join(HOME, "jobs", tk + ".log")
        self.db.execute("insert into jobs(ticket,name,gen,kind,what,status,exit,log,t0,t1,tree,note) values(?,?,?,?,?,?,?,?,?,?,?,?)",
                        (tk, w["name"], w["gen"], kind, what, "queued", None, log, now(), None, tree, note))
        self.upd(w, pending=w["pending"] + 1, state="WAITING_JOB")
        asyncio.ensure_future(self.run_job(w, tk, kind, what, cmd, log))
        return tk

    async def run_job(self, w, tk, kind, what, cmd, log, cwd=None, on_done=None):
        async with self.pool[kind if kind in self.pool else "build"]:
            pk = kind if kind in self.pool else "build"
            self.pool_run[pk] += 1
            try:
                await self._run_job_body(w, tk, kind, what, cmd, log, cwd)
            finally:
                self.pool_run[pk] -= 1
        await self._finish_job(w, tk, kind, what, log, on_done)

    async def _run_job_body(self, w, tk, kind, what, cmd, log, cwd):
        if self.db.execute("select status from jobs where ticket=?", (tk,)).fetchone()[0] == "CANCELLED":
            self.job_rc[tk] = -15
            return
        self.db.execute("update jobs set status='running' where ticket=?", (tk,))
        with open(log, "w") as f:
            f.write("$ %s\n" % cmd); f.flush()
            pr = await asyncio.create_subprocess_exec("bash", "-c", cmd, cwd=cwd or w["wt"], stdout=f, stderr=subprocess.STDOUT,
                                                      stdin=subprocess.DEVNULL, start_new_session=True)
            self.db.execute("update jobs set pid=? where ticket=?", (pr.pid, tk))
            try:
                rc = await asyncio.wait_for(pr.wait(), JOB_TIMEOUT)
            except asyncio.TimeoutError:
                os.killpg(pr.pid, signal.SIGTERM); rc = await pr.wait()
                f.write("\ncxo: killed after %ds\n" % JOB_TIMEOUT)
        self.job_rc[tk] = rc

    async def _finish_job(self, w, tk, kind, what, log, on_done):
        rc = self.job_rc.pop(tk)
        if self.db.execute("select status from jobs where ticket=?", (tk,)).fetchone()[0] == "CANCELLED":
            cw = self.cur(w["name"]) if w else None
            if cw and cw["gen"] == w["gen"]:
                self.upd(cw, pending=max(0, cw["pending"] - 1))
                if cw["pending"] == 0 and cw["state"] == "WAITING_JOB":
                    self.upd(cw, state="WORKING")
            return
        self.db.execute("update jobs set status='done', exit=?, t1=? where ticket=? and status='running'", (rc, now(), tk))
        with open(log, errors="replace") as f:
            tail = "".join(f.readlines()[-30:])
        if on_done:
            await on_done(rc, tail)
            return
        cw = self.cur(w["name"])
        if not cw or cw["gen"] != w["gen"] or cw["state"] in ("RETIRED", "DEAD"):
            return
        if kind == "build" and rc == 0:
            row = self.db.execute("select what, tree from jobs where ticket=?", (tk,)).fetchone()
            need = json.loads(cw["umbrella"] or "[]")
            if need and set(need) <= set(row[0].split()) and row[1]:
                self.upd(cw, green_tree=row[1])
        self.artifact(cw)
        self.upd(cw, pending=max(0, cw["pending"] - 1))
        if cw["pending"] == 0 and cw["state"] == "WAITING_JOB":
            self.upd(cw, state="WORKING")
        note = (self.db.execute("select note from jobs where ticket=?", (tk,)).fetchone() or [None])[0]
        self.event(cw, kind.upper(), "%s exit=%d %s%s" % (tk, rc, what[:120], (" [%s]" % note) if note else ""))
        await self.deliver(cw, "RESULT %s %s exit=%d (%s)\nlog: %s\n%s%s" % (tk, kind, rc, what[:200], log,
                           ("tree: %s\n" % note) if note else "", tail))

    def dirty_job(self, w, a):
        """--allow-dirty: (env prefix, note). The build script's dirty-tree refusal stays the default; the opt-in sets CXO_ALLOW_DIRTY=1
        for it and records the tree's diff hash so the deputy can tie the result to the exact tree."""
        if not a.get("allow_dirty"):
            return "", None
        return "export CXO_ALLOW_DIRTY=1; ", dirty_info(w["wt"])[1]

    async def tool_request_build(self, w, a):
        targets = [t for t in a.get("targets", []) if re.match(r"^[A-Za-z0-9_.+:/@-]+$", t)]
        if not targets:
            return "no valid targets", False
        ad, note = self.dirty_job(w, a)
        cmd = (". %s 2>/dev/null; " % BOX_ENV) + ad + (w["build_cmd"] or BUILD_CMD).format(targets=" ".join(shlex.quote(t) for t in targets))
        tk = self.new_job(w, "build", " ".join(targets), cmd, tree=tree_id(w["wt"]), note=note)
        return "ticket=%s queued (%s). %s" % (tk, " ".join(targets), WAIT_TEXT), True

    async def tool_request_journey(self, w, a):
        script = os.path.normpath(a.get("script", ""))
        full = os.path.join(w["wt"], script)
        if script.startswith("..") or os.path.isabs(script) or not os.path.isfile(full):
            return "script must be an existing file inside your lane (got %r)" % a.get("script"), False
        jbin = os.path.join(os.path.dirname(w["wt"].rstrip("/")), "cxo-artifacts")
        prep = ""
        if not os.path.isdir(jbin) and os.path.exists(FETCH_ARTIFACTS):
            prep = "%s %s %s --link >/dev/null || echo 'cxo: fetch-artifacts %s failed; {bin}/{manifest} unavailable'; " % (
                FETCH_ARTIFACTS, ARTIFACT_TIP, shlex.quote(jbin), ARTIFACT_TIP)
        args = [x.replace("{bin}", os.path.join(jbin, "bin")).replace("{manifest}", os.path.join(jbin, "manifest.json")) for x in a.get("args", [])]
        run = {".py": "python3 ", ".sh": "bash "}.get(os.path.splitext(script)[1], "")
        cmd = ". %s 2>/dev/null; %s%s%s %s" % (BOX_ENV, prep, run, shlex.quote(script), " ".join(shlex.quote(x) for x in args))
        tk = self.new_job(w, "journey", script + " " + " ".join(args), cmd)
        return "ticket=%s queued (journey %s). %s" % (tk, script, WAIT_TEXT), True

    async def tool_request_cargo(self, w, a):
        spec = a.get("spec", "").strip()
        toks = shlex.split(spec)
        if not toks or toks[0] not in ("build", "test", "check", "run", "clippy") or re.search(r"[;&|`$<>]", spec):
            return "spec must be one cargo subcommand (build/test/check/run/clippy) with plain args", False
        if toks[0] == "test" and ("-p" not in toks and "--package" not in toks or
                                  not ("--test" in toks or "--lib" in toks or [t for t in toks[1:] if not t.startswith("-")
                                       and toks[toks.index(t) - 1] not in ("-p", "--package", "--features", "-j")])):
            return "cargo test needs -p PACKAGE and a filter or --test NAME (never an unfiltered suite)", False
        tgt = os.path.join(os.path.dirname(w["wt"].rstrip("/")), "rust-target")
        ad, note = self.dirty_job(w, a)
        cmd = ". %s 2>/dev/null; %sexport CARGO_TARGET_DIR=%s; %s" % (BOX_ENV, ad, shlex.quote(tgt), CARGO_CMD.format(spec=spec))
        tk = self.new_job(w, "cargo", spec, cmd, note=note)
        return "ticket=%s queued (cargo %s). %s" % (tk, spec, WAIT_TEXT), True

    async def tool_build_status(self, w, a):
        row = self.db.execute("select status,exit,log from jobs where ticket=?", (a.get("ticket", ""),)).fetchone()
        if not row:
            return "unknown ticket", False
        if row[0] == "INTERRUPTED":
            return "status=INTERRUPTED (hub restart killed it). Request it again, then END YOUR TURN.", True
        if row[0] != "done":
            self.upd(w, polls=w["polls"] + 1)
            if w["polls"] in (2, 5):
                self.event(w, "POLLING", "worker polled build_status %d times" % w["polls"])
            return "status=%s. %s" % (row[0], WAIT_TEXT), True
        return "status=done exit=%s log=%s (the full result was delivered as a message)" % (row[1], row[2]), True

    async def tool_submit(self, w, a):
        if w["thread"] in self.turn_flags:
            self.turn_flags[w["thread"]]["submit_tried"] = True
        need = json.loads(w["umbrella"] or "[]")
        if need and w["green_tree"] != tree_id(w["wt"]):
            self.event(w, "SUBMIT_REFUSED", "umbrella not green on this tree")
            return ("REFUSED: this worker must build the umbrella green on the exact tree it submits. Call "
                    "request_build(%s), end your turn, and submit after a RESULT with exit=0 (no edits in between)." % json.dumps(need)), True
        findings, waived = guard(w, a.get("waivers") or [])
        if findings:
            git(w["wt"], "reset", "-q")
            self.event(w, "SUBMIT_REFUSED", "; ".join(findings)[:600])
            return ("REFUSED by hub guards:\n- " + "\n- ".join(findings) +
                    "\nFix these and submit again, or ask_deputy. Waivers ('rule:path reason') are for deliberate deletions only."), True
        if subprocess.run(["git", "diff", "--cached", "--quiet", "HEAD"], cwd=w["wt"]).returncode == 0:
            return "nothing changed since your last submit (%s); it stands. End your turn now." % (w["sha"] or "HEAD")[:10], True
        msg = "%s\n\n%s\n\nClaims:\n%s\n%sCx-Worker: %s g%d\nCo-Authored-By: %s via cxo" % (
            a.get("title", "cx: " + w["name"]), a.get("body", ""), "\n".join("- " + c for c in a.get("claims", [])),
            ("Waived:\n" + "\n".join("- " + x for x in waived) + "\n") if waived else "", w["name"], w["gen"], w["model"])
        r = subprocess.run(["git"] + GIT_ID + ["commit", "-q", "-F", "-"], cwd=w["wt"], input=msg, text=True, capture_output=True)
        if r.returncode:
            return "commit failed: " + r.stderr[-400:], False
        sha = git(w["wt"], "rev-parse", "HEAD").strip()
        un = json.loads(w["unprot"] or "[]")
        if un:  # one-shot: spent by this submit
            allow = [g for g in json.loads(w["allow"]) if g not in [x for x, added in un if added]]
            self.upd(w, unprot="[]", allow=json.dumps(allow))
        pushed = ""
        if PUSH_REMOTE and not w["nopush"]:
            ref = PUSH_PREFIX + w["name"]
            pr = subprocess.run(["git", "push", "-q", "-f", PUSH_REMOTE, "HEAD:refs/heads/" + ref], cwd=w["wt"], capture_output=True, text=True)
            pushed = " pushed=" + ref if pr.returncode == 0 else " PUSH-FAILED(%s)" % pr.stderr.strip()[-200:]
        files = git(w["wt"], "diff", "--name-only", w["base"], sha).split()
        self.upd(w, state="SUBMITTED", sha=sha)
        self.event(w, "SUBMIT", "%s..%s files=%d%s%s%s claims: %s" % (w["base"][:10], sha[:10], len(files), pushed,
                   " umbrella=green" if need else "", (" WAIVED: " + "; ".join(waived)) if waived else "",
                   " | ".join(a.get("claims", []))[:400]))
        return "submitted %s. End your turn now." % sha[:10], True

    # ---- turns
    async def start_turn(self, w, text):
        r = await self.rpc("turn/start", {"threadId": w["thread"], "input": [{"type": "text", "text": text}], "effort": w["effort"]})
        if "error" in r:
            return "turn/start failed: " + r["error"].get("message", "")
        self.upd(w, turn=r["result"]["turn"]["id"])
        self.turn_flags.setdefault(w["thread"], {"submit_tried": False, "warned": set()})
        return None

    async def new_thread(self, name, gen, deputy, model, effort, wt, base, allow, protect, prompt, budget, extra, fork_from=None):
        r = await self.rpc("thread/fork", fork_from) if fork_from else await self.rpc("thread/start", {
            "cwd": wt, "model": model, "sandbox": "workspace-write", "approvalPolicy": APPROVAL, "dynamicTools": TOOLS,
            "developerInstructions": DEV_INSTR, "multiAgentMode": "explicitRequestOnly"})
        if "error" in r:
            return None, "thread start failed: " + r["error"].get("message", "")
        tid = r["result"]["thread"]["id"]
        self.db.execute("insert into workers(name,gen,deputy,model,effort,thread,wt,base,state,created,allow,protect,budget,build_cmd,umbrella,nopush)"
                        " values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (name, gen, deputy, model, effort, tid, wt, base, "WORKING", now(),
                        json.dumps(allow), json.dumps(protect), budget, extra.get("build_cmd"), extra.get("umbrella"), 1 if extra.get("nopush") else 0))
        w = self.cur(name)
        err = await self.start_turn(w, prompt)
        if err:
            self.upd(w, state="DEAD")
            return None, err
        return w, None

    # ---- deputy commands
    def pace_ok(self):
        if self.paused:
            return "usage limit hit; paused"
        if self.rate and self.rate.get("ordinaryUsageAllowed") is False:
            return "ordinaryUsageAllowed=false"
        pr = ((self.rate or {}).get("rateLimits") or {}).get("primary") or {}
        if pr.get("resetsAt") and pr.get("windowDurationMins"):
            f = 1 - (pr["resetsAt"] - now()) / (pr["windowDurationMins"] * 60.0)
            if pr.get("usedPercent", 0) > 100 * (f + 1.0 / 7) * 0.85:  # linear pace + one day of headroom
                return "ahead of pace: used %d%% at %.0f%% of window" % (pr["usedPercent"], 100 * f)
        return None

    async def mk_lane(self, lane, frm):
        """mk-lane, then re-point the lane's main at the SHARED remote's ref (E2-1: the warm base can lag the remote).
        frm: None|main|next -> that branch on the shared remote when it has it; any other ref/SHA is fetched from it."""
        base_kw = frm in (None, "main", "next")
        pr = await asyncio.create_subprocess_exec(*([MKLANE] + (["--from", frm] if frm in ("main", "next") else []) + [lane]),
                                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        o = (await pr.communicate())[0].decode(errors="replace")
        wt = os.path.join(LANES, lane, "src")
        if pr.returncode or not os.path.isdir(wt):
            return None, "ERR mk-lane exit %s: %s" % (pr.returncode, o.strip()[-300:]), ""
        note = ""
        if "shared" in git(wt, "remote").split():
            ref = (frm or "main") if base_kw else frm
            r = subprocess.run(["git", "-C", wt, "fetch", "-q", "shared", ref], capture_output=True, text=True)
            if r.returncode == 0:
                sha = git(wt, "rev-parse", "FETCH_HEAD").strip()
                old = git(wt, "rev-parse", "HEAD").strip()
                if sha and sha != old:
                    git(wt, "checkout", "-q", "-B", "main", sha)
                    note = " (warm base %s -> shared/%s %s)" % (old[:8], ref, sha[:8])
            elif not base_kw:
                return None, "ERR --from %s: not fetchable from the shared remote: %s" % (frm, r.stderr.strip()[-200:]), ""
        elif not base_kw:
            return None, "ERR --from %s needs the shared remote, which this lane lacks" % frm, ""
        return wt, None, note

    async def c_spawn(self, a):
        name = a["name"]
        if not re.match(r"^[a-z0-9][a-z0-9._-]*$", name):
            return "ERR name must match [a-z0-9][a-z0-9._-]*"
        old = self.cur(name)
        if old:
            return "ERR name %s exists (g%d %s); pick a new name or use renew" % (name, old["gen"], old["state"])
        p = self.pace_ok()
        if p and not a.get("force"):
            return "ERR admission refused: " + p
        brief = a.get("brief", "").strip()
        if not brief:
            return "ERR empty brief (pipe it on stdin)"
        try:  # validate everything BEFORE mk-lane so a bad flag leaves no orphan lane (E2-2)
            budget = parse_n(a["budget"]) if a.get("budget") else DEFAULT_BUDGET
        except ValueError:
            return "ERR bad --budget %r (N or 12M)" % a["budget"]
        allow = a.get("allow") or []
        protect = ([] if a.get("no_default_protect") else DEFAULT_PROTECT) + (a.get("protect") or [])
        clash = allow_vs_protect(allow, protect)
        if clash:  # E2-3
            return "ERR --allow is covered by a protect glob (the guard would revert the edit): %s; use --no-default-protect and list the protects you want" % \
                ", ".join("%s~%s" % c for c in clash)
        note = ""
        if a.get("mklane"):
            wt, err, note = await self.mk_lane(name, a.get("from"))
            if err:
                return err
            base = git(wt, "rev-parse", "HEAD").strip()
        elif a.get("wt"):
            wt = os.path.abspath(a["wt"]); base = git(wt, "rev-parse", "HEAD").strip()
        else:
            repo = os.path.abspath(a["repo"]); base = git(repo, "rev-parse", a.get("base") or "HEAD").strip()
            wt = os.path.join(HOME, "wt", name)
            r = subprocess.run(["git", "-C", repo, "worktree", "add", "-q", "-b", "cx/" + name, wt, base], capture_output=True, text=True)
            if r.returncode:
                return "ERR worktree: " + r.stderr.strip()[-300:]
        gd = git(wt, "rev-parse", "--git-common-dir").strip()
        excl = os.path.join(wt, gd, "info", "exclude") if not os.path.isabs(gd) else os.path.join(gd, "info", "exclude")
        os.makedirs(os.path.dirname(excl), exist_ok=True)
        with open(excl, "a") as f:
            f.write("\n# cxo\n" + "\n".join("/" + x for x in IGNORE) + "\n")
        with open(os.path.join(HOME, "briefs", name + ".md"), "w") as f:
            f.write(brief)
        umb = None
        if a.get("umbrella"):
            umb = json.dumps(UMBRELLA if a["umbrella"] == "default" else a["umbrella"].split())
        prompt = brief + "\n\n---\nWORKTREE: %s (base %s)\nALLOWED PATHS: %s\nPROTECTED PATHS: %s\n%s" % (
            wt, base[:10], ", ".join(allow) or "(any not protected)", ", ".join(protect),
            ("BEFORE SUBMIT: request_build(%s) must come back exit=0 on the exact tree you submit.\n" % umb) if umb else "")
        w, err = await self.new_thread(name, 1, a["deputy"], a.get("model") or DEFAULT_MODEL, a.get("effort") or "high", wt, base,
                                       allow, protect, prompt, budget,
                                       {"build_cmd": a.get("build_cmd"), "umbrella": umb, "nopush": a.get("no_push")})
        return "ERR " + err if err else "spawned %s g1 %s thread=%s wt=%s%s" % (name, w["model"], w["thread"][:8], wt, note)

    def live(self, name):
        w = self.cur(name)
        if not w:
            return None, "ERR no worker %s" % name
        if w["state"] in ("RETIRED", "DEAD"):
            return None, "ERR REFUSED: %s g%d is %s since %s; no live generation. Do not message it." % (
                name, w["gen"], w["state"], time.strftime("%m-%dT%H:%MZ", time.gmtime(w["retired"] or w["created"])))
        return w, None

    async def c_send(self, a):
        w, err = self.live(a["name"])
        if err:
            return err
        if w["state"] == "BUDGET" and w["tokens"] >= w["budget"]:
            return "ERR %s is over budget (%dM >= %dM): raise it with `cxo budget %s N` first" % (
                w["name"], w["tokens"] // 10**6, w["budget"] // 10**6, w["name"])
        if w["state"] == "BUDGET":
            self.upd(w, state="WORKING")
        text = "DEPUTY: " + a["text"]
        if w["turn"] and not a.get("now"):
            self.db.execute("insert into msgs(name,gen,ts,text) values(?,?,?,?)", (w["name"], w["gen"], now(), a["text"]))
            return "queued for %s's next report (auto-steer after %dm)" % (w["name"], PIGGY_S // 60)
        out = await self.deliver(w, text)
        return out if out.startswith("ERR") else "%s %s" % (out, w["name"])

    async def c_answer(self, a):
        return await self.c_send({"name": a["name"], "text": "ANSWER to %s: %s" % (a["ask"], a["text"]), "now": True})

    async def c_allow(self, a):
        w, err = self.live(a["name"])
        if err:
            return err
        clash = allow_vs_protect(a.get("globs", []), json.loads(w["protect"]))
        if clash:
            return "ERR allow covered by protect (guard would revert): " + ", ".join("%s~%s" % c for c in clash)
        allow = json.loads(w["allow"]) + [g for g in a.get("globs", []) if g not in json.loads(w["allow"])]
        self.upd(w, allow=json.dumps(allow))
        self.db.execute("update workers set allow=? where name=?", (json.dumps(allow), w["name"]))
        return "%s allow: %s" % (w["name"], " ".join(allow))

    async def c_unprotect(self, a):
        """deputy-approved edit to a protected path (e.g. a fixture re-emit): the next submit may include it, once."""
        w, err = self.live(a["name"])
        if err:
            return err
        globs = a.get("globs") or []
        if not globs:
            return "ERR unprotect NAME GLOB..."
        un, allow = json.loads(w["unprot"] or "[]"), json.loads(w["allow"])
        for g in globs:
            added = bool(allow) and g not in allow
            if added:
                allow.append(g)
            un.append([g, added])
        self.upd(w, unprot=json.dumps(un), allow=json.dumps(allow))
        self.event(w, "UNPROTECTED", "deputy approved one submit touching protected %s" % " ".join(globs))
        self.db.execute("insert into msgs(name,gen,ts,text) values(?,?,?,?)", (w["name"], w["gen"], now(),
                        "you may now edit %s (deputy-approved, for your next submit only)" % " ".join(globs)))
        return "%s: next submit may touch %s (one-shot; also added to allow where scoped)" % (w["name"], " ".join(globs))

    async def c_rebase(self, a):
        """rebase a live worker's lane onto REF, hub-side (the sandbox's .git is read-only)."""
        w, err = self.live(a["name"])
        if err:
            return err
        wt, ref = w["wt"], a.get("ref") or ""
        if not ref:
            return "ERR rebase NAME REF"
        if subprocess.run(["git", "status", "--porcelain", *stage_pathspec()], cwd=wt, capture_output=True, text=True).stdout.strip():
            return ("ERR %s's worktree is dirty. Tell the worker to finish and `report` (a stash-free state: submit, or revert), then rebase. "
                    "Never git stash." % w["name"])
        sha = git(wt, "rev-parse", "--verify", "-q", ref + "^{commit}").strip()
        if not sha:  # not local: try the shared remote
            for rem in [r for r in ("shared", PUSH_REMOTE or "origin") if r]:
                r = subprocess.run(["git", "fetch", "-q", rem, ref], cwd=wt, capture_output=True, text=True)
                if r.returncode == 0:
                    sha = git(wt, "rev-parse", "FETCH_HEAD").strip()
                    break
        if not sha:
            return "ERR cannot resolve %s in the lane or the shared remote" % ref
        old_head = git(wt, "rev-parse", "HEAD").strip()
        r = subprocess.run(["git"] + GIT_ID + ["rebase", sha], cwd=wt, capture_output=True, text=True)
        if r.returncode:
            files = git(wt, "diff", "--name-only", "--diff-filter=U").split()
            subprocess.run(["git", "rebase", "--abort"], cwd=wt, capture_output=True)
            self.event(w, "REBASE_CONFLICT", "onto %s: %s" % (sha[:10], " ".join(files)))
            return "ERR rebase conflicts onto %s, aborted (lane unchanged). conflicting: %s" % (sha[:10], " ".join(files) or r.stderr.strip()[-200:])
        new_head = git(wt, "rev-parse", "HEAD").strip()
        old_base = w["base"]
        # the submitted sha (if any) moved with the rebase; the old green tree no longer describes the lane
        self.upd(w, base=sha, green_tree=None, sha=new_head if w["sha"] else w["sha"])
        self.event(w, "REBASED", "%s onto %s (base %s -> %s, head %s -> %s)" % (ref, sha[:10], old_base[:10], sha[:10], old_head[:10], new_head[:10]))
        self.db.execute("insert into msgs(name,gen,ts,text) values(?,?,?,?)", (w["name"], w["gen"], now(),
                        "your lane was rebased onto %s by the hub; re-read files that changed upstream and re-request any build" % sha[:10]))
        return "%s rebased onto %s (base %s -> %s)" % (w["name"], sha[:10], old_base[:10], sha[:10])

    async def c_budget(self, a):
        w, err = self.live(a["name"])
        if err:
            return err
        try:
            n = parse_n(a["n"])
        except ValueError:
            return "ERR bad budget %r (N or 12M)" % a["n"]
        self.upd(w, budget=n)
        return "%s budget=%dM (used %dM)%s" % (w["name"], n // 10**6, w["tokens"] // 10**6,
                                                "; it is idle: send it 'continue'" if w["state"] == "BUDGET" and n > w["tokens"] else "")

    async def c_wait(self, a):
        end = now() + min(int(a.get("timeout") or 540), 590)
        while True:
            q = "select id,ts,worker,kind,text from events where seen=0" + (" and deputy=?" if a.get("deputy") else "") + " order by id"
            rows = self.db.execute(q, (a["deputy"],) if a.get("deputy") else ()).fetchall()
            if rows:
                for r in rows:
                    self.db.execute("update events set seen=1 where id=?", (r[0],))
                return "\n".join("%s %s %s %s" % (time.strftime("%H:%M", time.localtime(r[1])), r[3], r[2], r[4]) for r in rows)
            if now() >= end:
                return "(no events)"
            self.ev_signal.clear()
            try:
                await asyncio.wait_for(self.ev_signal.wait(), end - now())
            except asyncio.TimeoutError:
                pass

    async def c_status(self, a):
        def rpj(h, w):  # model requests per hub job: the disguised-polling meter (E2-5)
            n = h.db.execute("select count(*) from jobs where name=? and gen=?", (w["name"], w["gen"])).fetchone()[0]
            return "%.0f" % ((w["reqs"] or 0) / n) if n else "-"
        out = []
        for name in self.live_names():
            w = self.cur(name)
            if (a.get("deputy") and w["deputy"] != a["deputy"]) or (w["state"] in ("RETIRED", "DEAD") and not a.get("all")):
                continue
            out.append("%s g%d %s %s %s turn=%s rep=%d/%s item=%s tok=%.1fM unc=%.2fM req=%d polls=%d jobs=%d budget=%dM req/job=%s decl=%d%s" % (
                w["name"], w["gen"], w["deputy"], w["state"], w["model"], "on" if w["turn"] else "off", w["reports"], ago(w["last_report"]),
                ago(w["last_item"]), w["tokens"] / 1e6, (w["unc"] or 0) / 1e6, w["reqs"] or 0, w["polls"] or 0, w["pending"] or 0,
                w["budget"] // 10**6, rpj(self, w), w["declined"] or 0, (" sha=" + w["sha"][:10]) if w["sha"] else ""))
        q = dict(self.db.execute("select kind,count(*) from jobs where status='queued' group by kind").fetchall())
        out.append("pools " + " ".join("%s %d/%d%s" % (k, self.pool_run[k], n, (" +%dq" % q[k]) if q.get(k) else "") for k, n in self.pool_n.items()))
        for t in self.db.execute("select name,state,green,last from trains").fetchall():
            out.append("train %s %s green=%s last=%s" % (t[0], t[1], (t[2] or "-")[:10], t[3] or "-"))
        return "\n".join(out) or "(no workers)"

    async def c_limits(self, a):
        self.rate = (await self.rpc("account/rateLimits/read", {})).get("result", self.rate)
        pr = ((self.rate or {}).get("rateLimits") or {}).get("primary") or {}
        return "used=%s%% window=%sm resets=%s allowed=%s paused=%s pace=%s" % (pr.get("usedPercent"), pr.get("windowDurationMins"),
            time.strftime("%m-%d %H:%M", time.localtime(pr["resetsAt"])) if pr.get("resetsAt") else "?",
            (self.rate or {}).get("ordinaryUsageAllowed"), self.paused, self.pace_ok() or "ok")

    async def c_interrupt(self, a):
        w, err = self.live(a["name"])
        if err:
            return err
        if not w["turn"]:
            return "%s idle" % w["name"]
        r = await self.rpc("turn/interrupt", {"threadId": w["thread"], "turnId": w["turn"]})
        return "ERR " + r["error"]["message"] if "error" in r else "interrupted %s" % w["name"]

    async def retire_w(self, w, why, archive=True):
        if w["turn"]:
            await self.rpc("turn/interrupt", {"threadId": w["thread"], "turnId": w["turn"]})
        self.upd(w, state="RETIRED", retired=now(), turn=None)
        if archive:
            await self.rpc("thread/archive", {"threadId": w["thread"]})
        self.event(w, "RETIRED", why)

    async def c_retire(self, a):
        w, err = self.live(a["name"])
        if err:
            return err
        await self.retire_w(w, a.get("why") or "by deputy")
        return "retired %s g%d tok=%.1fM" % (w["name"], w["gen"], w["tokens"] / 1e6)

    async def c_renew(self, a):
        """fresh thread, same worktree, starting from the worker's own WORKLOG.md (or a fork if --fork)"""
        w, err = self.live(a["name"])
        if err:
            return err
        with open(os.path.join(HOME, "briefs", w["name"] + ".md")) as f:
            brief = f.read()
        extra = a.get("text", "").strip()
        prev = {k: w[k] for k in ("state", "turn", "retired")}
        # a fork needs the source thread un-archived: archive it only after the fork exists
        await self.retire_w(w, "renewed to g%d" % (w["gen"] + 1), archive=not a.get("fork"))
        g, fp = w["gen"] + 1, None
        if a.get("fork"):
            fp = {"threadId": w["thread"]}
            if a.get("before_turn"):
                fp["beforeTurnId"] = a["before_turn"]
            prompt = "DEPUTY (after fork): " + (extra or "Continue from your last good state.")
        else:
            prompt = ("You are generation %d of worker %s. Your predecessor's state is in WORKLOG.md in the worktree and in the "
                      "changes there. Read WORKLOG.md first, then continue the brief below.\n%s\n\n%s") % (
                      g, w["name"], ("DEPUTY: " + extra) if extra else "", brief)
        nw, err = await self.new_thread(w["name"], g, w["deputy"], a.get("model") or w["model"], w["effort"], w["wt"], w["base"],
                                        json.loads(w["allow"]), json.loads(w["protect"]), prompt, w["budget"],
                                        {"build_cmd": w["build_cmd"], "umbrella": w["umbrella"], "nopush": w["nopush"]}, fork_from=fp)
        if err and fp:  # failed fork: put the source generation back instead of stranding the name
            self.db.execute("delete from workers where name=? and gen=?", (w["name"], g))
            self.upd(w, state="WORKING" if prev["state"] in ("RETIRED", "DEAD") else prev["state"], retired=prev["retired"])
            return "ERR fork failed (g%d restored, turn interrupted): %s" % (w["gen"], err)
        if fp:
            await self.rpc("thread/archive", {"threadId": w["thread"]})
        return "ERR " + err if err else "renewed %s g%d %s thread=%s" % (w["name"], g, nw["model"], nw["thread"][:8])

    async def c_log(self, a):
        w = self.cur(a["name"])
        if not w:
            return "ERR no worker"
        p = os.path.join(HOME, "logs", "%s.g%d.log" % (w["name"], int(a.get("gen") or w["gen"])))
        if not os.path.exists(p):
            return "(empty)"
        with open(p) as f:
            return "".join(f.readlines()[-int(a.get("n") or 20):]).rstrip()

    async def c_ping(self, a):
        return "hub ok codex=%s home=%s workers=%d" % (self.codex_ver, HOME, self.db.execute("select count(*) from workers").fetchone()[0])

    # ---- integration train: merge one range at a time, umbrella after EACH merge
    async def c_train(self, a):
        name = a["name"]
        if self.db.execute("select 1 from trains where name=?", (name,)).fetchone():
            return "ERR train %s exists" % name
        lane = "train-" + name
        wt, err, note = await self.mk_lane(lane, a.get("from"))
        if err:
            return err
        head = git(wt, "rev-parse", "HEAD").strip()
        self.db.execute("insert into trains values(?,?,?,?,?,?)", (name, a.get("deputy") or "-", wt, head, "GREEN", "created"))
        return "train %s at %s%s wt=%s (base assumed green; run `cxo merge %s --recheck` to prove it)" % (name, head[:10], note, wt, name)

    async def c_merge(self, a):
        t = self.db.execute("select name,deputy,wt,green,state from trains where name=?", (a["name"],)).fetchone()
        if not t:
            return "ERR no train %s" % a["name"]
        name, dep, wt, green, state = t
        if a.get("abort"):
            git(wt, "reset", "-q", "--hard", green)
            self.db.execute("update trains set state='GREEN', last='aborted' where name=?", (name,))
            return "train %s reset to green %s" % (name, green[:10])
        if state == "BUILDING":
            return "ERR train %s is building; wait for TRAIN_GREEN/TRAIN_RED" % name
        if state == "RED" and not a.get("recheck"):
            return "ERR train %s is RED; fix it in %s (spawn a mergefix --wt there), then `merge %s --recheck`, or `--abort`" % (name, wt, name)
        what = "recheck"
        if not a.get("recheck"):
            ref = a["ref"] if a["ref"].startswith("refs/") else "refs/heads/" + (a["ref"] if a["ref"].startswith(PUSH_PREFIX) else PUSH_PREFIX + a["ref"])
            f = subprocess.run(["git", "fetch", "-q", PUSH_REMOTE or "origin", ref], cwd=wt, capture_output=True, text=True)
            if f.returncode:
                return "ERR fetch %s: %s" % (ref, f.stderr.strip()[-200:])
            m = subprocess.run(["git"] + GIT_ID + ["merge", "--no-ff", "-q", "-m", "train %s: merge %s" % (name, ref), "FETCH_HEAD"],
                               cwd=wt, capture_output=True, text=True)
            if m.returncode:
                git(wt, "merge", "--abort")
                return "ERR textual conflict merging %s: %s" % (ref, (m.stdout + m.stderr).strip()[-300:])
            what = ref
        head = git(wt, "rev-parse", "HEAD").strip()
        self.db.execute("update trains set state='BUILDING', last=? where name=?", (what, name))
        cmd = ". %s 2>/dev/null; %s" % (BOX_ENV, BUILD_CMD.format(targets=" ".join(shlex.quote(x) for x in UMBRELLA)))
        tk = "t%d" % (int(now() * 1000) % 1000000000)
        log = os.path.join(HOME, "jobs", tk + ".log")
        ev = {"deputy": dep, "name": "train-" + name, "gen": 0}

        async def done(rc, tail):
            if rc == 0:
                pushed = ""
                if PUSH_REMOTE:
                    p = subprocess.run(["git", "push", "-q", "-f", PUSH_REMOTE, "HEAD:refs/heads/%strain-%s" % (PUSH_PREFIX, name)],
                                       cwd=wt, capture_output=True, text=True)
                    pushed = " pushed=%strain-%s" % (PUSH_PREFIX, name) if p.returncode == 0 else " PUSH-FAILED"
                self.db.execute("update trains set state='GREEN', green=? where name=?", (head, name))
                self.event(ev, "TRAIN_GREEN", "%s %s umbrella green at %s%s" % (name, what, head[:10], pushed), deputy=dep)
            else:
                self.db.execute("update trains set state='RED' where name=?", (name,))
                self.event(ev, "TRAIN_RED", "%s %s umbrella RED at %s (green stays %s) log=%s :: %s" % (
                    name, what, head[:10], green[:10], log, tail.strip().replace("\n", " | ")[-500:]), deputy=dep)
        self.db.execute("insert into jobs(ticket,name,gen,kind,what,status,exit,log,t0,t1,tree) values(?,?,?,?,?,?,?,?,?,?,?)",
                        (tk, "train-" + name, 0, "train", what, "queued", None, log, now(), None, head))
        asyncio.ensure_future(self.run_job(None, tk, "train", what, cmd, log, cwd=wt, on_done=done))
        return "train %s: %s merged at %s; umbrella ticket=%s (event TRAIN_GREEN/TRAIN_RED follows)" % (name, what, head[:10], tk)

    # ---- hub restart: jobs that were running died with the old hub
    async def kill_groups(self, pgids, grace=None):
        """TERM each process group, wait up to `grace` s for it to vanish, then KILL. Jobs are session leaders (pgid == pid)."""
        grace = self.kill_grace if grace is None else grace
        live = []
        for p in pgids:
            try:
                os.killpg(p, signal.SIGTERM); live.append(p)
            except OSError:
                pass
        end = now() + grace
        while live and now() < end:
            await asyncio.sleep(0.1)
            live = [p for p in live if self._alive(p)]
        for p in live:
            try:
                os.killpg(p, signal.SIGKILL)
            except OSError:
                pass

    @staticmethod
    def _alive(pgid):
        try:
            os.killpg(pgid, 0); return True
        except OSError:
            return False

    async def recover_jobs(self):
        rows = self.db.execute("select ticket,name,gen,kind,what,pid from jobs where status in ('running','queued')").fetchall()
        await self.kill_groups([r[5] for r in rows if r[5]])  # the dead hub's children: kill BEFORE reporting, or they run orphaned
        by_worker = {}
        for tk, name, gen, kind, what, pid in rows:
            self.db.execute("update jobs set status='INTERRUPTED', t1=? where ticket=?", (now(), tk))
            if kind == "train":
                tn = name[len("train-"):]
                t = self.db.execute("select deputy from trains where name=?", (tn,)).fetchone()
                self.db.execute("update trains set state='RED', last='interrupted by hub restart' where name=?", (tn,))
                self.event({"deputy": t[0] if t else "-", "name": name, "gen": 0}, "JOB_INTERRUPTED",
                           "%s train build %s killed by hub restart; train marked RED: `cxo merge %s --recheck`" % (tk, what, tn))
                continue
            w = self._row(self.db.execute("select * from workers where name=? and gen=?", (name, gen)))
            if not w or w["state"] in ("RETIRED", "DEAD"):
                continue
            self.event(w, "JOB_INTERRUPTED", "%s %s %s killed by hub restart; worker told to re-request one" % (tk, kind, what[:100]))
            by_worker.setdefault((name, gen), (w, []))[1].append((tk, kind, what))
        for w, jobs in by_worker.values():  # one message per worker, one re-request at a time (no storm)
            lst = "; ".join("%s %s (%s)" % (tk, kind, what[:100]) for tk, kind, what in jobs)
            await self.deliver(w, "HUB: a hub restart INTERRUPTED %d of your jobs (processes killed, no result): %s. Re-request ONLY the "
                                  "single most important one (request_%s), END YOUR TURN, and request the others one at a time "
                                  "after each result." % (len(jobs), lst, jobs[0][1]))

    async def c_cancel(self, a):
        r = self.db.execute("select ticket,name,gen,kind,what,status,pid from jobs where ticket=?", (a.get("ticket", ""),)).fetchone()
        if not r:
            return "ERR no job %s" % a.get("ticket")
        tk, name, gen, kind, what, st, pid = r
        if st not in ("running", "queued"):
            return "ERR job %s is %s" % (tk, st)
        if kind == "train":
            return "ERR %s is a train build: `cxo merge TRAIN --abort` (or --recheck)" % tk
        self.db.execute("update jobs set status='CANCELLED', t1=? where ticket=?", (now(), tk))
        if pid:
            await self.kill_groups([pid])
        w = self._row(self.db.execute("select * from workers where name=? and gen=?", (name, gen)))
        if w and w["state"] not in ("RETIRED", "DEAD"):
            self.event(w, "JOB_CANCELLED", "%s %s %s cancelled by deputy" % (tk, kind, what[:100]))
            await self.deliver(w, "HUB: your %s job %s (%s) was CANCELLED by the deputy; it produced no result. Do not re-request "
                                  "it unless told to." % (kind, tk, what[:160]))
        return "cancelled %s (%s %s)" % (tk, kind, what[:60])

    def stop_jobs(self):
        """hub shutdown: kill the live jobs' process groups; rows stay 'running' so the next start reports them."""
        for (p,) in self.db.execute("select pid from jobs where status='running' and pid is not null").fetchall():
            try:
                os.killpg(p, signal.SIGKILL)
            except OSError:
                pass

    # ---- monitor
    async def monitor(self):
        while True:
            await asyncio.sleep(20)
            for name in self.live_names():
                w = self.cur(name)
                if w["state"] in ("RETIRED", "DEAD", "BUDGET") or not w["turn"]:
                    continue
                if w["tokens"] > w["budget"]:
                    await self.rpc("turn/interrupt", {"threadId": w["thread"], "turnId": w["turn"]})
                    self.upd(w, state="BUDGET")
                    self.event(w, "BUDGET", "token budget %dM exceeded (%.1fM, uncached %.2fM); interrupted. `cxo budget %s N` then "
                               "send, or renew/retire" % (w["budget"] // 10**6, w["tokens"] / 1e6, (w["unc"] or 0) / 1e6, w["name"]))
                    continue
                for iid, (cmd, t0) in list(self.execs.get(w["thread"], {}).items()):
                    if now() - t0 > EXEC_CAP_S:  # approved (short-looking) but still running: tell it, once
                        self.execs[w["thread"]].pop(iid, None)
                        self.event(w, "LONG_EXEC", "in-sandbox command running %ds: %s" % (now() - t0, cmd[:140]))
                        await self.rpc("turn/steer", {"threadId": w["thread"], "expectedTurnId": w["turn"], "input": [{"type": "text",
                            "text": "DEPUTY: that command has run over %ds in your sandbox. Do not wait on it with notes; for anything long use "
                                    "request_build / request_cargo / request_journey and END YOUR TURN." % EXEC_CAP_S}]})
                if w["last_item"] and now() - w["last_item"] > STALL_S and not w["stalled"]:
                    self.upd(w, stalled=1)
                    self.event(w, "STALL", "no activity for %dm in an active turn" % ((now() - w["last_item"]) // 60))
                old = self.db.execute("select id,text from msgs where name=? and gen=? and delivered=0 and ts<?",
                                      (w["name"], w["gen"], now() - PIGGY_S)).fetchall()
                if old:
                    r = await self.rpc("turn/steer", {"threadId": w["thread"], "expectedTurnId": w["turn"],
                                                      "input": [{"type": "text", "text": "DEPUTY: " + "\nDEPUTY: ".join(t for _, t in old)}]})
                    if "error" not in r:
                        for i, _ in old:
                            self.db.execute("update msgs set delivered=1 where id=?", (i,))

    # ---- socket server
    async def client(self, reader, writer):
        try:
            req = json.loads(await reader.readline())
            fn = getattr(self, "c_" + req["cmd"], None)
            out = await fn(req.get("args") or {}) if fn else "ERR unknown command"
        except Exception as e:
            out = "ERR %r" % e
        writer.write((json.dumps({"out": out}) + "\n").encode())
        await writer.drain()
        writer.close()

    async def run(self):
        self.codex_ver = subprocess.run([CODEX, "--version"], capture_output=True, text=True).stdout.strip()
        await self.start_codex()
        await self.recover_jobs()
        if os.path.exists(SOCK):
            os.unlink(SOCK)
        srv = await asyncio.start_unix_server(self.client, path=SOCK, limit=1 << 24)
        os.chmod(SOCK, 0o600)
        asyncio.ensure_future(self.monitor())
        def term():
            self.stop_jobs(); os._exit(0)
        asyncio.get_running_loop().add_signal_handler(signal.SIGTERM, term)
        async with srv:
            await srv.serve_forever()


async def _hub_main():
    await Hub().run()


def guard(w, waivers):
    """stage everything except IGNORE, then judge the staged diff against base. Returns (findings, waived)."""
    wt, base = w["wt"], w["base"]
    git(wt, "add", "-A", *stage_pathspec())
    files = [f for f in git(wt, "diff", "--cached", "--name-only", base).split("\n") if f and f not in IGNORE]
    if not files:
        return ["empty: no changes against base %s" % base[:10]], []
    allow, prot = json.loads(w["allow"]), json.loads(w["protect"])
    once = [g for g, _ in json.loads(w.get("unprot") or "[]")]
    found = []
    for f in files:
        if any(fnmatch.fnmatch(f, g) for g in prot) and not any(fnmatch.fnmatch(f, g) for g in once):
            found.append("protected:%s" % f)
        elif allow and not any(fnmatch.fnmatch(f, g) for g in allow):
            found.append("scope:%s (outside ALLOWED %s)" % (f, ",".join(allow)))
    cur = None
    for line in git(wt, "diff", "--cached", "-U0", base).split("\n"):
        if line.startswith("+++ "):
            cur = line[6:] if line.startswith("+++ b/") else cur
        elif line.startswith("--- "):
            cur = line[6:] if line.startswith("--- a/") else cur
        elif line.startswith("+") and cur:
            for rule, rx in ([] if DATA_FILE_RX.search(cur) else ADDED_RULES):
                if re.search(rx, line[1:]) and not (rule == "pipe-tail" and not re.search(r"\.(sh|bash|py|toml|yml|yaml)$|^scripts/", cur)):
                    found.append("%s:%s +%s" % (rule, cur, line[1:].strip()[:80]))
        elif line.startswith("-") and cur:
            for rule, rx in ([] if DATA_FILE_RX.search(cur) else REMOVED_RULES):
                if re.search(rx, line[1:]):
                    found.append("%s:%s -%s" % (rule, cur, line[1:].strip()[:80]))
    waived, keep = [], []
    wkeys = {x.split(" ", 1)[0]: x for x in waivers}
    for f in found:
        key = f.split(" ", 1)[0]
        if key in wkeys and not key.startswith(("protected:", "scope:", "empty")):
            waived.append(wkeys[key])
        else:
            keep.append(f)
    return keep, waived


# ---------------------------------------------------------------- client
def call(cmd, args, timeout=600):
    import socket
    s = socket.socket(socket.AF_UNIX)
    s.settimeout(timeout)
    try:
        s.connect(SOCK)
    except OSError:
        raise ConnectionError("ERR hub not running (cxo hub start)")
    s.sendall((json.dumps({"cmd": cmd, "args": args}) + "\n").encode())
    buf = b""
    while not buf.endswith(b"\n"):
        chunk = s.recv(1 << 16)
        if not chunk:
            break
        buf += chunk
    return json.loads(buf)["out"]


USAGE = """cxo — Codex hub. One terse line per item; ERR... on failure (exit 1).
  hub start|stop|run | ping | limits | status [-d DEP] [--all]
  spawn NAME -d DEP (--mklane [--from main|next|REF|SHA] | --repo PATH [--base REF] | --wt PATH) [-m MODEL] [-e EFFORT]
        [--allow GLOB]... [--protect GLOB]... [--no-default-protect] [--budget N|12M] [--umbrella default|"T1 T2"]
        [--build-cmd 'CMD {targets}'] [--no-push] [--force]   < brief.md
  cancel TICKET              (kill a running/queued job's process group; worker is told; status CANCELLED)
  rebase NAME REF            (hub-side `git rebase REF` in the lane; refuses a dirty tree; conflicts abort + list files)
  unprotect NAME GLOB...     (deputy-approved one-shot edit of a protected path; event UNPROTECTED)
  send NAME [--now] TEXT...   answer NAME ASKID TEXT...   allow NAME GLOB...   budget NAME N|12M
  wait [-d DEP] [-t SECS<=590]   interrupt NAME   retire NAME [why...]   log NAME [-n N] [--gen G]
  renew NAME [--fork [--before-turn ID]] [-m MODEL] [TEXT...]
  train NAME -d DEP [--from main|next|REF|SHA]     merge TRAIN REF | merge TRAIN --recheck | merge TRAIN --abort
  selftest [-m MODEL]"""


def parse(argv):
    a, pos, i = {}, [], 0
    flags = {"-d": "deputy", "--deputy": "deputy", "--repo": "repo", "--base": "base", "--wt": "wt", "-m": "model", "--model": "model",
             "-e": "effort", "--budget": "budget", "-t": "timeout", "-n": "n", "--gen": "gen", "--before-turn": "before_turn",
             "--from": "from", "--umbrella": "umbrella", "--build-cmd": "build_cmd"}
    multi = {"--allow": "allow", "--protect": "protect"}
    bools = {"--now": "now", "--all": "all", "--force": "force", "--fork": "fork", "--mklane": "mklane",
             "--no-default-protect": "no_default_protect", "--no-push": "no_push", "--abort": "abort", "--recheck": "recheck"}
    while i < len(argv):
        x = argv[i]
        if x in flags:
            a[flags[x]] = argv[i + 1]; i += 2
        elif x in multi:
            a.setdefault(multi[x], []).append(argv[i + 1]); i += 2
        elif x in bools:
            a[bools[x]] = True; i += 1
        else:
            pos.append(x); i += 1
    return a, pos


def selftest(model):
    """Exercises: report; submit refused (scope + umbrella-not-built); `allow`; request_build delivered without polling
    (tokens measured across the wait); clean submit; request_journey outside the sandbox (unix socket); retire; refusals."""
    ts = time.strftime("%m%d%H%M%S")
    repo = os.path.join(HOME, "selftest", "repo-" + ts)
    for d in ("allowed", "other", "journeys"):
        os.makedirs(os.path.join(repo, d))
    files = {"allowed/a.txt": "a\n", "other/b.txt": "b\n", "journeys/smoke.py":
             "import socket, os, sys, tempfile\np = os.path.join(tempfile.mkdtemp(), 's')\ns = socket.socket(socket.AF_UNIX)\n"
             "s.bind(p); s.listen(1)\nc = socket.socket(socket.AF_UNIX); c.connect(p)\nprint('JOURNEY-SMOKE PASS unix-socket ok args=%s' % sys.argv[1:])\n"}
    for p, t in files.items():
        with open(os.path.join(repo, p), "w") as f:
            f.write(t)
    for c in (["init", "-q"], ["add", "-A"], GIT_ID + ["commit", "-q", "-m", "selftest base"]):
        subprocess.run(["git"] + c, cwd=repo, check=True)
    name, dep = "selftest-" + ts, "selftest"
    brief = ("SELFTEST. Do exactly this, nothing else:\n1. Call report(phase='start', note='begin').\n"
             "2. Append a line 'hello' to allowed/a.txt AND append a line 'hello' to other/b.txt (both, deliberately).\n"
             "3. Call submit(title='selftest', body='selftest', claims=['appended hello'], waivers=[]).\n"
             "4. If submit is refused, call report(phase='refused', note=<the findings>) and then END YOUR TURN. Do not fix anything yet.")
    res, t0 = [], time.time()

    def step(label, ok, detail):
        res.append(ok)
        print("%s %-36s %s" % ("PASS" if ok else "FAIL", label, detail.replace("\n", " | ")[:300]))
        sys.stdout.flush()

    def st():
        s = [l for l in call("status", {"deputy": dep, "all": True}).split("\n") if l.startswith(name + " ")][0]
        g = lambda k: float(re.search(k + r"=([\d.]+)", s).group(1))
        return s, g

    def wait_for(kinds, limit, need=None):
        end, seen = time.time() + limit, []
        while time.time() < end:
            out = call("wait", {"deputy": dep, "timeout": min(120, max(1, int(end - time.time())))})
            if out != "(no events)":
                seen += out.split("\n")
                hit = [e for e in seen if e.split(" ")[1] in kinds and (need is None or need in e)]
                if hit:
                    return hit[0], seen
        return None, seen

    def idle(limit=180):
        for _ in range(limit // 3):
            if "turn=off" in call("status", {"deputy": dep}):
                return True
            time.sleep(3)
        return False

    out = call("spawn", {"name": name, "deputy": dep, "repo": repo, "allow": ["allowed/*", "journeys/*"], "model": model, "effort": "low",
                         "brief": brief, "budget": 3000000, "force": True, "umbrella": "SelftestUmbrella",
                         "build_cmd": "sleep 45; echo built {targets}", "no_push": True})
    step("spawn (--umbrella, --build-cmd)", out.startswith("spawned"), out)
    if not out.startswith("spawned"):
        return 1
    ev, seen = wait_for({"SUBMIT_REFUSED", "SUBMIT"}, 420)
    step("first submit refused (scope or umbrella)", bool(ev) and " SUBMIT_REFUSED " in ev and ("scope:other/b.txt" in ev or "umbrella" in ev),
         ev or " | ".join(seen))
    s, g = st()
    step("worker reported via tool", g("rep") >= 1, s)
    idle()
    out = call("allow", {"name": name, "globs": ["other/*"]})
    step("cxo allow widens scope", "other/*" in out, out)
    out = call("send", {"name": name, "text": "Scope now includes other/*. Call request_build(['SelftestUmbrella']) and follow its "
                        "instructions exactly; when its RESULT arrives with exit=0, call submit again (same arguments)."})
    step("deputy send (idle -> new turn)", out.startswith("turn started"), out)
    ev, seen = wait_for({"BUILD"}, 300)
    s0, g0 = st()  # the worker ended its turn right after request_build; nothing ran until this RESULT
    step("build requested and completed", bool(ev) and "exit=0" in ev, ev or " | ".join(seen))
    ev2, seen2 = wait_for({"SUBMIT", "SUBMIT_REFUSED"}, 300, need=None)
    s1, g1 = st()
    log = call("log", {"name": name, "n": 60})
    # the wait window: between the request_build tool call and the delivered RESULT the model must make no requests
    lines = log.split("\n")
    i_req = max([i for i, l in enumerate(lines) if "tool request_build" in l] or [-1])
    i_end = next((i for i in range(i_req + 1, len(lines)) if "turn end" in lines[i]), None)
    step("no build_status polls", g1("polls") == 0 and "build_status" not in log, "polls=%d" % g1("polls"))
    step("worker ended turn while build ran", i_end is not None and "tool" not in " ".join(lines[i_req + 1:i_end]),
         " / ".join(lines[i_req:i_end + 1])[-200:])
    step("clean submit accepted (umbrella green)", bool(ev2) and " SUBMIT " in ev2 and "umbrella=green" in ev2, ev2 or " | ".join(seen2))
    wt = os.path.join(HOME, "wt", name)
    files = sorted(git(wt, "show", "--name-only", "--format=", "HEAD").split())
    step("commit holds a.txt+b.txt, no WORKLOG", files == ["allowed/a.txt", "other/b.txt"], "HEAD files=%s" % files)
    step("selftest did not push", "pushed=" not in (ev2 or ""), (ev2 or "")[:120])
    idle()
    out = call("send", {"name": name, "text": "Call request_journey(script='journeys/smoke.py', args=['--bin', '{bin}']) and end your "
                        "turn. When the RESULT arrives, call report(phase='journey', note=<the PASS line>) and end your turn."})
    ev, seen = wait_for({"JOURNEY"}, 300)
    step("request_journey ran outside sandbox", bool(ev) and "exit=0" in ev, ev or " | ".join(seen))
    idle()
    jlog = call("log", {"name": name, "n": 80})
    step("journey RESULT reached the worker", "JOURNEY-SMOKE PASS" in jlog or "unix-socket ok" in jlog, jlog.split("\n")[-3:][0][:200])
    out = call("retire", {"name": name, "why": "selftest done"})
    step("retire", out.startswith("retired"), out)
    out = call("send", {"name": name, "text": "are you there?"})
    step("send to retired name refused", out.startswith("ERR REFUSED"), out)
    out = call("allow", {"name": name, "globs": ["x"]})
    step("allow on retired name refused", out.startswith("ERR REFUSED"), out)
    s, g = st()
    print("worker: " + s)
    print("tokens at build result: tok=%.2fM unc=%.3fM req=%d | at submit: tok=%.2fM unc=%.3fM req=%d" % (
        g0("tok"), g0("unc"), g0("req"), g1("tok"), g1("unc"), g1("req")))
    print("log:\n" + call("log", {"name": name, "n": 60}))
    print("limits: " + call("limits", {}))
    print("%s %d/%d in %ds" % ("SELFTEST PASS" if all(res) else "SELFTEST FAIL", sum(res), len(res), time.time() - t0))
    return 0 if all(res) else 1


def selftest_local():
    """No Codex, no box: guard rules, budget/allow parsing, request_cargo validation, the BUDGET interrupt (mock rpc),
    and the train on real git (clean merge -> GREEN, semantic conflict -> TRAIN_RED, textual conflict, abort)."""
    g = globals()
    root = tempfile.mkdtemp(prefix="cxo-local-")
    g["HOME"] = os.path.join(root, "home")
    g["PUSH_REMOTE"] = os.path.join(root, "remote.git")
    g["BOX_ENV"] = "/nonexistent"
    g["BUILD_CMD"] = "if test -e RED; then echo planted RED; exit 3; fi  # {targets}"
    res = []

    def step(label, ok, detail=""):
        res.append(bool(ok))
        print("%s %-44s %s" % ("PASS" if ok else "FAIL", label, str(detail).replace("\n", " | ")[:200]))

    def sh(cwd, *c):
        return subprocess.run(["git"] + GIT_ID + list(c), cwd=cwd, capture_output=True, text=True, check=True).stdout
    # -- pure helpers
    step("parse_n 15M / 1.5m / 7", (parse_n("15M"), parse_n("1.5m"), parse_n("7")) == (15000000, 1500000, 7))
    step("allow~protect: TokenCensus.lean covered", allow_vs_protect(["TokenCensus.lean"], DEFAULT_PROTECT) != [])
    step("allow~protect: Kernel/Foo* clean", allow_vs_protect(["Kernel/Foo*"], DEFAULT_PROTECT) == [])
    # -- guard
    wr = os.path.join(root, "gw")
    os.makedirs(os.path.join(wr, "scripts/gates/objective-manifest")); os.makedirs(os.path.join(wr, "L"))
    sh(root, "init", "-q", "gw")
    open(os.path.join(wr, "scripts/gates/objective-manifest/p.tsv"), "w").write("-theorem\tFoo\th1\n")
    open(os.path.join(wr, "L/A.lean"), "w").write("theorem foo : True := trivial\n")
    sh(wr, "add", "-A"); sh(wr, "commit", "-q", "-m", "b"); base = sh(wr, "rev-parse", "HEAD").strip()
    open(os.path.join(wr, "scripts/gates/objective-manifest/p.tsv"), "w").write("-theorem\tFoo\th2\n")
    w = {"wt": wr, "base": base, "allow": "[]", "protect": "[]"}
    f, _ = guard(w, [])
    step("guard: regenerated pin TSV not flagged (E2-4)", f == [], f)
    open(os.path.join(wr, "L/A.lean"), "w").write("-- gone\n")
    f, _ = guard(w, [])
    step("guard: Lean theorem deletion still flagged", any(x.startswith("del-theorem:L/A.lean") for x in f), f)
    # -- hub-level
    async def hub_tests():
        h = Hub()
        # budget interrupt
        calls = []

        async def rpc(m, p):
            calls.append(m); return {}
        h.rpc = rpc
        h.db.execute("insert into workers(name,gen,deputy,model,effort,thread,wt,base,state,turn,tokens,budget,created,allow,protect,"
                     "last_item) values('b',1,'d','m','low','th','/x','0','WORKING','tu',5000000,1000000,0,'[]','[]',0)")
        real_sleep = asyncio.sleep
        async def fast(t): await real_sleep(0.01)
        g["asyncio"].sleep = fast
        mt = asyncio.ensure_future(h.monitor()); await real_sleep(0.2); mt.cancel()
        g["asyncio"].sleep = real_sleep
        step("budget interrupt: turn/interrupt + BUDGET", "turn/interrupt" in calls and h.cur("b")["state"] == "BUDGET"
             and h.db.execute("select 1 from events where kind='BUDGET'").fetchone(), calls)
        r = await h.c_send({"name": "b", "text": "hi"})
        step("send refused while over budget", r.startswith("ERR") and "budget" in r, r)
        r = await h.c_budget({"name": "b", "n": "9M"})
        step("budget raise", "budget=9M" in r, r)
        # request_cargo
        jobs = []
        h.new_job = lambda w, kind, what, cmd, tree=None, note=None: jobs.append((kind, cmd, note)) or "c1"
        w = {"name": "b", "gen": 1, "wt": "/lanes/b/src"}
        for spec, ok in (("test -p mini-client", False), ("test -p mini-client --test frames", True), ("test -p x frames_roundtrip", True),
                         ("build -p x; rm -rf /", False), ("publish", False), ("check -p mini-client", True)):
            msg, queued = await h.tool_request_cargo(w, {"spec": spec})
            step("request_cargo %r" % spec, queued == ok, msg[:90])
        step("request_cargo sets CARGO_TARGET_DIR beside the lane", jobs and "CARGO_TARGET_DIR=/lanes/b/rust-target" in jobs[0][1], jobs[:1])
        # E2-5: long in-sandbox work is refused with a hint; narration is flagged
        sent, steers = [], []
        h.send = lambda o: sent.append(o)
        async def rpc2(m, p):
            steers.append((m, p)); return {}
        h.rpc = rpc2
        h.db.execute("insert into workers(name,gen,deputy,model,effort,thread,wt,base,state,turn,tokens,budget,created,allow,protect,"
                     "last_item,reqs) values('e',1,'d','m','low','te','/x','0','WORKING','tu',0,99000000,0,'[]','[]',0,60)")
        for i, (cmd, want) in enumerate((("/bin/zsh -lc 'lake build Minidregg'", "request_build"),
                                         ("rg -n x scripts/pipeline/merge-gate-checks.sh", None),
                                         ("rg -n 'a|merge-gate-checks|b' scripts/ && cat scripts/pipeline/check-objective-proofs.sh", None),
                                         ("/bin/zsh -lc \"grep -n hyp-ledger scripts/x.sh | head\"", None),
                                         ("bash -n scripts/pipeline/merge-gate-checks.sh", None),
                                         ("FOO=1 bash scripts/pipeline/check-objective-proofs.sh", "request_journey"),
                                         ("bash scripts/pipeline/merge-gate-checks.sh", "request_journey"),
                                         ("sed -n 1,5p native/resource-client/journey.d/m4.sh", None),
                                         ("/bin/zsh -lc 'cd x && chmod +x edge/mini/journey/run.sh'", None),
                                         ("bash -n native/resource-client/journey.d/m4.sh", None),
                                         ("bash native/resource-client/journey.d/m4.sh --fast", "request_journey"),
                                         ("/bin/zsh -lc 'cd w && python3 edge/mini/journey/go.py x'", "request_journey"), ("cargo test -p x --test y", "request_cargo"),
                                         ("bash scripts/pipeline/merge-gate-checks.sh", "request_journey"), ("ls journeys/", None),
                                         ("/bin/zsh -lc 'grep -rn hyp-ledger scripts'", None), ("lake env lean Foo.lean", None))):
            n0 = len(sent)
            await h.on_request({"id": 100 + i, "method": "item/commandExecution/requestApproval", "params": {"threadId": "te", "command": cmd}})
            await real_sleep(0.01)
            dec = sent[n0]["result"]["decision"]
            hinted = steers and steers[-1][0] == "turn/steer" and want and want in steers[-1][1]["input"][0]["text"]
            step("exec approval %r" % cmd[:34], dec == ("decline" if want else "accept") and (not want or hinted), (dec, want))
        step("EXEC_REFUSED events + declined counter", h.cur("e")["declined"] == 7 and
             h.db.execute("select count(*) from events where kind='EXEC_REFUSED'").fetchone()[0] == 7)
        await h.on_request({"id": 200, "method": "item/fileChange/requestApproval", "params": {"threadId": "te"}})
        step("fileChange approval accepted", sent[-1]["result"]["decision"] == "accept")
        h.execs["te"] = {"i1": ("sleep 5", now() - 60)}
        h.upd(h.cur("e"), state="WORKING")
        real_sleep2 = asyncio.sleep
        async def fast2(t): await real_sleep2(0.01)
        g["asyncio"].sleep = fast2
        mt = asyncio.ensure_future(h.monitor()); await real_sleep2(0.2); mt.cancel()
        g["asyncio"].sleep = real_sleep2
        step("running exec over cap -> LONG_EXEC + steer", h.db.execute("select count(*) from events where kind='LONG_EXEC'").fetchone()[0] == 1)
        w = h.cur("e"); outs = []
        for _ in range(6):
            outs.append((await h.tool_report(w, {"phase": "x", "note": "still running"}))[0])
        step("cadence: >4 reports, no artifact -> NARRATING", "END YOUR TURN" in outs[-1] and "narrating" not in outs[0] and
             h.db.execute("select count(*) from events where kind='NARRATING'").fetchone()[0] == 1, outs[-1][:80])
        h.artifact(w)
        step("artifact resets the cadence", "narrating" not in (await h.tool_report(w, {}))[0])
        step("status shows req/job and decl", "req/job=" in await h.c_status({}) and "decl=7" in await h.c_status({}))
        # train
        sh(root, "init", "-q", "--bare", "remote.git")
        seed = os.path.join(root, "seed")
        sh(root, "clone", "-q", g["PUSH_REMOTE"], "seed")
        open(os.path.join(seed, "x.txt"), "w").write("a\nb\nc\n"); sh(seed, "add", "-A"); sh(seed, "commit", "-q", "-m", "base")
        sh(seed, "push", "-q", "origin", "HEAD:refs/heads/main")
        def lane(n, fn, text):
            sh(seed, "checkout", "-q", "-B", n, "origin/main"); open(os.path.join(seed, fn), "w").write(text)
            sh(seed, "add", "-A"); sh(seed, "commit", "-q", "-m", n); sh(seed, "push", "-q", "-f", "origin", "%s:refs/heads/lane/%s" % (n, n))
        lane("ok", "y.txt", "y\n"); lane("red", "RED", "x\n"); lane("c1", "x.txt", "a\nB1\nc\n"); lane("c2", "x.txt", "a\nB2\nc\n")
        twt = os.path.join(root, "train")
        sh(root, "clone", "-q", g["PUSH_REMOTE"], "train"); sh(twt, "checkout", "-q", "main")
        head = sh(twt, "rev-parse", "HEAD").strip()
        h.db.execute("insert into trains values('t','d',?,?,'GREEN','created')", (twt, head))
        async def ev(kind):
            for _ in range(300):
                r = h.db.execute("select text from events where kind=? order by id desc limit 1", (kind,)).fetchone()
                if r and r[0] not in seen:
                    seen.add(r[0]); return r[0]
                await real_sleep(0.05)
        seen = set()
        r = await h.c_merge({"name": "t", "ref": "ok"}); e = await ev("TRAIN_GREEN")
        step("train: clean merge -> TRAIN_GREEN", e and "umbrella green" in e, r + " / " + str(e))
        r = await h.c_merge({"name": "t", "ref": "red"}); e = await ev("TRAIN_RED")
        step("train: semantic break -> TRAIN_RED", e and "RED" in e and "planted RED" in e, e)
        r = await h.c_merge({"name": "t", "ref": "c1"})
        step("train: merges refused while RED", r.startswith("ERR") and "RED" in r, r)
        r = await h.c_merge({"name": "t", "abort": True})
        step("train: abort resets to green", head not in r and "reset" in r and not os.path.exists(os.path.join(twt, "RED")), r)
        r = await h.c_merge({"name": "t", "ref": "c1"}); await ev("TRAIN_GREEN")
        r = await h.c_merge({"name": "t", "ref": "c2"})
        step("train: textual conflict refused, tree clean", r.startswith("ERR textual") and not sh(twt, "status", "--porcelain").strip(), r)
        # ---- CXO-FIX-2: rebase / unprotect / allow-dirty / interrupted jobs
        rr = os.path.join(root, "rb")
        sh(root, "init", "-q", "-b", "main", "rb")
        for fn, t in (("f.txt", "1\n2\n3\n"), ("g.txt", "g\n")):
            open(os.path.join(rr, fn), "w").write(t)
        sh(rr, "add", "-A"); sh(rr, "commit", "-q", "-m", "base"); b0 = sh(rr, "rev-parse", "HEAD").strip()
        sh(rr, "checkout", "-q", "-b", "up-ok"); open(os.path.join(rr, "h.txt"), "w").write("h\n"); sh(rr, "add", "-A"); sh(rr, "commit", "-q", "-m", "up")
        up_ok = sh(rr, "rev-parse", "HEAD").strip()
        sh(rr, "checkout", "-q", "-b", "up-bad", b0); open(os.path.join(rr, "f.txt"), "w").write("1\nUP\n3\n"); sh(rr, "commit", "-qam", "up2")
        sh(rr, "checkout", "-q", "-b", "lane", b0); open(os.path.join(rr, "f.txt"), "w").write("1\nLANE\n3\n"); sh(rr, "commit", "-qam", "lane work")
        h.db.execute("insert into workers(name,gen,deputy,model,effort,thread,wt,base,state,created,allow,protect,sha,green_tree) "
                     "values('r',1,'d','m','low','tr',?,?,'WORKING',0,'[]','[]','x','gt')", (rr, b0))
        open(os.path.join(rr, "dirty.txt"), "w").write("d\n")
        r = await h.c_rebase({"name": "r", "ref": "up-ok"})
        step("rebase: dirty worktree refused, no stash advice", r.startswith("ERR") and "dirty" in r and "Never git stash" in r, r)
        os.unlink(os.path.join(rr, "dirty.txt"))
        r = await h.c_rebase({"name": "r", "ref": "up-bad"})
        step("rebase: conflict aborted, files listed, lane intact", r.startswith("ERR") and "f.txt" in r and not sh(rr, "status", "--porcelain").strip()
             and not os.path.isdir(os.path.join(rr, ".git/rebase-merge")) and h.cur("r")["base"] == b0, r)
        r = await h.c_rebase({"name": "r", "ref": "up-ok"})
        w = h.cur("r")
        step("rebase: clean -> base moved, REBASED event, green reset", w["base"] == up_ok and w["green_tree"] is None
             and sh(rr, "merge-base", "--is-ancestor", up_ok, "HEAD") == "" and h.db.execute("select 1 from events where kind='REBASED'").fetchone(), r)
        r = await h.c_rebase({"name": "r", "ref": "no-such-ref"})
        step("rebase: unresolvable ref refused", r.startswith("ERR"), r)
        # unprotect: protected edit refused, approved once, then protected again
        w = {"wt": wr, "base": base, "allow": "[]", "protect": json.dumps(["scripts/gates/*"]), "unprot": None}
        open(os.path.join(wr, "L/A.lean"), "w").write("theorem foo : True := trivial\n")
        open(os.path.join(wr, "scripts/gates/objective-manifest/p.tsv"), "w").write("-theorem\tFoo\th3\n")
        f, _ = guard(w, [])
        step("unprotect: protected edit flagged before approval", any(x.startswith("protected:scripts/gates") for x in f), f)
        h.db.execute("insert into workers(name,gen,deputy,model,effort,thread,wt,base,state,created,allow,protect) "
                     "values('u',1,'d','m','low','tu2','/x','0','WORKING',0,'[\"L/*\"]','[\"scripts/gates/*\"]')")
        r = await h.c_unprotect({"name": "u", "globs": ["scripts/gates/objective-manifest/*"]})
        wu = h.cur("u")
        f, _ = guard(dict(w, unprot=wu["unprot"], allow=wu["allow"]), [])
        step("unprotect: approved path passes the guard + UNPROTECTED event", f == [] and h.db.execute(
             "select 1 from events where kind='UNPROTECTED'").fetchone(), (r, f))
        wu["wt"], wu["base"] = wr, base
        un = json.loads(wu["unprot"])
        h.upd(wu, unprot="[]", allow=json.dumps([g for g in json.loads(wu["allow"]) if g not in [x for x, ad in un if ad]]))
        f, _ = guard(dict(w, unprot=h.cur("u")["unprot"], allow=h.cur("u")["allow"]), [])
        step("unprotect: spent once (consumed state refuses again)", any(x.startswith(("protected:", "scope:")) for x in f), f)
        # allow-dirty: hash recorded only on opt-in, env set only on opt-in
        dr = os.path.join(root, "dr"); sh(root, "init", "-q", "dr"); open(os.path.join(dr, "a"), "w").write("1\n"); sh(dr, "add", "-A"); sh(dr, "commit", "-q", "-m", "c")
        wd = {"name": "b", "gen": 1, "wt": dr, "build_cmd": None}
        jobs.clear()
        await h.tool_request_build(wd, {"targets": ["T"]})
        step("allow-dirty: default build leaves env + note unset", "CXO_ALLOW_DIRTY" not in jobs[0][1] and jobs[0][2] is None, jobs[0])
        open(os.path.join(dr, "a"), "w").write("2\n")
        await h.tool_request_build(wd, {"targets": ["T"], "allow_dirty": True})
        n1 = jobs[1][2]
        open(os.path.join(dr, "a"), "w").write("3\n")
        await h.tool_request_build(wd, {"targets": ["T"], "allow_dirty": True})
        step("allow-dirty: DIRTY-TREE diff hash recorded, differs per tree", "CXO_ALLOW_DIRTY=1" in jobs[1][1] and "DIRTY-TREE" in n1
             and "diff_sha1=" in n1 and n1 != jobs[2][2], n1)
        await h.tool_request_cargo(wd, {"spec": "check -p x", "allow_dirty": True})
        step("allow-dirty: request_cargo too", "CXO_ALLOW_DIRTY=1" in jobs[3][1] and jobs[3][2], jobs[3][1][:60])
        # pools: journeys saturated must not delay a build; each kind has its own width
        h.pool_n = {"build": 1, "journey": 1, "cargo": 1, "train": 1}
        h.pool = {k: asyncio.Semaphore(1) for k in h.pool_n}; h.pool_run = {k: 0 for k in h.pool_n}
        h.db.execute("insert into workers(name,gen,deputy,model,effort,thread,wt,base,state,created,allow,protect) "
                     "values('p',1,'d','m','low','tp','%s','0','WORKING',0,'[]','[]')" % root)
        wp = h.cur("p")
        async def noop(w, text): return "ok"
        h.deliver = noop
        t0 = now()
        for i, (kd, cm) in enumerate((("journey", "sleep 1.5"), ("journey", "sleep 1.5"), ("build", "true"))):
            h.db.execute("insert into jobs(ticket,name,gen,kind,what,status,log,t0) values(?,?,?,?,?,?,?,?)",
                         ("p%d" % i, "p", 1, kd, "x", "queued", os.path.join(root, "pj.log"), 0))
        for i, (kd, cm) in enumerate((("journey", "sleep 1.5"), ("journey", "sleep 1.5"), ("build", "true"))):
            asyncio.ensure_future(h.run_job(wp, "p%d" % i, kd, "x", cm, os.path.join(root, "pj%d.log" % i), cwd=root))
        await real_sleep(0.5)
        st = await h.c_status({})
        bdone = h.db.execute("select status from jobs where kind='build' and name='p'").fetchone()[0]
        step("pools: build finishes while journeys hold their pool", bdone == "done" and h.pool_run["journey"] == 1, (bdone, h.pool_run))
        step("pools: status shows occupancy + queue", "pools build 0/1 journey 1/1 +1q" in st, [l for l in st.split("\n") if l.startswith("pools")])
        await real_sleep(3.5)
        step("pools: journeys serialised by their own pool, all done", h.db.execute(
             "select count(*) from jobs where name='p' and status='done'").fetchone()[0] == 3 and now() - t0 > 3)
        # interrupted jobs on hub start
        told = []
        async def deliver(w, text): told.append((w["name"], text)); return "turn started"
        h.deliver = deliver
        h.db.execute("insert into workers(name,gen,deputy,model,effort,thread,wt,base,state,created,allow,protect) "
                     "values('j',1,'d','m','low','tj','/x','0','WORKING',0,'[]','[]')")
        for tk, st in (("b1", "running"), ("b2", "queued"), ("b3", "done")):
            h.db.execute("insert into jobs(ticket,name,gen,kind,what,status,log,t0,pid) values(?,?,?,?,?,?,?,?,?)", (tk, "j", 1, "build", "Foo", st, "/l", 0, 999999))
        await h.recover_jobs()
        sts = dict(h.db.execute("select ticket,status from jobs where name='j'").fetchall())
        step("hub start: running/queued -> INTERRUPTED, done kept", sts == {"b1": "INTERRUPTED", "b2": "INTERRUPTED", "b3": "done"}, sts)
        await h.recover_jobs()
        # orphans: a long job (+ a TERM-ignoring child) from a dead hub is gone after recovery
        saved = list(told)
        h.kill_grace = 1.0
        orph = subprocess.Popen(["bash", "-c", "(trap '' TERM; sleep 60) & sleep 60"], start_new_session=True)
        await real_sleep(0.3)
        h.db.execute("insert into jobs(ticket,name,gen,kind,what,status,log,t0,pid) values('orph','j',1,'journey','long','running','/l',0,?)", (orph.pid,))
        t1 = now()
        await h.recover_jobs()
        step("hub start: orphaned job group (even TERM-ignoring) is killed", not Hub._alive(orph.pid) and orph.poll() is not None
             and h.db.execute("select status from jobs where ticket='orph'").fetchone()[0] == "INTERRUPTED", now() - t1)
        orph.wait()
        # cancel: kills a sleeping job, marks CANCELLED, tells the worker, delivers no RESULT
        told.clear()
        h.db.execute("insert into jobs(ticket,name,gen,kind,what,status,log,t0) values('cx','j',1,'journey','zzz','queued',?,0)", (os.path.join(root, "cx.log"),))
        fut = asyncio.ensure_future(h.run_job(h.cur("j"), "cx", "journey", "zzz", "sleep 60", os.path.join(root, "cx.log"), cwd=root))
        await real_sleep(0.5)
        pid = h.db.execute("select pid from jobs where ticket='cx'").fetchone()[0]
        r = await h.c_cancel({"ticket": "cx"})
        await asyncio.wait_for(fut, 15)
        step("cancel: sleeping job killed, CANCELLED, worker told, no RESULT", pid and not Hub._alive(pid) and r.startswith("cancelled")
             and h.db.execute("select status from jobs where ticket='cx'").fetchone()[0] == "CANCELLED"
             and len(told) == 1 and "CANCELLED" in told[0][1] and not any("RESULT" in t for _, t in told), (r, told))
        step("cancel: finished job refused", (await h.c_cancel({"ticket": "b3"})).startswith("ERR"))
        told[:] = saved
        step("hub start: INTERRUPTED is terminal (second restart reports nothing)", len(told) == 1, len(told))
        step("hub start: worker told to re-request, event raised", len(told) == 1 and "ONLY" in told[0][1] and "INTERRUPTED" in told[0][1] and "request_build" in told[0][1]
             and h.db.execute("select count(*) from events where kind='JOB_INTERRUPTED' and text like '%Foo%'").fetchone()[0] == 2, told[:1])
    asyncio.run(hub_tests())
    print("%s %d/%d (scratch %s)" % ("LOCAL SELFTEST PASS" if all(res) else "LOCAL SELFTEST FAIL", sum(res), len(res), root))
    return 0 if all(res) else 1


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(USAGE); return 0
    cmd, rest = argv[0], argv[1:]
    if cmd == "hub":
        sub = rest[0] if rest else "run"
        pidf = os.path.join(HOME, "hub.pid")
        if sub == "run":
            asyncio.run(_hub_main()); return 0
        if sub == "start":
            os.makedirs(HOME, exist_ok=True)
            try:
                print("already running: " + call("ping", {}, 5)); return 0
            except Exception:
                if os.path.exists(SOCK):
                    os.unlink(SOCK)
            p = subprocess.Popen([sys.executable, os.path.abspath(__file__), "hub", "run"], stdout=open(os.path.join(HOME, "hub.log"), "a"),
                                 stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=True)
            open(pidf, "w").write(str(p.pid))
            for _ in range(60):
                time.sleep(0.5)
                try:
                    print(call("ping", {}, 10)); return 0
                except Exception:
                    pass
            print("ERR hub did not come up; see %s/hub.log" % HOME); return 1
        if sub == "stop":
            try:
                os.kill(int(open(pidf).read()), signal.SIGTERM); print("stopped")
            except Exception as e:
                print("ERR %r" % e); return 1
            return 0
    a, pos = parse(rest)
    if cmd == "selftest-local":
        return selftest_local()
    if cmd == "selftest":
        return selftest(a.get("model") or DEFAULT_MODEL)
    if cmd == "spawn":
        a["name"] = pos[0]; a["brief"] = sys.stdin.read()
    elif cmd in ("send", "renew"):
        a["name"] = pos[0]; a["text"] = " ".join(pos[1:])
    elif cmd == "answer":
        a["name"] = pos[0]; a["ask"] = pos[1]; a["text"] = " ".join(pos[2:])
    elif cmd == "retire":
        a["name"] = pos[0]; a["why"] = " ".join(pos[1:])
    elif cmd in ("allow", "unprotect"):
        a["name"] = pos[0]; a["globs"] = pos[1:]
    elif cmd == "rebase":
        a["name"] = pos[0]; a["ref"] = pos[1] if len(pos) > 1 else ""
    elif cmd == "budget":
        a["name"] = pos[0]; a["n"] = pos[1]
    elif cmd == "cancel":
        a["ticket"] = pos[0]
    elif cmd in ("interrupt", "log", "train"):
        a["name"] = pos[0]
    elif cmd == "merge":
        a["name"] = pos[0]; a["ref"] = pos[1] if len(pos) > 1 else ""
    try:
        out = call(cmd, a)
    except ConnectionError as e:
        print(e); return 1
    print(out)
    return 1 if out.startswith("ERR") else 0


if __name__ == "__main__":
    sys.exit(main())
