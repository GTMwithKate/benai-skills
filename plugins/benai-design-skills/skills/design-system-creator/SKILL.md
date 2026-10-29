---
name: design-system-creator
description: Produces a complete, Claude-Design-compatible design system folder for any brand — ready to upload to Claude Design's "Set up your design system" flow and use across every future asset (websites, landing pages, pitch decks, Instagram/LinkedIn carousels, infographics, emails, ads). Handles two paths — building a brand from scratch (research → synthesis → full system) or extracting the design system from an existing business's published assets (website scrape, logos, fonts, past creatives). Use whenever the user wants to stand up a design system from zero, codify a brand they already run but never formalized, set up tokens/typography/color/voice guidelines, build reusable brand assets, or feed a brand kit into Claude Design / Claude Skills / any LLM-assisted asset-creation pipeline. Trigger even if the user says "brand kit," "brand guidelines," "style guide," "brand book," "design language," or "set up my brand for AI" — those are all in scope.
---

# Design System Creator

This skill produces a complete, portable **design system folder** — the kind a modern brand uses as the single source of truth for every asset it ever publishes: web, landing pages, pitch decks, Instagram carousels, LinkedIn carousels, emails, infographics, ads, and everything else.

The final output is a folder that can be:

- uploaded directly to **Claude Design's "Set up your design system"** flow,
- fed as context to any LLM that produces brand assets,
- referenced by a design team as a living style guide.

## Step 0 — Detect what the machine has, then start anyway

This skill never blocks on a missing tool. It runs at the best rung available,
says which rung that is in one sentence, and delivers the full design system
either way. The one thing it will not do is invent a value to cover a gap.

Run the detector:

```bash
echo "node:       $(node -v 2>/dev/null || echo MISSING)"
echo "firecrawl:  $(command -v firecrawl >/dev/null 2>&1 && firecrawl --status 2>&1 | grep -o 'Authenticated' || echo MISSING)"
echo "playwright: $(npx -y playwright --version 2>/dev/null || echo MISSING)"
echo "chromium:   $(ls ~/Library/Caches/ms-playwright 2>/dev/null | grep -c chromium || echo 0)"
echo "eds:        $(test -f .claude/skills/extract-design-system/SKILL.md && echo OK || echo MISSING)"
```

| What answered | Rung you are on | What you use |
|---|---|---|
| Nothing but the user | **0 — Told** | Their hex codes, brand book PDF, screenshots. Best source there is when a real brand book exists |
| `node` | **1 — Read** | [scripts/extract-brand.mjs](scripts/extract-brand.mjs), bundled, zero install, zero API key. Real declared CSS: colours by frequency, font families, radius, shadow, spacing scale, custom properties, Google Fonts links, logo URLs |
| `playwright` + a chromium build | **2 — Rendered** | Computed styles after JavaScript runs, a real screenshot, logo rasterisation via [scripts/render.mjs](scripts/render.mjs) |
| `firecrawl` authenticated | **3 — Interpreted** | `--format branding`, the structured brand kit: personality, component inventory, typographic roles, competitor sweep |

Node is always there, because Claude Code runs on it. **So rung 1 is always
available and there is never a reason to stop.** Rungs 2 and 3 are upgrades you
mention once, after you have handed something over, never as a gate before.

Full guidance, including exactly how to fill the gaps each rung leaves without
guessing, is in [references/extraction-ladder.md](references/extraction-ladder.md).
Read it before Branch B. Install instructions for the optional tools are in
[references/setup.md](references/setup.md).

> Say the rung out loud, once, in the user's terms: *"Reading your site directly,
> which gets colours, fonts and spacing out of the CSS. I will flag anything I
> could not see."* Then keep going.

## The first interview question

Once the tools are in place, ask the user exactly **one** question to figure out which path they're on:

> **Are we creating a brand-new design system from scratch, or are we extracting the design system from a business you already run?**

Don't branch, don't suggest, don't assume. Their answer picks one of two workflows:

- **"New / from scratch / nothing yet"** → Branch A. Load [references/branch-a-fresh.md](references/branch-a-fresh.md).
- **"Existing business / existing site / existing brand"** → Branch B. Load [references/branch-b-extract.md](references/branch-b-extract.md).

If the answer is ambiguous ("we have a logo but nothing else," "we've been running for a year but it's all ad-hoc"), they're almost certainly on Branch B — extraction — because you have real artifacts to work from. Confirm this with them before proceeding.

