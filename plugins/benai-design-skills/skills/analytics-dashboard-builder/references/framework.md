# The design framework

Every skill in this plugin follows the same four steps. Follow them in order.

## 1. Find the design system

Look for a `design-system/` folder in the working directory or project root. This is the output shape of the design-system-creator skill: a tokens file (colors, type, spacing, radii, shadows), component patterns, and usage rules.

If no design system exists, offer the user three paths and let them pick:
- Run the **design-system-creator** skill to build one.
- Run the **firecrawl-brand-extractor** skill on their website to extract one.
- State their brand colors and fonts directly in chat.

Never guess brand values. No design system and no answer from the user means you ask. A wrong hex code is worse than a question.

## 2. Collect references

Gather 1 to 3 examples of what good looks like for THIS specific output. Ask the user for links or files, or research examples that match their product and goal. Never design from zero context.

## 3. /design to plan — always with variations

Before you build, use the /design command to open a design canvas and present **2 to 3 distinct layout variations** side by side. Each variation should differ in structure, not just color. The user picks one (or asks for a mix).

This step is mandatory. Do not skip it, even for "quick" requests.

After the build, use /design again for edits: put the built output on the canvas and iterate there with the user.

## 4. Iterate, then finish

Apply the user's feedback in small rounds. When the user approves, export the final asset and tell them exactly where it was saved.
