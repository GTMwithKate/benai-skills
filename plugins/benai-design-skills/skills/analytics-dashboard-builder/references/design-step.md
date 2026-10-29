# The /design step

Before writing any dashboard code, open a design canvas with the `/design` command and present the layout as two or three distinct variations, side by side on one canvas.

## Why

It is the cheapest review round available. The user sees the real hierarchy, the card proportions and the length of the copy while all of it is still free to change. Describing a layout in prose gets agreement that evaporates the moment they see the page. And showing one layout gets a shrug where showing three gets a decision: a single option can only be accepted or rejected, while options expose what the user actually cares about.

## What each variation is

One artboard per variation, all on the same canvas so they compare at a glance. Each is a wireframe-fidelity mock of the whole page: section bands, cards with their spans, chart placeholders, labels at real length. No polish, no final palette — structure only, so the round stays cheap.

Make the variations differ in structure, not in colour:

- a different section order or grouping
- a different hero: which number gets the big card
- a different density: fewer large cards versus more small ones

Two variations that differ only in accent colour are one variation shown twice, and they waste the round.

Label each artboard (A, B, C) and give each a one-line trade-off in the chat, so the user can answer with a letter.

## Rules

**No invented numbers.** Placeholders stay visibly blank: underscores or grey blocks. A mocked figure gets believed, then quoted, then defended.

**Missing data looks missing.** A shaded or clearly distinct block for an unconfirmed source, never something that reads as a real zero.

**Landscape, at dashboard width.** If a layout does not fit a landscape artboard it will not fit a screen either, and that is useful information now rather than after the build.

**A header strip on every variation**, carrying the real date (from the machine, not from memory) and one freshness stamp per source.

## The pick

The user picks a variation, or asks for a mix of two. Apply their edits on the canvas and iterate. Expect two or three rounds; they are cheap rounds. Move to code only once the user says the picture is right.

## After the build

The canvas comes back at step 10. Edit rounds with the owner run through `/design`: put the built page's current state on the canvas, let them mark what to change, apply the change, then republish the live page in place. Using the same tool for planning and for editing means the owner never has to describe a visual change in prose.

## Fallback

If the `/design` command is not available on the current surface, fall back to monospace box-drawing wireframes in fenced code blocks, one per variation, same rules: landscape, blank placeholders, a header strip. The gate does not change either way: two or three structural options, the user picks, agreement before any code.
