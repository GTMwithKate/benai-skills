---
name: carousel-builder
description: Turn one piece of source content (a newsletter, YouTube transcript, blog post, LinkedIn post, or raw brief) into a finished social media carousel in the user's own brand, exported as slide PNGs plus a swipeable PDF. Picks the slide count (3-10), writes the copy with a hook-substance-CTA arc, renders every slide from HTML templates filled with the brand's design tokens, and exports print-ready files. Use whenever the user says "build a carousel", "make a LinkedIn carousel", "make an Instagram carousel", "turn this into slides", "repurpose this into a carousel", or hands over content and asks for a swipeable multi-slide post, even if they never say the word "carousel".
---

# Carousel Builder

Turn source content that is handed to you into a finished, on-brand, image-first carousel: individual slide PNGs plus one assembled PDF (the format LinkedIn documents and most schedulers accept).

**Scope.** This skill only builds the carousel from content it is given and returns the files. It does not scan inboxes, choose which content to repurpose, schedule anything, or post anywhere. The caller finds the source and handles delivery.

The carousel must **make its point on its own**. Assume the social caption is one line; the slides carry the whole argument.

This skill follows the plugin's four-step framework. Read `references/framework.md` first; the steps below are that framework applied to carousels.

## Step 1 — Find the design system (never guess brand values)

Look for a `design-system/` folder in the working directory or project root (the output shape of the **design-system-creator** skill). From it, fill the carousel token sheet:

1. Read `design-system/tokens/tokens.css` (or `tokens.json`) and `design-system/foundations/color.md` + `typography.md`.
2. Write a `tokens.css` for this run by copying `assets/templates/tokens.css` and filling every variable from the brand:

| Carousel token | Fill from |
|---|---|
| `--carousel-bg` | The brand's primary light surface / background color |
| `--carousel-ink` | The brand's darkest text color |
| `--carousel-muted` | A secondary body-text color (or the ink at ~70% strength if the system defines one) |
| `--carousel-accent` | The single brand accent color |
| `--carousel-highlight` | A soft tint of the accent for the marker-style headline highlight (use the system's tint if it has one; otherwise derive one with `color-mix()` in CSS, never by inventing a hex) |
| `--carousel-bar` | A near-ink dark for the footer bar (or the ink itself) |
| `--carousel-font-display` | The brand's display/heading font stack |
| `--carousel-font-body` | The brand's body font stack |

If the design system bundles font files or Google Fonts links, wire them in with `@font-face` or a fonts link so the export renders the real type.

**No `design-system/` folder?** Offer the user three paths and let them pick: run **design-system-creator** to build one, run **firecrawl-brand-extractor** on their website, or state their colors and fonts directly in chat. Never invent a hex code or font. A wrong brand value is worse than a question.

Also pick up voice: if `design-system/foundations/voice.md` exists, its rules govern the copy in Step 4.

## Step 2 — Collect references

Gather 1-3 examples of what good looks like for this carousel: past carousels the brand has published (check `design-system/assets/templates/`), competitor carousels the user admires, or links the user provides. If nothing exists, ask for one example or agree on a direction in chat. Never design from zero context.

## Step 3 — /design the layout (mandatory, 2-3 variations)

Before building anything, use the **/design** command to open a design canvas and present **2 to 3 distinct layout variations** of the carousel side by side — typically the hook slide plus one substance slide per variation. Each variation must differ in structure (composition, hierarchy, footer treatment, highlight style), not just color. The user picks one or asks for a mix.

Do not skip this step, even for "quick" requests. After the build, put the finished slides back on a /design canvas for visual iteration.

## Step 4 — Build, iterate, export

### 4a. Read the source, find the ONE point

Accept whatever content is provided. Identify the single argument the carousel makes: one point, backed up. If the source only teases ("watch my video"), reconstruct the real substance so the carousel stands alone. If the source has several disconnected ideas, pick the most useful one.

### 4b. Slide count and copy

Read `references/copywriting.md`, then pick the count (3-10, typically 5-8) and write every slide's copy following the arc: hook slides up front, text-heavier substance slides in the middle, one CTA slide at the end. One idea per slide, exactly one accent highlight per headline, slot budgets respected.

### 4c. Render slides from the HTML templates

Read `references/export.md` for the exact flow. In short:

1. Copy the matching template from `assets/templates/` for each slide (`slide-hook.html`, `slide-body.html`, `slide-cta.html`) into the working folder as `slide-01.html` … `slide-NN.html`, next to your filled `tokens.css`.
2. Fill each template's copy slots and the page indicator (`NN / NN`). Adjust layout details to match the variation the user picked in Step 3.
3. Screenshot each HTML file at 1080x1350 (4:5 portrait, accepted by LinkedIn and Instagram) and assemble the PNGs into a PDF.

QA every slide: read each PNG back and confirm the text is complete, nothing overflows or clips, and only one phrase per headline is highlighted. Fix the HTML and re-export any slide that fails.

**Optional image-model path.** If the user prefers illustrated, image-generated slides and has an image-generation tool connected, you may render slides from prompts instead of HTML — but treat it as optional, verify spelling on every generated slide, and still composite text-critical elements (footer, page numbers) in HTML or code. The HTML path is the default because it is deterministic and free.

### 4d. Iterate, then finish

Apply feedback in small rounds on the /design canvas. When the user approves, export the final PNGs + PDF to the working folder (default `./<slug>-carousel/`, or a path the caller gives) and report the exact paths, the slide count, and the topic.

## Hard rules

1. Never guess a brand color, font, or logo. Every visual value traces to the design system or an explicit user answer.
2. Templates and generated HTML use the `--carousel-*` tokens only; no hard-coded brand hex values.
3. The carousel is self-contained: it teaches or proves its point without the caption.
4. Exactly one highlighted phrase per headline; the highlight is the punchline, never a connector word.
5. A swipe cue (small arrow or "swipe" marker) on every slide except the last.
6. If the brand has a logo file in `design-system/logo/`, place it in the footer via HTML — never ask an image model to draw a logo.
7. Slide count 3-10, chosen from the content, not from habit.

## Files

| File | Contains |
|------|----------|
| `references/framework.md` | The plugin-wide four-step design framework. |
| `references/copywriting.md` | Slide-count logic, the copy arc, slot budgets, voice rules. |
| `references/export.md` | The HTML render + screenshot + PDF flow, with fallbacks. |
| `assets/templates/tokens.css` | The token sheet to fill from the user's design system. |
| `assets/templates/slide-hook.html` | Big-headline hook/cover slide template. |
| `assets/templates/slide-body.html` | Substance slide template (bullets / numbered steps). |
| `assets/templates/slide-cta.html` | Final CTA slide template. |
| `scripts/export.sh` | Screenshot every `slide-*.html` and assemble the PDF. |

## Sibling skills

**design-system-creator** builds the `design-system/` folder this skill reads. **firecrawl-brand-extractor** pulls brand values from a live website. **design-review** can score the finished carousel before it goes out. **infographic-builder** is the right tool when the user wants one dense single image instead of a swipeable sequence.
