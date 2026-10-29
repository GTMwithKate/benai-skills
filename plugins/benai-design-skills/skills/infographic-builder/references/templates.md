# The template kit

The finalized templates live in `assets/kit/`. Every colour, font and identity string in
them is a token that `scripts/build.py` resolves from the user's brand.json, so the same
composition renders in any brand. The sample copy inside each template is exactly that,
sample copy: replace all of it with the user's material.

To see what a template looks like before committing to it, build the kit with the user's
brand and render a quick PNG:

```bash
python3 scripts/build.py --src assets/kit --out /tmp/kit-preview --brand <brand.json>
python3 scripts/render_png.py /tmp/kit-preview CheatSheetLight --out /tmp/preview.png --scale 1
```

Looking at the picture takes seconds and prevents the usual mistake, which is forcing a
teaching layout onto a one-line idea that wanted a quote card.

## Choosing

| If the input is | Reach for | Because |
|---|---|---|
| One claim, an opinion, a confession | **Quote** | The claim is the design. Anything else competes with it |
| A claim plus proof, a before and after | **QuoteBoxed** | The table under the hook does the proving |
| A method, a stack, a set of rules | **CheatSheet** | Five numbered blocks, each a different shape, so it stays scannable |
| A rule the reader applies to their own case | **DecisionTree** | Questions down, outcomes out to the side |
| A pipeline or an argument with layers | **Stack** (build from CheatSheet) | Bands with arrows showing which way the work flows |

## The templates

### Quote
`assets/kit/Quote.dcxt.html` -> `QuoteLight`, `QuoteDark`

1080x1080. Avatar, name, handle, three short paragraphs. No footer, no logo, no highlighted
words. Roughly 64px display type, so the copy has to be tight: three lines of eight to
twelve words each is the shape that works.

Use it when the post's hook is strong enough to stand alone. If you find yourself wanting
to add a bullet list, you picked the wrong template.

### QuoteBoxed
`assets/kit/QuoteBoxed.dcxt.html` -> `QuoteBoxedLight`, `QuoteBoxedDark`

1080x1080. The same header, a heavier headline, then a bordered card holding a two-column
table with an 8px offset shadow. Built for before-and-after, was-mine versus runs-itself,
old way versus new way. Carries the brand mark alone in the bottom right corner (dropped
automatically when the brand has no mark).

Three rows is the sweet spot. Four fits. Five crowds it.

### CheatSheet
`assets/kit/CheatSheet.dcxt.html` -> `CheatSheetLight`, `CheatSheetDark`

1080x1350. Five numbered blocks, deliberately different shapes so the eye keeps moving: a
four-column rule grid, a stepped ladder with an accent rail, a data table with a chip
column, a bare logo row, and a three-column bullet strip. Gradient hairlines between
sections, no panels or cards.

This is the saveable format. It is also the one most likely to overflow, so run
`check.py` and expect to trim.

Reuse the block shapes freely. They are the vocabulary, not a fixed script: a build with
three blocks is fine, and a block can be swapped for a different one from the same set.

### DecisionTree
`assets/kit/DecisionTree.dcxt.html` -> `DecisionTreeLight`, `DecisionTreeDark`

1080x1350. Questions run down the left in a spine, each NO branch exits right onto its own
outcome card, YES continues down. Outcome cards carry real app logos.

Three or four questions is the limit. Past that the spine gets thin and the outcome cards
get squeezed. If the logic needs more, it is two infographics.

The connectors are absolutely positioned rules with CSS-triangle arrowheads, built so the
line touches both boxes. Keep that if you rebuild it; floating arrows are what made the
first version fail to read as a chart.

### LogoLibrary
`assets/kit/LogoLibrary.dcxt.html` -> `LogoLibraryLight`, `LogoLibraryDark`

1080x1350. A reference sheet of every mark in the library. Useful to show someone what is
available, and as a check that the logo engine still renders after a change. Not a posting
format.

## Building a layout the kit does not cover

Compose from the pieces rather than starting blank. The bands in a layered stack, the
tinted ladder in the cheat sheet, the outcome cards in the decision tree: these are
interchangeable. Copy the closest template, gut the middle, and keep the header, the
footer and the tokens.

If what you build turns out well, promote it. See `improving-the-kit.md`.

## Tokens

`build.py` resolves these from brand.json, per theme. One source therefore yields both
modes. The full list, so a hand-built layout can use them too:

| Token | What it is |
|---|---|
| `@GROUNDBG@` | Page background. Flat on light, faint gradient on dark |
| `@INK@` `@MUTED@` | Primary and secondary text |
| `@LINE@` `@HAIR@` | Full-strength stroke, and the quiet hairline |
| `@BOX@` | Complete border shorthand. 2px ink on light, 1px soft on dark |
| `@RULE@` `@RULE2@` | Gradient section rule, and the heavier header rule |
| `@CARD@` `@PANEL@` `@PANEL2@` | Surface fills, plain to tinted |
| `@ACCENT@` `@ACCENT2@` | Accent fill and accent emphasis |
| `@SUCCESS@` `@DANGER@` | For genuine success and danger only |
| `@ONACCENT@` | Text colour that is safe on the accent fill |
| `@NUM@` `@NUMC@` | The section numeral style, and a numeral colour safe on any band |
| `@SHADOW@` | Offset shadow colour |
| `@DISPLAYFONT@` `@BODYFONT@` `@MONOFONT@` | The three font stacks |
| `@FONTLINK@` | The Google Fonts stylesheet URL for those stacks |
| `@AUTHOR@` `@HANDLE@` `@AVATAR@` | The person on the quote cards |
| `@SITE@` | The quiet domain attribution on teaching formats |
| `@BRANDMARK@` | The brand's small mark, per mode. Empty means the element is dropped |

`<!--OUT:Light=Foo,Dark=Bar-->` at the top of a source renames the two outputs.
