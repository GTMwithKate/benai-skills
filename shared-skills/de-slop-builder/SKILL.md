---
name: de-slop-builder
description: Build your own personalized de-slop quality gate, an alignment layer that checks AI output before it ships. It interviews you, then generates a complete de-slop skill wired to your standards: the universal checks ship as-is, and your voice, visual, and company-fit layer is distilled from your docs or extracted from your real example outputs when you have no brand guide. It sets up a slop log in one consistent place (an Obsidian vault, a fixed folder, or a Google Doc via MCP), segmented by teammate for a team or a single stream for an individual. Use when the user says "build my own de-slop", "set up de-slop for my company or myself", "personalize the de-slop skill", "create an alignment gate", "make a slop check for my outputs", or wants their own version of the de-slop skill or slop log.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task, AskUserQuestion
---

# De-Slop Builder

This skill builds the user their own **de-slop** gate: the quality layer that checks a finished AI output against a standard before it ships, renders one scorecard table, and logs the run. You are not running de-slop here. You are constructing a personalized copy of it and wiring it to this user's standards.

The point is alignment. Once writing got cheap, the bottleneck moved to verifying that what got written fits the company: its facts, its voice, its taste, its visual system. A de-slop gate makes that standard explicit and checkable, so a whole team can be aligned on what "good" means and catch what does not belong before it leaves the building. For a solo user it does the same job against their own bar.

## The two layers

Every de-slop has two layers, and only one of them is yours to personalize.

1. **Universal layer.** AI writing tells, factual accuracy, internal consistency, leftover artifacts, readability, and the universal craft slice of visual design. These are the same for everyone. They ship verbatim. Do not "improve" them.
2. **Personalized layer.** Voice, the brand slice of visual design, company fit (positioning, offers, facts, audience), and per-channel context profiles. These you generate from the user's standards.

`references/check-inventory.md` is the exact split: which check is universal, which is personalized, and what each personalized one needs as input. Read it first so you know what you are gathering and what you are just copying.

## What you produce

A complete skill folder the user can invoke exactly like the original de-slop:

```
<their-de-slop>/
  SKILL.md                 # generated from assets/SKILL.template.md, wired to them
  references/
    output-format.md       # ships verbatim from assets/output-format.md
    checks/
      ai-writing.md        # universal, verbatim
      factual-accuracy.md  # universal, verbatim
      consistency.md       # universal, verbatim
      artifacts.md         # universal, verbatim
      readability.md       # universal, verbatim
      voice.md             # personalized, you write it
      visual.md            # personalized, you write it (or mark brand-slice not configured)
      company-fit.md       # personalized, you write it
    contexts/
      _template.md         # verbatim
      <profile>.md         # optional, distilled from real examples, added over time
```

Plus a slop log in one consistent location, scaffolded for a team or an individual.

The generated `SKILL.md` must preserve the original flow byte-for-byte in spirit: Step A classify, Step B which checks fire, Step C grade in bundles of three with at most three sub-agents at once each on Sonnet, Step D severity and verdict, Step E the locked scorecard in `output-format.md` with the ✅ / ⚠️ / ❌ states, Step F append to the log. Same emojis, same Source-column mapping, same two-tier suggestions, same hard rules. The only differences are the standard it points at and where it logs.

## Procedure

