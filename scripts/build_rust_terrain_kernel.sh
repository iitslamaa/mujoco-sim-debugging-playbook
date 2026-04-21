#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT="${1:-/tmp/mujoco_rust_terrain_kernel}"
REPEATS="${2:-5}"

if command -v rustc >/dev/null 2>&1; then
  RUSTC="$(command -v rustc)"
elif [ -x "$HOME/.cargo/bin/rustc" ]; then
  RUSTC="$HOME/.cargo/bin/rustc"
else
  echo "rustc not found; install Rust to build rust/terrain_kernel.rs" >&2
  exit 127
fi

"$RUSTC" -C opt-level=3 "$ROOT/rust/terrain_kernel.rs" -o "$OUTPUT"
"$OUTPUT" "$REPEATS"
