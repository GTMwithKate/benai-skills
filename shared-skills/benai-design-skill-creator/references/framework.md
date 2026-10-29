# The design framework

Every design output - and every skill this skill generates - follows the same four steps, in order. The order is the method: each step exists because skipping it produces a predictable failure.

## 1. Find the design system

Look for a `design-system/` folder in the working directory or project root. This is the output shape of the design-system-creator skill: a tokens file (colors, type, spacing, radii, shadows), foundations files, component patterns, logo assets, and usage rules.

If no design system exists, stop and route the user:

- Run the **design-system-creator** skill to build one.
- Run the **firecrawl-brand-extractor** skill on their website to extract one fast.

Never guess brand values. No design system and no answer from the user means you ask. A wrong hex code is worse than a question - and inside a reusable skill, a wrong hex code repeats forever.

## 2. Collect references and templates

Gather 1 to 3 examples of what good looks like for THIS specific output. Ask the user for links or files first (their references outrank anything researched), then research examples that match their product and goal. Never design from zero context.

For skill creation, this step also builds the starter templates: 2-4 layouts in the user's brand, every value resolved from their tokens.

## 3. /design to plan - always with variations

Before building the final thing, use the /design command to open a design canvas and present **2 to 3 distinct variations** side by side. Each variation differs in structure - hierarchy, composition, grouping - not just color. Include light and dark when the use case calls for it. Give each option an honest case and its main tradeoff, then say which you would pick, so the user pushes back on a recommendation instead of facing a blank decision.

This step is mandatory. Do not skip it, even for "quick" requests. A wrong layout found on a canvas costs one round; a wrong layout found after the build costs the build.

**Hard rule - live artboards, never flattened images.** Every artboard placed on a /design canvas is live HTML/CSS: all text is real, clickable, editable elements styled with the brand tokens. Never put a PNG or screenshot on the canvas as the deliverable - a canvas of flattened images cannot be edited, which defeats the entire human-in-the-loop point of the gate. Generated imagery (photos, illustrations, AI-generated art) may appear only as image LAYERS inside an HTML artboard, with the type kept in HTML on top of it.

## 4. Final output on the /design canvas

Build the picked variation, then put the finished output on a /design canvas - as live HTML/CSS artboards, per the hard rule above, never as flattened images. **The canvas is the deliverable.** The user edits any element directly there - click to select, inline text edits, notes - and exports the final asset (PNG/PDF) from the canvas. Apply feedback in small rounds on the canvas; before exporting, re-read the canvas, because the user's edits are newer than yours.

Only if /design is unavailable do you deliver files directly, and you say why the canvas was skipped.

When the user approves, state exactly where everything was saved - and write down anything they taught you along the way (see `self-improvement.md`).
