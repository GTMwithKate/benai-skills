# Design

Everything here came from real dashboards that looked fine in a screenshot and got rejected the moment somebody read them. This is not taste. Each rule below is a fault that shipped.

**Where this file and `dataviz` disagree, this file wins on typography, layout, card geometry and elevation. `dataviz` wins on colour and on which chart mark answers a question.** They do disagree in three named places, and each one is resolved inline below. Do not average them.

Read the whole file before writing any CSS. Then run the audit at the bottom and paste the result into the chat before you publish. A build that skips the audit ships the same faults again: that has already happened once, with every rule below already written down.

## Contents

- The house style
- The fourteen hard bans
- The one mistake that causes most others
- Fonts
- Typography
- Layout and grid
- Sections
- Cards
- Charts
- Colour
- Icons and logos
- Copy
- Light and dark
- Interactions
- The pre-publish audit

## The house style

The target is a modern developer-platform dashboard. Think of the Vercel dashboard: near-neutral greys, hairline borders, one accent used sparingly, thin geometric icons, tight consistent spacing, and interactions that feel immediate. Clean and technical. Nothing decorative anywhere.

Concretely, that means:

- **Restraint is the default.** A dashboard is an instrument panel. It should look like a tool, not a poster
- **Hairline borders, not heavy ones.** 1px at low contrast against the card fill. A thick ink outline reads as a sticker
- **Elevation by background lift, not by shadow.** A card sits above the page because it is a step lighter or darker, not because it casts a shadow. If you use a shadow at all, make it soft, short and near-black at low opacity
- **Small radius, one value.** 6px or 8px, the same on every card, chip, pill and tooltip on the page
- **A neutral ramp does most of the work.** Page ground, card fill, border, muted text, primary text. Five neutrals and one accent will build the entire page
- **Thin geometric icons.** See Icons and logos. Rounded, chunky or filled icon sets read as cartoonish next to real data
- **Tight, consistent spacing.** Pick a scale of 4px, 8px, 12px, 16px, 24px, 32px and use only those numbers
- **Interactions that respond.** Hover states, a focus ring, a sliding tab indicator, transitions in the 120 to 160ms range. See Interactions

**When the brand supplies a louder treatment.** Some brand kits specify thick outlines, hard offset shadows, or a set of bright pastel fills. Apply that character in light mode, at the quietest setting that still reads as the brand, and hold the house style underneath it: same grid, same spacing scale, same icon weight, same restraint in how many colours carry meaning. Then soften it in dark mode per Light and dark, because a hard light-coloured shadow on a dark ground looks like a rendering fault. Brand character is a layer over this style, not a replacement for it.

"At the quietest setting" needs a number, because otherwise two builders read it differently and both claim compliance. So: a thick brand outline becomes a 1px hairline. A hard offset shadow becomes at most a 4px offset at no more than 12% opacity, in light mode only. A palette of bright tints becomes one tint as the card fill and the rest as section identity. If the brand's own designer would call that too quiet, that is a conversation with the owner, not a licence to turn it up.

## The fourteen hard bans

Break one of these and the page gets rejected. No exceptions, no "but it looks good here".

1. **No text below 14px.** Anywhere. Not labels, not notes, not axis text, not chart labels, not tooltips, not the header. If it does not fit at 14px, the content is too long or the box is too small. Fix that instead.
2. **No horizontal rule under or beside a section name.** The long thin line trailing off a section header is the single most recognisable sign that a machine built the page. Separate sections with space and a bigger heading. Never with a line.
3. **No decorative divider lines at all.** No `border-bottom` under a heading, no `<hr>`, no gradient hairline across the page. Borders belong to cards and tables, where they enclose something.
4. **No transparent cards.** Every card gets a solid fill that differs from the page ground, plus a visible border. A card that is just text floating on the page background reads as unfinished.
5. **No small grey subtitle beside a section heading.** "Acquisition *coming in*". "Retention *going out*". Delete it. The heading is the label. If the reader needs the explanation, the heading is wrong. This ban is about section headings only. A card title row does carry its window, at title size, and that is required rather than banned.
6. **No freshness text in the header.** A string like "fresh Stripe live, mirror 03:47Z, Kit 19 Aug, PostHog live" is nine data points of clutter above the first real number. One icon, with the detail on hover, and nothing more. The report date and timezone are not freshness text and belong in the header.
7. **No narration on a card face.** "The month where the machine is spinning" is a sentence a person writes, not a label. Card faces carry a noun label, a number, a delta, and at most one factual note. Tooltips may contain sentences, because a definition is a sentence.
8. **No badge or pill spam.** At most two status pills on the whole page, and only where the state changes what the reader should do. "FLAT", "NOT COMPARABLE" and "ACTION" on three adjacent cards is noise dressed as signal.
9. **No info marker on every title.** The little dotted-underline hint after each card name becomes wallpaper by the fourth one. Four per page, maximum, counting any marker in the header.
10. **No empty box.** A card with its content pinned to the top and bottom and a void in the middle is worse than a smaller card. Fill the box or shrink the box.
11. **No page without the owner's logo and section icons.** The owner's own logo goes in the header. If you cannot get it, ask for it. Do not silently ship a text wordmark in its place. Every section heading carries an icon.
12. **No italics.** Not for vendor names, not for notes, not for emphasis, not for units. Italics in a data interface look unprofessional and they hurt legibility at small sizes. Carry emphasis with weight or colour.
13. **No serif anywhere.** Not for labels, not for numerals, not as a fallback nobody expected to hit. A serif dashboard reads as a printed quarterly report, which is the opposite of the house style. See Fonts: this ban is broken by accident far more often than on purpose.
14. **No hard offset shadow on a dark ground.** A light or high-contrast offset shadow behind a dark card reads as a double edge, or as a rendering fault. Dark mode gets its separation from background lift and a hairline border. See Light and dark.

