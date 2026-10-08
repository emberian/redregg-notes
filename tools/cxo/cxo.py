#!/usr/bin/env python3
"""cxo — Codex hub for Claude deputies. One resident process owns a private `codex app-server`,
the worker registry, events, asks, builds and the rate-limit gate. Deputies use the CLI.
Design: redregg/work/CODEX-ORCHESTRATION-DESIGN-20261008.md. Usage: README.md beside this file."""
import asyncio, json, os, sys, time, sqlite3, re, fnmatch, subprocess, shlex, signal, itertools

HOME = os.path.expanduser(os.environ.get("CXO_HOME", "~/.cxo"))
SOCK = os.environ.get("CXO_SOCK") or os.path.join(HOME, "hub.sock")
if len(SOCK) > 100:  # AF_UNIX path limit
    import hashlib
    SOCK = "/tmp/cxo-%d-%s.sock" % (os.getuid(), hashlib.sha1(HOME.encode()).hexdigest()[:10])
CODEX = os.environ.get("CXO_CODEX", "codex")
CODEX_HOME = os.environ.get("CXO_CODEX_HOME", os.path.join(HOME, "codex-home"))
DEFAULT_MODEL = os.environ.get("CXO_DEFAULT_MODEL", "gpt-5.6-sol")
BUILD_CMD = os.environ.get("CXO_BUILD_CMD", "swarm-build lake build {targets}")
MAX_BUILDS = int(os.environ.get("CXO_MAX_BUILDS", "2"))
PUSH_REMOTE = os.environ.get("CXO_PUSH_REMOTE", "")  # e.g. /srv/git/minidregg.git; empty = no push
PUSH_PREFIX = os.environ.get("CXO_PUSH_PREFIX", "lane/")  # the shared remote's pre-receive accepts lane/<name> only
MKLANE = os.environ.get("CXO_MKLANE", "/srv/warm-base/mk-lane.sh")
LANES = os.environ.get("PIPELINE_LANES", "/srv/lanes")
STALL_S, ASK_S, PIGGY_S = 900, 900, 600
DEFAULT_PROTECT = ["Assurance/NativeAcceptedFixture*", "AxiomCensus*.lean", "TokenCensus*", "Theory/AxiomPin.lean",
                   "scripts/gates/*", "scripts/pipeline/*", ".github/*", "lakefile*", "lean-toolchain", "lake-manifest.json"]
GIT_ID = ["-c", "commit.gpgsign=false", "-c", "user.name=ember arlynx", "-c", "user.email=cmrx64@gmail.com"]

DEV_INSTR = """You are a Codex worker for a coordinating deputy, reached only through these tools:
- report(phase, note): call at start, after each milestone, and at least every 15 minutes. Its reply may carry deputy instructions; follow them.
- ask_deputy(question, default, must_wait): ask instead of guessing. It returns at once. If you must wait, END YOUR TURN right after; never idle-wait inside a turn.
- request_build(targets) / build_status(ticket, wait_s): the ONLY way to build more than a single file. Never run lake build of many modules yourself.
- submit(title, body, claims, waivers): the ONLY way to finish. The hub commits your working tree and checks it. Do not run git commit yourself.
Keep WORKLOG.md in the worktree root: decisions and why, assumptions, current state. A successor starts from it.
Forbidden: sorry/admit, new axioms, new native_decide, deleting or weakening a theorem/test/assertion, editing pins, fixtures,
gates or toolchain files, `|| true`, piping a build into tail, pkill -f, git stash, printing the environment.
If submit is refused, fix the findings and submit again, or ask_deputy. Ending a turn without submit counts as a stall."""

