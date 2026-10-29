---
name: infographic-builder
description: Produce an on-brand infographic in YOUR brand from whatever the user has, LinkedIn copy, a YouTube link, an X or Reddit post, a newsletter, or a one-line idea. Builds on a kit of finalized, brand-adaptive templates (quote card, cheat sheet, decision tree) that render with real multi-colour app logos in light and dark, adapts them to the user's design system on first run, presents layout variations on a design canvas, and exports the winner as a PNG. Use this skill whenever the user wants a visual, graphic, image, infographic, quote card, cheat sheet, decision tree or diagram to go with a post, or says "make a visual for this", "turn this video into an infographic", "what image should go with this post", "design something for LinkedIn", "graphic for X", or "image for the Reddit post". Also use it when a post has been written and the next obvious step is the image, even if the user has not asked yet.
---

# Infographic builder

## What this produces

A finished, on-brand image for social, in the user's brand. Two canvas sizes cover
everything:

- **1080x1080** for a quote card, the unit that carries a single claim.
- **1080x1350** for anything that teaches: a cheat sheet, a decision tree, a layered stack.

Every template exists in light and dark. Both come from one source file, so a copy fix in
one mode cannot silently miss the other.

The kit carries no brand of its own. Every colour, font and identity string in the
templates is a token, resolved at build time from a `brand.json` generated from the user's
design system. The workflow below follows the four steps in `references/framework.md`;
read that file first if you have not.

## Step 1: Find the design system, and adapt the kit to it

Look for a `design-system/` folder in the working directory or project root (the output
shape of the design-system-creator skill).

**First run for this user** (no `design-system/infographic-brand.json` yet): generate it.
Read `references/brand-adaptation.md` and follow it: map the design system's tokens into
the brand.json schema, derive dark mode honestly if the system is light-only, build the
whole kit once with the new brand, look at the rendered PNGs, then save the file to
`design-system/infographic-brand.json`. This is the step that turns the neutral templates
into the user's templates, and every later run inherits it.

**No design system at all?** Offer the user three paths and let them pick:

- Run the **design-system-creator** skill to build one.
- Run the **firecrawl-brand-extractor** skill on their website to extract one.
- State their brand colours and fonts directly in chat.

**Never guess brand values.** No design system and no answer from the user means you ask.
A wrong hex code is worse than a question. The bundled `brand.default.json` is a grayscale
pipeline-test placeholder, not a fallback brand: nothing built from it goes to the user as
a deliverable.

**Every run after that**: the saved brand.json is picked up automatically by the scripts.
Skip straight to step 2.

## Step 2: Collect references and read the input

Gather 1 to 3 examples of what good looks like for this specific output, from the user or
from research into their product and audience. Never design from zero context.

Then read the actual input. `references/inputs.md` maps each kind of input (post copy, a
YouTube link, a Reddit thread, a raw brief) to a template and tells you what to pull out
of it. If a YouTube link comes in with no transcript, fetch one before designing; a visual
built from a title is a guess.

`references/templates.md` is the catalogue: what each template is for, and the limit where
it stops working.

**Write the artboard copy before you touch the layout.** Infographic copy is not post
copy. It is shorter, and every line has to survive being read at thumbnail size. Sentence
case, no em dashes, and no invented numbers. Where a real figure belongs but you do not
have it, put a bracketed slot such as `[0h]` and say so at handover, because a note here
becomes somebody's fact tomorrow.

Read `references/house-rules.md` before you build anything. Every time. It is short, and
every rule in it was a correction on a real infographic.

## Step 3: /design to plan, always with variations

**This step is mandatory. Do not skip it, even for "quick" requests.**

Before building the final asset, invoke the `design` skill and put **2 to 3 genuinely
distinct layout variations** on one canvas for the user to pick from. Distinct in
structure, not in shade: the reliable pair is one concept that puts the **claim** on
screen (quote card) and one that draws the **mechanism** behind it (cheat sheet, decision
tree, or stack). Four variants of the same layout in slightly different colours is not a
choice.

To produce the variations:

```bash
python3 scripts/new_project.py --template Quote --into <working-dir>
# edit <working-dir>/src/Quote.dcxt.html  (repeat for the other concepts)
python3 scripts/build.py --src <working-dir>/src --out <working-dir>
python3 scripts/check.py <working-dir>
```

`new_project.py` copies a template plus the brand into a working folder; never edit
`assets/kit/` in place for a one-off job. `build.py` resolves the brand tokens for both
modes and swaps the logo tokens for real app vectors (`references/logos.md` covers the
logo engine). `check.py` reports any artboard whose content overflows its frame, in the
real webfont and in the fallback font, since PNG export does not embed webfonts. Then look
at it yourself: a layout can pass every mechanical check and still have the accent sitting
on the same accent.

The artboards `build.py` produces are already `.dc.html` files, which is exactly what the
canvas takes, so pass them through as they are. Lay the canvas out so comparison is easy:
one row per concept, light and dark side by side, and a sticky note above each row
carrying its case and its tradeoff. Give each option an honest case and its main tradeoff,
then say which one you would use and why, so the user has a recommendation to push back on
rather than a blank decision. A set where only your favourite gets an argument is a rigged
vote.

## Step 4: Iterate, then finish

Apply the user's feedback in small rounds, on the canvas, where they can also edit
elements themselves and leave notes. Before exporting, re-read the canvas: the user may
have edited it, and their version is newer than yours.

Export only what they pick:

```bash
python3 scripts/render_png.py <working-dir> QuoteDark --out ~/Downloads/name.png
```

Scale 2 is the default and gives 2160x2700 for a 1080x1350 artboard, which stays sharp
after LinkedIn recompresses it. Tell the user exactly where the file was saved, and name
any bracketed placeholder numbers still in the copy.

## When the user reworks a layout

If the user materially changes a layout on the canvas, that change is worth more than the
one post. Read `references/improving-the-kit.md` and promote it: read their saved canvas,
diff it against what you generated, re-tokenize their concrete values, and fold the change
into the source template so light and dark stay together and the template stays
brand-portable. Then say what you promoted. Cosmetic edits (a word swap, a nudged margin)
stay local.

## Scripts

| Script | What it does |
|---|---|
| `scripts/new_project.py` | Copy a kit template plus the brand into a working folder |
| `scripts/build.py` | Render sources to light and dark artboards, resolving brand and logo tokens |
| `scripts/check.py` | Report overflow in both the webfont and the fallback font |
| `scripts/render_png.py` | Screenshot one artboard to PNG through headless Chrome |
| `scripts/add_logo.py` | Pull a real app vector into the kit's logo library, or list what is there |

## References

| File | Read it when |
|---|---|
| `references/framework.md` | The four-step method every skill in this plugin follows |
| `references/brand-adaptation.md` | First run for a user, or their brand changed |
| `references/templates.md` | Choosing a template, or checking what the kit already covers |
| `references/house-rules.md` | Before building anything. Every time |
| `references/inputs.md` | Turning a link, a post or a brief into a template choice and copy |
| `references/logos.md` | Placing app logos, or an app is missing from the library |
| `references/improving-the-kit.md` | The user reworked something, or you built a layout worth keeping |

Siblings in this plugin: **design-system-creator** and **firecrawl-brand-extractor** feed
this skill its brand; **carousel-builder**, **visuals-builder** and **email-design** cover
the formats this one does not.