## The one mistake that causes most others

**Do not force the page into one viewport height.** `overflow: hidden` with flex rows looks like discipline and is the root cause of nearly every other fault: labels shrink to unreadable sizes, bars compress to slivers, and cards develop voids because a flex row stretched a box with nothing to fill it.

Size the content properly, then let the page be as tall as it needs. Dense and landscape is the goal. A page and a half of vertical scroll is fine. Three screens of scroll is not.

## Fonts

**The font stack must resolve to a face that is actually present.** This is the rule that a real test build broke, and it broke it silently. A brand kit specified Space Grotesk falling back to Montserrat, then Georgia, then serif. External requests are banned, neither brand face was installed, and the entire dashboard rendered in Georgia. It passed every other check in this file and looked like a printed report.

So, in this order:

1. **Embed the brand faces as base64 data URIs** in the file, if the licence allows it. SIL Open Font License and Apache 2.0 faces do allow embedding, which covers most of what brand kits actually specify. Subset to the characters the page uses and to the two or three weights you need, or the file gets large for no reason. This is the best answer: it keeps the brand and it keeps the page self-contained
2. **If the licence does not allow embedding, or you cannot get the files, append a system sans before any serif fallback.** Use `system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`. Then say in the chat that the page renders in a system sans rather than the brand face, and why
3. **Never leave a serif at the end of a stack.** A serif fallback is not a safe default for a dashboard, it is ban 13 waiting to fire on a machine that happens to lack the brand font

Check what actually rendered rather than what you asked for. Read back the computed font family on a heading and on a numeral, and report both. A stack is a wish; the computed value is the fact.

**Verify a trial licence before shipping a display face.** A trial licence does not cover a published page.

## Typography

**Nothing below 14px.** This is ban 1 and it is the most-broken rule in this file, so it appears twice.

| Role | Size | Weight |
|---|---|---|
| Hero number | 48 to 60px | 600 to 700, monospace |
| Section header | 20 to 24px | 600 to 700 |
| Card title | 15px | 600, uppercase, slight letter-spacing |
| Card value | 28 to 36px | 600 to 700, monospace |
| Delta | 15px | 700 |
| Note | 14px | 400 |
| Chart labels and axes | 14px | 400 to 600 |

Title and delta share 15px, and the note sits on the 14px floor. That gives a normal card three sizes: 14, 15 and the value. Weight and colour carry the delta, not size.

Do not push secondary text up to 16px to create hierarchy. A reviewer measured the result and called the cards noticeably chunkier than the target look. 14px is the floor and it is also the right size for a note.

**Three type sizes per card, no more.** The value, 15px for the title and delta, and 14px for the note. A card carrying five sizes reads as a ransom note. If you need a fourth, the card is carrying too much.

**Weight rather than size for hierarchy.** The house style leans on 400, 600 and 700 and almost nothing else. Reaching for 800 or 900 to make something stand out usually means the layout is wrong.

**The monospace face.** No brand kit ever specifies one, so default to `ui-monospace, SF Mono, Menlo, Consolas, "Liberation Mono", monospace` unless the brand names its own. Use it for every numeral, including the hero. `dataviz` prefers a proportional face for a large standalone value; this file wins, because a hero that changes width every morning is worse than one that is slightly wider.

