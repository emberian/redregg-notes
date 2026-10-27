/* replay.c — replay a trace of kernel calls against a build of the kernel; every reply must be the
   recorded byte string. Reports calls, mismatches and the time spent inside the kernel. Built twice:
   natively (leanc) and to wasm (emcc), from the same generated C. */
#include <lean/lean.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
extern lean_object* tg_genesis(lean_object*);
extern lean_object* tg_host(uint8_t, lean_object*);
extern lean_object* tg_follow(uint32_t, uint8_t, lean_object*);
lean_object* initialize_nanodregg_Web_Sim_Testground(uint8_t builtin);
void lean_initialize_runtime_module(void);
void lean_io_mark_end_initialization(void);
static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec * 1e3 + t.tv_nsec / 1e6; }
static lean_object* ba(const uint8_t* p, size_t n) { lean_object* a = lean_alloc_sarray(1, n, n); if (n) memcpy(lean_sarray_cptr(a), p, n); return a; }
static uint32_t rd32(FILE* f) { uint8_t b[4]; if (fread(b, 1, 4, f) != 4) return 0; return b[0] | b[1] << 8 | b[2] << 16 | (uint32_t)b[3] << 24; }
int main(int argc, char** argv) {
  lean_initialize_runtime_module();
  lean_object* r = initialize_nanodregg_Web_Sim_Testground(1);
  if (lean_io_result_is_error(r)) { fprintf(stderr, "init failed\n"); return 2; }
  lean_dec_ref(r); lean_io_mark_end_initialization();
  FILE* f = fopen(argv[1], "rb"); if (!f) { perror("trace"); return 2; }
  int calls = 0, bad = 0; double ms = 0, msHost = 0, msFollow = 0;
  int kind;
  while ((kind = fgetc(f)) != EOF) {
    uint32_t i = rd32(f); int op = fgetc(f); uint32_t n = rd32(f);
    uint8_t* p = malloc(n + 1); if (fread(p, 1, n, f) != n) break;
    uint32_t rn = rd32(f); uint8_t* rp = malloc(rn + 1); if (fread(rp, 1, rn, f) != rn) break;
    double t = now();
    lean_object* res = kind == 0 ? tg_genesis(ba(p, n)) : kind == 1 ? tg_host((uint8_t)op, ba(p, n)) : tg_follow(i, (uint8_t)op, ba(p, n));
    double dt = now() - t; ms += dt; if (kind == 1) msHost += dt; if (kind == 2) msFollow += dt;
    lean_object* v = lean_io_result_get_value(res);
    size_t vn = lean_sarray_size(v);
    if (vn != rn || memcmp(lean_sarray_cptr(v), rp, rn) != 0) { if (bad < 5) fprintf(stderr, "call %d kind %d op %d: reply differs (%zu vs %u bytes)\n", calls, kind, op, vn, rn); bad++; }
    lean_dec(res); free(p); free(rp); calls++;
  }
  printf("calls %d mismatches %d kernel-ms %.1f (writer %.1f, follow %.1f)\n", calls, bad, ms, msHost, msFollow);
  return bad ? 1 : 0;
}
