# Email client constraints - the survival ruleset

Email HTML is roughly 2003-era web development with a few modern islands. The reason: every client runs its own rendering engine, and the worst one (Outlook on Windows, which renders with Microsoft Word) sets the floor. Design for the floor, enhance for the ceiling.

## Contents

1. [The rendering landscape](#the-rendering-landscape)
2. [Layout: tables only](#layout-tables-only)
3. [CSS: inline is truth](#css-inline-is-truth)
4. [Fonts](#fonts)
5. [Images](#images)
6. [Bulletproof buttons (VML)](#bulletproof-buttons-vml)
7. [Backgrounds, gradients, and glass fallbacks](#backgrounds-gradients-and-glass-fallbacks)
8. [Dark mode](#dark-mode)
9. [Gmail specifics: clipping and stripping](#gmail-specifics-clipping-and-stripping)
10. [Outlook specifics: mso conditionals](#outlook-specifics-mso-conditionals)
11. [Mobile](#mobile)
12. [Plain-text alternative](#plain-text-alternative)
13. [Pre-delivery checklist detail](#pre-delivery-checklist-detail)

---

## The rendering landscape

| Client | Engine | Fidelity | What it punishes |
|---|---|---|---|
| Apple Mail / iOS Mail | WebKit | High - most modern CSS works | Little; this is the ceiling |
| Gmail (web + apps) | Custom sanitizer | Medium | Head styles beyond basics, >102KB emails, unsupported selectors |
| Outlook on Windows (classic desktop) | MS Word | Low - the floor | Divs for layout, border-radius, background images on divs, max-width, padding on some elements |
| Outlook.com / new Outlook / Outlook Mac | Web engine | Medium-high | Less than classic; still test VML paths |
| Yahoo / AOL | Custom | Medium | Some media-query quirks, class name mangling |
| Samsung Mail, misc Android | Varies | Medium | Assume Gmail-app-level support |

Rule of thumb: if a technique needs to work everywhere, it must survive Word's renderer. If it only needs to *enhance*, gate it so Outlook never sees it.

## Layout: tables only

- Structure everything with `<table>`, `<tr>`, `<td>`. Add `role="presentation"` to every layout table so screen readers skip the table semantics.
- Set `border="0" cellpadding="0" cellspacing="0"` on every table. Control spacing with `padding` on `<td>` only - margins are unreliable, and padding on `<div>`/`<p>` is ignored in places.
- Outer wrapper: a 100%-width table with the page background color, containing a centered inner table of fixed width **600px** (up to 640px is acceptable). Outlook ignores `max-width`, so the fixed width must live on the table itself, wrapped in an mso conditional or set via `width="600"` attribute plus `style="width:600px;max-width:100%"`.
- One column is the default. Multi-column rows must be built as side-by-side `<td>`s (desktop) that stack via the mobile pattern below - or better, avoid multi-column below the hero entirely.
- Spacing rhythm: use a consistent spacer scale (e.g. 8 / 16 / 24 / 32 / 48px) implemented as `<td>` padding. Empty spacer rows with explicit `height` and `line-height` also work and are more Outlook-stable for vertical gaps.

## CSS: inline is truth

- Every visual property that matters goes in the element's `style=""` attribute. Assume the `<head>` `<style>` block may be removed entirely (some clients and some forwarding paths strip it).
- The `<style>` block is only for things that *cannot* be inlined: `@media` queries (mobile + dark mode), `:hover` niceties, and client-targeting hacks. Everything in it must be a progressive enhancement - the email must look correct with the block deleted.
- Banned or unreliable properties for the baseline layer: `position`, `float` for layout, `display:flex/grid`, `backdrop-filter`, `box-shadow` (fine as enhancement, absent in Outlook), `border-radius` (renders square in classic Outlook - acceptable degradation, but never let content depend on the rounding), CSS variables, `transform`, animations for critical content.
- Shorthand pitfalls: write `background-color` explicitly rather than relying on `background` shorthand parsing; some sanitizers drop the shorthand.

## Fonts

- No external font loading in the baseline: no `@font-face` from CDNs, no `@import`. (Exception: `@font-face` inside the `<style>` block is fine as pure enhancement - Apple Mail honors it, everyone else falls to the stack. Only self-evident enhancement, never layout-affecting.)
- Every text element carries a full web-safe stack inline. Map the brand font to the closest stack:
  - Geometric/grotesque sans -> `Helvetica Neue, Helvetica, Arial, sans-serif`
  - Humanist sans -> `'Segoe UI', Tahoma, Verdana, sans-serif`
  - Serif -> `Georgia, 'Times New Roman', serif`
  - Mono accents -> `'Courier New', Courier, monospace`
- Pick the fallback for *width similarity* first (line-wrap points shift otherwise), weight second.
- Minimums: 14px body (16px preferred), 22px+ headings, `line-height` written in px (unitless line-height misbehaves in Outlook).

## Images

- Always set `width` (HTML attribute AND inline style), `alt`, and `style="display:block"` (kills mystery gaps under images).
- Alt text policy: decorative images get `alt=""`; meaningful images get alt text that carries the message, styled via inline `color`/`font-size` on the `<img>` so blocked-image state still reads as designed. Many clients block images by default - the email must make sense with zero images loaded.
- Retina: export at 2x, set the HTML width to the display size.
- Formats: PNG/JPG everywhere; SVG is not safe (Gmail and Outlook strip it); animated GIF works broadly (classic Outlook shows frame 1 - make frame 1 complete).
- Never build an email that is one giant image. It fails image-blocking, accessibility, dark mode, and spam filtering all at once.
- Host images on HTTPS with stable URLs; no data URIs (Gmail strips them).

## Bulletproof buttons (VML)

The button must be clickable across the whole visual area and render in Outlook. The standard pattern - a VML roundrect for Outlook wrapped in conditionals, with an inline-styled `<a>` for everyone else:

```html
<!--[if mso]>
<v:roundrect xmlns:v="urn:schemas-microsoft-com:vml"
  xmlns:w="urn:schemas-microsoft-com:office:word"
  href="https://example.com/cta"
  style="height:48px;v-text-anchor:middle;width:220px;" arcsize="17%"
  strokecolor="#1A56DB" fillcolor="#1A56DB">
  <w:anchorlock/>
  <center style="color:#FFFFFF;font-family:Helvetica,Arial,sans-serif;font-size:16px;font-weight:bold;">
    Get started
  </center>
</v:roundrect>
<![endif]-->
<!--[if !mso]><!-->
<a href="https://example.com/cta"
   style="background-color:#1A56DB;border-radius:8px;color:#FFFFFF;display:inline-block;
          font-family:Helvetica,Arial,sans-serif;font-size:16px;font-weight:bold;
          line-height:48px;text-align:center;text-decoration:none;width:220px;
          -webkit-text-size-adjust:none;mso-hide:all;">Get started</a>
<!--<![endif]-->
```

Swap colors, radius (`arcsize` is radius as % of height), width, and label per design. If the design button uses a gradient, the VML `fillcolor` and the `<a>` `background-color` both use the gradient's midpoint solid; the gradient itself is applied as an enhancement `background-image` on the `<a>` only.

## Backgrounds, gradients, and glass fallbacks

Layering rule: **solid color first, effect second.** Every element that carries a gradient, image, or glass effect declares in order:

```html
style="background-color:#EAF0FB;               /* fallback everyone gets */
       background-image:linear-gradient(...);  /* enhancement */"
```

- The fallback solid must be chosen deliberately - typically the visual average of the effect - and text contrast must pass against the *fallback*, not just the effect.
- Full-width background images behind content need VML fills for Outlook (`v:rect` + `v:fill`); use sparingly, and only when the design genuinely needs them. A solid or tinted band is usually the better trade.
- Glass/translucency degradations are specified in `liquid-glass.md` - in email-safe terms, every glass card becomes a solid tinted card with a 1px border. `rgba()` backgrounds are OK for most modern clients but the tint must also be pre-flattened into the fallback hex.

## Dark mode

Three behaviors exist, and one email must survive all three:

1. **No change** (many clients): email renders as designed.
2. **Honors your overrides** (Apple Mail, some Outlook): `@media (prefers-color-scheme: dark)` styles apply.
3. **Forced inversion** (Gmail apps, Outlook apps in some modes): the client recolors your email itself - light backgrounds darkened, dark text lightened - ignoring your media query.

Required plumbing in `<head>`:

```html
<meta name="color-scheme" content="light dark">
<meta name="supported-color-schemes" content="light dark">
<style>
  :root { color-scheme: light dark; supported-color-schemes: light dark; }
  @media (prefers-color-scheme: dark) {
    .dm-bg   { background-color:#111418 !important; }
    .dm-card { background-color:#1C2128 !important; border-color:#2D333B !important; }
    .dm-text { color:#E6E8EB !important; }
    .dm-muted{ color:#9AA4AF !important; }
  }
</style>
```

Defensive rules against forced inversion:

- Never use pure white (#FFFFFF) as the main canvas or pure black text (#000000); off-white (#FAFAF8) and near-black (#1A1A1A) invert less violently and read better anyway.
- Logos: use a version with padding baked in on a transparent background that works on BOTH light and dark, or put the logo on a `<td>` with an explicit background color that you also override in dark mode. A dark logo on transparent background disappears when the canvas is force-darkened - this is the single most common dark-mode failure.
- Test the brand accent color against both the light and dark surfaces; adjust the dark-mode variant if contrast drops below 4.5:1.
- Meaningful color-coded content (success green, error red) needs dark-mode variants too.

## Gmail specifics: clipping and stripping

- **102KB clipping**: Gmail truncates messages whose HTML exceeds ~102KB, replacing the rest with a "[Message clipped]" link - which hides your footer and unsubscribe link (a compliance problem, not just cosmetic). Budget: keep the final HTML under ~90KB to leave room for ESP tracking rewrites, which inflate every URL. Minify before sending if close. Images do not count toward this limit; only the HTML does.
- Gmail keeps `<head>` styles but only standard selectors: class and element selectors are fine; attribute selectors, `:not()`, and complex combinators may cause it to drop the *entire* `<style>` block. One invalid rule can nuke all your media queries - lint the block.
- Gmail rewrites/strips `id` attributes and strips `<style>` in some forwarded/replied contexts - another reason inline styles are the source of truth.
- No `data:` URIs, no `<svg>`, no `<form>` (varies), no `position`.

## Outlook specifics: mso conditionals

Classic Outlook on Windows renders with Word. Target or hide from it with conditional comments:

```html
<!--[if mso]>   ...Outlook-only (VML, ghost tables, explicit widths)... <![endif]-->
<!--[if !mso]><!-->  ...everyone except Outlook...  <!--<![endif]-->
```

- **Ghost tables**: when a section uses divs for fluid behavior, wrap an Outlook-only fixed-width table around it so Word gets rigid geometry.
- No `max-width`, no `border-radius`, no `background-image` on table cells (needs VML), margin support is patchy, `padding` on `<p>`/`<div>` ignored - use `<td>` padding.
- Line-height: add `mso-line-height-rule:exactly;` before `line-height` on text elements.
- Spacer `<td>`s need `font-size` and `line-height` set to their height, plus `&nbsp;` or they may collapse.
- Word may widen tables containing long unbroken strings (URLs) - break long links or wrap them.
- DPI scaling on Windows: define widths in px on tables and set `<o:PixelsPerInch>96</o:PixelsPerInch>` in the mso head block (present in the base template).

## Mobile

- Media query pattern (put classes, not element selectors, in the query - Gmail-safe):

```html
@media only screen and (max-width:620px) {
  .container { width:100% !important; }
  .stack     { display:block !important; width:100% !important; }
  .px-mobile { padding-left:20px !important; padding-right:20px !important; }
  .hide-mobile { display:none !important; }
}
```

- Side-by-side `<td>`s that must stack: give each `class="stack"`. Where media queries are unsupported, the fixed 600px still scales down acceptably because... it doesn't - so keep critical text >= 14px and the single-column default.
- Tap targets: buttons >= 44px tall, full-width buttons on mobile are the safest CTA pattern.
- Test at 320px (small Android), 375-393px (iPhone), and 600px+.

## Plain-text alternative

Always produce one alongside the HTML (ESPs send it as the `text/plain` MIME part; some watches/voice assistants/preview panes use it, and it improves spam scoring).

Format: brand name and one-line premise up top, then the message in short paragraphs, links on their own lines spelled out in full, clear section dividers (a line of dashes), unsubscribe and address info at the bottom. No markdown syntax, no leftover merge tags.

## Pre-delivery checklist detail

Run each check and report pass/fail with the fix applied:

1. **Outlook**: strip the `<style>` block mentally (or actually, in a copy) - does the inline-only version hold? VML present for every button and any background image? No layout-critical border-radius?
2. **Gmail size**: `wc -c` the final HTML. Under ~90KB target, hard fail over 100KB.
3. **Gmail styles**: `<style>` block contains only class/element selectors and media queries; no CSS the sanitizer chokes on.
4. **Apple Mail / enhancement layer**: gradients, radius, shadows, glass tints render; the email actually looks premium at the ceiling, not just safe at the floor.
5. **Dark mode**: meta tags present; `.dm-*` overrides cover canvas, cards, text, borders; logo survives both schemes; no pure #FFFFFF canvas or #000000 text.
6. **Mobile**: single column at 320px, tap targets, font minimums, `.stack` classes on all multi-column rows.
7. **Images off**: read the email with images blocked - is the message intact from alt text + live text alone?
8. **Plain text**: exists, current, links resolve.
9. **Accessibility**: `lang` on `<html>`, `role="presentation"` on layout tables, contrast >= 4.5:1 against fallback backgrounds, heading hierarchy sensible.
10. **Links**: every href absolute HTTPS, no placeholder `#`, UTM/merge tags per the sending platform's syntax.
