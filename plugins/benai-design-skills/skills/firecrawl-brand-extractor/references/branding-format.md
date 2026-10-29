# The `branding` Format: Field Reference

What `--format branding` actually returns, documented from real runs rather than from
the marketing page. Field presence varies by site: a minimal site returns fewer fonts
and no `borderColor`, a rich site returns more. Treat every field as optional.

## Command

```bash
firecrawl scrape "<url>" --format branding --pretty -o .firecrawl/brand.json
```

The payload is `{ "branding": {...}, "metadata": {...} }`. Everything below lives under
`.branding`. The sibling `.metadata` is the standard scrape metadata: `title`,
`description`, `ogTitle`, `ogImage`, `favicon`, `statusCode`, `creditsUsed`, and so on.

## Top-level keys

| Key | Type | What it holds |
| --- | --- | --- |
| `colorScheme` | string | `light` or `dark` |
| `colors` | object | The palette by role |
| `fonts` | array | Font families with an inferred role |
| `typography` | object | Font families, stacks, and sizes |
| `spacing` | object | Base spacing unit and border radius |
| `components` | object | Primary and secondary button specs |
| `images` | object | Logo, favicon, OG image, logo link and alt text |
| `personality` | object | LLM read on tone, energy, audience |
| `designSystem` | object | Framework and component library guess |
| `confidence` | object | Scores for buttons, colors, overall |
| `__llm_logo_reasoning` | object | Why that logo was picked |
| `__llm_button_reasoning` | object | Why those buttons were picked |
| `__llm_metadata` | object | Whether the LLM passes ran and succeeded |

Strip the `__llm_*` keys before handing anything to a user. They are diagnostics.

## `colors`

```json
{
  "primary": "#061B31",
  "secondary": "#FFE0D1",
  "accent": "#533AFD",
  "background": "#FFFFFF",
  "textPrimary": "#533AFD",
  "link": "#533AFD"
}
```

Roles are inferred, not declared by the site, so the labels are the weakest part of the
payload while the hex values themselves are reliable.

Two failure modes worth knowing:

- **`textPrimary` picking up a brand color.** The example above is a real Stripe run.
  `#533AFD` is Stripe's accent purple, not its body text color, which is a near-black.
  When `textPrimary` matches `accent` or `link`, or is saturated rather than
  near-black or near-white, treat it as wrong and read the real value off a screenshot.
- **`primary` and `background` swapping on light sites.** On sites with a near-white
  background and a dark headline color, which of the two lands in `primary` is not
  guaranteed. Check `colorScheme` and sanity-check against contrast.

Some sites also return `textSecondary` or `border`. Do not rely on them being present.

## `fonts` and `typography`

```json
"fonts": [
  { "family": "Sohne", "role": "body" },
  { "family": "SF Pro Display", "role": "heading" }
],
"typography": {
  "fontFamilies": { "primary": "Sohne", "heading": "SF Pro Display" },
  "fontStacks": {
    "heading": ["Sohne", "SF Pro Display", "sans-serif"],
    "body": ["Sohne", "SF Pro Display", "sans-serif"],
    "paragraph": ["Sohne", "SF Pro Display", "sans-serif"]
  },
  "fontSizes": { "h1": "48px", "h2": "32px", "body": "32px" }
}
```

`role` can come back as `unknown` when a site uses a single family throughout, which is
correct behavior rather than a failure.

`fontSizes.body` is the least reliable field in the whole payload. In the run above it
reported 32px because it sampled an oversized hero paragraph; Stripe's real body copy is
much smaller. Anything at or above 24px deserves a visual check.

`fontStacks` sometimes repeats the same stack for heading and body even when the site
genuinely uses two families. Prefer `fontFamilies` and the `fonts` array when the two
disagree.

Font families are reported as names, not as webfont files. To actually use them, check
availability on Google Fonts or Adobe Fonts, or find the `@font-face` source by scraping
the stylesheet separately.

## `spacing`

```json
{ "baseUnit": 8, "borderRadius": "0px" }
```

`baseUnit` is a number in pixels and is the most useful single value for rebuilding a
layout system: 4 and 8 are the common answers. `borderRadius` here is the page-level
default, which is frequently `0px` even on sites whose buttons are rounded. For the
radius that actually matters, read `components`.

## `components`

```json
{
  "buttonPrimary": {
    "background": "#533AFD",
    "textColor": "#FFFFFF",
    "borderRadius": "4px",
    "borderRadiusCorners": {
      "topLeft": "4px", "topRight": "4px",
      "bottomRight": "4px", "bottomLeft": "4px"
    },
    "shadow": "none"
  },
  "buttonSecondary": {
    "background": "#FFFFFF",
    "textColor": "#533AFD",
    "borderColor": "#B9B9F9",
    "borderRadius": "4px",
    "borderRadiusCorners": { "...": "..." },
    "shadow": "none"
  }
}
```

