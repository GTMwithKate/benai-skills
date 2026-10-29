# Use case: websites and landing pages

Marketing pages: a landing page for an offer, a homepage, a campaign page, a pricing page. The generated skill produces page designs as live artboards first; production code comes after the design is approved on the canvas.

## Page types to offer

Ask which the user usually needs (AskUserQuestion): full landing page (the anatomy below), campaign page (hero, proof, how-it-works, CTA), homepage (broader nav, multiple offers), or a single-section refresh. The answer sets the generated skill's default scope.

## Landing-page anatomy (the default section order)

1. **Nav** - mark, 3-5 links, one CTA. Sticky, quiet.
2. **Hero** - the promise in one assertion headline, one subline naming who it is for, primary CTA, optional product visual. The hero answers "what is this and why should I care" in 3 seconds.
3. **Social proof band** - logos or a one-line stat. Early, small, quiet.
4. **Problem / shift** - the pain in the visitor's words, then the reframe.
5. **How it works** - 3 steps, one line each. More than 3 means the offer is not distilled yet.
6. **Feature or benefit sections** - alternating layout rhythm, each with one screenshot/visual and one assertion headline.
7. **Case study / testimonial** - a real name, a real outcome.
8. **Pricing** (if the page sells directly) - the deal readable in 2 seconds.
9. **Final CTA band** - dark or wash variant, the ask restated.
10. **Footer** - the boring, complete one.

Ask which sections the user's usual page needs; the answer becomes the generated skill's default anatomy.

## Layout and spacing

- Max content width ~1200px, reading measure 65-75 characters, section rhythm from the design system's spacing scale - and only from it. Pick the scale once; every gap on the page is one of its steps.
- **Vary spacing for rhythm.** Identical padding on every section is monotony; generous space around the hero and CTA bands, tighter inside feature grids.
- Cards are the lazy answer. Use one only when it is genuinely the best affordance; nested cards are always wrong. Most content does not need a container at all.
- Never a horizontal scrollbar at any width. That is a bug, not a style.

## Typography discipline

- Two font families maximum, both from the design system. The display face carries the voice; a common utilitarian face as the visual voice reads as a demo page.
- Hierarchy through scale and weight: at least a 1.25x ratio between adjacent steps, and a bold 4-6x ratio between the hero headline and body.
- Body 16-18px, line-height 1.5-1.75, line length capped at 65-75ch.
- Emphasis by weight or color token, never italics-as-decoration, never gradient text.

## Color discipline

- Every color, radius, shadow, and font from tokens - a landing page is where hardcoded values sneak in fastest.
- Pick a color commitment before painting: restrained (tinted neutrals, one accent under ~10% of the surface), committed (one brand color carries 30-60%), or drenched (a hero section IS the color). Say which you picked; do not drift between them per section.
- Never pure black or pure white; tint every neutral toward the brand hue by the design system's neutral ramp.
- **Category-reflex check**: if the palette could be guessed from the industry name alone (finance = navy, health = teal on white), it came from a reflex, not the brand. Re-anchor on the tokens.

## Motion rules

- **Gate first**: does this element earn motion at all? Things seen constantly (nav, hover on every card) get near-imperceptible motion or none. The delight budget lives on things seen once - the hero, a section reveal.
- Entrances use ease-out, never ease-in; built-in easings are weak, use a strong custom curve. Enter from opacity 0 plus a slight translate or scale 0.95-0.97, never scale(0).
- Durations: hovers 100-200ms, reveals 200-400ms, nothing over 500ms without a story reason. Animate transform and opacity only.
- Scroll reveals fire once, stagger grouped items 30-80ms, and never block reading or clicking.
- No parallax, no marquee heroes, no autoplaying motion loops next to body copy.
- Gate hover effects behind `@media (hover: hover) and (pointer: fine)`; respect `prefers-reduced-motion` with gentler fades, not zero.

## Anti-slop bans (rewrite the element, never argue with the ban)

| Banned | Instead |
|---|---|
| Purple-to-pink gradient hero | The brand's own accent, committed |
| Gradient text | One solid color, emphasis by weight or size |
| Colored side-stripe accents on cards | Full hairline borders or a background tint |
| Glassmorphism as a default | Solid surfaces from the token ramp |
| Identical icon+heading+text card grids | Vary structure: one wide, two narrow; a list; a diagram |
| Emoji as icons | One icon library, consistent stroke weight |
| Stock trope photos (handshakes, laptops with charts) | Real product screenshots, then illustration, in that order |
| Fabricated stats, fake logo walls, dummy testimonials | Honest placeholders that say real material is needed |
| Restated headings and filler copy | Every word earns its place |

Real product screenshots beat illustrations; illustrations beat stock photos. The one exception to any ban: the brand's own design system genuinely uses the pattern - then it is a signature, not slop.

## Accessibility and responsive floors

- Text contrast at least 4.5:1 against its ground - check the muted text tokens especially, they fail most often.
- Visible focus rings on every interactive element; tab order matches visual order; labels tied to form fields; alt text on meaningful images.
- Touch targets at least 44x44px; mobile body text at least 16px.
- Fluid type via `clamp()`; content reflows at every width with no horizontal scroll; space reserved for late-loading content so nothing jumps.

## Where to look (from ../sources.md)

Curated galleries for direction, real-site archives for section rhythm, component libraries for copyable blocks restyled with the design system's tokens rather than used as-is. One icon library per site, consistent stroke weight. Full annotated list in `../sources.md`; a user-supplied reference outranks all of it.

## The audit before delivery (every page, every round)

Run this as a checklist and report pass/fail in one short block before showing the page:

1. Every color, font, radius, and shadow traces to a token - no rogue values.
2. No banned pattern from the table above.
3. Contrast, focus, touch-target, and reduced-motion checks pass.
4. No horizontal scroll at mobile, tablet, and 1440px widths.
5. Hero answers what-and-for-whom in 3 seconds; headlines are assertions.
6. Screenshot the page and read the screenshot as a visitor - most faults are visible in the render and invisible in the source.

## /design delivery

Variations gate: 2-3 structurally distinct page directions shown as hero-plus-two-sections artboards - e.g. product-shot hero vs type-led editorial hero vs dark technical - with an honest case and tradeoff each. Final delivery: the full page as one tall artboard (or one artboard per section for long pages) on a /design canvas, where the user edits copy and layout directly and exports. Production code (HTML/React) is generated from the approved canvas state afterward.

**Live artboards only.** Every artboard is live HTML/CSS - nav links, headlines, body copy, buttons all real editable text on brand tokens. Never place flattened PNG mockups on the canvas. Screenshots and imagery go in as image layers inside the HTML artboard, type kept in HTML on top.

## Self-improvement

Every correction the user makes - a section they always delete, a motion they call too much, a layout they keep picking - gets written into this file (or the generated skill's copy) in the same session, so the next page starts from what they taught you.
