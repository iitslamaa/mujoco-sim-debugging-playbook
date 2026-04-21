#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT="${1:-/tmp/mujoco_terrain_kernel}"

c++ -std=c++17 -O3 -Wall -Wextra -pedantic "$ROOT/cpp/terrain_kernel.cpp" -o "$OUTPUT"
"$OUTPUT"
