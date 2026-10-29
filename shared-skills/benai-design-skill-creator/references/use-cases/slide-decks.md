# Use case: slide decks

Presentations: pitch decks, teaching decks, internal reviews, webinar slides. 16:9 artboards, exported as PDF from the canvas. The generated skill produces **animated HTML decks**: the canvas is where the user edits and exports, and the deck also lives as one self-contained HTML file with real motion for presenting in a browser.

## Presentation structure

Ask what the deck usually does (AskUserQuestion): sell (pitch), teach (course/webinar), report (internal review), or inspire (keynote). The answer sets the arc:

- **Sell**: problem, stakes, the shift, the offer, proof, ask.
- **Teach**: promise, framework overview, one section per part, recap, next step.
- **Report**: headline number first, what moved it, what happens next. Never suspense.
- **Keynote**: one idea, escalating proof, one closing line.

## Aesthetic discovery (before any full deck)

Non-designers cannot answer "what style do you want" in the abstract. Ask what **feeling** the deck should create - impressed, energized, focused, or inspired - then show, never describe: the /design variations gate below doubles as the style exploration. The feeling also sets the motion register:

| Feeling | Visual direction | Motion direction |
|---|---|---|
| Impressed / confident | High contrast, oversized numbers, one bold accent | Slow fades, large scale-ins, restraint |
| Energized / excited | Color-blocked fields, punchy contrast | Springy easing, staggered pops |
| Focused / calm | Paper ground, editorial type, whitespace | Very little; 200-300ms fades only |
| Inspired / moved | Atmospheric ground, elegant serif-led display type | Staggered text reveals, gentle drift |

Fonts and colors always resolve from the design system's tokens; the feeling picks *which* tokens lead, never new values.

## One idea per slide

The rule that fixes most bad decks. A slide with two points is two slides. Headlines are assertions, not labels: "Churn halved after onboarding rework", not "Churn update". If the audience only read the headlines, the deck should still make its argument.

## Starter templates to offer (build 3-4 of these as the slide vocabulary)

- **Title / section divider** - huge type, brand color field or paper, nothing else.
- **Big number** - one stat at display size, one line of context.
- **Three-column** - three parallel ideas of equal weight; never four.
- **Chart/stat slide** - one chart, its takeaway as the headline.
- **Quote/case slide** - a customer or authority carrying the point.
- **Closing CTA** - the one thing to do next, at title-slide weight.

## Type scale and density

Slides are read from meters away, not centimeters. Working scale from the design system's type ramp: headlines at display size (60-80pt equivalent), body no smaller than the system's large body, maximum 3 sizes per slide. Bullets are 3-7 words - a paragraph on a slide is a document pretending to be a deck. A consistent footer (mark plus deck title) on every content slide, dropped on title and divider slides.

Hard density ceilings - when content exceeds them, split the slide, never shrink the type:

| Slide type | Maximum content |
|---|---|
| Title | 1 heading + 1 subtitle + optional tagline |
| Content | 1 heading + 4-6 bullets or 2 short paragraphs |
| Feature grid | 6 cards |
| Chart | 1 chart + its takeaway headline |
| Code | 8-10 lines, never scrolling |
| Quote | 1 quote + attribution |

## Animation rules (what separates designed from generated)

Motion is a seasoning, not a course. Every rule below has a reason; break none of them.

- **Entrances use ease-out, always.** Never ease-in on anything the audience is watching arrive - it delays the exact moment they are looking at. Built-in CSS easings are weak; use a strong custom ease-out curve.
- **Enter from scale 0.95 + opacity 0, never scale(0).** Nothing real appears from nothing.
- **Stagger grouped elements by 30-80ms.** Bullets, cards, and columns cascading in reads as intentional; everything landing at once reads as a page load.
- **One reveal pattern per deck.** Pick one entrance (fade-up, fade-only, or clip reveal) and use it everywhere. A deck where every slide invents its own transition reads as a template demo.
- **Durations**: content reveals 200-400ms; slide-to-slide transitions up to 500ms; nothing longer without a narrative reason.
- **Animate transform and opacity only.** Width, height, and position animations stutter and shift layout mid-read.
- **Reveal on arrival, not on load.** Trigger entrances when the slide becomes current (Intersection Observer or the controller), so slide 7's animation still fires when the presenter gets there.
- **Respect reduced motion.** `prefers-reduced-motion` gets gentle fades, not zero transitions.
- **Never animate data the audience is reading.** A chart may draw in once; its values never drift for style.

## Deck engineering (the HTML file)

- One self-contained file: inline CSS and JS, zero dependencies. Fonts per the design system; if it bundles files, embed them.
- **Viewport fit is a hard gate.** Every slide fills exactly one viewport, `overflow: hidden`, no internal scrolling ever. Type and spacing scale with `clamp()`. Content that does not fit becomes another slide.
- Keyboard (arrows, space), wheel, and touch navigation, plus a quiet progress indicator.
- Never negate a CSS function directly (`-clamp(...)` fails silently); wrap it: `calc(-1 * clamp(...))`.
- Verify at desktop, tablet, and phone sizes before delivery; any slide that overflows at any size fails the gate.

## Common failure modes (check before every delivery)

| Failure | Fix |
|---|---|
| Bullet walls | One idea per slide; split |
| Label headlines ("Q3 update") | Rewrite as assertions |
| Same layout 12 slides straight | Rotate the slide vocabulary; add dividers |
| Generic gradient + default UI font as the visual voice | Lead with the design system's display face and palette |
| Text shrunk to force a fit | Split the slide; density ceilings above |
| Every element animating, all at once | One reveal pattern, staggered, ease-out |
| Chart with no takeaway | The takeaway is the headline |
| Footer on title slides | Footers on content slides only |

## /design delivery

Variations gate: 2-3 genuinely distinct visual directions shown as a title slide plus one content slide each - e.g. paper-ground editorial vs dark technical vs color-blocked - not the same layout recolored. Name the feeling and the tradeoff of each. Final delivery: the full deck on a /design canvas, one 16:9 artboard per slide, in order; the user edits any slide directly there and exports the PDF from the canvas. The animated HTML deck file is generated from the approved canvas state, same tokens, same copy.

**Live artboards only.** Every slide on the canvas is live HTML/CSS - headlines, bullets, footers, chart labels all real editable text on brand tokens. Never place flattened PNG slides on the canvas; a deck the presenter cannot retitle is not a deliverable. Photography and generated imagery go in as image layers inside the HTML artboard, type kept in HTML on top.

## Sources

Reference sites for deck direction live in `../sources.md`. A user-supplied example deck outranks anything researched.

## Self-improvement

When the user corrects a deck - a layout they reject, a motion they find too much, a slide type they keep asking for - write the correction into this file (or the generated skill's copy of it) in the same session. Feedback that stays in chat is feedback the next deck ignores.