1. **Read `references/check-inventory.md`** so you hold the universal-versus-personalized split in mind.
2. **Interview** the user with `references/interview.md`. Three things to settle: scope (individual or team), home base (where the log can live consistently), and the source of their standard (existing docs, or real example outputs you will extract from).
3. **Lock the log location** with `references/log-setup.md`. The cardinal rule: the log lives in exactly one place, addressed the same way every run. Settle this before generating, because the generated Step F hardcodes it.
4. **Gather and build the personalized layer.** For each personalized check, either distill the user's docs or extract from their examples. `references/voice-extraction.md` is the method for building a voice profile from diverse real outputs when there is no brand guide. Build `company-fit.md` from a short facts intake. Build `visual.md` from shipped assets, or ship only the universal craft slice and mark the brand slice not configured.
5. **Generate the skill.** Create the folder. Copy the universal checks and `output-format.md` verbatim from `references/assets/`. Drop in the personalized files you just built. Fill `references/assets/SKILL.template.md` with their name, their log path, and team-or-solo, and write it as the generated `SKILL.md`. Create the log from the team or individual template.
6. **Verify.** Ask for one real, recent output and run the new gate on it end to end. Confirm it classifies correctly, fires the right checks, renders the locked scorecard, and appends one entry to the log in the agreed place. Fix any wiring before declaring done.
7. **Hand off.** Tell them the invoke phrase, where the log lives, how the team segmentation works (or that it is a single stream), and how to refresh the standard later (re-run this builder, or edit the personalized files; the universal layer never needs touching).

## Step 1 detail. Scope: individual or team

Ask outright. It changes one thing only: the log.

- **Individual.** The log is a single chronological stream of that person's runs. No segmentation. The supervisory framing does not apply.
- **Team.** The log is segmented by person, each teammate getting their own section with a recurring-pattern summary, under one supervisory read at the top. This is the alignment payoff: an owner can see at a glance who runs the gate, and what keeps showing up in each person's work, so coaching is specific and not a vibe. The segmentation is a logging convention baked into the generated Step F. You never pre-fill it with invented entries. It fills as the team actually uses the gate.

## Step 4 detail. Building the personalized checks

- **Voice (`voice.md`).** If they have a brand voice doc, distill it. If they do not, extract one from real outputs: see `references/voice-extraction.md`. Ask for 5 to 10 diverse, genuinely on-brand pieces across channels (a LinkedIn post, an email, a Slack message, a deck or one-pager, a landing section, a support reply) plus 1 to 2 they consider off, to calibrate the flag side. Diversity is the point: it lets you separate the constant (their voice and values) from the channel. Capture the banned words and hard guardrails too. A no-em-dash rule, if they want one, lives here as a guardrail, not in the universal layer.
- **Company fit (`company-fit.md`).** Distill strategy, positioning, and ICP docs if they exist. Otherwise run the short facts intake in `interview.md`: what they sell and the prices, who they serve and who they explicitly exclude, live versus retired offers, real metrics, domains, and a never-say list. Pull exact values. A wrong price or a retired offer stated as live is the kind of thing this check exists to catch, so the source has to be exact.
- **Visual (`visual.md`).** If they have brand or design guidelines, distill the palette, type, and layout tokens. If not, extract from 5 to 10 shipped assets (thumbnails, slides, a page, a one-pager). If there is no usable visual standard, ship the universal craft slice only (legibility, one clear focal point, alignment, no placeholder art, sufficient contrast) and write in `visual.md` that the brand slice is not configured yet. Never invent a brand system they did not give you.
- **Context profiles (`contexts/`).** Optional and additive. Start with none or one. Each profile is thin and built by distilling real examples of that channel, using `contexts/_template.md`. Tell the user they grow these over time.

## Hard rules

- The universal layer ships unchanged. If you find yourself editing `ai-writing.md`, `factual-accuracy.md`, `consistency.md`, `artifacts.md`, or `readability.md`, stop. Company-specific guardrails belong in the personalized files.
- Settle the log location before you generate. A log scattered across whatever folder they happened to work in is a broken log. One place, addressed the same way every run.
- Never seed the log with fake entries to make it look used. It fills from real runs. An empty log with a clear structure is the correct starting state.
- Distill standards from real examples wherever you can, not from rules written in the abstract. The original voice and context files were built that way and it is why they work.
- Preserve the generated skill's flow, output format, emojis, and Source mapping exactly. The personalization is the standard and the log location, nothing else.
- No em dashes anywhere you write. Use commas, periods, or restructure.
- Generate only what the user gave you a basis for. If a standard is missing and cannot be extracted, mark that check not configured rather than inventing it.
