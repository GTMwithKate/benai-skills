---
type: reference
status: active
tags: [de-slop-builder, inventory]
---

# Check inventory: universal vs personalized

This is the split. It decides what you copy and what you build. Read it before the interview so you gather the right inputs and waste no time personalizing things that are the same for everyone.

## The nine checks

| Check | Layer | Ships how | Needs from the user |
|---|---|---|---|
| AI writing tells | Universal | Verbatim | Nothing. Same for everyone. |
| Factual accuracy | Universal | Verbatim | Nothing. Verified against the world. |
| Consistency | Universal | Verbatim | Nothing. Internal coherence only. |
| Artifacts | Universal | Verbatim | Nothing. Leftover junk is leftover junk. |
| Readability | Universal | Verbatim | Nothing. The universal clarity slice. |
| Visual (craft slice) | Universal | Verbatim, inside `visual.md` | Nothing. Legibility, focal point, alignment, contrast, no placeholder art. |
| Voice | Personalized | You write `voice.md` | A voice doc, or diverse example outputs to extract from. |
| Visual (brand slice) | Personalized | You write the brand half of `visual.md` | Brand or design guidelines, or shipped assets to extract from. |
| Company fit | Personalized | You write `company-fit.md` | Strategy and ICP docs, or the short facts intake. |
| Completeness | Universal mechanism | No file, graded against the ask | Nothing. Always available, fires only when a clear ask is in context. |

Context profiles (`contexts/`) are personalized and optional. They are per-channel shapes distilled from real examples, added over time. Start with zero or one.

## Why these five (plus craft) are universal

They do not depend on who the company is.

- **AI writing tells.** Significance inflation, AI vocabulary, chatbot artifacts, the rule of three, em-dash overuse, and the rest are properties of the text, not the brand. One nuance below.
- **Factual accuracy.** World-truth. Whether a claim is true does not change by company. Whether it matches the company's own numbers is a different check (Company fit), and that one is personalized.
- **Consistency.** Self-contradiction and numbers that do not add up are internal to the document.
- **Artifacts.** Placeholders, model meta-comments, dead links, broken structure. Junk for anyone.
- **Readability.** The universal slice of clarity: can a reader parse it on the first pass. Taste and whether it sounds like the brand is the Voice check, which is personalized.
- **Visual craft slice.** Is it legible, is there one clear focal point, is it aligned, is contrast sufficient, is there no leftover placeholder art. These are design hygiene. The palette, the fonts, the exact tokens, the surfaces are the brand slice, and that is personalized.

## The one universal-file nuance: em dashes

The universal `ai-writing.md` treats em dashes as **overuse**, a soft tell, the standard humanizer position. Some brands ban them outright. That hard "zero em dashes" rule is a company guardrail, so it belongs in the personalized `voice.md`, not in the universal file. When you build `voice.md`, ask whether they want a hard no-em-dash rule and, if so, record it there. Do not edit the universal file to add it.

## Why these four are personalized

They are the company.

- **Voice.** Who they sound like, the register per channel, their banned words and guardrails, their signature moves. This is the densest personalization and the one most often missing as a written doc, which is why `voice-extraction.md` exists.
- **Visual brand slice.** Palette, type, layout tokens, and the surfaces they design for. Grade one surface by another surface's rules and you are wrong, so the profile has to name the surfaces.
- **Company fit.** Positioning and the facts canon: offers, prices, metrics, audience and who is excluded, live versus retired offers, domains, the never-say list. Exact values, pulled not paraphrased. This is where a wrong price or a dead offer gets caught.
- **Completeness.** The mechanism is universal (does it do the job the ask asked for), but there is no standard file. It grades against the ask itself, so nothing to personalize and nothing to ship.

## What this means for the interview

You are gathering inputs for exactly three personalized files: `voice.md`, `visual.md`, `company-fit.md`. Everything else is copy-paste. Spend the user's time there, and only there.