TOOLS = [
    {"type": "function", "name": "report", "description": "Report progress to your deputy; returns any deputy instructions.",
     "inputSchema": {"type": "object", "properties": {"phase": {"type": "string"}, "note": {"type": "string"}},
                     "required": ["phase", "note"], "additionalProperties": False}},
    {"type": "function", "name": "ask_deputy", "description": "Ask your deputy a question. Returns at once. If you cannot proceed without the answer (must_wait=true), end your turn right after asking; the answer arrives as a new message. Otherwise proceed with your default.",
     "inputSchema": {"type": "object", "properties": {"question": {"type": "string"}, "default": {"type": "string"}, "must_wait": {"type": "boolean"}},
                     "required": ["question", "default", "must_wait"], "additionalProperties": False}},
    {"type": "function", "name": "request_build", "description": "Queue a build of the given targets in your worktree on a build slot. Returns a ticket.",
     "inputSchema": {"type": "object", "properties": {"targets": {"type": "array", "items": {"type": "string"}}},
                     "required": ["targets"], "additionalProperties": False}},
    {"type": "function", "name": "build_status", "description": "Status of a build ticket; waits up to wait_s (max 300) for it to finish. Returns exit code and log tail.",
     "inputSchema": {"type": "object", "properties": {"ticket": {"type": "string"}, "wait_s": {"type": "integer"}},
                     "required": ["ticket", "wait_s"], "additionalProperties": False}},
    {"type": "function", "name": "submit", "description": "Finish: the hub commits your working tree and checks scope and weakening guards. waivers: 'rule:path reason' strings for deliberate deletions.",
     "inputSchema": {"type": "object", "properties": {"title": {"type": "string"}, "body": {"type": "string"},
                     "claims": {"type": "array", "items": {"type": "string"}}, "waivers": {"type": "array", "items": {"type": "string"}}},
                     "required": ["title", "body", "claims", "waivers"], "additionalProperties": False}},
]

ADDED_RULES = [("sorry", r"\bsorry\b"), ("admit", r"\badmit\b"), ("axiom", r"^\s*(private\s+)?axiom\b"),
               ("native_decide", r"\bnative_decide\b"), ("heartbeats0", r"maxHeartbeats\s+0\b"), ("or-true", r"\|\|\s*true\b"),
               ("pipe-tail", r"\|\s*tail\b"), ("ignore-test", r"#\[ignore\]|\.skip\(|@pytest\.mark\.skip"), ("pkill-f", r"pkill\s+-f")]
REMOVED_RULES = [("del-theorem", r"^\s*(@\[[^\]]*\]\s*)?(private\s+|protected\s+)?(theorem|lemma|example)\b"),
                 ("del-assert", r"#assert_|\bassert(_eq|_ne)?!?\s*\(|#guard\b|#\[test\]|\bdef test_")]


