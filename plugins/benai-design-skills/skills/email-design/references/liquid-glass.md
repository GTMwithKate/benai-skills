# Liquid glass - the aesthetic, the snippets, and how it degrades

"Liquid glass" is the translucent, frosted-glass card language: soft depth, blurred backdrop, hairline borders that catch light, gentle inner glow. It makes an email feel like a modern product surface instead of a flat flyer. It lives in **Layer A only** (the design preview); Layer B carries its degraded twin. This file gives you the construction recipe, ready snippets, and the exact degradation mapping.

## Anatomy of a glass component

A convincing glass card is five layers, not one blur:

1. **Backdrop** - something worth blurring: a soft gradient mesh, brand-colored blobs, or imagery behind the card. Glass over a flat color just looks gray.
2. **Fill** - translucent tint, usually white or brand-tinted at 8-18% alpha. Lighter alpha = more "liquid," heavier = more "frosted."
3. **Blur** - `backdrop-filter: blur(14-24px)`, optionally `saturate(160%)` to keep the backdrop colors alive through the glass.
4. **Border** - 1px at 20-35% white alpha; on dark backdrops, a top-edge highlight (brighter top border or an inset top glow) sells the "lit edge."
5. **Shadow** - large, soft, low-opacity drop shadow for lift, plus optionally a subtle `inset` white glow at the top.

Restraint rules: one or two glass surfaces per viewport, never nested glass, and body text sits on the most opaque part of the card. Contrast is checked against the *flattened* color, not the pretty one.

## Snippets (Layer A preview)

### CSS custom properties (swap in brand tokens)

```css
:root {
  --glass-fill: rgba(255,255,255,0.12);
  --glass-fill-strong: rgba(255,255,255,0.22);
  --glass-border: rgba(255,255,255,0.28);
  --glass-blur: 18px;
  --glass-radius: 20px;
  --glass-shadow: 0 8px 32px rgba(8,12,24,0.24);
}
```

### Glass card (HTML + CSS)

```html
<div class="glass-card">
  <h3>Early access is open</h3>
  <p>Be first in when the new workspace launches.</p>
</div>

<style>
.glass-card {
  background: var(--glass-fill);
  backdrop-filter: blur(var(--glass-blur)) saturate(160%);
  -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(160%);
  border: 1px solid var(--glass-border);
  border-radius: var(--glass-radius);
  box-shadow: var(--glass-shadow),
              inset 0 1px 0 rgba(255,255,255,0.35); /* lit top edge */
  padding: 28px;
}
</style>
```

### Backdrop worth blurring (gradient blobs)

```css
.email-canvas {
  position: relative;
  background:
    radial-gradient(420px 300px at 15% 0%,  rgba(64,120,255,0.35), transparent 70%),
    radial-gradient(380px 280px at 90% 20%, rgba(180,90,255,0.28), transparent 70%),
    linear-gradient(180deg, #0E1220 0%, #141A2E 100%);
}
```

### Glass button

```css
.glass-btn {
  display: inline-block;
  padding: 14px 28px;
  border-radius: 999px;
  color: #fff;
  background: linear-gradient(180deg, rgba(255,255,255,0.24), rgba(255,255,255,0.10));
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.35);
  box-shadow: 0 4px 16px rgba(8,12,24,0.28), inset 0 1px 0 rgba(255,255,255,0.4);
  text-decoration: none;
  font-weight: 600;
}
```

### React (same card, for a component-based preview)

```jsx
const glass = {
  background: "rgba(255,255,255,0.12)",
  backdropFilter: "blur(18px) saturate(160%)",
  WebkitBackdropFilter: "blur(18px) saturate(160%)",
  border: "1px solid rgba(255,255,255,0.28)",
  borderRadius: 20,
  boxShadow: "0 8px 32px rgba(8,12,24,0.24), inset 0 1px 0 rgba(255,255,255,0.35)",
  padding: 28,
};

export function GlassCard({ children }) {
  return <div style={glass}>{children}</div>;
}
```

### Light-mode glass (over pale backdrops)

```css
.glass-card--light {
  background: rgba(255,255,255,0.55);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(20,30,60,0.10);
  box-shadow: 0 8px 28px rgba(20,30,60,0.10);
}
```

## The degradation map (Layer A -> Layer B)

Email clients do not run `backdrop-filter` (even Apple Mail support is inconsistent), so the email-safe build delivers the *flattened equivalent*. The principle: **pre-composite the glass.** Compute what the glass would look like averaged over its backdrop and bake that into a solid color.

| Layer A effect | Layer B email-safe twin | Notes |
|---|---|---|
| Glass card (`backdrop-filter` + rgba fill) | `<td>` with solid pre-flattened tint, 1px solid border, `border-radius` as enhancement | Flatten: mix the backdrop color with the fill at its alpha. E.g. backdrop `#141A2E` + white @ 12% -> `#2A3040`. Contrast-check text against this hex. |
| Gradient-blob backdrop | Solid `background-color` (the gradient's average) + `background-image: linear-gradient(...)` as enhancement | Outlook gets the solid; WebKit clients get the gradient. Radial blobs usually simplify to one linear gradient. |
| Lit top edge (inset glow) | Drop it, or a 1px lighter top border on the card `<td>` | Cheap and safe. |
| Soft drop shadow | Drop it; optionally `box-shadow` in the enhancement `<style>` block | Never structural. |
| Glass button | Bulletproof VML button (see email-client-constraints.md), solid brand fill, `border-radius` + gradient overlay as enhancement | The pill radius renders square in classic Outlook - acceptable. |
| Blur-revealed imagery behind card | Static image slice exported from the preview, with alt text | Only when the section truly needs it; images-off state must still read. |
| Saturate/backdrop color play | Nothing - bake into the exported palette | |
| `border-radius: 20px` | Keep inline (most clients honor it); Outlook renders square | Square corners must still look intentional - keep borders and padding consistent. |

### Worked example: one card, both layers

Layer A (preview):

```html
<div class="glass-card" style="background:rgba(255,255,255,0.12);backdrop-filter:blur(18px);
     border:1px solid rgba(255,255,255,0.28);border-radius:20px;padding:28px;">
  <h3 style="color:#FFFFFF;">Early access is open</h3>
</div>
```

Layer B (email-safe, backdrop was #141A2E):

```html
<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
  <tr>
    <td class="dm-card" style="background-color:#2A3040;border:1px solid #4A5060;
        border-radius:20px;padding:28px;">
      <h3 style="margin:0;color:#FFFFFF;font-family:Helvetica,Arial,sans-serif;
          font-size:22px;mso-line-height-rule:exactly;line-height:28px;">
        Early access is open
      </h3>
    </td>
  </tr>
</table>
```

Same geometry, same type, same padding - the glass became a solid tinted card. A recipient on Apple Mail with the enhancement styles sees rounded corners and the gradient canvas; a recipient on classic Outlook sees a clean rectangular tinted card. Nobody sees a broken layout.

## Flattening math (quick reference)

Composite `fill` (alpha a) over `backdrop`: `result = fill*a + backdrop*(1-a)` per RGB channel.

White @ 12% over `#141A2E` (20,26,46): R = 255*.12+20*.88 = 48, G = 255*.12+26*.88 = 54, B = 255*.12+46*.88 = 71 -> `#303647` (round per channel; eyeballing to the nearest pleasant hex is fine - it is a design decision, not physics). Do this once per glass surface and record it in the degradation ledger during Layer A.
