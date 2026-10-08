#!/usr/bin/env python3
"""cxo — Codex hub for Claude deputies. One resident process owns a private `codex app-server`,
the worker registry, events, jobs (builds, journeys, cargo, train checks), submit guards and the
rate-limit gate. Deputies use the CLI. Design: redregg/work/CODEX-ORCHESTRATION-DESIGN-20261008.md;
usage: README.md beside this file; experiment record: redregg/work/CXO-EXPERIMENT-1.md."""
import asyncio, json, os, sys, time, sqlite3, re, fnmatch, subprocess, shlex, signal, itertools, tempfile

HOME = os.path.expanduser(os.environ.get("CXO_HOME", "~/.cxo"))
SOCK = os.environ.get("CXO_SOCK") or os.path.join(HOME, "hub.sock")
if len(SOCK) > 100:  # AF_UNIX path limit
    import hashlib
    SOCK = "/tmp/cxo-%d-%s.sock" % (os.getuid(), hashlib.sha1(HOME.encode()).hexdigest()[:10])
CODEX = os.environ.get("CXO_CODEX", "codex")
CODEX_HOME = os.environ.get("CXO_CODEX_HOME", os.path.join(HOME, "codex-home"))
DEFAULT_MODEL = os.environ.get("CXO_DEFAULT_MODEL", "gpt-5.6-sol")
DEFAULT_BUDGET = int(os.environ.get("CXO_DEFAULT_BUDGET", "12000000"))
BUILD_CMD = os.environ.get("CXO_BUILD_CMD", "swarm-build lake build {targets}")
CARGO_CMD = os.environ.get("CXO_CARGO_CMD", "swarm-build cargo {spec}")
BOX_ENV = os.environ.get("CXO_BOX_ENV", "/srv/pipeline/box.env")
FETCH_ARTIFACTS = os.environ.get("CXO_FETCH_ARTIFACTS", "/srv/pipeline/scripts/fetch-artifacts")
ARTIFACT_TIP = os.environ.get("CXO_ARTIFACT_TIP", "green")
UMBRELLA = os.environ.get("CXO_UMBRELLA", "Minidregg Host.Main:leanArts ObjectiveProofs").split()
MAX_JOBS = int(os.environ.get("CXO_MAX_JOBS", "3"))
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
        {"targets": ARR}, ["targets"]),
    _fn("request_journey", "Run a journey/acceptance script from your lane outside the sandbox. In args, {bin} and {manifest} expand to the "
        "prebuilt base artifact set (unchanged Rust/Host binaries); for a Host you changed, request_build it first and pass its path. "
        "Returns a ticket; then END YOUR TURN.", {"script": S, "args": ARR}, ["script", "args"]),
    _fn("request_cargo", "Run a FILTERED cargo command outside the sandbox, e.g. 'test -p mini-client --test frames' or "
        "'build -p minidregg-host --bin x'. Tests need -p and a filter or --test. Returns a ticket; then END YOUR TURN.", {"spec": S}, ["spec"]),
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
         "polls": "int default 0", "pending": "int default 0", "nopush": "int default 0"}


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
        self.rid = itertools.count(1)
        self.pending = {}       # rpc id -> future
        self.turn_flags = {}    # thread -> {"submit_tried": bool, "warned": set()}
        self.job_sem = asyncio.Semaphore(MAX_JOBS)
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
                self.wlog(w, "run [%s] %s" % (it.get("exitCode"), it.get("command")))
            elif t == "fileChange":
                self.wlog(w, "edit " + " ".join(os.path.relpath(c.get("path", "?"), w["wt"]) for c in it.get("changes", [])))
            elif t == "dynamicToolCall":
                self.wlog(w, "tool %s %s" % (it.get("tool"), json.dumps(it.get("arguments"))[:250]))
        elif meth == "item/started":
            self.upd(w, last_item=now())
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
        hit = [x for x in paths if any(fnmatch.fnmatch(x, g) for g in json.loads(w["protect"])) and x not in flags["warned"]]
        if hit and w["turn"]:
            flags["warned"].update(hit)
            msg = "STOP: you edited protected path(s) %s. Revert them now; protected files are not yours to change." % ", ".join(hit)
            asyncio.ensure_future(self.rpc("turn/steer", {"threadId": w["thread"], "expectedTurnId": w["turn"],
                                                          "input": [{"type": "text", "text": msg}]}))
            self.event(w, "GUARD", "protected edit steered: " + ", ".join(hit))

    async def on_request(self, m):
        meth, p, rid = m["method"], m.get("params") or {}, m["id"]
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
        return ("DEPUTY: " + "\nDEPUTY: ".join(ms)) if ms else "ack", True

    async def tool_ask_deputy(self, w, a):
        q, d = a.get("question", ""), a.get("default", "")
        aid = "a%d" % next(self.rid)
        if a.get("must_wait"):
            self.upd(w, state="WAITING_ASK")
            self.event(w, "ASK", "%s %s Q: %s | default: %s" % (aid, w["name"], q, d))
            return "Question %s sent. %s" % (aid, WAIT_TEXT), True
        self.event(w, "NOTE", "%s Q(non-blocking): %s | default: %s" % (aid, q, d))
        return "noted; proceed with your default and record it in WORKLOG.md", True

    def new_job(self, w, kind, what, cmd, tree=None):
        tk = "%s%d" % (kind[0], int(now() * 1000) % 1000000000)
        log = os.path.join(HOME, "jobs", tk + ".log")
        self.db.execute("insert into jobs values(?,?,?,?,?,?,?,?,?,?,?)", (tk, w["name"], w["gen"], kind, what, "queued", None, log, now(), None, tree))
        self.upd(w, pending=w["pending"] + 1, state="WAITING_JOB")
        asyncio.ensure_future(self.run_job(w, tk, kind, what, cmd, log))
        return tk

    async def run_job(self, w, tk, kind, what, cmd, log, cwd=None, on_done=None):
        async with self.job_sem:
            self.db.execute("update jobs set status='running' where ticket=?", (tk,))
            with open(log, "w") as f:
                f.write("$ %s\n" % cmd); f.flush()
                pr = await asyncio.create_subprocess_exec("bash", "-c", cmd, cwd=cwd or w["wt"], stdout=f, stderr=subprocess.STDOUT,
                                                          stdin=subprocess.DEVNULL, start_new_session=True)
                try:
                    rc = await asyncio.wait_for(pr.wait(), JOB_TIMEOUT)
                except asyncio.TimeoutError:
                    os.killpg(pr.pid, signal.SIGTERM); rc = await pr.wait()
                    f.write("\ncxo: killed after %ds\n" % JOB_TIMEOUT)
        self.db.execute("update jobs set status='done', exit=?, t1=? where ticket=?", (rc, now(), tk))
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
        self.upd(cw, pending=max(0, cw["pending"] - 1))
        if cw["pending"] == 0 and cw["state"] == "WAITING_JOB":
            self.upd(cw, state="WORKING")
        self.event(cw, kind.upper(), "%s exit=%d %s" % (tk, rc, what[:120]))
        await self.deliver(cw, "RESULT %s %s exit=%d (%s)\nlog: %s\n%s" % (tk, kind, rc, what[:200], log, tail))

    async def tool_request_build(self, w, a):
        targets = [t for t in a.get("targets", []) if re.match(r"^[A-Za-z0-9_.+:/@-]+$", t)]
        if not targets:
            return "no valid targets", False
        cmd = (". %s 2>/dev/null; " % BOX_ENV) + (w["build_cmd"] or BUILD_CMD).format(targets=" ".join(shlex.quote(t) for t in targets))
        tk = self.new_job(w, "build", " ".join(targets), cmd, tree=tree_id(w["wt"]))
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
        cmd = ". %s 2>/dev/null; export CARGO_TARGET_DIR=%s; %s" % (BOX_ENV, shlex.quote(tgt), CARGO_CMD.format(spec=spec))
        tk = self.new_job(w, "cargo", spec, cmd)
        return "ticket=%s queued (cargo %s). %s" % (tk, spec, WAIT_TEXT), True

    async def tool_build_status(self, w, a):
        row = self.db.execute("select status,exit,log from jobs where ticket=?", (a.get("ticket", ""),)).fetchone()
        if not row:
            return "unknown ticket", False
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
            "cwd": wt, "model": model, "sandbox": "workspace-write", "approvalPolicy": "never", "dynamicTools": TOOLS,
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
        if a.get("mklane"):
            pr = await asyncio.create_subprocess_exec(*([MKLANE] + (["--from", a["from"]] if a.get("from") else []) + [name]),
                                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            o = (await pr.communicate())[0].decode(errors="replace")
            wt = os.path.join(LANES, name, "src")
            if pr.returncode or not os.path.isdir(wt):
                return "ERR mk-lane exit %s: %s" % (pr.returncode, o.strip()[-300:])
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
        allow = a.get("allow") or []
        protect = ([] if a.get("no_default_protect") else DEFAULT_PROTECT) + (a.get("protect") or [])
        umb = None
        if a.get("umbrella"):
            umb = json.dumps(UMBRELLA if a["umbrella"] == "default" else a["umbrella"].split())
        prompt = brief + "\n\n---\nWORKTREE: %s (base %s)\nALLOWED PATHS: %s\nPROTECTED PATHS: %s\n%s" % (
            wt, base[:10], ", ".join(allow) or "(any not protected)", ", ".join(protect),
            ("BEFORE SUBMIT: request_build(%s) must come back exit=0 on the exact tree you submit.\n" % umb) if umb else "")
        w, err = await self.new_thread(name, 1, a["deputy"], a.get("model") or DEFAULT_MODEL, a.get("effort") or "high", wt, base,
                                       allow, protect, prompt, int(a.get("budget") or DEFAULT_BUDGET),
                                       {"build_cmd": a.get("build_cmd"), "umbrella": umb, "nopush": a.get("no_push")})
        return "ERR " + err if err else "spawned %s g1 %s thread=%s wt=%s" % (name, w["model"], w["thread"][:8], wt)

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
        allow = json.loads(w["allow"]) + [g for g in a.get("globs", []) if g not in json.loads(w["allow"])]
        self.upd(w, allow=json.dumps(allow))
        self.db.execute("update workers set allow=? where name=?", (json.dumps(allow), w["name"]))
        return "%s allow: %s" % (w["name"], " ".join(allow))

    async def c_budget(self, a):
        w, err = self.live(a["name"])
        if err:
            return err
        n = int(float(a["n"].rstrip("Mm")) * 10**6) if a["n"][-1:] in "Mm" else int(a["n"])
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
        out = []
        for name in self.live_names():
            w = self.cur(name)
            if (a.get("deputy") and w["deputy"] != a["deputy"]) or (w["state"] in ("RETIRED", "DEAD") and not a.get("all")):
                continue
            out.append("%s g%d %s %s %s turn=%s rep=%d/%s item=%s tok=%.1fM unc=%.2fM req=%d polls=%d jobs=%d budget=%dM%s" % (
                w["name"], w["gen"], w["deputy"], w["state"], w["model"], "on" if w["turn"] else "off", w["reports"], ago(w["last_report"]),
                ago(w["last_item"]), w["tokens"] / 1e6, (w["unc"] or 0) / 1e6, w["reqs"] or 0, w["polls"] or 0, w["pending"] or 0,
                w["budget"] // 10**6, (" sha=" + w["sha"][:10]) if w["sha"] else ""))
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

    async def retire_w(self, w, why):
        if w["turn"]:
            await self.rpc("turn/interrupt", {"threadId": w["thread"], "turnId": w["turn"]})
        self.upd(w, state="RETIRED", retired=now(), turn=None)
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
        await self.retire_w(w, "renewed to g%d" % (w["gen"] + 1))
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
        pr = await asyncio.create_subprocess_exec(*([MKLANE] + (["--from", a["from"]] if a.get("from") else []) + [lane]),
                                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        o = (await pr.communicate())[0].decode(errors="replace")
        wt = os.path.join(LANES, lane, "src")
        if pr.returncode or not os.path.isdir(wt):
            return "ERR mk-lane exit %s: %s" % (pr.returncode, o.strip()[-300:])
        head = git(wt, "rev-parse", "HEAD").strip()
        self.db.execute("insert into trains values(?,?,?,?,?,?)", (name, a.get("deputy") or "-", wt, head, "GREEN", "created"))
        return "train %s at %s wt=%s (base assumed green; run `cxo merge %s --recheck` to prove it)" % (name, head[:10], wt, name)

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
        self.db.execute("insert into jobs values(?,?,?,?,?,?,?,?,?,?,?)", (tk, "train-" + name, 0, "train", what, "queued", None, log, now(), None, head))
        asyncio.ensure_future(self.run_job(None, tk, "train", what, cmd, log, cwd=wt, on_done=done))
        return "train %s: %s merged at %s; umbrella ticket=%s (event TRAIN_GREEN/TRAIN_RED follows)" % (name, what, head[:10], tk)

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
        if os.path.exists(SOCK):
            os.unlink(SOCK)
        srv = await asyncio.start_unix_server(self.client, path=SOCK, limit=1 << 24)
        os.chmod(SOCK, 0o600)
        asyncio.ensure_future(self.monitor())
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
    found = []
    for f in files:
        if any(fnmatch.fnmatch(f, g) for g in prot):
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
            for rule, rx in ADDED_RULES:
                if re.search(rx, line[1:]) and not (rule == "pipe-tail" and not re.search(r"\.(sh|bash|py|toml|yml|yaml)$|^scripts/", cur)):
                    found.append("%s:%s +%s" % (rule, cur, line[1:].strip()[:80]))
        elif line.startswith("-") and cur:
            for rule, rx in REMOVED_RULES:
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
  spawn NAME -d DEP (--mklane [--from main|next] | --repo PATH [--base REF] | --wt PATH) [-m MODEL] [-e EFFORT]
        [--allow GLOB]... [--protect GLOB]... [--no-default-protect] [--budget N|12M] [--umbrella default|"T1 T2"]
        [--build-cmd 'CMD {targets}'] [--no-push] [--force]   < brief.md
  send NAME [--now] TEXT...   answer NAME ASKID TEXT...   allow NAME GLOB...   budget NAME N|12M
  wait [-d DEP] [-t SECS<=590]   interrupt NAME   retire NAME [why...]   log NAME [-n N] [--gen G]
  renew NAME [--fork [--before-turn ID]] [-m MODEL] [TEXT...]
  train NAME -d DEP [--from main|next]     merge TRAIN REF | merge TRAIN --recheck | merge TRAIN --abort
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
    elif cmd == "allow":
        a["name"] = pos[0]; a["globs"] = pos[1:]
    elif cmd == "budget":
        a["name"] = pos[0]; a["n"] = pos[1]
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
