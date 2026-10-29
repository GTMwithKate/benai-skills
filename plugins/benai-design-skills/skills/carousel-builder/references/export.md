# Export: HTML slides to PNGs to PDF

The primary render path is deterministic: HTML templates + the brand token sheet, screenshotted headlessly. No image model required.

## Working folder layout

```
<slug>-carousel/
├── tokens.css        — copied from assets/templates/tokens.css, filled from the design system
├── slide-01.html …   — one file per slide, copied from the matching template and filled
├── slides/           — exported PNGs
└── <slug>.pdf        — the assembled carousel
```

Keep `tokens.css` next to the slide files; the templates link it with a relative path.

## Dimensions

Default **1080 x 1350** (4:5 portrait). LinkedIn documents and Instagram both accept it. Use 1080 x 1080 only if the user asks for square. If you change the size, change it in both the screenshot command and the templates' `.slide` rule.

## Screenshot each slide

Run the bundled script from the working folder:

```bash
bash <skill-dir>/scripts/export.sh            # renders slide-*.html -> slides/*.png -> <slug>.pdf
```

The script prefers headless Chrome/Chromium, because it is present on nearly every machine and needs no install:

```bash
chrome --headless=new --screenshot=slides/slide-01.png \
  --window-size=1080,1350 --hide-scrollbars --default-background-color=00000000 \
  "file://$PWD/slide-01.html"
```

Fallbacks, in order, if no Chrome-family browser is found:

1. **Playwright** (if installed): `npx playwright screenshot --viewport-size=1080,1350 slide-01.html slides/slide-01.png`
2. Ask the user which browser they have; a one-line install of Chromium also works.

Give fonts a beat to load: the script passes `--virtual-time-budget=4000` to Chrome. If a slide exports with fallback type, check the `@font-face`/fonts link in `tokens.css`.

## Assemble the PDF

The script tries these in order; use the same order manually:

```bash
# 1. img2pdf (lossless, portable)
python3 -c "import img2pdf,glob; open('<slug>.pdf','wb').write(img2pdf.convert(sorted(glob.glob('slides/slide-*.png'))))"
# 2. ImageMagick
magick slides/slide-*.png <slug>.pdf
# 3. macOS built-in, no installs
# (Quartz via sips produces one PDF per image; prefer 1 or 2. As a last resort,
#  Preview or any "images to PDF" step the user already has will do.)
```

## QA pass (mandatory)

Read every exported PNG back with the Read tool and check:

- All copy present, spelled exactly as written, nothing clipped or overflowing.
- Exactly one highlighted phrase per headline.
- Page indicator correct (`03 / 07` style), swipe cue on every slide except the last.
- The logo (if any) renders crisply; a broken image icon means a wrong relative path.

Fix the HTML and re-run the export for any failing slide.

## Optional: image-model render path

If the user explicitly wants illustrated or photographic slides and has an image-generation tool connected (any image model works), you may generate slide art from prompts instead of, or underneath, the HTML text layer. Rules when you do:

- This path is **optional, never required**; default to HTML.
- Build prompts from the brand tokens (name the colors and type feel from the design system, never from memory).
- Image models misspell: keep generated slides text-light, verify every word, re-generate failures.
- Text-critical elements — footer, page numbers, logo, dense bullets — stay in HTML/code compositing. Never let an image model draw a logo.
