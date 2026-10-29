# Brand kit (step 2)

One kit styles all three stages: title cards, motion clips and captions. Collect it once, save it as `brand.json` in the project root, and read it in every later run.

## What to ask
| Setting | Ask for | Default |
|---|---|---|
| Canvas | background colour for full-frame cutaways | `#E9E7E2` |
| Ink | main text colour | `#0B0B0B` |
| Surface | card and panel colour | `#FFFFFF` (on dark footage `#F4F2EE`) |
| Accent | one accent colour | `#FF5A1F` |
| Heading font | Google Fonts name | Geist (bundled in `engine/fonts/`) |
| Mono font | code, file names, terminals | Geist Mono (bundled) |
| Caption style | frosted pill or bold pill | frosted pill |
| Logo | file in `motion/inputs/` | none |

## Where the kit goes
- Motion: write the kit into `motion/brand.css` as CSS variables (`--bg --ink --muted --accent --card --line --font`). Every film reads them. Add any other tokens the design system has (body font, tints, `on-tint`, a dark ground); the list is a minimum. Type sizes for video come from `references/motion-principles.md`, not the design system's page scale. For a non-Geist font, put the files in `motion/fonts/` and add an `@font-face` there.
- Remotion (edit, captions): write the kit into `src/lib/brand.ts` and import it in every composition. Values in the reference files are examples only.

## Rules
- Never use pure `#000` for a background. Use the ink colour.
- One accent. No gradients on UI parts, no glows.
- If the project has a design project folder (made by `benai-design-setup`), take the kit from its `design-system/` (README, `tokens.json`, fonts, logos) and follow the use case's `feedback.md` and `examples/`. Otherwise "our design system" means the brand's Design System artifact: list them with Artifact `list`, `type` "Design System", and read its `project/README.md` and `project/tokens.json`. Copy its fonts into `motion/fonts/`.

