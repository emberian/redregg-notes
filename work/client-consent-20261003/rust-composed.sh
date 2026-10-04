#!/usr/bin/env bash
set -euo pipefail
cd /tank/dregg-build/codex-client-consent-rust-20261003/src
export CARGO_TARGET_DIR=/tank/dregg-build/codex-client-consent-rust-20261003/target CARGO_BUILD_JOBS=2
cargo nextest run --release --offline --locked --manifest-path native/resource-client/Cargo.toml --bin mini -E 'test(client_consent::tests::) or test(render::text::) or test(path_tests::) or test(chat::tests::) or test(shell::session_fs::tests::) or test(shell::tests::)'
cargo build --release --offline --locked --manifest-path native/resource-client/Cargo.toml --bin mini
echo SCOPED-PASS-composed-consent-service-production
