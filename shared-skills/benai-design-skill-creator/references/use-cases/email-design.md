# Use case: email design

Marketing and product emails that look premium AND survive real clients (Outlook, Gmail, Apple Mail, dark mode, mobile). Design at full fidelity, then degrade deliberately - never let a client degrade it for you.

Mostly a B2C use case - start by asking what the emails are usually FOR (AskUserQuestion): **promotion/sale, product launch, newsletter/digest, lifecycle** (welcome, onboarding, winback). The answer changes the references, the layout, and the template set:

| Goal | What good looks like |
|---|---|
| Promo / sale | The deal readable in 2 seconds; urgency without clutter |
| Launch | One hero moment, one CTA, drama above the fold |
| Newsletter / digest | Scannable modular sections, clear rhythm, restrained per-item styling |
| Lifecycle | Warmth plus a single next step; progressive reveal |

## Starter templates to offer (pick 2-4 by style)

- **Photo-realistic** - hero photography carries the email; type sits in clean bands around it. **Ask for real product images when it is their product** - a stock stand-in teaches the template the wrong proportions. Breaks with images blocked, so live text must carry the message anyway.
- **Minimalistic** - type-led, one column, generous space, one CTA. The strongest default for lifecycle and digest emails. Breaks when a promo needs offer drama it refuses to give.
- **Product-first** - the product shot is the hero, offer legibility above the fold, modular cards below. The promo and launch workhorse. Breaks without a decent product shot - ask before assuming one exists.

## Reference research (before any design)

1. **Ask the user first**: emails they like - links, screenshots, forwards. User-supplied references outrank anything researched.
2. **Then research on two axes**: their PRODUCT (industry, price point, audience) and this email's GOAL. A promo for a skincare brand and a changelog for a developer tool pull completely different references.
3. Show **2-3 picks** with one line each on what to steal ("the modular card rhythm", "the offer typography"). Never more than 3 - more shifts the decision burden back onto the user. Every pick must be achievable in email-safe HTML after degradation; a reference whose whole appeal is video or heavy interactivity will only disappoint.

Source pointers live in `../sources.md` (real-send archives to search by brand or goal keyword; curated galleries by email type, often with inspectable HTML; visual-direction boards to treat as palette and density, never as client-safe layouts).

## The two-layer build (why email is different)

The tools that make an email look premium (gradients, glass effects, web fonts, flexbox) are exactly what email clients strip. Outlook on Windows renders with Word and sets the floor; Apple Mail is the ceiling. So design in two layers:

1. **Layer A - design preview, full fidelity.** The approved look, built with everything modern CSS offers, kept at **600-640px wide** so the layout never depends on width the email cannot have.
2. **Layer B - email-safe render.** A faithful translation down, not a rebuild: same hierarchy, same spacing rhythm, same copy, degraded effects.

**The degradation ledger** (keep it while designing Layer A): for every effect, note its email-safe twin - glass card becomes a solid pre-flattened tinted card with a 1px border; gradient button becomes a solid brand-color button (gradient as enhancement only); brand font becomes a web-safe stack picked for width similarity first; soft shadow gets dropped. An element with **no acceptable degraded form gets redesigned now**, not discovered broken later. Bake both layers into the generated skill so future runs translate instead of rebuilding.

## Layer B non-negotiables

- **Tables only.** Structure in `<table>`/`<tr>`/`<td>`, `role="presentation"` on every layout table, spacing via `<td>` padding (margins are unreliable). Fixed-width 600px inner table - Outlook ignores `max-width`.
- **Inline CSS is the source of truth.** Assume the `<style>` block may be stripped; it exists only for media queries (mobile, dark mode) and enhancements. Banned in the baseline: flex, grid, `position`, `backdrop-filter`, CSS variables, layout-critical `border-radius`.
- **Fonts**: no external font loading in the baseline. Every text element carries a full web-safe stack inline, mapped from the brand font by **width similarity first** (line-wrap points shift otherwise), weight second:

| Brand font shape | Email-safe stack |
|---|---|
| Geometric / grotesque sans | `Helvetica Neue, Helvetica, Arial, sans-serif` |
| Humanist sans | `'Segoe UI', Tahoma, Verdana, sans-serif` |
| Serif | `Georgia, 'Times New Roman', serif` |
| Mono accents | `'Courier New', Courier, monospace` |

- **Bulletproof VML buttons** for Outlook: a VML roundrect inside `[if mso]` conditionals, an inline-styled `<a>` for everyone else, the whole visual area clickable. A gradient button uses the gradient's midpoint solid in both, gradient as enhancement only.
- **A solid background-color fallback behind every gradient or glass effect.** Declare the solid first, the effect second. Text contrast is checked against the FALLBACK color, not the pretty one.
- **Gmail clips at ~102KB** of HTML and hides the footer and unsubscribe link (a compliance problem). Working budget: **under ~90KB**, leaving room for the sending platform's tracking rewrites. Images do not count; only the HTML does. One invalid rule in the `<style>` block can make Gmail drop the whole block - lint it.
- **Dark-mode defenses**: `color-scheme` / `supported-color-schemes` meta tags plus `prefers-color-scheme` overrides. Never a pure-white canvas or pure-black text - off-white and near-black invert less violently. The classic casualty is a dark logo on a transparent background vanishing when the canvas is force-darkened - use a logo version that works on both, or an explicit background you also override.
- **Alt text on every image**; meaningful images carry the message in their alt text, because image blocking is a default state. Never an email that is one giant image. `display:block` on every `<img>`, 2x exports, HTTPS-hosted, no SVG, no data URIs.
- **Mobile**: single column at 320-400px, tap targets 44px+, body 14px+ (16px preferred), headings 22px+, line-height in px.
- **Hidden preheader line** right after `<body>`. **Plain-text alternative** written and delivered alongside - short, scannable, links spelled out in full.

## Client-survival checklist (goes into the generated skill verbatim)

1. Outlook: layout holds on tables alone, VML buttons present, nothing depends on border-radius.
2. Gmail: under the ~90KB budget, all critical styling inlined, `<style>` block clean.
3. Apple Mail: the premium layer actually renders there - the ceiling is where the approved design is seen.
4. Dark mode: meta tags present, overrides cover canvas/cards/text/borders, logo survives both schemes.
5. Mobile: single column at 320px, tap targets 44px+, body 14px+.
6. Images off: the message is intact from alt text and live text alone.
7. Plain-text alternative exists and is current.
8. Contrast 4.5:1 against the FALLBACK background; `lang` set; heading order sensible; every href absolute HTTPS, no placeholder `#`.

If the sending platform is known, also check its quirks: merge-tag syntax, and whether it re-inlines or strips styles.

## /design delivery

**Variations gate (mandatory):** 2-3 distinct structures as 600px-wide artboards - hero-first vs text-led editorial vs modular card stack - each labeled with the reference it traces to. The user picks or mixes; do not skip for "quick" requests, because a wrong layout found after the email-safe build costs the build.

**Final delivery:** the approved design preview on a /design canvas for edit rounds, then the email-safe HTML plus plain-text version delivered as files, with the checklist results stated in one compact block the user can forward for approval.

**Live artboards only.** Every artboard on the canvas is live HTML/CSS - subject line, headings, body, buttons all real editable text styled with brand tokens. Never place a flattened PNG mock of the email on the canvas. Product photos and hero imagery go in as image layers inside the HTML artboard, type kept in HTML on top - which mirrors how the email itself must be built, since image-only emails die with image blocking.

## References and self-improvement

More reference sources for email are listed in `../sources.md` - show the user 3-5 at Step 4.

**This file improves itself.** When the user gives layout-changing feedback, a new reference, or a hard rule ("never X") about their emails, fold it into this file - or the generated skill's own templates and rules - in the same session, then say what changed.
