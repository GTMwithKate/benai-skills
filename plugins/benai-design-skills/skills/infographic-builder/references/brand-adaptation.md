# Adapting the kit to a brand

The templates carry no brand of their own. Every colour, font and identity string is a
token, and `scripts/build.py` resolves them from a single `brand.json`. Adapting the kit
to a user therefore means one thing: generating their `brand.json` and saving it where
future runs find it, at `design-system/infographic-brand.json` in their project.

Do this once, on the first run, before building anything. After that every build picks it
up automatically.

## Where the values come from

In order of preference:

1. **The user's `design-system/` folder**, the output of the design-system-creator skill
   (or firecrawl-brand-extractor). Read its tokens file: colours, type stacks, radii,
   shadows. This is the authoritative source.
2. **The user, directly in chat**, when no design system exists. Ask for brand colours,
   fonts, domain, and the name and handle that should appear on quote cards.

**Never guess.** No design system and no answer from the user means you stop and ask. A
wrong hex code on a published graphic is worse than a question. Do not fill gaps with
colours that "look right" for their industry, and do not build with the bundled
`brand.default.json` placeholder for anything the user will actually publish.

## The brand.json schema

```json
{
  "site": "example.com",
  "author": { "name": "Jane Doe", "handle": "@janedoe", "avatar": "avatar.png" },
  "brandmark": { "light": "mark-dark-on-light.png", "dark": "mark-light-on-dark.png" },
  "fonts": {
    "link": "https://fonts.googleapis.com/css2?family=...&display=swap",
    "display": "'Font Name', 'Helvetica Neue', Arial, sans-serif",
    "body": "'Font Name', 'Helvetica Neue', Arial, sans-serif",
    "mono": "'Mono Name', 'SF Mono', Consolas, monospace"
  },
  "light": {
    "ground": "...", "ink": "...", "muted": "...", "hair": "...",
    "card": "...", "panel": "...", "panel2": "...",
    "accent": "...", "accent2": "...", "onaccent": "...",
    "success": "...", "danger": "...", "shadow": "..."
  },
  "dark": { "...same keys..." }
}
```

`build.py` derives everything else (gradients, border weights, the numeral style, dark
mode's softer hairlines) from these primitives, so the brand file only has to answer
questions a design system can actually answer.

## Mapping a design system's tokens

A design system tokens file, whether CSS custom properties or JSON, usually names roles
rather than these exact keys. Map by role:

| brand.json key | Typical design-system token | If the system does not define it |
|---|---|---|
| `light.ground` | background / surface / paper / bone | Ask |
| `light.ink` | text / foreground / ink | Ask |
| `light.muted` | text-secondary / muted | Mix ink toward ground by ~35% |
| `light.hair` | border / divider | Mix ink toward ground by ~80% |
| `light.card` | surface / card | Same as ground |
| `light.panel` `panel2` | surface-alt / secondary background | Tint ground slightly toward the accent |
| `light.accent` | a light tint of the brand accent | Accent at ~15% over the ground |
| `light.accent2` | the brand accent itself (link / primary button colour) | Ask |
| `light.onaccent` | text-on-accent / button label | Ink, if the accent fill is light |
| `light.success` `danger` | semantic success / error tints | Soft neutral green and red tints |
| `light.shadow` | shadow colour | Ink. A system that declares `shadow: none` still needs one here, because the offset shadow is structural in QuoteBoxed; use ink and mention it |
| `fonts.display` | heading / display family with its fallback stack | Ask |
| `fonts.body` | body family | Display family |
| `fonts.mono` | code / mono family | `'SF Mono', Consolas, monospace` |

Example of the shape you will meet: a tokens file defining `--brand-ink: <hex>` for text,
`--brand-bone: <hex>` for the page ground, one accent hue in two or three interaction
weights, and display plus body font stacks. That maps directly: ink to `ink`, bone to
`ground`, the lightest accent weight to `accent`, the strongest to `accent2`, the declared
font stacks (with their fallbacks) into `fonts`.

Derived values are fine and normal; write them down as derived in your handover so the
user can correct them. What is not fine is inventing the primitives themselves.

## Dark mode when the brand only defines light

Most extracted design systems are light-only. Derive dark honestly:

- `dark.ground`: a near-black tinted toward the light ground's hue. Never pure `#000`.
- `dark.ink`: the light ground colour usually works as dark ink.
- `dark.muted`, `dark.hair`: mix dark ink toward dark ground (~40% and ~82%).
- `dark.card` / `panel` / `panel2`: ground lifted a few steps.
- `dark.accent`: keep the light accent fill. `dark.accent2`: lighten the brand accent
  until it reads on the dark ground.
- Tell the user dark mode was derived, and put both modes on the canvas so they can react
  to it.

## Fonts

`@FONTLINK@` must be a single Google Fonts stylesheet URL covering every family and weight
the templates use (display 500 and 700, body 400 and 600, mono 400). If the brand font is
not on Google Fonts (proprietary faces like a company's own type), pick the closest Google
Fonts match for the artboards, keep the brand's own declared fallbacks in the stacks, and
say so at handover. Every stack needs real fallbacks: PNG export cannot embed webfonts,
which is exactly why `check.py` measures both.

## Identity

- `author`: the person whose face and handle sit on quote cards. Copy their avatar image
  into the folder next to brand.json and reference it by filename.
- `brandmark`: a small square-ish mark, one version per mode (typically a dark-on-light
  and a light-on-dark file). Brands without a usable small mark leave both empty, and
  `build.py` drops the element cleanly instead of rendering a broken image.
- `site`: the bare domain for the quiet attribution line on teaching formats.

## Verify before first use

After writing the brand.json, build the whole kit once and look at it:

```bash
python3 scripts/build.py --src assets/kit --out /tmp/brand-check --brand <brand.json>
python3 scripts/check.py /tmp/brand-check
python3 scripts/render_png.py /tmp/brand-check CheatSheetLight --out /tmp/brand-check/l.png --scale 1
python3 scripts/render_png.py /tmp/brand-check CheatSheetDark --out /tmp/brand-check/d.png --scale 1
```

Look at both PNGs. The two failures a fresh brand causes are an accent too light to carry
emphasis, and muted text that vanishes on the dark ground. Fix the brand.json, not the
templates. Then save it to `design-system/infographic-brand.json` and tell the user it is
their infographic brand from now on.