def now(): return time.time()
def ago(t): return "-" if not t else "%dm" % ((now() - t) // 60)


# ---------------------------------------------------------------- hub
class Hub:
    def __init__(self):
        os.makedirs(HOME, exist_ok=True)
        for d in ("wt", "logs", "builds", "briefs"):
            os.makedirs(os.path.join(HOME, d), exist_ok=True)
        self.db = sqlite3.connect(os.path.join(HOME, "registry.sqlite"), isolation_level=None)
        self.db.executescript("""
        create table if not exists workers(name text, gen int, deputy text, model text, effort text, thread text, wt text,
          base text, state text, turn text, last_item real, last_report real, reports int default 0, tokens int default 0,
          nudges int default 0, stalled int default 0, budget int default 3000000, created real, retired real, allow text, protect text, sha text,
          primary key(name, gen));
        create table if not exists events(id integer primary key, ts real, deputy text, worker text, kind text, text text, seen int default 0);
        create table if not exists msgs(id integer primary key, name text, gen int, ts real, text text, delivered int default 0);
        create table if not exists builds(ticket text primary key, name text, targets text, status text, exit int, log text, t0 real, t1 real);""")
        self.rid = itertools.count(1)
        self.pending = {}       # rpc id -> future
        self.turn_flags = {}    # thread -> {"submit_tried": bool, "warned": set()}
        self.build_done = {}    # ticket -> asyncio.Event
        self.build_sem = asyncio.Semaphore(MAX_BUILDS)
        self.rate = None
        self.paused = False
        self.ev_signal = asyncio.Event()

    # ---- registry helpers
    def cur(self, name):
        r = self.db.execute("select * from workers where name=? order by gen desc limit 1", (name,))
        row = r.fetchone()
        return dict(zip([c[0] for c in r.description], row)) if row else None

    def by_thread(self, tid):
        r = self.db.execute("select * from workers where thread=?", (tid,))
        row = r.fetchone()
        return dict(zip([c[0] for c in r.description], row)) if row else None

    def upd(self, w, **kv):
        sets = ",".join("%s=?" % k for k in kv)
        self.db.execute("update workers set %s where name=? and gen=?" % sets, list(kv.values()) + [w["name"], w["gen"]])
        w.update(kv)

    def event(self, w, kind, text):
        self.db.execute("insert into events(ts,deputy,worker,kind,text) values(?,?,?,?,?)",
                        (now(), w["deputy"] if w else "-", ("%s/g%d" % (w["name"], w["gen"])) if w else "-", kind, text))
        self.ev_signal.set()

    def wlog(self, w, line):
        with open(os.path.join(HOME, "logs", "%s.g%d.log" % (w["name"], w["gen"])), "a") as f:
            f.write(time.strftime("%H:%M:%S ") + line.replace("\n", " ")[:400] + "\n")

    # ---- app-server
    async def start_codex(self):
        if not os.path.exists(os.path.join(CODEX_HOME, "auth.json")):
            raise SystemExit("no auth.json in %s (copy it; see README)" % CODEX_HOME)
        env = dict(os.environ, CODEX_HOME=CODEX_HOME)
        self.proc = await asyncio.create_subprocess_exec(CODEX, "app-server", "--listen", "stdio://", env=env, cwd=HOME,
            stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE,
            stderr=open(os.path.join(HOME, "app-server.stderr"), "a"), limit=1 << 26)
        asyncio.ensure_future(self.reader())
        await self.rpc("initialize", {"clientInfo": {"name": "cxo", "title": "cxo hub", "version": "1"},
            "capabilities": {"experimentalApi": True, "optOutNotificationMethods": [
                "item/agentMessage/delta", "item/reasoning/textDelta", "item/reasoning/summaryTextDelta",
                "item/reasoning/summaryPartAdded", "item/commandExecution/outputDelta", "item/fileChange/outputDelta",
                "item/plan/delta", "command/exec/outputDelta"]}})
        self.send({"jsonrpc": "2.0", "method": "initialized"})
        r = await self.rpc("account/rateLimits/read", {})
        self.rate = r.get("result")
        # re-attach live workers after a hub restart
        for row in self.db.execute("select name from workers where state not in ('RETIRED','DEAD') group by name").fetchall():
            w = self.cur(row[0])
            if w["state"] in ("RETIRED", "DEAD"):
                continue
            res = await self.rpc("thread/resume", {"threadId": w["thread"]})
            if "error" in res:
                self.upd(w, state="DEAD"); self.event(w, "DEAD", "resume failed: %s" % res["error"].get("message"))
            else:
                self.upd(w, turn=None); self.event(w, "RESUMED", "hub restarted; worker idle. send it 'continue' if needed")

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
                for row in self.db.execute("select name from workers where state not in ('RETIRED','DEAD') group by name").fetchall():
                    w = self.cur(row[0]); self.event(w, "HUB_CODEX_EXIT", "app-server exited; restart the hub")
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
            if self.rate is None:
                self.rate = {}
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
            self.upd(w, tokens=p["tokenUsage"]["total"]["totalTokens"])
        elif meth == "error":
            e = p.get("error", {})
            info = e.get("codexErrorInfo")
            if info in ("usageLimitExceeded",) or (isinstance(info, str) and "usage" in info.lower()):
                self.paused = True
            if not p.get("willRetry"):
                self.event(w, "ERROR", "%s %s" % (info, e.get("message", "")[:200]))
        elif meth == "turn/completed":
            st = p["turn"].get("status")
            flags = self.turn_flags.pop(w["thread"], {"submit_tried": False})
            self.upd(w, turn=None)
            self.wlog(w, "turn end " + str(st))
            if w["state"] in ("RETIRED", "DEAD"):
                return
            if st == "failed":
                self.event(w, "TURN_FAILED", json.dumps(p["turn"].get("error"))[:300])
            elif w["state"] == "WORKING" and not flags["submit_tried"] and st == "completed":
                if w["nudges"] < 1:
                    self.upd(w, nudges=w["nudges"] + 1)
                    asyncio.ensure_future(self.start_turn(w, "You ended your turn without calling submit. Either submit with evidence, "
                                                            "or call ask_deputy(must_wait=true) with what blocks you and then end your turn."))
                else:
                    self.event(w, "NO_SUBMIT", "turn ended twice without submit; worker idle")
            elif st == "interrupted":
                self.event(w, "INTERRUPTED", "turn interrupted; worker idle")

    def check_protected_live(self, w, diff):
        flags = self.turn_flags.get(w["thread"])
        if flags is None:
            return
        paths = set(re.findall(r"^diff --git a/(\S+) b/", diff, re.M))
        prot = json.loads(w["protect"])
        hit = [p for p in paths if any(fnmatch.fnmatch(p, g) for g in prot) and p not in flags["warned"]]
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
            try:
                text, ok = await getattr(self, "tool_" + p["tool"])(w, p.get("arguments") or {})
            except Exception as e:
                text, ok = "hub error in %s: %r" % (p.get("tool"), e), False
        self.send({"jsonrpc": "2.0", "id": rid, "result": {"success": ok, "contentItems": [{"type": "inputText", "text": text}]}})

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
            return "Question %s sent. END YOUR TURN NOW with no further actions; the deputy's answer arrives as a new message." % aid, True
        self.event(w, "NOTE", "%s Q(non-blocking): %s | default: %s" % (aid, q, d))
        return "noted; proceed with your default and record it in WORKLOG.md", True

    async def tool_request_build(self, w, a):
        targets = [t for t in a.get("targets", []) if re.match(r"^[A-Za-z0-9_.+:/@-]+$", t)]
        if not targets:
            return "no valid targets", False
        tk = "b%d" % int(now() * 1000 % 1e9)
        log = os.path.join(HOME, "builds", tk + ".log")
        self.db.execute("insert into builds values(?,?,?,?,?,?,?,?)", (tk, w["name"], " ".join(targets), "queued", None, log, now(), None))
        self.build_done[tk] = asyncio.Event()
        asyncio.ensure_future(self.run_build(w, tk, targets, log))
        return "ticket=%s queued; poll build_status(ticket, wait_s<=300)" % tk, True

    async def run_build(self, w, tk, targets, log):
        async with self.build_sem:
            self.db.execute("update builds set status='running' where ticket=?", (tk,))
            cmd = BUILD_CMD.format(targets=" ".join(shlex.quote(t) for t in targets))
            with open(log, "w") as f:
                f.write("$ %s\n" % cmd); f.flush()
                pr = await asyncio.create_subprocess_shell(cmd, cwd=w["wt"], stdout=f, stderr=subprocess.STDOUT)
                rc = await pr.wait()
            self.db.execute("update builds set status='done', exit=?, t1=? where ticket=?", (rc, now(), tk))
            self.build_done[tk].set()
            self.event(w, "BUILD", "%s exit=%d %s" % (tk, rc, " ".join(targets)))

    async def tool_build_status(self, w, a):
        tk = a.get("ticket", "")
        row = self.db.execute("select status,exit,log from builds where ticket=?", (tk,)).fetchone()
        if not row:
            return "unknown ticket", False
        if row[0] != "done" and tk in self.build_done:
            try:
                await asyncio.wait_for(self.build_done[tk].wait(), min(max(int(a.get("wait_s", 0)), 0), 300))
            except asyncio.TimeoutError:
                pass
            row = self.db.execute("select status,exit,log from builds where ticket=?", (tk,)).fetchone()
        tail = ""
        if os.path.exists(row[2]):
            with open(row[2], errors="replace") as f:
                tail = "".join(f.readlines()[-40:])
        return "status=%s exit=%s log=%s\n%s" % (row[0], row[1], row[2], tail), True

    async def tool_submit(self, w, a):
        if w["thread"] in self.turn_flags:
            self.turn_flags[w["thread"]]["submit_tried"] = True
        findings, waived = guard(w, a.get("waivers") or [])
        if findings:
            git(w["wt"], "reset", "-q")
            self.event(w, "SUBMIT_REFUSED", "; ".join(findings)[:600])
            return ("REFUSED by hub guards:\n- " + "\n- ".join(findings) +
                    "\nFix these and submit again, or ask_deputy. Waivers ('rule:path reason') are for deliberate deletions only."), True
        msg = "%s\n\n%s\n\nClaims:\n%s\n%sCx-Worker: %s g%d\nCo-Authored-By: %s via cxo" % (
            a.get("title", "cx: " + w["name"]), a.get("body", ""), "\n".join("- " + c for c in a.get("claims", [])),
            ("Waived:\n" + "\n".join("- " + x for x in waived) + "\n") if waived else "", w["name"], w["gen"], w["model"])
        r = subprocess.run(["git"] + GIT_ID + ["commit", "-q", "-F", "-"], cwd=w["wt"], input=msg, text=True, capture_output=True)
        if r.returncode:
            return "commit failed: " + r.stderr[-400:], False
        sha = git(w["wt"], "rev-parse", "HEAD").strip()
        pushed = ""
        if PUSH_REMOTE:
            ref = PUSH_PREFIX + w["name"]
            pr = subprocess.run(["git", "push", "-q", "-f", PUSH_REMOTE, "HEAD:refs/heads/" + ref], cwd=w["wt"], capture_output=True, text=True)
            pushed = " pushed=" + ref if pr.returncode == 0 else " PUSH-FAILED(%s)" % pr.stderr.strip()[-200:]
        files = git(w["wt"], "diff", "--name-only", w["base"], sha).split()
        self.upd(w, state="SUBMITTED", sha=sha)
        self.event(w, "SUBMIT", "%s..%s files=%d%s%s claims: %s" % (w["base"][:10], sha[:10], len(files), pushed,
                   (" WAIVED: " + "; ".join(waived)) if waived else "", " | ".join(a.get("claims", []))[:400]))
        return "submitted %s. End your turn now." % sha[:10], True

    # ---- turns
    async def start_turn(self, w, text):
        r = await self.rpc("turn/start", {"threadId": w["thread"], "input": [{"type": "text", "text": text}], "effort": w["effort"]})
        if "error" in r:
            return "turn/start failed: " + r["error"].get("message", "")
        self.upd(w, turn=r["result"]["turn"]["id"])
        self.turn_flags.setdefault(w["thread"], {"submit_tried": False, "warned": set()})
        return None

    async def new_thread(self, name, gen, deputy, model, effort, wt, base, allow, protect, prompt, budget, fork_from=None):
        if fork_from:
            r = await self.rpc("thread/fork", fork_from)
        else:
            r = await self.rpc("thread/start", {"cwd": wt, "model": model, "sandbox": "workspace-write", "approvalPolicy": "never",
                "dynamicTools": TOOLS, "developerInstructions": DEV_INSTR, "multiAgentMode": "explicitRequestOnly"})
        if "error" in r:
            return None, "thread start failed: " + r["error"].get("message", "")
        tid = r["result"]["thread"]["id"]
        self.db.execute("insert into workers(name,gen,deputy,model,effort,thread,wt,base,state,created,allow,protect) values(?,?,?,?,?,?,?,?,?,?,?,?)",
                        (name, gen, deputy, model, effort, tid, wt, base, "WORKING", now(), json.dumps(allow), json.dumps(protect)))
        w = self.cur(name)
        self.upd(w, budget=budget)
        err = await self.start_turn(w, prompt)
        if err:
            self.upd(w, state="DEAD")
            return None, err
        return w, None

    # ---- deputy commands
    def pace_ok(self):
        if self.paused:
            return "usage limit hit; paused"
        r = (self.rate or {}).get("rateLimits") or {}
        if self.rate and self.rate.get("ordinaryUsageAllowed") is False:
            return "ordinaryUsageAllowed=false"
        pr = r.get("primary") or {}
        if pr.get("resetsAt") and pr.get("windowDurationMins"):
            span = pr["windowDurationMins"] * 60.0
            f = 1 - (pr["resetsAt"] - now()) / span
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
        if a.get("mklane"):
            cmd = [MKLANE] + (["--from", a["from"]] if a.get("from") else []) + [name]
            pr = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
        brief = a.get("brief", "").strip()
        if not brief:
            return "ERR empty brief (pipe it on stdin)"
        with open(os.path.join(HOME, "briefs", name + ".md"), "w") as f:
            f.write(brief)
        allow = a.get("allow") or []
        protect = ([] if a.get("no_default_protect") else DEFAULT_PROTECT) + (a.get("protect") or [])
        prompt = brief + "\n\n---\nWORKTREE: %s (base %s)\nALLOWED PATHS: %s\nPROTECTED PATHS: %s\n" % (
            wt, base[:10], ", ".join(allow) or "(any not protected)", ", ".join(protect))
        w, err = await self.new_thread(name, 1, a["deputy"], a.get("model") or DEFAULT_MODEL, a.get("effort") or "high",
                                       wt, base, allow, protect, prompt, int(a.get("budget") or 3000000))
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
        text = a["text"]
        if w["state"] in ("SUBMITTED", "WAITING_ASK", "BUDGET"):
            if w["state"] == "BUDGET":
                self.upd(w, budget=w["tokens"] + 1000000)
            self.upd(w, state="WORKING", nudges=0)
        if w["turn"] and a.get("now"):
            r = await self.rpc("turn/steer", {"threadId": w["thread"], "expectedTurnId": w["turn"], "input": [{"type": "text", "text": "DEPUTY: " + text}]})
            if "error" not in r:
                return "steered %s" % w["name"]
            w = self.cur(w["name"])
            if w["turn"]:
                return "ERR steer: " + r["error"].get("message", "")
        if w["turn"]:
            self.db.execute("insert into msgs(name,gen,ts,text) values(?,?,?,?)", (w["name"], w["gen"], now(), text))
            return "queued for %s's next report (auto-steer after %dm)" % (w["name"], PIGGY_S // 60)
        err = await self.start_turn(w, "DEPUTY: " + text)
        return "ERR " + err if err else "turn started %s" % w["name"]

    async def c_answer(self, a):
        return await self.c_send({"name": a["name"], "text": "ANSWER to %s: %s" % (a["ask"], a["text"]), "now": True})

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
        q = "select name, max(gen) from workers group by name"
        out = []
        for name, _ in self.db.execute(q).fetchall():
            w = self.cur(name)
            if a.get("deputy") and w["deputy"] != a["deputy"]:
                continue
            if w["state"] in ("RETIRED", "DEAD") and not a.get("all"):
                continue
            out.append("%s g%d %s %s %s turn=%s rep=%d/%s item=%s tok=%dk%s" % (w["name"], w["gen"], w["deputy"], w["state"], w["model"],
                       "on" if w["turn"] else "off", w["reports"], ago(w["last_report"]), ago(w["last_item"]), w["tokens"] // 1000,
                       (" sha=" + w["sha"][:10]) if w["sha"] else ""))
        return "\n".join(out) or "(no workers)"

    async def c_limits(self, a):
        r = await self.rpc("account/rateLimits/read", {})
        self.rate = r.get("result", self.rate)
        rl = (self.rate or {}).get("rateLimits") or {}
        pr = rl.get("primary") or {}
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
        return "retired %s g%d" % (w["name"], w["gen"])

    async def c_renew(self, a):
        """fresh thread, same worktree, starting from the worker's own WORKLOG.md (or a fork if --fork)"""
        w, err = self.live(a["name"])
        if err:
            return err
        with open(os.path.join(HOME, "briefs", w["name"] + ".md")) as f:
            brief = f.read()
        extra = a.get("text", "").strip()
        await self.retire_w(w, "renewed to g%d" % (w["gen"] + 1))
        g = w["gen"] + 1
        if a.get("fork"):
            fp = {"threadId": w["thread"]}
            if a.get("before_turn"):
                fp["beforeTurnId"] = a["before_turn"]
            prompt = "DEPUTY (after fork): " + (extra or "Continue from your last good state.")
            nw, err = await self.new_thread(w["name"], g, w["deputy"], a.get("model") or w["model"], w["effort"], w["wt"], w["base"],
                                            json.loads(w["allow"]), json.loads(w["protect"]), prompt, 3000000, fork_from=fp)
        else:
            prompt = ("You are generation %d of worker %s. Your predecessor's state is in WORKLOG.md in the worktree and in the "
                      "uncommitted/committed changes there. Read WORKLOG.md first, then continue the brief below.\n%s\n\n%s") % (
                      g, w["name"], ("DEPUTY: " + extra) if extra else "", brief)
            nw, err = await self.new_thread(w["name"], g, w["deputy"], a.get("model") or w["model"], w["effort"], w["wt"], w["base"],
                                            json.loads(w["allow"]), json.loads(w["protect"]), prompt, 3000000)
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

    # ---- monitor
    async def monitor(self):
        while True:
            await asyncio.sleep(20)
            for (name,) in self.db.execute("select distinct name from workers").fetchall():
                w = self.cur(name)
                if w["state"] in ("RETIRED", "DEAD") or not w["turn"]:
                    continue
                if w["tokens"] > w["budget"]:
                    await self.rpc("turn/interrupt", {"threadId": w["thread"], "turnId": w["turn"]})
                    self.upd(w, state="BUDGET")
                    self.event(w, "BUDGET", "token budget %dk exceeded (%dk); interrupted. send to resume (raises nothing), or renew/retire" % (w["budget"] // 1000, w["tokens"] // 1000))
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


def git(cwd, *args):
    return subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True, text=True).stdout


def guard(w, waivers):
    """stage everything, then judge the staged diff against base. Returns (findings, waived)."""
    wt, base = w["wt"], w["base"]
    git(wt, "add", "-A")
    files = [f for f in git(wt, "diff", "--cached", "--name-only", base).split("\n") if f]
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


USAGE = """cxo — Codex hub. Commands (one terse line out; ERR... on failure, exit 1):
  hub start|stop|run              resident hub (start = detached)
  ping | limits | status [-d DEP] [--all]
  spawn NAME -d DEP (--mklane [--from main|next] | --repo PATH [--base REF] | --wt PATH) [-m MODEL] [-e EFFORT] [--allow GLOB]... [--protect GLOB]...
        [--no-default-protect] [--budget TOKENS] [--force]   < brief.md
  send NAME [--now] TEXT...       queued for next report (default) | steer now | new turn if idle
  wait [-d DEP] [-t SECS<=590]    block for events: ASK SUBMIT SUBMIT_REFUSED GUARD STALL NO_SUBMIT BUILD ERROR RETIRED ...
  answer NAME ASKID TEXT...      (delivered as a steer, or a new turn if idle)
  interrupt NAME | retire NAME [why...] | renew NAME [--fork [--before-turn ID]] [-m MODEL] [TEXT...]
  log NAME [-n N] [--gen G]
  selftest [-m MODEL]"""


def parse(argv):
    a, pos, i = {}, [], 0
    flags = {"-d": "deputy", "--deputy": "deputy", "--repo": "repo", "--base": "base", "--wt": "wt", "-m": "model", "--model": "model",
             "-e": "effort", "--budget": "budget", "--from": "from", "-t": "timeout", "-n": "n", "--gen": "gen", "--before-turn": "before_turn"}
    multi = {"--allow": "allow", "--protect": "protect"}
    bools = {"--now": "now", "--all": "all", "--force": "force", "--fork": "fork", "--mklane": "mklane", "--no-default-protect": "no_default_protect"}
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
    """spawn -> report -> submit refused (planted scope violation) -> fix -> submit ok -> retire -> send refused."""
    ts = time.strftime("%m%d%H%M%S")
    repo = os.path.join(HOME, "selftest", "repo-" + ts)
    os.makedirs(os.path.join(repo, "allowed")); os.makedirs(os.path.join(repo, "other"))
    for p, t in (("allowed/a.txt", "a\n"), ("other/b.txt", "b\n")):
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
        print("%s %-34s %s" % ("PASS" if ok else "FAIL", label, detail.replace("\n", " | ")[:300]))
        sys.stdout.flush()

    def wait_for(kinds, limit):
        end, seen = time.time() + limit, []
        while time.time() < end:
            out = call("wait", {"deputy": dep, "timeout": min(120, max(1, int(end - time.time())))})
            if out != "(no events)":
                seen += out.split("\n")
                hit = [e for e in seen if e.split(" ")[1] in kinds]
                if hit:
                    return hit[0], seen
        return None, seen

    out = call("spawn", {"name": name, "deputy": dep, "repo": repo, "allow": ["allowed/*"], "model": model, "effort": "low",
                         "brief": brief, "budget": 400000, "force": True})
    step("spawn", out.startswith("spawned"), out)
    if not out.startswith("spawned"):
        return 1
    ev, seen = wait_for({"SUBMIT_REFUSED", "SUBMIT"}, 420)
    step("planted scope violation refused", bool(ev) and " SUBMIT_REFUSED " in ev and "scope:other/b.txt" in ev, ev or "timeout: " + " | ".join(seen))
    st = call("status", {"deputy": dep})
    m = re.search(r"rep=(\d+)", st)
    step("worker reported via tool", bool(m) and int(m.group(1)) >= 1, st)
    # let the refused turn end, then send the fix as a deputy
    for _ in range(60):
        if "turn=off" in call("status", {"deputy": dep}):
            break
        time.sleep(3)
    out = call("send", {"name": name, "text": "Now restore other/b.txt to exactly its original content (single line 'b'), keep the change to allowed/a.txt, and call submit again."})
    step("deputy send (idle -> new turn)", out.startswith(("turn started", "queued", "steered")), out)
    ev, seen = wait_for({"SUBMIT"}, 420)
    step("clean resubmit accepted", bool(ev), ev or "timeout: " + " | ".join(seen))
    wt = os.path.join(HOME, "wt", name)
    files = git(wt, "show", "--name-only", "--format=", "HEAD").split()
    step("commit touches only allowed/a.txt", files == ["allowed/a.txt"], "HEAD files=%s branch=%s" % (files, git(wt, "rev-parse", "--abbrev-ref", "HEAD").strip()))
    out = call("retire", {"name": name, "why": "selftest done"})
    step("retire", out.startswith("retired"), out)
    out = call("send", {"name": name, "text": "are you there?"})
    step("send to retired name refused", out.startswith("ERR REFUSED"), out)
    out = call("spawn", {"name": name, "deputy": dep, "repo": repo, "brief": "x", "force": True})
    step("respawn of retired name refused", out.startswith("ERR name"), out)
    st = call("status", {"deputy": dep, "all": True})
    print("worker: " + st)
    print("log:\n" + call("log", {"name": name, "n": 40}))
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
        if sub == "run":
            asyncio.run(_hub_main()); return 0
        pidf = os.path.join(HOME, "hub.pid")
        if sub == "start":
            os.makedirs(HOME, exist_ok=True)
            try:
                print("already running: " + call("ping", {}, 5)); return 0
            except Exception:
                if os.path.exists(SOCK):
                    os.unlink(SOCK)
            p = subprocess.Popen([sys.executable, os.path.abspath(__file__), "hub", "run"], stdout=open(os.path.join(HOME, "hub.log"), "a"),
                                 stderr=subprocess.STDOUT, start_new_session=True)
            open(pidf, "w").write(str(p.pid))
            for _ in range(60):
                time.sleep(0.5)
                if os.path.exists(SOCK):
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
    elif cmd in ("interrupt", "log"):
        a["name"] = pos[0]
    try:
        out = call(cmd, a)
    except ConnectionError as e:
        print(e); return 1
    print(out)
    return 1 if out.startswith("ERR") else 0


if __name__ == "__main__":
    sys.exit(main())
