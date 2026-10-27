import io

def rep(path, a, b, label):
    s = open(path).read()
    n = s.count(a)
    assert n == 1, f"{path} {label}: found {n}"
    open(path, "w").write(s.replace(a, b))
    print(f"patched {path} ({label})")

# ---- nd.js: the two new kernel calls (tg_holds as JSON like tg_lies; tg_iface beside tg_source)
rep("testground/nd.js",
    "    cell: (i, id) => call(K._w_cell, i, enc.encode(id)),",
    """    cell: (i, id) => call(K._w_cell, i, enc.encode(id)),
    // a package's grades and held fields (Web.Sim.Teach); the Vault scene's menu as JSON (tg_holds)
    iface: (i, pkg) => call(K._w_iface, i, enc.encode(pkg)),
    holds: () => JSON.parse(dec.decode(out(K._w_holds()))),""",
    "nd.js exports")

# ---- glue.c: the externs and the two wrappers
rep("Web/c/glue.c",
    "extern lean_object* tg_cell(uint32_t, lean_object*);",
    """extern lean_object* tg_cell(uint32_t, lean_object*);
extern lean_object* tg_iface(uint32_t, lean_object*);
extern lean_object* tg_holds(lean_object*);""",
    "glue externs")
rep("Web/c/glue.c",
    'EMSCRIPTEN_KEEPALIVE int32_t w_cell(uint32_t i, const uint8_t* p, size_t n) { return io_take(tg_cell(i, ba(p, n))); }',
    """EMSCRIPTEN_KEEPALIVE int32_t w_cell(uint32_t i, const uint8_t* p, size_t n) { return io_take(tg_cell(i, ba(p, n))); }
EMSCRIPTEN_KEEPALIVE int32_t w_iface(uint32_t i, const uint8_t* p, size_t n) { return io_take(tg_iface(i, ba(p, n))); }
EMSCRIPTEN_KEEPALIVE int32_t w_holds(void) { return take_string(tg_holds(lean_box(0))); }""",
    "glue wrappers")

# ---- index.html: one line, the scene module (after testground.js, which holds `demos` live)
rep("testground/index.html",
    '<script type="module" src="testground.js"></script>',
    """<script type="module" src="testground.js"></script>
<script type="module" src="scenes-vault.js"></script>""",
    "index.html script")

# ---- testground.js: the tour step, after the claims demo
rep("testground/testground.js",
    "  { say: 'The meter: each Turn records its member and its ticks",
    """  { say: 'Value under a grade. The Vault\'s methods declare how much they may move. A withdraw past the grade is refused and nothing moves. A row of the vault names value the object holds: a deposit that pays nothing is refused (legUnfunded).', demo: 'vault' },
  { say: 'The meter: each Turn records its member and its ticks""",
    "tour step")

# ---- gate.sh: the runner beside the axes, and its control
rep("testground/build/gate.sh",
    "node axes-run.mjs || { echo \"FAIL an axis demo did not answer as scripted (axes-run.mjs)\"; exit 1; }",
    """node axes-run.mjs || { echo "FAIL an axis demo did not answer as scripted (axes-run.mjs)"; exit 1; }
node scenes-vault-run.mjs || { echo "FAIL the Vault scene did not meet the journey's menu (scenes-vault-run.mjs)"; exit 1; }""",
    "gate run")
rep("testground/build/gate.sh",
    "  if node axes-run.mjs --harness-control; then echo \"FAIL harness: axes-run.mjs --harness-control passed\"; exit 0; fi",
    """  if node axes-run.mjs --harness-control; then echo "FAIL harness: axes-run.mjs --harness-control passed\"; exit 0; fi
  if node scenes-vault-run.mjs --harness-control; then echo "FAIL harness: scenes-vault-run.mjs --harness-control passed\"; exit 0; fi""",
    "gate control")

print("done")
