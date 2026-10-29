# Use case: infographics

One dense single image that carries a claim or teaches a method. **1080x1080** for a single claim, **1080x1350** for anything that teaches. Body copy never drops below 14px at 1080 wide - these get read on a phone at a third of that. If the copy will not fit above that floor, cut a section rather than shrinking the type.

**Build light AND dark from one source file.** The two modes drift apart the moment they are separate files - a copy fix lands in one and silently misses the other. Dark is not light inverted: hairlines soften to gradients that fade right, box borders drop to ~1px at ~30% opacity, but flow-chart connectors stay full strength (a chart with faint arrows is just a list).

## Starter templates to offer (pick 2-4 by taste)

| Template | Use when | Limit |
|---|---|---|
| **Tweet-style quote card** | One claim, an opinion, a confession strong enough to stand alone | Avatar, name, handle, three short lines (8-12 words each) - nothing else. No footer, no logo, no highlights: every extra element competes with the claim. Wanting a bullet list means wrong template |
| **Boxed quote + proof table** | A claim plus proof, before/after, old way vs new way | Two-column table under the headline; three rows is the sweet spot, four fits, five crowds it. May carry the brand mark alone, bottom right |
| **Cheat sheet (dense "a lot happening")** | A method, a stack, a set of rules - the saveable format | Numbered blocks in deliberately different shapes (rule grid, stepped ladder, small table, logo row) so the eye keeps moving. Most likely to overflow - check fit before showing it |
| **Decision tree / flowchart** | A rule the reader applies to their own case | Questions run down a spine, each NO exits right to an outcome card, YES continues down. 3-4 questions maximum; more is two infographics |
| **Card grid** | 4-9 uniform items (tools, rules, mistakes) | Scannable and even; the boring-reliable option. Breaks when items are unequal in weight |
| **Visual-led** | One central diagram or image does the teaching | Minimal copy around it; breaks when copy creeps back in |
| **Icon-heavy with real tool logos** | Stacks, workflows, comparisons naming real apps | Every named app shows its REAL mark (see logos below) |

Every color, font, and identity string in a template is a token resolved from the design system - never hardcoded. Fold in any logos or reference images the user supplies.

## Composition rules (each one was a correction on a real infographic)

- **Never default black or white grounds.** Grounds come from the brand's surface colors; when the system defines only one mode, derive the other from its hue - pure black or white reads as a default, not a decision.
- **Accents are highlighters, not paint.** Squint and you should see three tones: ground, ink, one accent pop. Watch for **accent on accent** - a numeral in the accent color on a band filled with the same accent disappears; anything on a colored band takes ink or a safe numeral color.
- **Rules, not boxes.** Hairline rules separate sections; panels and stacked borders read boxy and loud, worst in dark mode. Full borders only on genuine objects: flow-chart boxes, logo tiles.
- **Treat every section the same.** One section without the rule the others have reads as broken. Consistent rhythm is most of what makes a dense layout feel designed.
- **Numbering is a numeral, not a chip.** A large figure in a safe color; a box around a number is decoration.
- **Connectors must touch both boxes**, with the arrowhead on the line end. Floating arrows stop reading as a chart. Every branch lands on an actual outcome card.
- Sentence case everywhere. ALL CAPS only in a short overline at 12-14px with wide letter-spacing.

## Real logos - never redrawn

If the infographic names an app (Gmail, Slack, Notion, Claude...), it shows that app's real vector mark, pulled live from the **svgl.app API** (`https://api.svgl.app?search=<name>`). A drawn approximation always looks slightly wrong, and the brand owner is the one who notices.

- **Size by height, not width** - many marks are not square (Gmail is 512x399); setting both dimensions squashes them.
- **Prefer bare marks over tiles.** A grid of light tiles on a dark ground reads loud; tiles only when marks sit on a busy surface and need separating.
- **Near-black marks (Notion, X, GitHub) vanish on dark grounds** - fall back to that brand's single-color glyph drawn in the dark theme's ink. That is correct behavior, not a bug.
- **No published vector?** A bordered name chip at the same height as its neighbors - matching the height and rhythm makes it read as deliberate. Say at handover which marks are chips.
- Marks name the tool; they never imply endorsement.

