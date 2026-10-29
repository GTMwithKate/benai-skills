---
type: reference
status: active
tags: [de-slop-builder, voice, extraction]
---

# Voice extraction from real examples

For the common case: the user has no written brand voice, but they have shipped plenty of work they consider on-brand. You build `voice.md` by distilling it. This is the same method that produced the original voice and context files, and it works better than asking someone to describe their own voice in the abstract, because almost nobody can.

## Why diversity matters

Ask for outputs across different channels and audiences, not six versions of the same thing. The reason is mechanical. Any single piece blends two things: the constant (who they are: their voice, their values, their taste) and the variable (the channel: a LinkedIn post is short and hooky, an email is longer, a Slack message is casual). Give yourself one channel and you cannot tell which is which. Give yourself a LinkedIn post, an email, a Slack message, a proposal, and a support reply, and the constant is whatever survives across all of them. That constant is the voice. What changes between them is the register, which becomes the per-channel context profiles later.

Aim for 5 to 10 on-brand pieces and 1 to 2 the user considers off. The off ones are not filler. They tell you where the line is, which is what a flag needs.

## What to pull out

Read across the whole set and write `voice.md` from what is actually there. Do not import these as headings blindly; capture what the examples show.

1. **Voice DNA.** One or two lines naming who they sound like. The original is "the friend who failed first and figured it out." Yours might be "the operator who shows the receipts" or "the calm expert who never oversells." Find the through-line, the stance the writer takes toward the reader across every sample.
2. **The mix.** Roughly what the voice is made of, in proportions. Vulnerability versus authority versus encouragement. Plain language versus domain language versus technical terms. This keeps the grader from flattening the voice into one note.
3. **Register by audience.** How the voice shifts between external marketing, internal docs, and 1:1 messages. Each shift becomes a line here and, if it earns its own profile, a file in `contexts/`.
4. **Banned words and guardrails.** The strongest signal in the off examples and the absences in the good ones. What do they never say. Hype words, corporate filler, AI vocabulary, specific phrasings they avoid. If they want a hard no-em-dash rule, it lives here. A single banned word in outward copy should be a finding, so list them explicitly.
5. **Signature moves.** The recurring patterns in the good set. A particular hook shape, a "most people do X, the few do Y" structure, crediting sources by name, ending on a short aphorism. These are what Aligned looks like, and their absence is a soft flag.
6. **The pulse.** What makes their writing feel alive rather than clean-but-dead: first person where it fits, a real opinion, varied sentence rhythm, an admission of what is hard. Name the markers so the grader can flag soulless copy even when it breaks no rule.

## Build the two examples

End `voice.md` with two real, short examples pulled from what they gave you:

- **On-profile.** A genuine, on-voice piece, with one or two lines on why it ships.
- **Off-profile.** A weak one (theirs if they gave you an off example, otherwise the same idea rewritten wrong), with what is wrong called out: the banned words, the missing signature move, the wrong register.

These two examples do more work than any list of adjectives. They are the calibration the grader leans on.

## Values fall out of this

The user framed this as an alignment skill, and values are part of voice extraction, not a separate exercise. What a company refuses to say, what it leads with, who it includes and excludes, what it treats as proof: those are values, and they show up in the writing. Capture them. The voice profile and the company-fit profile together are the standard everyone aligns to.

## If they truly have almost nothing

A brand-new solo user with two or three pieces. Extract what you can, write a thin `voice.md`, and say plainly in the file that it is provisional and built from a small sample. Tell the user to re-run the builder once they have more shipped work. A thin honest profile beats a thick invented one.
