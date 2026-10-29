---
name: email-design
description: Design marketing and product emails that look premium AND render correctly in real email clients (Outlook, Gmail, Apple Mail, dark mode, mobile). Covers the full pipeline - pull brand tokens from the user's design system, research reference emails on milled.com / Pinterest / reallygoodemails matched to the product and goal, present 2-3 layout variations on a /design canvas, build a modern liquid-glass design preview, then render it down to bulletproof table-based email-safe HTML and run a client-survival checklist. Use whenever the user wants to design, build, redesign, or code an email - a launch announcement, newsletter, promo, onboarding sequence, product update, digest, or "make this email look better / not break in Outlook." Trigger even if the user only says "email template," "HTML email," "newsletter design," or "email that works in Gmail."
---

# Email Design

Design an email in two layers: a modern, premium design preview first, then a faithful translation down to HTML that survives real email clients. The two-layer split exists because the tools that make an email look premium (backdrop-filter, gradients, flexbox, web fonts) are exactly the tools email clients strip. Design at full fidelity, then degrade deliberately - never let a client degrade it for you.

This skill follows the plugin's shared four-step framework (`references/framework.md`): find the design system, collect references, /design with variations, iterate and finish. The steps below are that framework specialized for email.

## Step 1 - Brand tokens (never guessed)

Look for a `design-system/` folder in the working directory or project root - the output of the **design-system-creator** skill. Read its tokens: colors, type scale, spacing, radii, logo assets, voice notes.

If there is no design system, offer three paths and let the user pick:

1. Run **design-system-creator** to build one.
2. Run **firecrawl-brand-extractor** on their website to extract one.
3. State brand colors, fonts, and logo directly in chat.

A wrong hex code is worse than a question. If the user gives nothing and no system exists, ask - do not proceed with invented brand values.

Two email-specific token notes to capture now, because they change the build later:

- **Fonts**: note the brand font, then map it to a web-safe fallback stack immediately (see `references/email-client-constraints.md`, "Fonts"). The design preview may use the real font; the email-safe build uses the stack.
- **Dark-mode pair**: ask (or derive from the design system) what the brand's dark-surface color is. Every background in the email will need a deliberate answer for dark mode.

## Step 2 - Reference research

Never design an email from zero context.

1. **Ask the user first**: do they have reference emails they like? Screenshots, links, emails from their own inbox, competitor sends. User-supplied references outrank anything researched.
2. **Then research**, matched to two axes: the user's PRODUCT (what industry, what price point, what audience) and the email's GOAL (launch, newsletter, promo, onboarding, digest, winback). A promo for a DTC skincare brand and a changelog email for a developer tool should pull completely different references.
3. Pick **2-3 references** and show them to the user (links or screenshots) with one line each on what to steal from it. Wait for a reaction before designing.

Primary sources and how to search each - milled.com (the large searchable archive of real brand emails), Pinterest, and reallygoodemails.com - are detailed in `references/reference-research.md`. Read it before researching.

## Step 3 - /design planning (mandatory)

Before building anything, use the **/design** command to open a design canvas and present **2-3 distinct email layout variations** side by side, each as a 600px-wide artboard. Distinct means different structure - hero-first vs. text-led editorial vs. modular card stack - not the same layout in three colors. Label each variation with the layout idea it represents and which reference inspired it.

The user picks one, or asks for a mix. Do not skip this step for "quick" requests; a wrong layout discovered after the email-safe build costs far more than a canvas round.

Use /design again for every later edit round: put the current design on the canvas and iterate there.

## Step 4 - Build in two layers

### Layer A: design preview (full fidelity)

Build the chosen variation as a modern web preview - this is the "what it should feel like" artifact the user approves. Here you may use everything email clients cannot do: real brand fonts, gradients, and the **liquid-glass aesthetic** - translucent frosted cards with depth. Snippets and construction rules are in `references/liquid-glass.md`. Keep the canvas 600-640px wide even in the preview, so the layout never depends on width the email cannot have.