**Contrast, not just size.** Muted grey around `#999` measures roughly 2.8:1 on a light ground and fails accessibility even at a readable size. Use `#666` as the floor on light, and no dimmer than 70% opacity of the ink colour on dark. Fixing size alone leaves half the problem in place.

## Layout and grid

- Landscape. Use the full width before adding another row
- Never a horizontal scrollbar. That is a bug
- Most important number biggest, top left. Money usually
- No tabs inside the data, and no drill-downs. If a number needs a drill-down, the drill-down is a link to the tool that owns it
- Twelve-column grid, and every card spans a whole number of columns. Cards that nearly line up look broken
- Whole page maximum around 1400px, centred, with real margins. Edge-to-edge content on a wide monitor is unreadable
- **Gutters must exceed any shadow offset.** A card shadow that reaches its neighbour looks like a bug. If the brand treatment uses an offset shadow, the column and row gaps have to clear it, and the page padding has to clear it at the right edge

## Sections

Sections are how the page becomes scannable, and they are also where the machine-built look creeps in. So:

- Section heading is an icon plus a word or two, at 20 to 24px
- Separate sections with vertical space, around 40px. Not a line, not a border, not a rule. See bans 2 and 3
- Three to five sections. Six is a sign the page is trying to be two pages
- The heading stands alone on its line. Nothing beside it: no count, no subtitle, no timestamp, no small grey gloss

## Cards

- **Uniform heights inside every row.** Ragged boxes are the loudest visual complaint there is
- Solid fill, hairline border, one radius. The same treatment on every card on the page
- Pin the note line to the bottom with `margin-top: auto`, so cards with different content lengths still align
- Label, value, delta, and at most one note line. No subtitles
- A single number in a large box reads as empty. Give counting metrics two or three windows, such as 24 hours, 7 days and 30 days, rather than padding with whitespace
- **When a metric genuinely has only one window**, and a second would have to be invented, fill the box with factual key and value rows instead: the population, the window, the numerator and denominator, the target. Never invent a second window to fill space. That is ban 10 and "never invent a number" pulling in opposite directions, and the key and value rows satisfy both
- Definitions go in a tooltip on the title, not on the face of the tile, and only on the cards that need one
- Nest small cards in a column beside a large one so rows bottom out level, rather than stretching one card to fill
- The window belongs at the top of the card, in the title row, at title size. Not at the bottom in small grey text

## Charts

Pick the mark from the question, not from variety:

| Question | Mark |
|---|---|
| How does this compare across categories | Horizontal bars, sorted, value labels at the end |
| How has this moved over time | Line, or area for a single series |
| What is the composition of a whole | Stacked bar by default. A donut only for two or three parts whose values are clearly separated |
| How does one value sit against a target | Progress bar or meter, with the target marked |
| Where in a range do things sit | Histogram with real bands |

The part-to-whole row is the second place this file and `dataviz` disagree. `dataviz` defaults to a stacked bar and warns against a donut for comparing close values. That is the better default, so it is the default here. A donut is allowed for two or three well-separated parts, where it reads faster.

Rules that matter more than the choice:

- A part-to-whole mark asserts that the parts sum to the whole. Two independent rates do not, so they are bars, not a donut
- Sort bars by value unless the category has a natural order
- **Value labels sit outside the end of the bar, always.** Never inside the fill for some bars and outside for others depending on length. Mixed placement looks accidental
- Every bar chart gets real axis labels at 14px. A row of unlabelled bars is decoration
- **14px labels need a wide category gutter, so plan for it in the wireframe.** A measured build needed 96px for tenure band labels and 124px for a mini-bar label column, taken straight out of the bar length. That is the cost of the type floor and it is worth paying. Buy the width back by shortening the label text, never by shrinking the type
- Time axes run in date order with dates. An axis of "age in days" counting upward reads backwards
- Meters put the value in the card, not floating in the track, with the target marked on the scale
- **Missing data inside a chart is drawn, never coloured.** Use an unfilled hatch or a dashed outline with a muted stroke, so a gap can never be mistaken for a real low value and no second colour has to be introduced
- Turn off any hover shadow or axis-pointer band. The grey block that appears behind bars on hover reads as a rendering fault
- Charts draw synchronously and re-measure on a `ResizeObserver`. Initialising inside `requestAnimationFrame` means a page opened in a background tab renders no charts at all
- **Draw chart text at 1:1.** A `viewBox` plus `width: 100%` silently rescales 14px text below the floor at some widths. Measure the container and draw at real pixels

## Colour

