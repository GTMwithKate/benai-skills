# Taste discovery

A design system fixes the brand values. It does not fix the taste decisions inside one use case: how dense, how loud, how playful, how photographic. When any of those are unclear, ask - never guess. A guessed taste produces a template the user tolerates; an asked taste produces a template they keep.

## How to ask

Use the AskUserQuestion tool. One question per axis, 2-4 concrete options each, and only the axes the current decision actually needs (usually 1-3 of them, not all five). Concrete means the option describes what they would see, not an adjective. "Minimal" is an adjective; "lots of white space, one idea per screen, small type" is an option.

If the design system's foundations already answer an axis (a voice file that says "quiet and technical" answers mood), do not re-ask it.

## The five axes

### Density
How much lives on one artboard?
- **Airy** - one idea per view, generous space, the eye rests
- **Balanced** - a headline plus 3-5 supporting elements
- **Dense** - a lot happening: grids, tables, many labeled parts, built to be saved and studied

### Color energy
How hard does color work?
- **Quiet** - near-neutral surfaces, one accent used sparingly
- **Confident** - accent carries hierarchy, tinted panels, clear color blocking
- **Loud** - saturated fields, high contrast, color is the composition

### Mood
What should it feel like in 3 seconds?
- **Technical** - precise, engineered, hairlines and mono details
- **Warm** - human, friendly, soft shapes
- **Editorial** - magazine-like, type-led, opinionated
- **Playful** - unexpected angles, humor allowed

### Type personality
What does the type say before anyone reads it?
- **Neutral workhorse** - clean sans, disappears behind the content
- **Characterful display** - a headline face with opinion, quiet body
- **Editorial serif** - serif-led, reads as considered and written
- **Mono/technical** - code-adjacent, systems energy

### Imagery style
What fills the visual slots?
- **Photography** - real photos of real people/products
- **Pure design-system** - shapes, tokens, type, and color only; no imagery
- **Icons and logos** - icon-led, real app marks where tools are named
- **Illustration** - drawn elements in a consistent style

## When to ask

- **Step 3 (starter templates)**: ask the axes the use-case file flags as open. Build templates only after the answers.
- **Step 6 (variations)**: if the user's canvas feedback contradicts an earlier answer ("too empty" after picking Airy), ask a one-line follow-up rather than silently flipping.
- **Inside generated skills**: bake the answered axes into the skill's rules file as defaults, and keep the rule that any NEW unclear taste question gets asked with AskUserQuestion, not guessed.

## What is never a taste question

Brand colors, fonts, and logos. Those come from the design system or an explicit user statement - they are facts, not preferences, and there is no option set to offer. Missing brand values route back to the Step 2 gate.
