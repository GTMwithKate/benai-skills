---
type: check
layer: 2-company
status: active
last-refreshed: {{DATE}}
source: distilled from {{VISUAL SOURCE: brand or design guidelines, or the shipped assets listed}}. Re-run de-slop-builder to refresh.
---

# Check: visual

Does the visual match the standard for its surface. Detect the surface first if there is more than one system, grading one surface by another's rules is wrong. Flag and suggest the concrete change.

## Universal craft slice (ships for everyone, do not delete)

Regardless of brand, a designed surface should hold these. Flag a break even when no brand rule is set.

- One clear focal point. Not everything competing for attention.
- Legible text: sufficient contrast against its background, a readable size, not text lost in a busy image.
- Alignment and a sane grid: elements line up, spacing is consistent, nothing visibly off-axis.
- No leftover placeholder art, broken images, or stand-in lorem boxes.

Misaligned (craft): no focal point, text that cannot be read, obvious misalignment, or placeholder art shipping.

## Brand slice

{{Fill this from their guidelines or extracted assets. If they have no usable visual standard, delete this section's specifics and write: "Brand slice not configured yet. Grading the universal craft slice only. Re-run de-slop-builder with shipped assets to add the brand layer." Otherwise capture, per surface:}}

### Surface {{A: e.g. web, slides, decks, docs}}
- Colors: {{exact palette, hexes, fills vs gradients, any hard rules like never a black background}}
- Fonts: {{heading, body, data or mono, fallback}}
- Tokens: {{shadows, borders, radii, spacing system}}

### Surface {{B: e.g. thumbnails, ads, social}}
- {{the distinct system for this surface: background, accent, headline rules, subject treatment}}

Misaligned (brand): {{the per-surface violations: off-palette color, wrong fonts, wrong background, headline too long, missing required accent, and so on}}.

## Grading

- Aligned: matches the right surface's palette, fonts, and layout, one clear focal point, craft slice clean.
- Drift: a near-off hex, weak hierarchy, a soft shadow where a hard one belongs, a minor craft slip.
- Misaligned: see the craft and per-surface lists above.