- **Direction, not sign.** Every metric declares whether up is good, up is bad, or neutral. Colour comes from that declaration. Churn rising is bad even though the number rose
- A confounded comparison renders neutral, with the reason on the card
- Two categories that are not good and bad get an accent and a neutral, not green and red
- **One accent hue for emphasis and progress.** Status colours are a separate, small set and they are allowed on a meter fill when the metric is off target. That is not a second accent. What is banned is decoration: a multi-stop gradient across a progress bar, or a third and fourth hue introduced for variety
- No brand gradient stripe across the top of the page. It was a trend in 2021 and now reads as a template
- **When a brand hands you several pale tints, use exactly one as the card fill**, on every card, and move the others to section identity, such as the icon chip beside each section heading. Four tints spread across the cards reads as colour coding whether you meant it or not: a pink card beside a green one looks like bad beside good
- No pale colour wash carrying meaning. A pale red tile reads as a pink card. Carry status with ink, the border and a glyph
- **Validate the palette with `dataviz` before publishing.** Run the categorical check when the page has a categorical series. When every chart is single-series or a one-hue ordinal ramp, run the ordinal check instead, and record in the audit that you validated it as ordinal and why. Running the categorical check on an accent-plus-grey pair will fail on chroma and tell you nothing

## Icons and logos

This section got ignored on a real build and the page was rejected on sight. It is ban 11.

**The owner's logo.** Top left in the header, at around 24 to 28px, inlined. Ask for it if you cannot find it. A page of somebody's numbers with no mark of whose numbers they are is not finished, and a typed wordmark standing in for a logo is a placeholder, not a solution.

**Thirty three glyphs ship with this skill**, in `assets/icons/`. They are Lucide, ISC licensed, already re-stroked to 1.5px, and they cover what a business dashboard needs: money, people, activity, trend arrows, windows, targets, plugs and the mode toggle. Use them first. They are bundled so the icon rule cannot break on a machine with no web access, which is the failure mode that would otherwise leave a page with no icons at all.

**Icon weight is part of the house style.** Thin, geometric, consistent stroke. Vercel's dashboard uses its own Geist set; the closest freely available matches are [Lucide](https://lucide.dev) at a 1.5px stroke and [Radix Icons](https://www.radix-ui.com/icons), both MIT. [Phosphor](https://phosphoricons.com) is fine at **light** or **regular** weight only. Never bold, never fill: at bold weight it reads as cartoonish next to real numbers, which is exactly the note a real reviewer gave.

Pick one set and use it for the whole page. Mixed sets are visible immediately, so if you need a glyph the bundle does not have, take it from Lucide or Radix rather than mixing in a third set, and re-stroke it to 1.5px.

**Vendor marks.** Real marks, inlined as SVG or a data URI, around 18 to 20px.

- Put the mark on the **section heading** when every card in that section comes from one source. Repeating the same logo on eleven cards is clutter, and it was the one clear fault in an otherwise clean test build
- Put it on the **card** only where cards in the same section come from different sources
- Use the vendor's own brand colour when it stays visible in both modes. When it does not, such as a mark registered in black, or a pale mint that disappears on a light card, use the page's ink token instead and say so. A visible mark in the wrong colour beats an invisible mark in the right one
- **Never a lookalike.** Generic icon libraries frequently hold an entry under a similar name belonging to a different company. Putting the wrong company's mark on someone's dashboard is worse than having no mark
- If a genuine mark cannot be obtained, use a glyph tinted with the brand's own colour, and say in the chat which marks you could not get. Do not hand-draw a coloured rectangle with the company name typed inside it: it reads as a badge, not a logo

## Copy

Dashboard labels, not narration. Nouns over sentences. See ban 7.

- "Failed checkouts", not "signups that did not work out"
- "Price breakdown", not "what members actually pay"
- Section names are plain and by area: Revenue, Retention, Audience, Community. Not "Are we on pace"
- A note line states a fact about the number: its population, its window, or what is missing. It never draws a conclusion or tells a story
- No italics, per ban 12
- No em dashes
- No footnote stacks. One note line, and everything else in a tooltip
- Read every string on the page out loud before publishing. Anything that sounds like a person talking is a label that needs rewriting

## Light and dark

Ship both. Toggled by a segmented control, same data, same structure, same component geometry, same spacing, same radius, same icon set, same grid. Only the surfaces, the ink and the elevation treatment change.

**Elevation is the one thing that must change.** This is a correction to an earlier version of this file, which said to keep the shadow identical across modes. That produced a light hard-edged shadow behind dark cards, and it looked like a fault. So:

