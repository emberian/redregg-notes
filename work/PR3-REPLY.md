<!-- For Ember to post on emberian/minidregg PR #3 (not posted). Landed commit: c1cc0a89 on lane/perf-client
     (on top of H 22166640). Close #3 with this once lane/perf-client is on main; adjust the sha if it is rebased. -->

Thanks, pug. This landed, folded into a change we already had in flight for the same cost.

Our lane had already made the same move: one codec child per `mini` process, commit 22166640 on `lane/perf-client`. So we did not merge #3 as-is. Both rewrite the body of `local_frame`, and they conflict. What landed is ours plus your pieces, in c1cc0a89, with you as co-author:

- The child is keyed by `anchor_binding`: the image path, its inode identity and the settings bytes. A Host image replaced in place now starts a new child. Ours had keyed on the path and the settings bytes only, so it would have kept serving the old image.
- The child is dropped explicitly when the settings change during a frame.
- Your test `codec_loop_is_reused_only_for_the_same_image_and_settings`, unchanged. It was red on our version (2 starts where 3 were expected, at the replaced image) and is green now. It now holds a test lock shared with our codec tests, because they all use the process-wide slot.

What differs from your version:

- The settings path is not part of the key, only the bytes are (through `anchor_binding`). The codec child parses the settings once at start and never reads the file again, so the path does not change what it answers. Inside one process the path does change: `mini workspace create` renames its attempt directory (`attempts/a-<nonce>` to `attempts/create-<name>`) between frames. With the path in the key, our N=4 strace census went from 45 to 53 Host execs, one extra codec start per create. `codec_child_is_kept_across_a_renamed_settings_directory` pins this.
- Pure verbs go through the child on every path, not only when local consent is pinned, so your "plain" rows will move too. The client's one-shot exit-2 handling of pure verbs is gone, because nothing reaches it any more.
- A refusal keeps the child. The child decodes its own refusal, as the session path does, and the error now reads `host refused <verb>: <reason>; encoded refusal: <hex>`. It used to read `local consent refused before signing: ...`. If that decode exchange fails, the child is dropped and the refusal is reported undecoded. That case has its own test.
- The same lane also removes the per-process SHA-256 of the Host image (764d6bb6), which is your inferred ~145 ms per `mini` start. `mini` now uses the workspace's pinned `hostSha256`. The file is checked when `serve` starts, and on request with `mini --verify-host` or `MINI_VERIFY_HOST=1`.

What your deployment needs to do:

- If anything matches on the old refusal text, match `host refused <verb>:` instead.
- If you relied on every `mini` invocation re-hashing the Host image, set `MINI_VERIFY_HOST=1` (or pass `--verify-host`) where you want that check. If the image is replaced under a running `serve`, `serve` refuses at its next start with a pin mismatch.
- Nothing else changes. The frames, the replies and the env in `deploy/candidate/run.sh` stay as they are.

Your measurements are in the commit message: write p50 from 1.75 s to 1.36 s, and Host execs from 284 to 54. Your per-write breakdown is going into our performance notes.
