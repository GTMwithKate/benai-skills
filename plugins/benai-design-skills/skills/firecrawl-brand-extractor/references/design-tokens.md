# From Branding JSON to Usable Design Tokens

Turning a `branding` payload into something a designer or developer can actually build
with, plus the multi-site comparison workflow.

## Pick the output format from the ask

| The ask | Deliver |
| --- | --- |
| "what are their brand colors" | A hex table with role labels and a confidence note |
| "build me a brand kit / style guide" | CSS custom properties, plus fonts and component specs |
| "set up design tokens" | A `tokens.json` in W3C design-token shape |
| "make our site look like theirs" | CSS variables plus the button specs, with the shadow string preserved verbatim |
| "compare us against these competitors" | One extraction per site, then a comparison table |
| "feed this into a design system generator" | The stripped branding object as JSON |

## CSS custom properties

The most portable output. Map the payload directly:

```css
:root {
  /* Color */
  --color-primary: #061b31;
  --color-secondary: #ffe0d1;
  --color-accent: #533afd;
  --color-background: #ffffff;
  --color-text: #0a0c0c;        /* verified visually, not from textPrimary */
  --color-link: #533afd;

  /* Type */
  --font-heading: "SF Pro Display", sans-serif;
  --font-body: "Sohne", sans-serif;
  --size-h1: 48px;
  --size-h2: 32px;
  --size-body: 16px;            /* corrected; extractor reported 32px */

  /* Spacing, from baseUnit: 8 */
  --space-1: 8px;
  --space-2: 16px;
  --space-3: 24px;
  --space-4: 32px;
  --radius: 4px;

  /* Components */
  --btn-primary-bg: #533afd;
  --btn-primary-text: #ffffff;
  --btn-secondary-bg: #ffffff;
  --btn-secondary-text: #533afd;
  --btn-secondary-border: #b9b9f9;
  --btn-shadow: none;
}
```

Two habits that matter here:

- **Build the spacing scale from `baseUnit`** as multiples (1x, 2x, 3x, 4x). The payload
  gives you the unit, not the scale.
- **Comment any value you corrected**, as with `--size-body` above. The person receiving
  this needs to know which numbers came from the extractor and which came from your
  visual check.

## W3C design tokens

For Style Dictionary, Tokens Studio, or Figma variable import:

```json
{
  "color": {
    "primary":    { "$value": "#061B31", "$type": "color" },
    "accent":     { "$value": "#533AFD", "$type": "color" },
    "background": { "$value": "#FFFFFF", "$type": "color" }
  },
  "font": {
    "heading": { "$value": "SF Pro Display", "$type": "fontFamily" },
    "body":    { "$value": "Sohne", "$type": "fontFamily" }
  },
  "space": {
    "base": { "$value": "8px", "$type": "dimension" }
  },
  "radius": {
    "default": { "$value": "4px", "$type": "dimension" }
  }
}
```

## Tailwind theme

```js
// tailwind.config.js
export default {
  theme: {
    extend: {
      colors: {
        primary: '#061B31',
        secondary: '#FFE0D1',
        accent: '#533AFD',
      },
      fontFamily: {
        heading: ['SF Pro Display', 'sans-serif'],
        body: ['Sohne', 'sans-serif'],
      },
      borderRadius: { DEFAULT: '4px' },
    },
  },
}
```

## Extracting the fields with jq

Pull a flat, quotable summary:

```bash
jq -r '
  .branding |
  "Scheme:     \(.colorScheme)",
  "Primary:    \(.colors.primary)",
  "Secondary:  \(.colors.secondary)",
  "Accent:     \(.colors.accent)",
  "Background: \(.colors.background)",
  "Heading:    \(.typography.fontFamilies.heading)",
  "Body:       \(.typography.fontFamilies.primary)",
  "Base unit:  \(.spacing.baseUnit)px",
  "Btn fill:   \(.components.buttonPrimary.background)",
  "Btn shadow: \(.components.buttonPrimary.shadow)",
  "Confidence: \(.confidence.overall)"
' .firecrawl/brand.json
```

Generate CSS variables straight from the palette:

```bash
jq -r '.branding.colors | to_entries[] | "  --color-\(.key | ascii_downcase): \(.value);"' \
  .firecrawl/brand.json
```

That lowercases the key as-is, so `textPrimary` becomes `--color-textprimary`. Rename
the multi-word ones by hand, or accept it for a quick pass.

Strip the bulk before passing the object to another tool or model:

```bash
jq '.branding | del(.images.logo, .__llm_logo_reasoning, .__llm_button_reasoning, .__llm_metadata)' \
  .firecrawl/brand.json > .firecrawl/brand-clean.json
```

## Competitor sweep

Extract several sites in parallel, then compare.

```bash
mkdir -p .firecrawl
for site in stripe.com linear.app vercel.com; do
  name="${site%%.*}"
  firecrawl scrape "https://$site" --format branding --pretty \
    -o ".firecrawl/brand-$name.json" &
done
wait
```

Build the comparison table:

```bash
for f in .firecrawl/brand-*.json; do
  jq -r --arg f "$(basename "$f" .json | sed 's/^brand-//')" '
    .branding |
    "| \($f) | \(.colors.primary) | \(.colors.accent) | \(.typography.fontFamilies.heading) | \(.spacing.baseUnit)px | \(.components.buttonPrimary.borderRadius) | \(.confidence.overall) |"
  ' "$f"
done
```

Which yields:

| Site | Primary | Accent | Heading font | Base unit | Btn radius | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| stripe | `#061B31` | `#533AFD` | SF Pro Display | 8px | 4px | 0.93 |

When presenting a sweep, lead with the pattern rather than the rows: where the category
converges (everyone on 8px and a near-black primary), and where the target stands apart.
That comparison is the actual insight; the table is just evidence.

## Handing off to a design system generator

The cleaned branding object is a good input for a design-system or brand-kit generator.
Two rules when you do this:

1. **Pass the cleaned object, not the raw file.** The inline logo data URI will blow up
   a context window on its own.
2. **Pass the corrections with it.** If you overrode `textPrimary` or `fontSizes.body`
   after a visual check, state that in the handoff so the downstream tool does not
   reintroduce the bad value.

## Rules for presenting extracted brands

- Give hex values as text, never only as a color swatch. People need to copy them.
- Name what you verified and what you did not. "Palette and buttons confirmed against a
  screenshot, body text size not checked" is a useful sentence.
- Never present `personality` as fact. It is an LLM read on the brand, useful as a
  prompt for voice work.
- Extracting a public site's computed styles for analysis, comparison, or inspiration is
  ordinary practice. Reproducing a competitor's logo, wordmark, or licensed typeface in
  your own product is a different matter, and worth saying out loud when a request drifts
  from "match this style" toward "copy this brand".
