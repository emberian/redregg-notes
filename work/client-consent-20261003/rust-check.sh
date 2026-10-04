#!/usr/bin/env bash
set -euo pipefail
cd /tank/dregg-build/codex-client-consent-rust-20261003/src
export CARGO_TARGET_DIR=/tank/dregg-build/codex-client-consent-rust-20261003/target CARGO_BUILD_JOBS=2
cargo nextest run --release --offline --locked --manifest-path native/resource-client/Cargo.toml --bin mini -E 'test(client_consent::tests::) or test(render::text::tests::)'
echo SCOPED-PASS-client-consent-and-terminal-control
