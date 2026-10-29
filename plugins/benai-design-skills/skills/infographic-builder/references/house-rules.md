# House rules

Every rule here started as a correction on a real infographic. The first version of this
kit had footers on the quote cards, boxes around everything, decoration where restraint
belonged, and a decision tree whose arrows floated near the boxes instead of joining them.
Knowing why a rule exists is what lets you apply it to a layout nobody has built yet.

These rules are about composition, not colour. Colour and type come from the user's
brand.json and are never hardcoded.

## The ground

**Never default black or default white.** The grounds come from the brand's own surface
colours. A brand with warm surfaces gets a warm near-black dark ground and a warm
off-white light ground; a cool brand gets cool ones. Pure `#000` or pure `#FFF` reads as
a default, not a decision, so when a design system only defines one ground, derive the
other from it rather than reaching for absolute black or white.

**Type.** The display font carries anything with weight, the body font carries prose, the
mono font carries numbers, times and code. All three come from brand.json. Sentence case
for every headline. Title Case reads as a press release. ALL CAPS is allowed only in a
short overline at 12 to 14px with wide letter-spacing.

**No em dashes anywhere.** Restructure the sentence, or use a period, a comma or a colon.

## Colour

The brand accent pair does the highlighting: `@ACCENT@` for fills, `@ACCENT2@` for the
strongest emphasis. `@SUCCESS@` and `@DANGER@` exist for meaning that is genuinely
success or danger, never as decoration.

Accents are highlighters, not paint. If an accent dominates a composition, rebalance.
When you squint you should see three tones: the ground, the ink strokes, one accent pop.

**Watch for accent on accent.** A numeral in the accent colour sitting on a band filled
with the same accent disappears. This went out publicly once. Any element sitting on a
coloured band takes `@NUMC@` or `@INK@`, never the same accent as the band. When you want
to mark a band as the payoff, give it a soft fill plus an accent left edge rather than
flooding it with the accent.

## The quote card

**Avatar, name, handle, text. Nothing else.**

No footer, no wordmark, no logo, no highlighted words. The claim is the whole design, and
every extra element competes with it. This is the most frequently violated rule because a
footer feels like polish; on a card whose only job is one sentence, it is clutter.

The boxed variant, which adds a before-and-after table under the claim, is the one
exception: it carries the brand mark alone, tucked into the bottom right corner. Still no
wordmark line.

## The teaching formats

Cheat sheets and decision trees earn more furniture because they have more to say. Even
so:

**Rules, not boxes.** Hairline rules separate sections. Panels, cards and stacked borders
make a layout read as boxy and loud, especially in dark mode where a 2px light border is
the brightest thing on screen. Keep the full `@BOX@` border for elements that are
genuinely objects: the boxes in a flow chart, a logo tile.

**Treat every section the same.** If four sections sit under a rule and the fifth does not,
the fifth reads as broken even when nobody can say why. Consistent rhythm is most of what
makes a dense layout feel designed.

**Numbering is a numeral, not a chip.** A 42px figure in `@NUMC@`. A box drawn around a
number is decoration around something that was already doing its job.

**The domain (`@SITE@`) sits small and quiet in the top right**, in mono, at 15px. It is
attribution, not branding. The quote cards carry none at all.

## Dark mode

Dark is not light inverted. It gets its own treatment, closer to how Vercel and Apple
handle dark surfaces. `build.py` derives most of this from the brand automatically:

- Section rules are gradient hairlines that fade out to the right, not flat lines.
- Box borders drop to 1px at about 30% opacity.
- Connector lines in a flow chart stay at full strength. A flow chart with faint arrows is
  just a list.
- Logo tiles, when used at all, stay on the light surface colour. That is what lets a
  near-black mark read.

Light and dark come from one source file. This is not a convenience; the two drifted apart
when they were separate files and a copy fix landed in one and not the other.

## Flow charts

**Lines must touch both boxes.** The first decision tree drew short arrows floating in the
gap between elements, and it read as a list with decoration rather than a chart. Draw
connectors as absolutely positioned rules that span the full gap, with the arrowhead
sitting on the line end so it meets the next box.

**Every branch lands on something.** A NO that exits to a loose numbered circle leaves the
reader hunting. Point it at the actual outcome card.

## Numbers and facts

**Never invent one.** A figure in an infographic becomes somebody's fact tomorrow, and it
travels further than the caption that hedged it. Where a real number belongs but you do not
have it, put a visibly bracketed slot such as `[0h]` and say so at handover. A row of
bracketed slots looks deliberate. A fabricated percentage looks fine right up until someone
asks where it came from.

## Sizes

| Format | Canvas | Use |
|---|---|---|
| Quote card | 1080x1080 | One claim, for X and LinkedIn |
| Teaching formats | 1080x1350 | Cheat sheet, decision tree, layered stack |

Body copy never drops below 14px at 1080 wide, because these get read on a phone at a
third of that. If the copy will not fit above that floor, the layout is carrying too much:
cut a section rather than shrinking the type.

## Before you hand it over

- Run `scripts/check.py`. It catches clipping in both the real font and the fallback.
- Look at the rendered PNG. Mechanical checks do not catch accent on accent, and they do
  not catch a brand accent that is too light to carry emphasis on this ground.
- **Publish the canvas with at least two directions.** Never hand over a single PNG as the
  first output. The canvas is where the user compares, edits in place and leaves a note
  saying why, and skipping it turns every change into a round trip through you.
- Say which numbers are placeholders.