- **Light mode** may use a soft shadow, or a hard offset shadow if the brand calls for one
- **Dark mode** separates surfaces with background lift and a hairline border. The card fill is a step lighter than the page, the border is a step lighter again. No offset shadow. If a shadow is needed for a floating element such as a tooltip, make it soft, short and near-black
- Sectioning in dark mode should be subtle. A gentle vertical gradient on the page ground, or a barely-lighter card surface, is the whole effect. If you can clearly see where the separation comes from, it is too strong

Dark tends to be the mode people keep open, so check the data ink there specifically: a pale tint that works on white often falls below contrast on near-black.

**Brand tints in dark.** Fold the card tint into the dark neutral ramp, keeping its hue family, rather than painting a pale pastel onto a dark page. Keep the brand tints at full strength only in small identity spots such as section icon chips.

**Ordinal ramps do not flip direction between modes.** Keep the lightest step on the same category in both, so the reader learns the ramp once. Both directions validate, and a flipped ramp makes dark a different design rather than the same one.

## Interactions

The feel matters, and it is cheap. A page that responds to the pointer reads as a product; a page that does not reads as a screenshot.

- Every interactive element has a hover state and a visible focus ring. Cards that do nothing on click do not get a hover state, because that promises an action that does not exist
- Transitions of 120 to 160ms, ease-out, on colour, background, border and opacity only. Never on width, height or position: layout that animates makes numbers hard to read
- Mode toggle is a segmented control with the active segment filled, and the choice remembered in `localStorage`
- Any tab strip uses a sliding indicator rather than a jumping one
- Tooltips open on hover and on keyboard focus, after about 100ms, positioned so they never leave the viewport. Style them like a card: same fill, same hairline border, same radius, 15px text
- Nothing animates on page load. Entrance animations delay the first number by exactly as long as they run

## The pre-publish audit

Run this before you publish, every time, including after every iteration round. Report it in the chat as a short pass or fail list. Do not publish with a fail.

Grep the file for the mechanical ones rather than eyeballing them.

| # | Check | How |
|---|---|---|
| 1 | No font size below 14px | Grep every `font-size` and every chart `fontSize`. Report the smallest value found. Confirm chart text draws at 1:1 |
| 2 | The font that actually rendered is a sans | Read back the computed `font-family` on a heading and on a numeral. Report both. A stack ending in a serif fails even if the brand face is first in the list |
| 3 | No section rules or dividers | Grep for `<hr`, `border-bottom` and `border-top` outside cards, tables and tooltips |
| 4 | Every card has a solid fill and a border | Grep `background` on the card class. `transparent` and `none` both fail |
| 5 | Owner logo present, every section heading has an icon | Say where the logo came from, or that you asked. Count headings against icons in headings |
| 6 | One icon set, thin or regular weight | Name the set and the weight. Bold or filled fails |
| 7 | Vendor marks correct and correctly placed | Name each vendor, whether the mark is real, its colour, and whether it sits on the section or the card |
| 8 | Two pills maximum, four info markers maximum | Count both |
| 9 | No narration on any card face | Quote any full sentence with a verb on a card face, value, delta or note. There should be none. Tooltips are exempt |
| 10 | No italics | Grep for `italic` |
| 11 | No card with a void | Name the tallest card in each row and what fills its middle |
| 12 | Dark mode elevation is lift, not an offset shadow | Say what separates surfaces in each mode |
| 13 | One radius, one spacing scale, gutters clear any shadow | Report the radius value and the gap values |
| 14 | `dataviz` palette validator run | Say when, which check, categorical or ordinal, and what it returned |
| 15 | No external requests | Grep for `http`, `src=` and `@import` |
| 16 | Both modes render, no horizontal scrollbar at 1440px | Say what you checked in each. Compare `scrollWidth` against `clientWidth` |
| 17 | Every number traces to a real pull | Name anything that does not, and how the page says so |
| 18 | Every supplied ratio recomputed from its inputs | Recompute each rate and average from its own numerator and denominator. If a supplied figure disagrees, say so rather than showing both. See `metric-patterns.md` |
| 19 | Every rate matches the definition it was agreed under | A ratio can recompute perfectly from its own inputs and still use the wrong denominator. Churn over customers at period end recomputes cleanly and is not the definition in `metric-patterns.md`, which is customers at period start. Check the definition, not just the arithmetic |
| 20 | The label on the card matches the definition behind it | Read every card title against what the number actually measures. A card labelled with an agreed definition that carries a different figure is a wrong number, however honest its footnote |

Then look at the page as a reader, not as its author. Render it, screenshot it, and read the screenshot. Every fault in the ban list is visible in a screenshot and invisible in the source, which is why every one of them shipped.
