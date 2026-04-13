#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"
OUT_FILE="$DIST_DIR/skills-bundle.zip"

mkdir -p "$DIST_DIR"

cd "$ROOT_DIR"
zip -r "$OUT_FILE" \
  skills/START_HERE.md \
  skills/skript-code-specialist \
  skills/javascript-code-specialist \
  skills/code-repair-specialist >/dev/null

echo "Created: $OUT_FILE"
