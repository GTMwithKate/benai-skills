# Visual QA Checklist

Run this against every rendered visual before presenting it to the user. It applies to all output formats: HTML/CSS, SVG, and Excalidraw JSON. For a batch, spawn a subagent with this file and the rendered outputs.

## 1. Color, contrast, tokens

- [ ] Every color in the file traces to a token in the resolved token map (`--ink`, `--surface`, `--accent-N`) or a documented derived tint. No colors invented mid-build, no tool defaults (browser default link blue, default diagram palettes).
- [ ] No pure `#000000` or `#FFFFFF` unless the brand tokens literally contain them.
- [ ] Body text passes WCAG AA (4.5:1) against its card fill. No grayed-out text for body copy; de-emphasis is done with size and weight.
- [ ] No card sits below full opacity without a documented reason (low opacity lets shadows bleed through and muddies the visual).

## 2. Text overflow and sizing

The most common failure: text boxes too narrow for their content, causing broken-looking wraps.

- [ ] Rough check per label: `text.length x fontSize x 0.55 < box width`. Widen the box if not.
- [ ] No unintended line breaks inside a label that should be one line.
- [ ] In HTML: no `overflow: hidden` or `text-overflow: ellipsis` silently cutting content; no `white-space: nowrap` forcing truncation.
- [ ] Minimum sizes: 16px body, 20px card labels, 28px titles, 14px only for minor annotations.

## 3. Alignment

- [ ] Title horizontally centered over the full diagram width; subtitle centered under it at the same x center.
- [ ] Stacked lists: all cards share the same x and width.
- [ ] Grid columns: columns evenly spaced; items within a column share the same x.
- [ ] Comparisons: left/right headers centered within their own panels (not the full canvas); matching attribute rows share the same y; bottom captions centered under their own side.

## 4. Shadow correctness (when using the solid offset shadow mechanic)

- [ ] Every card with a fill has its shadow; none missing.
- [ ] Shadow is `--ink`, solid, no blur, consistent offset across the whole visual (HTML: one `box-shadow` value everywhere; SVG/Excalidraw: same dx/dy on every shadow rect).
- [ ] In SVG/Excalidraw: shadow rectangle drawn BEFORE its card (earlier in element order), same width and height as the card, no border of its own.
- [ ] If the brand's own shadow style was used instead, it is applied consistently.

## 5. Redundancy

- [ ] No label repeats information already stated in its parent header.
- [ ] No duplicate text elements at the same position.
- [ ] Headers say what the section is; card labels say what the item is.

## 6. Structural consistency

- [ ] All cards in a list share identical width and height; all cards within a column share width.
- [ ] Uniform gaps: `gap = next_card_y - (current_card_y + current_card_height)` equal throughout.
- [ ] Arrow lengths consistent (same height for vertical, same width for horizontal).
- [ ] Comparisons mirrored: same item count, sizes, and spacing on both sides.
- [ ] Accent rotation follows the fixed order from style-mechanics.md (or the documented semantic exception).

## 7. Format-specific

### HTML/CSS
- [ ] Token block at the top of the file with real values; no unresolved placeholders.
- [ ] Font stack includes the design system's declared fallbacks.
- [ ] Border and radius match style-mechanics.md (2px solid `--ink`, small radius, never fully round).
- [ ] Reads correctly at 700-1200px viewport width.

### SVG
- [ ] ViewBox contains the full diagram with padding.
- [ ] Text elements set `font-family`, `font-size`, `text-anchor` correctly for centering.
- [ ] A comment block maps each literal color value to its token name.

### Excalidraw JSON
- [ ] All elements have unique `id` values; no `isDeleted: true` elements remain.
- [ ] `roundness: {"type": 3}` on rectangles, `fillStyle: "solid"` on filled shapes, `lineHeight: 1.25` on text.
- [ ] Text elements with `containerId` have a parent with a matching `boundElements` entry.

## Reporting format

```
QA ISSUES FOUND:
1. [CATEGORY] Description. Fix: [what to change]
2. ...

QA PASSED: [yes/no]
```

Fix issues before presenting the visual. Only surface an issue to the user when the fix needs their input.