## Brand adaptation via tokens

First run: map the design system's tokens into the kit's brand slots by role (ground, ink, muted, hairline, card, panel, accent, accent-strong, on-accent, semantic pair, shadow, three font stacks, author identity, domain). Derived values (muted mixed from ink, dark ground tinted from the light hue) are fine - name them as derived at handover so the user can correct them. **Inventing the primitives is not fine: no design system and no user answer means stop and ask.**

When the brand is light-only, derive dark honestly (near-black tinted toward the light ground's hue, accent lightened until it reads), tell the user dark was derived, and put both modes on the canvas so they can react.

## Overflow and the dual-font check

Check every artboard for content overflowing its frame **in the real webfont AND the fallback font** - PNG export cannot embed webfonts, so a layout that only fits in the webfont clips on export. Then look at the render yourself: mechanical checks catch clipping, not accent-on-accent or a brand accent too pale to carry emphasis on this ground.

## Reading the input

The user rarely says "build me a decision tree". They hand over a post, a link, or a sentence. The deciding question: **does the image repeat the claim, or show the mechanism?** Repeating the claim is a quote card; showing the mechanism is a cheat sheet, tree, or stack.

- **LinkedIn or X copy** - the hook is the quote card (lift it nearly verbatim; it was already written to stop a scroll). A numbered list or tool stack in the body is the cheat sheet; an if-this-then-that rule is a decision tree.
- **A YouTube link** - fetch the transcript before designing; a visual built from a title is a guess. Look for the diagram the creator drew in words, and for the "most people do X, and that is why it fails" beat. Numbers in a transcript are real and quotable; numbers you infer are not.
- **A Reddit post** - Reddit rewards the mechanism and punishes anything that reads as an ad. Prefer teaching formats, keep branding to the quiet domain line.
- **A raw brief** - ask what the reader should do differently after seeing it. "Agree with me" is a quote card, "apply this to their case" is a decision tree, "know the pieces" is a cheat sheet. Too thin to answer that means ask one question, not invent substance.

## Copy rules

Infographic copy is not post copy: shorter, and every line has to survive thumbnail size.

- One idea per block; a comma-spliced second thought means split or cut.
- Concrete nouns: "Monday numbers" beats "reporting workflows".
- A cheat-sheet body line is one sentence, around twelve words. A quote-card paragraph is 8-12.
- **Never invent a number** - a figure in an infographic becomes somebody's fact tomorrow, and it travels further than the caption that hedged it. Where a real figure belongs and you do not have it, use a visibly bracketed slot like `[0h]` and name it at handover. A row of bracketed slots looks deliberate; a fabricated percentage does not.
- A stat quoted from an older source is worth flagging for a re-check before posting.

## /design delivery

**Variations gate (mandatory):** 2-3 genuinely distinct concepts - the reliable pair is one that puts the **claim** on screen (quote card: stops the scroll, teaches nothing alone) and one that draws the **mechanism** (cheat sheet, tree, stack: stands alone and gets saved, but gives the answer away). Light and dark of each, one row per concept, a note above each row with its case and tradeoff, then your pick and why. A set where only your favourite gets an argument is a rigged vote.

**Final delivery** on a /design canvas; the user edits there and exports the PNG from the canvas at 2x scale, which stays sharp after platforms recompress it. Re-read the canvas before exporting - the user's edits are newer than yours.

**Live artboards only.** Every artboard is live HTML/CSS - headers, blocks, table cells, chips all real editable text on brand tokens. Never place a flattened PNG on the canvas as the deliverable. Logos and any generated or user-supplied images go in as image layers inside the HTML artboard, type kept in HTML on top.

## References and self-improvement

Reference sources for infographics (engagement-sorted feeds, explainer-guide archives, editorial benchmarks) are in `../sources.md` - show the user 3-5 at Step 4.

**This file improves itself.** When the user materially reworks a layout on the canvas, that change is worth more than one post: re-tokenize their concrete values and fold the change into the shared light+dark source. New references and hard rules ("never X") get written into this file - or the generated skill's own files - in the same session, then say what changed.