This is the highest-signal part of the payload. Button fills are computed styles read
off real elements rather than inferred, so `buttonPrimary.background` is usually a more
trustworthy read on the true brand color than `colors.primary`.

`shadow` is a raw CSS shadow string, which makes distinctive styles survive the trip.
A neo-brutalist site returns something like `rgb(0, 0, 0) 2px 2px 0px 0px`, which is
exactly what you need to reproduce the look.

`borderColor` appears only when the element has a visible border. `borderRadiusCorners`
matters only for asymmetric shapes; otherwise it repeats `borderRadius` four times.

## `images`

```json
{
  "logo": "data:image/svg+xml;utf8,%3Csvg%20xmlns...",
  "favicon": "https://.../favicon.svg",
  "ogImage": "https://.../Stripe.jpg?q=80",
  "logoHref": "/",
  "logoAlt": "Stripe logo"
}
```

`logo` is either a hosted URL or, often, a `data:` URI holding the entire inline SVG.
The data URI form can run to tens of thousands of characters, so never print it into a
conversation. It works directly in `<img src="...">` or CSS `url(...)`.

To save a data-URI logo to a file:

```bash
jq -r '.branding.images.logo' .firecrawl/brand.json \
  | sed 's/^data:image\/svg+xml;utf8,//' \
  | python3 -c 'import sys,urllib.parse; sys.stdout.write(urllib.parse.unquote(sys.stdin.read()))' \
  > logo.svg
```

For a base64-encoded data URI instead of a `utf8,` one, strip the prefix and pipe
through `base64 --decode`.

`favicon` and `ogImage` are ordinary URLs and are the easy option when a raster asset
will do. `logoAlt` is a decent source for the official brand name spelling.

## `personality`, `designSystem`, `confidence`

```json
"personality": {
  "tone": "professional",
  "energy": "medium",
  "targetAudience": "businesses and developers"
},
"designSystem": { "framework": "custom", "componentLibrary": "" },
"confidence": { "buttons": 0.95, "colors": 0.9, "overall": 0.925 }
```

`personality` is an LLM inference from page content and visual style. It is a reasonable
starting point for voice and positioning work, and should be presented as an inference
rather than as fact.

`designSystem.framework` returns `custom` for most hand-built sites and
`componentLibrary` is frequently empty. Low signal; do not build on it.

`confidence` is the field to read first. `overall` below roughly 0.8 means verify
visually before delivering anything. The sub-scores localize the doubt: low `colors` with
high `buttons` means trust the component specs and re-check the palette.

## A second example: what a clean run looks like

For contrast with Stripe, this is the *shape* of a good extraction from a
neo-brutalist style of site. The values below are illustrative, not from a real run;
always report the values your own extraction actually returns.

```json
{
  "colorScheme": "light",
  "fonts": [{ "family": "<single display font>", "role": "unknown" }],
  "colors": {
    "primary": "<pastel surface>", "secondary": "<pastel surface>",
    "accent": "<pastel accent>",
    "background": "<near-white>", "textPrimary": "<near-black>",
    "link": "<accent>"
  },
  "typography": {
    "fontFamilies": { "primary": "<font>", "heading": "<same font>" },
    "fontSizes": { "h1": "44px", "h2": "28px", "body": "18px" }
  },
  "spacing": { "baseUnit": 4, "borderRadius": "4px" },
  "components": {
    "buttonPrimary": {
      "background": "<accent>", "textColor": "<near-black>",
      "borderColor": "<near-black>",
      "borderRadius": "12px", "shadow": "rgb(0, 0, 0) 2px 2px 0px 0px"
    }
  }
}
```

Note what goes right here that went wrong on Stripe: a single font family correctly
reported with `role: unknown`, a sane 18px body size, a `textPrimary` that is genuinely
near-black, and a hard offset shadow that captures the brutalist style precisely.

## Combining with other formats

```bash
# Brand plus a screenshot to verify against
firecrawl scrape "<url>" --format branding,screenshot --pretty -o .firecrawl/brand.json

# Brand plus page copy, for visual and voice together
firecrawl scrape "<url>" --format branding,markdown --pretty -o .firecrawl/brand.json

# Brand plus every image on the page
firecrawl scrape "<url>" --format branding,images --pretty -o .firecrawl/brand.json
```

Full format list: `markdown`, `html`, `rawHtml`, `links`, `images`, `screenshot`,
`summary`, `changeTracking`, `json`, `attributes`, `branding`. One format returns raw
content; two or more return JSON.

Branding costs 1 credit, the same as a base scrape. Some other formats add a surcharge:
`json` and `--query` cost extra. Check `.metadata.creditsUsed` in any response for the
actual charge.
