---
name: visuals-builder
description: |
  Plan and build concept visuals, diagrams, infographics, and slide graphics in YOUR brand, using a library of 6
  proven template structures. Works from a video script, an outline, a blog post, or a direct instruction ("make
  a comparison of X vs Y"). Proposes 2 to 3 template options per concept, plans layout variations on a design
  canvas, then renders as HTML or SVG bound to your design tokens. Use this skill whenever the user wants to
  visualize a concept, illustrate an idea, or create visuals, diagrams, slides, or infographics for content:
  YouTube videos, presentations, social posts, documentation. Also trigger on "visualize", "diagram",
  "infographic", "slide", "chart this concept", "make a visual for", or when the user has a script or outline
  that needs visual support.
---

# Visuals Builder

You plan and generate concept visuals in the user's brand. Every visual follows one of 6 proven template structures, and every color, font, and spacing value comes from the user's design system, never from a hardcoded palette. You do not improvise new layouts unless no template fits, and you never guess brand values.

This skill follows the plugin's shared design framework. Read [references/framework.md](references/framework.md) first; the workflow below is that framework applied to concept visuals.

## Step 1: Find the design system

Before proposing anything visual, resolve the brand:

1. Look for a `design-system/` folder in the working directory or project root (the output of the **design-system-creator** skill). Read `tokens/tokens.css` or `tokens/tokens.json` for colors and type, and `foundations/color.md` for role assignments.
2. If there is no `design-system/` folder, offer the user three paths and let them pick:
   - Run the **design-system-creator** skill to build one.
   - Run the **firecrawl-brand-extractor** skill on their website to extract one.
   - State their brand colors and fonts directly in chat.

Never guess brand values. A wrong hex code is worse than a question.

From whatever source you resolve, fill this token map. Every template and technique in this skill refers to these tokens, so this map is the contract between the brand and the visuals:

| Token | Role | Typical source |
|---|---|---|
| `--ink` | Text, borders, shadows, arrows | darkest neutral in the palette |
| `--surface` | Canvas background | lightest neutral / ground color |
| `--accent-1` … `--accent-N` | Card fills, rotated across items | brand accent colors, ordered |
| `--font-heading` | Titles and headers | display/heading font |
| `--font-body` | Card labels, descriptions | body font |

If the brand has fewer than 3 accents, derive light tints of the accents you have (for card fills, tint toward `--surface` until `--ink` text passes contrast) and tell the user what you derived. If the brand is dark-ground, invert the roles consistently and say so.

## Step 2: Collect references

Gather 1 to 3 examples of what good looks like for this specific output: past visuals the user liked, competitor slides, a style they want to echo. Ask for links or files, or research examples matching their product and goal. Never design from zero context. If the user says "just use the design system," its `assets/templates/` folder and `BRAND-SUMMARY.md` count as references.

## Step 3: Understand the input and propose options

The user provides one of:
- A **script or long-form content**: analyze it section by section and identify concepts that benefit from visual support.
- An **outline**: identify which sections need visuals and what type.
- A **direct instruction**: "make a comparison diagram of X vs Y."

**Skip intros, hooks, demos, B-roll, and filler by default.** Only propose visuals for sections with a concept that lands better with on-screen support. Flag skipped sections so the user can confirm.

For each concept, propose, do not decide. Read [references/templates.md](references/templates.md) and present:

```
**Section: [section name]**
Concept: [what we're visualizing]

Primary: [template name]. [why it fits]
Alt A: [other template]. [tradeoff, e.g. "loses detail but reads faster"]
Alt B: [other template]. [tradeoff]

Content + icons (for Primary):
  - Title: "..."
  - Item 1: [icon] "..."
  - Item 2: [icon] "..."

Which template? And confirm copy + icons, or swap any?
```

Rules that govern every proposal:

1. **Always offer 2 to 3 template options with a one-line tradeoff each.** Even when one is clearly best, list an alternative. The user picks.
2. **Visual variety across a deck.** When producing multiple visuals for one piece of content, never repeat the same template structure. Track which templates earlier sections used and exclude them from later options.
3. **No arrows between independent items.** Arrows imply sequence or causation. Sibling items of equal weight get stacked or gridded, never chained.
4. **Include icons in every proposal** so the user confirms copy AND icons together. Pick from [references/icons.md](references/icons.md). Skip icons only if the user says no.
5. **Never build without explicit confirmation.** If the user redirects, update the proposal and re-confirm.
6. **One section at a time** unless the user says "do all of them."
7. **No em dashes in any output copy.** Use periods, commas, colons, or restructure.

Quick template selection matrix (full catalog in [references/templates.md](references/templates.md)):

| You want to say... | Template |
|---|---|
| "Here are N reasons / steps / levels" | **stacked-list** |
| "The same pattern repeats across N contexts" | **grid-columns** |
| "This process repeats and improves" | **cycle-loop** |
| "There is a core surrounded by layers" | **layered-concentric** |
| "Compare A vs B" | **side-by-side-comparison** |
| "X is made of these parts / categories" | **tree-breakdown** |

## Step 4: /design to plan, always with variations (mandatory)

Once the user confirms templates and copy, and before you render final files, use the **/design** command to open a design canvas and present **2 to 3 distinct layout variations** side by side. Distinct means structure, not color: different template interpretations, different density, different orientation. Build each variation with the resolved brand tokens so the user judges real candidates, not gray boxes.

This step is mandatory. Do not skip it, even for "quick" requests. The user picks one variation or asks for a mix.

After the build, use /design again for edits: put the built output on the canvas and iterate there with the user.

## Step 5: Build

Render the chosen variation as the final asset. Apply [references/style-mechanics.md](references/style-mechanics.md) (shadows, borders, color rotation, typography scale) with the token map from Step 1.

**Output formats:**

- **HTML/CSS (primary).** A standalone file with inline CSS. Define the token map as CSS custom properties at the top so a brand swap is a one-block edit. Pixel-precise, screenshots cleanly for video or social.
- **SVG (primary).** Raw SVG markup for embedding in other tools. Same tokens, applied as fill/stroke values with a comment block mapping each value to its token name.
- **Excalidraw (optional).** Only when the user explicitly asks for an editable hand-drawn-style file. Export the same structure as Excalidraw JSON (a `.excalidraw` file), applying the token colors to `strokeColor`/`backgroundColor` and the style mechanics (solid offset shadow as a dark rectangle behind each card, drawn first in the element array). Treat this as an export target, not the default.

**QA before presenting.** Run every rendered visual through [references/qa-checklist.md](references/qa-checklist.md): contrast, text overflow, alignment, shadow correctness, token compliance, structural consistency. Fix what you find before the user sees it. For a batch of visuals, spawn a subagent with the checklist and the files.

## Step 6: Iterate, then finish

Apply feedback in small rounds: swap a template, change labels, add or remove items, combine two templates. When the user approves, save the final files to a sensible project location and tell them exactly where. If the location is unclear, offer two likely homes and ask.

## When no template fits

Most concepts fit these 6 structures; a stacked list alone covers most cases. When one genuinely does not:

1. Explain why the existing templates fall short.
2. Suggest the closest one and what would need to change.
3. Propose combining two (e.g. a stacked list where each item holds a mini comparison).
4. Offer to design a new structure. If the user agrees, build it, then document it in `references/templates.md` so it becomes part of their library.

## Sibling skills

- **design-system-creator** builds the `design-system/` folder this skill consumes.
- **firecrawl-brand-extractor** pulls brand tokens from a live website.
- **infographic-builder**, **carousel-builder**, **email-design**, **analytics-dashboard-builder** cover other output types; hand off when the request is really one of those.
- **design-template-skill-creator** turns a recurring visual format into its own skill.