## What the skill produces (both branches, same structure)

Output a `design-system/` folder at the working-directory root, with this exact tree. The content differs by branch, but every file in the tree below gets produced:

```
design-system/
├── README.md
├── CLAUDE.md                       — load-order + non-negotiables for any LLM consuming this system
├── BRAND-SUMMARY.md                — one-page snapshot
├── foundations/
│   ├── brand.md
│   ├── voice.md
│   ├── vocabulary.md
│   ├── color.md
│   ├── typography.md
│   ├── spacing.md
│   ├── radius.md
│   ├── shadow.md
│   ├── motion.md
│   ├── iconography.md
│   └── imagery.md
├── tokens/
│   ├── tokens.json                 — W3C-ish schema
│   ├── tokens.css                  — CSS custom properties
│   └── tailwind.preset.js          — drop-in Tailwind preset
├── logo/
│   ├── mark.svg
│   ├── mark-inverse.svg
│   ├── wordmark.svg
│   ├── lockup-horizontal.svg
│   ├── lockup-stacked.svg
│   ├── favicon.svg
│   ├── [rendered .jpg / .png versions of the above]
│   └── usage.md
├── components/                     — React + Tailwind starters
│   ├── README.md
│   ├── utils.ts
│   ├── button.tsx
│   ├── input.tsx
│   ├── card.tsx
│   ├── feature-card.tsx
│   ├── badge.tsx
│   ├── nav.tsx
│   ├── hero.tsx
│   ├── testimonial.tsx
│   ├── cta-section.tsx
│   ├── stat.tsx
│   └── animated.tsx
├── voice/
│   ├── examples.md                 — do/don't pairs per surface
│   └── homepage-copy.md            — drop-in hero variants
├── applications/
│   ├── web.md
│   ├── presentations.md
│   ├── social-instagram.md
│   ├── social-linkedin.md
│   ├── email.md
│   ├── infographics.md
│   └── ads.md
└── assets/
    ├── patterns/                   — grid.svg, brand-wash.svg
    └── templates/                  — real published assets (preferred — copied from the user's working directory) and/or synthetic drafts (only where no real asset exists). On Branch B with published assets present, this folder is the user's actual decks / one-pagers / carousels / YouTube frames, organized by surface. The Marp theme CSS is always present (it's not a recreation — it's a CSS theme).
```

Full field-by-field content spec in [references/output-structure.md](references/output-structure.md).

## The asset-fidelity rules — read before either branch

These two rules apply on **both branches** and override the "produce every file" instinct. Real artifacts beat synthetic recreations every time.

### Rule 1 — When the user provides published assets, use them as templates. Do NOT recreate them.

