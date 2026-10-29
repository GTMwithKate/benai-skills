# Style Mechanics

Generic craft techniques that make these templates read as designed rather than generated. Every value below binds to the token map from Step 1 of SKILL.md. None of these carry a fixed color: if a mechanic conflicts with the user's design system (e.g. their brand uses soft blurred shadows, not solid offsets), the design system wins and you adapt the mechanic.

## The card (core building block)

Every template is built from one repeating unit: a content card with a border and a solid offset shadow.

```css
.card {
  background: var(--accent-1);          /* rotates per item, see below */
  border: 2px solid var(--ink);
  border-radius: 6px;                   /* slightly rounded, never a pill */
  box-shadow: 8px 8px 0 var(--ink);     /* solid offset, no blur */
  color: var(--ink);
}
```

Why a solid offset shadow: a hard `--ink` shadow with zero blur gives depth without the "default CSS drop shadow" look, and it survives compression in video and social exports. If the user's design system defines its own shadow style, use theirs instead.

In SVG or Excalidraw, the shadow is a second rectangle in `--ink`, same size as the card, offset roughly +8 to +12px right and +12 to +18px down, drawn BEFORE the card so it sits behind it (z-order = element order). Shadow has no border of its own; the card carries the 2px `--ink` border.

## Color rotation

Multi-item diagrams rotate card fills through the accent tokens in a fixed order: item 1 gets `--accent-1`, item 2 `--accent-2`, and so on, wrapping around. Fixed order matters: it makes a deck of many visuals feel like one family instead of random coloring.

- Card fills must be light enough (or dark enough, on a dark-ground brand) that `--ink` text on them passes WCAG AA (4.5:1 for body text). If an accent is too saturated for text, tint it toward `--surface` for the fill and keep the pure accent for small non-text elements.
- Semantic exceptions beat rotation: in comparisons, use the brand's positive accent vs its caution accent rather than blind rotation.

## Canvas and background

- The canvas is `--surface`, never pure white `#FFFFFF` or pure black `#000000` unless the brand tokens literally are those values.
- Text and borders are `--ink` on light grounds. Never gray-out text with reduced-contrast neutrals for body copy; de-emphasize with size and weight instead.

## Typography

- Titles: `--font-heading`, uppercase or strong weight, 28px minimum at a ~800-1200px canvas width.
- Card labels: `--font-body`, 18-20px, medium-to-bold weight.
- Descriptions/subtitles: `--font-body`, 16px. 14px only for minor annotations.
- Load fonts per the design system's `foundations/typography.md`, with the fallback stack it declares. In HTML output, include the fallback stack inline so the file degrades gracefully.

## Arrows and connectors

- Stroke: `--ink`, 2px, solid arrowhead.
- Dashed stroke is reserved for feedback/return paths (see cycle-loop template).
- Arrows connect only things with real sequence, causation, or dependency. Sibling items never get arrows.

## Icons

One Unicode emoji per card, placed inline before the label with two spaces of breathing room ("🔔  EVENT FIRES"). See [icons.md](icons.md) for the curated palette and selection guide. If the user's design system has its own icon set (see `foundations/iconography.md`), prefer that over emoji.

## Copy rules

- No em dashes anywhere: slide copy, labels, annotations. Use periods, commas, colons, or restructure the sentence.
- Card labels are scannable fragments, not sentences. Title case or all-caps per the brand's typography rules.
- A header says WHAT the section is; a card label says WHAT the item is. Never repeat the header inside a card.

## HTML output skeleton

Start every HTML visual with the token block so a brand swap is one edit:

```html
<style>
  :root {
    --ink: /* from design-system tokens */;
    --surface: /* from design-system tokens */;
    --accent-1: /* ... */;
    --accent-2: /* ... */;
    --accent-3: /* ... */;
    --font-heading: /* ... */, sans-serif;
    --font-body: /* ... */, sans-serif;
  }
</style>
```

Fill the values from the resolved token map. Never leave placeholder comments in a delivered file, and never fill them with values the user did not confirm.
