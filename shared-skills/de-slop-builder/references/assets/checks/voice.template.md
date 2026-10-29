---
type: check
layer: 2-company
status: active
last-refreshed: {{DATE}}
source: distilled from {{VOICE SOURCE: their brand voice doc, or the example outputs listed in voice-extraction}}. Re-run de-slop-builder to refresh.
---

# Check: voice

Does it sound like {{NAME OR ORG}}, in the right register for where it lives. Not whether it is true (Company fit) or how it looks (Visual). Also load the matching `references/contexts/` profile if one exists, the per-channel shape lives there. Flag and suggest.

## Voice DNA

{{One or two lines naming who they sound like, the through-line stance toward the reader across every sample. Example shape: "the operator who shows the receipts." Pull this from the examples, do not invent it.}}

{{The mix, in rough proportions: how much vulnerability vs authority vs encouragement; how much plain language vs domain language vs technical terms. Keeps the grader from flattening the voice to one note.}}

## Register by audience

{{One line per audience the examples revealed. Typical set:}}
- External marketing: {{how the voice reads in public-facing content}}
- Internal docs: {{same voice applied to notes and SOPs}}
- 1:1 messages: {{the personal register, if it differs}}

{{Any fixed convention: a newsletter sign-off, a DM having no sign-off, and similar.}}

## Banned words and guardrails

{{The hard rules. A single one is a finding. Pull these from what the off examples did and the good ones never do.}}

- {{Hype words they avoid}}
- {{Corporate filler they avoid}}
- {{AI vocabulary they avoid, on top of the universal ai-writing list}}
- {{If they want a hard no-em-dash rule, state it here. This is the one place that rule lives.}}

## Off-voice tells (Misaligned)

{{The specific failure shapes for this brand: wrong hook type, guru energy, hard sell where it does not belong, wrong register for the channel, jargon with no story, no pulse.}}

## Grading

- Aligned: right register for the audience, reads like {{NAME OR ORG}}, real pulse, zero guardrail breaks.
- Drift: on-voice but flat, or a hedge that should be cut. No hard break.
- Misaligned: a banned word, guru energy, sycophancy, or the wrong register for where it lives.

## On-profile example

{{A real, good, on-voice piece from their set, with one or two lines on why it ships.}}

## Off-profile example

{{A real weak one, or the same idea rewritten wrong, with what is off called out: the banned words, the missing signature move, the wrong register.}}