While designing Layer A, keep a running "degradation ledger": for every effect used, note what it becomes in the email-safe build (glass card -> solid tinted card; gradient button -> solid brand-color button with VML; brand font -> stack). `references/liquid-glass.md` has the standard mappings. If an element has no acceptable degraded form, redesign it now.

### Layer B: email-safe render

Translate the approved design down to production HTML. This is a translation, not a rebuild - same hierarchy, same spacing rhythm, same copy, degraded effects. The full ruleset is in `references/email-client-constraints.md`; read it before writing the HTML. The non-negotiables:

- Table-based layout (`role="presentation"` on every table), max **600-640px** wide, single column on mobile.
- **All CSS inlined** on elements; `<style>` block only for mobile media queries and dark-mode overrides (Gmail keeps head styles, others don't - inline is the source of truth).
- No JavaScript, no external stylesheets, no web-font `@import` - web-safe font stacks with graceful fallback.
- **Bulletproof buttons** with VML for Outlook (pattern in the constraints file and the base template).
- A solid `background-color` fallback behind every gradient or glass effect - clients that can't render the effect get a clean solid-color version, never a broken layout.
- Dark-mode meta tags (`color-scheme` / `supported-color-schemes`) plus `@media (prefers-color-scheme: dark)` overrides where supported.
- `alt` text on every image; meaningful images must carry the message in their alt text because image blocking is the default state in many clients.
- Preheader text (hidden preview line) right after `<body>`.

Start from `assets/base-template.html` - a compact email-safe skeleton with the doctype, meta set, Outlook conditionals, bulletproof button, and dark-mode block already correct. Restyle it with the brand tokens; do not re-derive the plumbing.

## Step 5 - Client-survival checklist (run before delivering)

Walk every item and state the result to the user. The detailed how-to for each check is in `references/email-client-constraints.md`.

1. **Outlook (Windows)**: layout holds on tables alone; VML buttons and background fills present; no reliance on border-radius, backdrop-filter, or max-width.
2. **Gmail**: total HTML under **102KB** (Gmail clips beyond that and hides the unsubscribe footer); all critical styling inlined; no unsupported selectors in the `<style>` block.
3. **Apple Mail**: highest-fidelity client - confirm the enhanced (gradient/glass-tinted) layer actually renders there, since this is where the premium version is seen.
4. **Dark mode**: check forced inversions - near-white backgrounds, pure-black text, and transparent-background logos are the usual casualties. Verify the dark-mode overrides and logo treatment.
5. **Mobile width**: single column at 320-400px, tap targets >= 44px, font sizes >= 14px body / 22px headings.
6. **Plain-text alternative**: write one - short, scannable, links spelled out. Deliver it alongside the HTML.
7. **Accessibility pass**: alt text present, contrast >= 4.5:1 for body text against its *fallback* background (not just the pretty one), semantic heading order, `lang` attribute set.

If a sending platform is known (Klaviyo, Mailchimp, Customer.io, Braze...), also check its specific quirks - merge-tag syntax and whether it re-inlines or strips styles.

## Step 6 - Iterate, then finish

Apply feedback in small rounds on the /design canvas (Layer A), re-render Layer B after design changes settle. When the user approves:

- Deliver the email-safe HTML file, the plain-text version, and the design-preview file.
- State exactly where each file was saved.
- Restate the checklist results in one compact block so the user can forward it with the email for approval.

## Sibling skills

- **design-system-creator** - build the brand token folder this skill consumes.
- **firecrawl-brand-extractor** - extract tokens from an existing website.
- **infographic-builder**, **carousel-builder**, **visuals-builder** - companion asset skills; reuse the same design-system folder so email and social assets match.
- **design-template-skill-creator** - turn a finished email design into its own reusable template skill.

## Reference files

| File | Read when |
|---|---|
| `references/framework.md` | Start of every run - the shared four-step framework. |
| `references/reference-research.md` | Step 2 - how to search milled.com, Pinterest, reallygoodemails by product + goal. |
| `references/liquid-glass.md` | Step 4A - glass component snippets and their degradation mappings. |
| `references/email-client-constraints.md` | Step 4B and Step 5 - the full survival ruleset per client. |
| `assets/base-template.html` | Step 4B - email-safe skeleton to restyle. |
