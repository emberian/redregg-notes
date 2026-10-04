#!/usr/bin/env bash
set -euo pipefail
cd /tank/dregg-build/codex-client-consent-rust-20261003/src
export CARGO_TARGET_DIR=/tank/dregg-build/codex-client-consent-rust-20261003/target CARGO_BUILD_JOBS=2
cargo nextest run --release --offline --locked --manifest-path native/resource-client/Cargo.toml --bin mini -E 'test(unhex_rejects_malformed_unicode_without_panicking) or test(decode_hex_malformed_payload_retains_empty_fallback) or test(payload_text_malformed_unicode_retains_diagnostic) or test(invocation_family_)'
cargo build --release --offline --locked --manifest-path native/resource-client/Cargo.toml --bin mini
echo SCOPED-PASS-current-decoder-family-production
