# Use case: carousels

Multi-slide swipeable posts (LinkedIn, Instagram). 1080x1350 (4:5) portrait slides, 3-10 per carousel, exported as PDF from the canvas. The carousel must **make its point on its own** - assume the caption is one line; the slides carry the whole argument.

## Starter templates to offer (pick 2-4 by taste)

Ask which of these fit how the user shows up online (AskUserQuestion, one line each):

- **Image-first** - a strong visual field per slide, short copy over or beside it. Use when the brand has real photography or an image model in the loop. Breaks when the image fights the headline for attention - keep copy short and give it a clear zone.
- **Tweet-style** - looks like a post screenshot: avatar, name, handle, then the claim. Ask whose photo anchors it (the user's, a teammate's, a stylized avatar). Breaks without a real human photo - a stock face reads as fake instantly.
- **No-human adaptive** - pure design-system: tokens, type, color blocking. The safest default when no photography exists; adapts to any brand automatically. Breaks only when every slide looks identical - vary the block composition per slide.
- **Street-style** - candid photographic backdrops with bold overlaid type; energy over polish. Use for opinion-led, personality-forward content. Breaks when type loses contrast against a busy photo - always add a scrim or solid type band.
- **Graphic-led** - each slide is a small diagram, chart, or framework drawing; the visual teaches. Use for methods and systems. Breaks past one concept per slide - a two-diagram slide is two slides.
- **Minimalistic** - one line per slide, huge type, maximum white space; lands hardest with the fewest slides. Breaks the moment copy runs long - if a line will not fit at full size, this is the wrong template for that content.

Whatever the style, build each slide as an HTML template driven by the design system's tokens: background, ink, muted, accent, one highlight tint, display and body font stacks. Templates use tokens only - never a hard-coded brand value. If the brand has a logo file, place it in the footer in HTML - never ask an image model to draw a logo.

## Slide count (3-10)

Pick the count from the content, not from habit. Typical is 5-8; **fewer lands harder**.

| Count | Fits |
|---|---|
| 3-4 | One sharp claim with one proof: hook, one substance slide, CTA |
| 5-6 | A method with 2-3 steps, or a claim with two proofs |
| 7-8 | A full framework, list, or before/after walkthrough |
| 9-10 | Only when the source genuinely has that many distinct, useful beats |

If you are cutting material to hit a count, you chose the right count. If you are stretching, go smaller - padding kills completion rate.

## The copy arc (do not make every slide a dramatic header)

1. **Hook (slides 1 to ~3)** - big-header, high-impact. Cover, problem, first turn toward the solution. One large headline, one accent highlight, a short body line. The cover sells the swipe: it must promise a specific payoff, not a topic.
2. **Substance (middle slides)** - text-heavier. A smaller header plus 2-4 short bullets, numbered steps, or a simple labeled comparison (before/after, two columns). **One idea per slide.** This is what makes the carousel worth saving.
3. **CTA (last slide)** - one the content earns. Never a CTA that leans on context the slides never gave.

**Self-contained rule:** if the source only teases ("watch my video"), reconstruct the real substance into the middle slides. The slides must actually teach or prove the point.

## Slot budgets

| Slot | Budget |
|---|---|
| Eyebrow | 2-5 words, uppercase, letter-spaced |
| Headline | 4-9 words (hook slides), up to ~12 (substance slides) |
| Highlight | 1-3 consecutive words inside the headline; **exactly one per headline** - the punchline, never a connector |
| Body (hook slides) | 1-2 fragment lines, ~10 words total |
| Bullets (substance slides) | 2-4 bullets, 3-7 words each |
| CTA line | One imperative sentence |

Budgets exist because slides are read at phone size in under two seconds each. When copy fights the budget, **cut the copy, not the type size**.

## Swipe cues and voice

- A swipe cue (small arrow or "swipe" marker) on every slide except the last. Page indicator in `03 / 07` style.
- If the design system defines a voice file, its rules win - read it before writing a word. Default when it defines none: second person, direct, practitioner tone; short punches; specific verbs, real nouns, real numbers; no buzzwords, no hedges; periods and colons over em dashes.

## CTA framings to draw from

- Follow: "Follow for the next one."
- Watch: "Watch the full breakdown."
- Save: "Save this before you need it."
- Get: "Comment '{keyword}' for the template."

Pick the one the content earns. A carousel that taught a method earns "watch the full breakdown" or "grab the template" over a generic follow.

## QA read-back pass (mandatory)

Render each slide and read it back before showing the user:

- All copy present, spelled exactly as written, nothing clipped or overflowing.
- Exactly one highlighted phrase per headline.
- Page indicator correct, swipe cue on every slide except the last.
- Logo renders crisply - a broken image icon means a wrong relative path.
- Any generated image: verify every word on it, because image models misspell.

Fix and re-render any failing slide before the canvas round.

## /design delivery

**Variations gate (mandatory):** 2-3 structurally distinct directions, each shown as the hook slide plus one substance slide. Distinct in composition, hierarchy, footer treatment, highlight style - not shade. Label each with its case and tradeoff, say which you would pick. The user picks or mixes; do not proceed on silence.

**Final delivery:** one artboard per slide, in order, at 1080x1350, on a /design canvas. The user edits slides there and **exports the PDF from the canvas** (the format LinkedIn and schedulers accept). Do not assemble a PDF yourself.

**Live artboards only.** Every slide on the canvas is live HTML/CSS - headlines, bullets, footer, page indicator all real editable text styled with brand tokens. Never place flattened PNG slides on the canvas; a PNG carousel cannot be edited and defeats the gate. For image-first and street-style, the photo or generated image goes in as an image layer inside the HTML artboard, with all type kept in HTML on top.

## References and self-improvement

Reference sources for carousels (creator swipe files, slide-count patterns, hook studies) are in `../sources.md` - show the user 3-5 at Step 4.

**This file improves itself.** When the user gives layout-changing feedback, a new reference, or a hard rule ("never X") about carousels, fold it into this file - or the generated skill's own files - in the same session, then say what changed.