If the user has handed you (or you've discovered in their working directory) any of: a one-pager PDF, a pitch deck, slide-template library, IG/LinkedIn carousels, ads, OG images, email screenshots, or any other published asset that demonstrates the brand's look — **copy those files into `design-system/assets/templates/` and reference them as the canonical templates.**

Do not write synthetic SVG recreations of carousel covers, OG images, LinkedIn posts, or any other surface for which the user already has a real version. A synthetic recreation will look "lazy" next to the real published artifact, and pasting it into a downstream tool (Claude Design, a designer's brief) will degrade the brand. The user's own assets are the highest-fidelity version of the brand that exists.

Concretely:
- **Browse the user's working directory before generating templates.** Look for `*.pdf`, `*.png`, `*.jpg` files at the project root, in subfolders that look organized (e.g., `slide-templates/`, `decks/`, `social/`, etc.), and in any folder the user mentioned in their prompt.
- **Copy real assets into `assets/templates/<surface>/` preserving structure.** E.g., a 28-template slide library lives in `assets/templates/deck-slides/<category>/<file>.png`.
- **Replace the asset-templates section of [output-structure.md](references/output-structure.md) with the real files** in your generated `README.md` for `assets/templates/`. Document which template to pick by content shape ("3 ideas equal weight → file X"), not by your made-up filename.
- **Only generate synthetic templates when no real asset exists for that surface, AND** explicitly flag each synthetic asset to the user with: *"I drafted this — let me know if it should be replaced with one of your real published versions."* On Branch A (fresh brand), every template is synthetic by definition; on Branch B, synthetic templates should be the exception, not the default.
- **Do not delete a real asset to make room for a synthetic one.** If the user provides a deck library *and* a YouTube intro slide, keep both. Templates are not deduplicated by surface — they're the user's canon.

### Rule 2 — When you render the logo, render it faithfully. Do NOT add features.

If the user provides a logo (file upload, website-scraped raster, or a clean reference photo of the asset in use), render an SVG that matches what's actually there. Don't add eye dots to a smiley that has none. Don't add a serif tail to a sans wordmark. Don't "improve" a 2-stroke mark by adding decorative elements. The brand owns the logo — the logo is what it is.

After producing logo SVGs, **diff your output against the source visually**: render the SVG with [scripts/render.mjs](scripts/render.mjs), open both side by side, and confirm every visible feature (and only those features) is present. If the source logo has lower resolution than you'd like, ask the user for a higher-res version — don't invent details to "clean it up."

If you're uncertain about a feature ("does this circle have eye dots or just a smile?"), zoom into the highest-resolution copy you can find and confirm before generating. When in doubt, render the simpler version and ask the user to confirm.

---

## The non-negotiables — enforced in every system you produce

These are the design laws. They are what make a system *feel* disciplined rather than generic. Apply them whether you're on Branch A or B. Full reasoning in [references/non-negotiables.md](references/non-negotiables.md); summary:

1. **One primary color.** Pick one confident hue. No "palette" of three competing primaries. Everything else is shades of ink (text) and semantic feedback colors.
2. **One typeface family.** Sans-serif. Ideally Inter (free, universal). A distinctive display face is allowed if licensed, but never two display faces. No script, no serif (serif is only allowed for very long-form legal/contract PDFs).
3. **One canvas choice.** Either warm off-white or pure white — pick one and use it consistently for marketing. Pure white feels clinical, warm off-white feels calm — choose based on the brand's personality, then commit.
4. **Sentence case for all headlines.** No Title Case. No ALL CAPS except in a ≤3-word overline.
5. **No hype vocabulary on public surfaces.** Banned everywhere: *revolutionary, game-changing, 10x, cutting-edge, supercharge, unleash, leverage, transform, synergy, seamless, robust, AI-powered (as a bare adjective).*
6. **Voice rules:** second-person singular ("you"), short sentences, name the user's world (their nouns: *chair, shop, appointment, chart, ticket*), not ours (*agent, LLM, platform, pipeline*).
7. **Imagery direction:** real photography of actual humans or spaces from the brand's context. No stock "diverse team around a laptop." No AI-generated humans. No generic "AI" visuals (glowing orbs, neural meshes, wireframe globes).
8. **Motion is minimal.** Fade + small translate. 160/240/480ms durations. No parallax, no looping hero video, no scroll-jacking, no confetti.
9. **No gradients-over-everything, no glassmorphism, no 3D, no neumorphism.** Calm, flat, confident.
10. **Every claim gets a number or a name.** "Saves time" is banned; "saves 4 hours a week" is required. Use real client names or acknowledge the data source.

If a design choice in either branch violates one of these, push back and propose the on-brand alternative.

## The brand teardown review — mandatory gate on both branches

Once the brand tokens are extracted (Branch B) or assembled and signed off (Branch A), and **before writing a single file of the final `design-system/` folder**, render the **brand teardown**: one self-contained HTML page built from the bundled template at [assets/brand-teardown-template.html](assets/brand-teardown-template.html). Publish it for review — as an artifact when artifact publishing is available, otherwise as a local HTML file you open for the user.

The teardown puts every token on screen as a live specimen, not a list of hex strings: it **shows, it does not explain**. Swatches painted in the real colors with measured contrast grades, the full type scale at true size, the logo on its grounds, spacing bars, radii and shadows rendered, a working hover demo if the brand has an interaction signature. Text stays at caption length; sections the brand has no data for get skipped, never padded with invented values — uncertain values carry a visible "unverified" tag.

The user approves, or disagrees and gives feedback. Corrections go **token by token: section, value, fix**. Apply them, re-render, ask again — loop until the user explicitly approves. Only after that approval do you generate the design-system folder. **Silence is not approval; nothing is written before sign-off.**

This gate exists because a wrong primary hex or a misidentified font propagates into every one of the ~40 files this skill produces. Ten seconds of visual review is cheaper than regenerating the folder. The teardown page **is** this skill's review surface — the whole review happens on it, in HTML.

Template, the 13-part structure, and the full flow: [references/brand-teardown.md](references/brand-teardown.md).

## Branch A — Fresh: research → synthesis → generate

Full workflow in [references/branch-a-fresh.md](references/branch-a-fresh.md). Summary:

1. **Discovery interview** — one focused pass of questions covering: the business (what, for whom, why it exists), the feeling they want someone to have in 3 seconds, 3–7 reference sites they love and *specifically* what draws them to each, any anti-references, color instinct, and constraints (existing name, licensed font, channel-only).
2. **Research via Firecrawl.** Search the category if the user can't name enough references. Scrape every reference URL with `firecrawl scrape <url> --format markdown,branding --full-page-screenshot`. The `branding` format returns structured tokens (colors, fonts, typography, spacing, components, personality). Save each to `brands/<slug>/`.
3. **Synthesize.** Write a `research/synthesis-and-direction.md` doc: what the category looks like (color/type/radius patterns), where this brand should break from the pack, and a concrete proposed direction with specific hex values, type pair, spacing/radius choices, motion rules, imagery direction, and voice principles. End with **the five sign-off questions** (color, typography, logo direction, name confirmation, component scope).
4. **Wait for sign-off.** Do not start generating the design system until the user confirms color + typography + logo + name at minimum.
5. **Brand teardown review.** Fill the bundled template ([assets/brand-teardown-template.html](assets/brand-teardown-template.html)) with the signed-off tokens per [references/brand-teardown.md](references/brand-teardown.md), publish it (artifact if available, else a local HTML file opened for the user), and wait for approval. Corrections go token by token — section, value, fix — then re-render and ask again. No design-system files get written before explicit approval.
6. **Generate.** Produce every file in the tree above using the templates in [assets/templates/](assets/templates/) and the guidance in [references/output-structure.md](references/output-structure.md). Render the logo SVGs to JPG + PNG via the script at [scripts/render.mjs](scripts/render.mjs). Because this is a fresh brand, all asset templates are synthetic — flag each one to the user and ask if they want to replace any with their own version after the first round of real assets goes live.
7. **Finalize.** Write the "Company name and blurb" + "Any other notes?" text for Claude Design per [references/claude-design-form.md](references/claude-design-form.md). Return the folder path + the form text to the user.

## Branch B — Extract: ingest → reconcile → codify

Full workflow in [references/branch-b-extract.md](references/branch-b-extract.md). Summary:

1. **Ingest interview.** Ask for: their public website URL (required); logo files (SVG preferred, any format accepted); fonts used (family names — actual font files optional); any published assets (pitch decks, IG/LinkedIn carousels, ads, proposals, email screenshots); their description of the business in 2 sentences; any "brand rules" they've been writing down informally.
2. **Scan the working directory for published assets.** Before scraping, `ls`/`find` the project root for PDFs, PNGs, JPGs, organized subfolders (`slide-templates/`, `decks/`, `social/`, `ads/`, etc.). Read a representative sample to confirm they're the brand's real artifacts. These become your `assets/templates/` payload — see Rule 1 in the asset-fidelity section above.
3. **Extract from the live site.** Run `firecrawl scrape <url> --format markdown,branding --full-page-screenshot --wait-for 5000` on the homepage plus 1–2 deeper pages (pricing, about). Run `npx extract-design-system <url>` for independent computed tokens. Save to `brands/<self-slug>/` and `.extract-design-system/`.
4. **Reconcile.** Compare what the scrapes found against what the user uploaded and what's in the working directory. Cross-check font names, primary colors, logo variants. Note any conflicts — the published asset usually wins over a stale website, but confirm with the user.
5. **Brand teardown review.** Fill the bundled template ([assets/brand-teardown-template.html](assets/brand-teardown-template.html)) with the reconciled tokens per [references/brand-teardown.md](references/brand-teardown.md), publish it (artifact if available, else a local HTML file opened for the user), and wait for approval. Extraction is fallible — a wrong hex or font caught here costs nothing; caught after generation it costs the whole folder. Corrections go token by token — section, value, fix — then re-render and ask again. No design-system files get written before explicit approval.
6. **Codify.** Generate every file in the tree above. Prefer extracted real values over invented ones. **Copy the user's real published assets into `assets/templates/<surface>/`** rather than recreating them as synthetic SVGs (Rule 1). When rendering the logo from the source artifact, render only what's there — no added eyes, no decorative additions (Rule 2). Where extraction is thin (voice, imagery direction, motion principles), interview the user briefly to fill the gap — *do not invent voice rules the brand doesn't already exhibit*.
7. **Finalize.** Same as Branch A — produce the Claude Design form text and hand it back. In the hand-off summary, list which templates are real (copied from the user's working dir) vs. synthetic (drafted by you and pending approval).

## Tools you have available

**Always present, no install:**

- **[scripts/extract-brand.mjs](scripts/extract-brand.mjs)** — the bundled extractor. `node scripts/extract-brand.mjs <url> [--json] [--pages=/pricing,/about]`. Fetches the page, follows its stylesheets, ranks every colour, font, radius, shadow and spacing value by declaration count, and lists the declared CSS custom properties. Prints its own `confidence`. This is rung 1 and it always works.
- **File tools** (Write, Edit, Read) — produce markdown and token files from the templates.
- **The user** — the highest-value source in the skill. A brand book PDF, three hex codes, or one homepage screenshot beats any scrape. Ask early.

**Optional upgrades, used when detected, never installed unasked:**

- **Playwright Node.js** — [scripts/render.mjs](scripts/render.mjs) renders SVG logos and template SVGs to JPG and PNG, and can read computed styles after JavaScript runs. `npm install playwright && npx playwright install chromium` is a ~200 MB download, so mention it, do not force it.
- **Firecrawl CLI** — `firecrawl scrape <url> --format markdown,branding --full-page-screenshot`. The `branding` format returns a structured brand kit rather than raw CSS, which is the best single call in this skill when the user has a key. Free tier is 500 credits a month; a full run costs 15 to 25. Set up with `npx -y firecrawl-cli@latest init --all --browser`.
- **extract-design-system** (`npx -y extract-design-system <url>`) — independent CSS-computed tokens, useful as a second opinion against rung 1. Needs Chromium.

**The rule:** a missing tool changes your confidence and what you mark unknown. It never changes whether you deliver, and it never licenses a guess. When two sources disagree, name both and say which you used.

## The final deliverable — always produce this

At the very end, regardless of branch, output two blocks of text the user can paste directly into Claude Design's setup form:

1. **Company name and blurb** — under 80 words. Name + what the business does + for whom + the list of asset surfaces it will publish.
2. **Any other notes?** — ~200–300 words. The most critical non-negotiables + specific visual/voice overrides that should bias Claude Design's output. Exact format in [references/claude-design-form.md](references/claude-design-form.md).

Do not skip this step. It is the hand-off and the whole point of producing the system in the first place.

## This skill is the foundation of the plugin

The `design-system/` folder this skill produces is what every sibling skill in this plugin reads before it designs anything. Point users to them once the system exists:

- **firecrawl-brand-extractor** — a deeper Branch B extraction pass when the Firecrawl CLI is available; its output feeds straight into this skill's reconcile step.
- **infographic-builder**, **carousel-builder**, **visuals-builder**, **analytics-dashboard-builder**, **email-design** — each consumes the tokens, voice, and application guides in this folder to produce on-brand assets for its surface.
- **design-template-skill-creator** — turns a recurring asset from this system into its own reusable skill.

A design system that exists but is never consumed is shelf-ware; hand users the next skill for whatever asset they need first.

## Where to go next

- **Which rung you are on and how to fill its gaps**: [references/extraction-ladder.md](references/extraction-ladder.md) — read before Branch B
- **Optional tool setup**: [references/setup.md](references/setup.md) — upgrades, not prerequisites
- Branch A full playbook: [references/branch-a-fresh.md](references/branch-a-fresh.md)
- Branch B full playbook: [references/branch-b-extract.md](references/branch-b-extract.md)
- Brand teardown review flow + 13-part structure: [references/brand-teardown.md](references/brand-teardown.md)
- Brand teardown HTML template: [assets/brand-teardown-template.html](assets/brand-teardown-template.html)
- Output spec (what every file should contain): [references/output-structure.md](references/output-structure.md)
- Non-negotiables + reasoning: [references/non-negotiables.md](references/non-negotiables.md)
- Claude Design hand-off text: [references/claude-design-form.md](references/claude-design-form.md)
- Rendering script: [scripts/render.mjs](scripts/render.mjs)
- Templates (tokens, logo, components, applications, voice): [assets/templates/](assets/templates/)
