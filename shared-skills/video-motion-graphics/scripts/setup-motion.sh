#!/usr/bin/env bash
# One-time setup for the motion stage in a project folder.
# usage: bash setup-motion.sh [motion_dir]   (default ./motion)
# Copies the engine in, and installs playwright-core (no browser download: it uses Google Chrome).
set -e
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
DIR="${1:-./motion}"
mkdir -p "$DIR"/films "$DIR"/out "$DIR"/work
need=()
command -v node >/dev/null || need+=("Node.js (https://nodejs.org)")
command -v ffmpeg >/dev/null || need+=("ffmpeg (Mac: brew install ffmpeg)")
command -v python3 >/dev/null || need+=("python3")
if [ ${#need[@]} -gt 0 ]; then echo "Install first: ${need[*]}"; exit 1; fi
rm -rf "$DIR/engine" && cp -R "$SKILL/engine" "$DIR/engine"
[ -f "$DIR/brand.css" ] || printf ':root {\n  /* Fill from the design system: --bg --ink --muted --accent --card --line --font */\n}\n' > "$DIR/brand.css"
if [ ! -d "$DIR/node_modules/playwright-core" ]; then
  [ -f "$DIR/package.json" ] || echo '{"private":true,"type":"module"}' > "$DIR/package.json"
  (cd "$DIR" && npm install --silent playwright-core)
fi
if [ ! -d "/Applications/Google Chrome.app" ] && ! command -v google-chrome >/dev/null; then
  echo "No Google Chrome found: installing Playwright's Chromium instead."
  (cd "$DIR" && npx --yes playwright install chromium)
fi
ffmpeg -hide_banner -encoders 2>/dev/null | grep -q prores_ks || echo "Note: this ffmpeg has no prores_ks, so transparent panels cannot render."
echo "Ready. Films go in $DIR/films, renders in $DIR/out."
