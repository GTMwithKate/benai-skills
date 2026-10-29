# Real logos

The rule is simple: if the infographic names an app, it shows that app's real mark. A
drawn approximation always looks slightly wrong, and the brand owner is the one who
notices. These are third-party app marks used inside the content, and they are the one
thing in this kit that does not change with the user's brand.

## Placing a logo

Four tokens. `build.py` swaps them for real vectors at render time.

| Token | Renders |
|---|---|
| `<!--MARK:claude:40-->` | The bare mark, 40px tall, theme aware |
| `<!--MARKW:claude:40:Claude-->` | The same, with a label under it |
| `<!--TILE:claude:60:31-->` | The mark on a light tile with a 2px ink border |
| `<!--TILEW:claude:60:31:Claude-->` | Tile plus label |

**Prefer bare marks.** Tiles were the original treatment and they read as loud, especially
a grid of light squares on a dark ground. Reach for a tile only when the marks sit on a
busy or mid-tone surface and need separating from it.

Sizing is by height, not width. Colour vectors are not all square (Gmail is 512x399), so
setting both dimensions squashes them. `build.py` sets the height and lets the width
follow.

## Colour, and the dark-ground problem

Most of the marks are the real multi-colour vector. Single-colour glyph sets turn Gmail
into a flat red envelope and Slack into a flat purple hash, which is why the colour
versions matter.

A mark whose artwork is essentially black (Notion, X, GitHub, Apple, Vercel, Anthropic)
disappears on the dark ground. `build.py` handles this: on dark it falls back to that
brand's single-colour glyph drawn in the dark theme's ink colour. Tiled marks keep their
colour in both modes because the light tile carries them. You do not need to think about
it, but you do need to know it is happening, so a Notion mark rendering in the light ink
on dark is correct rather than a bug.

## What is in the library

Run `python3 scripts/add_logo.py --list` for the current set. It covers the AI tools,
Google Workspace, the usual SaaS stack and the social platforms.

Six marks have no colour vector published anywhere and keep their glyph: Google Docs,
HubSpot, Mailchimp, Make, n8n and Zapier. For HubSpot, Zapier and Mailchimp the glyph is
the correct icon anyway.

## Adding one

```bash
python3 scripts/add_logo.py notion
python3 scripts/add_logo.py figma --url https://example.com/figma-icon.svg
```

It searches svgl, then gilbarbara/logos, then vectorlogo.zone, and keeps the squarest
candidate. Two guards worth knowing about:

- **Ids get namespaced with the slug.** A dozen inlined SVGs that all define `#a` fight
  over the same gradient and the page renders garbage.
- **Anything wider than 1.75:1 is rejected as a wordmark.** HubSpot and Zapier both came
  back as full text logos squeezed into a 40px icon slot.

## When a company publishes no vector

Some do not, and no public logo set carries them.

Use a bordered name chip at the same height as the marks beside it:

```html
<span style="border: 1px solid @HAIR@; border-radius: 6px; padding: 7px 12px;
             font-family: @DISPLAYFONT@;
             font-weight: 500; font-size: 16px; color: @MUTED@; flex: none;">Attio</span>
```

Matching the height and the rhythm is what makes it read as deliberate rather than as a
missing image. Say at handover which marks are chips, and offer to drop in a real file
if the user can get one from the company's brand page.

## Attribution

Marks belong to their owners. They are used to name the tool, never to imply an
endorsement. `LogoLibrary` carries that line at the bottom; a normal infographic does not
need it.
