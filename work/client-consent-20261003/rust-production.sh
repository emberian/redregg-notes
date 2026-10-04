#!/usr/bin/env bash
set -euo pipefail
cd /tank/dregg-build/codex-client-consent-rust-20261003/src
export CARGO_TARGET_DIR=/tank/dregg-build/codex-client-consent-rust-20261003/target CARGO_BUILD_JOBS=2
cargo nextest run --release --offline --locked --manifest-path native/resource-client/Cargo.toml --bin mini -E 'test(render::text::)'
cargo build --release --offline --locked --manifest-path native/resource-client/Cargo.toml --bin mini
echo SCOPED-PASS-consent-production-and-terminal-control
