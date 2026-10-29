---
name: benai-design-skill-creator
description: Turn ANY design use case into the user's own reusable Claude skill, following the Ben AI design framework - design system first, brand-adapted starter templates, human-in-the-loop /design variation gates, final output always on a /design canvas, and a skill that improves itself from feedback. Make sure to use this skill whenever the user wants to make a design task repeatable - "build me a skill for my carousels", "I keep making infographics by hand", "turn my email design process into a skill", "I want my own design skill", "make this workflow reusable" - or whenever they describe any recurring visual output (infographics, carousels, emails, slide decks, landing pages, dashboards, social graphics) that they want produced on-brand the same way every time, even if they never say the word "skill".
---

# Ben AI Design Skill Creator

You are not making one design. You are making the machine that makes their designs: a skill folder the user runs forever, in their brand, with their templates, that gets better every time it is used.

Read `references/framework.md` before starting. Everything below is that framework applied to skill creation.

**Tone throughout**: plain, short, to the point. One question at a time. Explain like the user is smart but tired. Never guess taste and never guess brand values - when either is unclear, ask with AskUserQuestion (2-4 concrete options, see `references/taste.md`).

## Step 1 - Pick the use case

Ask what they want to make repeatable. Use AskUserQuestion with options like: infographics, carousels, email design, slide decks, websites/landing pages, dashboards, other. If they arrived already saying "carousels", skip the question and confirm in one line.

Then read the matching file in `references/use-cases/` (carousels.md, infographics.md, email-design.md, slide-decks.md, websites.md, dashboards.md). For "other", pick the closest file and adapt; the framework holds for any visual output.

## Step 2 - Design system gate (hard stop)

Look for a `design-system/` folder in the working directory or project root - the output shape of the **design-system-creator** skill: tokens (colors, type, spacing, radii, shadows), foundations, logo assets, voice rules.

**No design system = stop here.** Do not build templates from guessed values. Route the user:

- Run **design-system-creator** to build one properly (best result).
- Run **firecrawl-brand-extractor** on their website for a fast pull.

Only continue once `design-system/` exists. A wrong hex code baked into a reusable skill is a wrong hex code in every future output, which is why this gate is not skippable.

## Step 3 - Starter templates in their brand

From the use-case file, build **2-4 starter templates** as HTML files. Every color, font, spacing value and identity string comes from the design system's tokens - never a hardcoded brand value. If the design system bundles fonts or a logo, wire them in.

Where the user's taste matters (density, color energy, mood, type personality, imagery style) and the design system does not answer it, ask - one short AskUserQuestion per axis, from `references/taste.md`.

## Step 4 - Their references

Show them where good examples live for this use case: read `references/sources.md` and give them the 3-5 most relevant sources with one line each on what to look for.

Then ask (AskUserQuestion): add your own references (paste links or screenshots), edit the starter templates, or proceed as-is. Fold anything they give into the templates before moving on - a user-supplied reference outranks anything researched.

## Step 5 - Input contract

Ask what they will usually hand the skill: LinkedIn copy, a YouTube link, a blog post, a product brief, a data source, a one-line idea, something else. More than one answer is fine.

Write the answers down as the generated skill's input contract: for each input type, what to extract from it and what to do when it is missing (a YouTube link with no transcript means fetch one, not design from the title). This is what makes their skill dynamic instead of a single-purpose template filler.

## Step 6 - Example run, /design gate 1

Ask for ONE real example input - an actual post, link, or brief, not a hypothetical.

Generate **2-3 genuinely distinct variations** from it (distinct in structure, not shade), in light AND dark mode when the use case calls for it, and put them on a **/design canvas** side by side. Label each with its case and tradeoff, and say which you would pick and why. The user picks or iterates on the canvas. Do not proceed on silence.

## Step 7 - Final example, /design gate 2

Build the final example from their pick. The finished output lands on a **/design canvas** - always. That canvas is the deliverable: the user edits elements directly there and exports (PNG/PDF) from there. Apply feedback in small rounds on the canvas until they call it done.

This final example doubles as the generated skill's worked example, so keep the files.

## Step 8 - Write their skill

Generate the user's own skill folder following `references/generated-skill.md`. It must carry:

- `SKILL.md` with frontmatter of **name and description only** - nothing else in the frontmatter, ever.
- Their templates (the Step 3 files, updated with everything learned in Steps 6-7).
- Their references (`references/sources.md` trimmed to this use case, plus anything they supplied).
- The input contract from Step 5.
- Both /design gates: variations before the build, final output on the canvas.
- The taste rule: unclear taste means an AskUserQuestion with concrete options, never a guess.
- The self-improvement clause from `references/self-improvement.md`, baked in as its own reference file.

Ask where their skills live (usually `~/.claude/skills/` or a project `.claude/skills/`) and write it there. Confirm the path back to them.

From now on their use case is one invocation of THEIR skill - this skill's job is done for that use case. If they have a second use case, start again at Step 1.

## Cross-cutting rules

1. **Design system first, always.** No templates, no examples, no generated skill before `design-system/` exists. Values trace to tokens or to an explicit user answer.
2. **Never guess taste.** Density, color energy, mood, type personality, imagery style: unclear means one AskUserQuestion with 2-4 concrete options. Same for brand values.
3. **Variations are structural.** Two layouts that differ only in color are one layout. Every /design gate offers real alternatives with an honest case and tradeoff each.
4. **The canvas is the deliverable, and it is live.** Final output always lands on /design, where the user edits and exports. Every artboard is live HTML/CSS - all text as real editable elements styled with brand tokens, never a flattened PNG or screenshot on the canvas. Generated imagery goes in only as image layers inside an HTML artboard, type kept in HTML on top. Only if /design is unavailable do you fall back to files, and you say why.
5. **Feedback becomes files.** Layout-changing feedback, new references, and hard rules ("never X") get written into the skill's own template/reference/rules files in the same session. See `references/self-improvement.md` - this applies to this skill and to every skill it generates.
6. **Short and plain.** No walls of prose. Report what happened, what is next, and what the user needs to decide.

## Files

| File | Read it when |
|---|---|
| `references/framework.md` | Start of every run - the four-step design framework |
| `references/taste.md` | Any time taste is unclear - the questions and how to ask them |
| `references/self-improvement.md` | Step 8, and whenever the user gives layout-changing feedback |
| `references/sources.md` | Step 4 - reference sites per use case |
| `references/generated-skill.md` | Step 8 - the exact shape of the skill you generate |
| `references/use-cases/carousels.md` | Step 1 picked carousels |
| `references/use-cases/infographics.md` | Step 1 picked infographics |
| `references/use-cases/email-design.md` | Step 1 picked email |
| `references/use-cases/slide-decks.md` | Step 1 picked slide decks |
| `references/use-cases/websites.md` | Step 1 picked websites or landing pages |
| `references/use-cases/dashboards.md` | Step 1 picked dashboards |

## Sibling skills

**design-system-creator** builds the `design-system/` folder this skill requires at Step 2. **firecrawl-brand-extractor** extracts one from a live website when speed matters more than depth.
