#!/usr/bin/env bash
# Export every slide-*.html in the current directory to slides/*.png,
# then assemble <slug>.pdf. Run from the carousel working folder.
#
#   bash export.sh [slug] [WIDTHxHEIGHT]
#
# Defaults: slug = "carousel", size = 1080x1350.
set -euo pipefail

SLUG="${1:-carousel}"
SIZE="${2:-1080,1350}"
SIZE="${SIZE/x/,}"

mkdir -p slides

# --- find a Chrome-family binary -------------------------------------------
CHROME=""
for c in \
  "google-chrome" "chromium" "chromium-browser" "chrome" \
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  "/Applications/Chromium.app/Contents/MacOS/Chromium" \
  "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" \
  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"; do
  if command -v "$c" >/dev/null 2>&1 || [ -x "$c" ]; then CHROME="$c"; break; fi
done

shopt -s nullglob
HTMLS=(slide-*.html)
[ ${#HTMLS[@]} -gt 0 ] || { echo "No slide-*.html files here." >&2; exit 1; }

for f in "${HTMLS[@]}"; do
  out="slides/${f%.html}.png"
  if [ -n "$CHROME" ]; then
    "$CHROME" --headless=new --disable-gpu --hide-scrollbars \
      --window-size="$SIZE" --virtual-time-budget=4000 \
      --screenshot="$out" "file://$PWD/$f" >/dev/null 2>&1
  else
    # Fallback: Playwright CLI (if installed)
    npx playwright screenshot --viewport-size="$SIZE" "$f" "$out" \
      || { echo "No headless browser found. Install Chrome/Chromium or Playwright." >&2; exit 1; }
  fi
  echo "rendered $out"
done

# --- assemble the PDF -------------------------------------------------------
if python3 -c "import img2pdf" 2>/dev/null; then
  python3 -c "import img2pdf,glob; open('$SLUG.pdf','wb').write(img2pdf.convert(sorted(glob.glob('slides/slide-*.png'))))"
elif command -v magick >/dev/null 2>&1; then
  magick slides/slide-*.png "$SLUG.pdf"
elif command -v convert >/dev/null 2>&1; then
  convert slides/slide-*.png "$SLUG.pdf"
else
  echo "PNGs are in slides/. No img2pdf or ImageMagick found for PDF assembly." >&2
  echo "Install one:  pip3 install img2pdf   or   brew install imagemagick" >&2
  exit 2
fi
echo "assembled $SLUG.pdf"
