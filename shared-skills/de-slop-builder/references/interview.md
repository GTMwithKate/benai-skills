---
type: reference
status: active
tags: [de-slop-builder, interview]
---

# Interview

Three things to settle, in order. Use AskUserQuestion for the choices. Keep it short. You are gathering inputs for three personalized files (`voice.md`, `visual.md`, `company-fit.md`) and the log location. Nothing else needs their time.

## 1. Scope

> Are you setting this up for yourself, or for a team?

- **Individual.** The log is a single stream of your runs. No segmentation.
- **Team.** The log is segmented by person, each with a recurring-pattern summary under one supervisory read. Get the roster: names of the people who will use the gate.

This decides which log template you use and how the generated Step F is written. It changes nothing else.

## 2. Home base for the log

Hand off to `references/log-setup.md` for the full decision. The short version of what to ask:

> Where do you work day to day? Do you keep an Obsidian vault, a fixed project folder, or should the log live in something cloud like a Google Doc?

Detect before you ask where you can: look for an `.obsidian` folder, a `.git` repo, a stable working directory. The rule you are enforcing: the log must live in one consistent place addressed the same way every run. Settle this now, because the generated skill hardcodes it.

## 3. Source of the standard

For each of the three personalized files, the user is in one of two situations. Ask per area, because most people have some docs and not others.

> For each of these, do you have a written doc, or should I work from real examples? Voice and tone. Visual or brand guidelines. Strategy, offers, and audience.

### If they have docs
Get the location: a vault path, a folder path, a Google Drive link, or pasted text. You will distill them. Confirm they are current.

### If they have no voice doc
Collect real outputs and extract. Ask for **5 to 10 diverse pieces they consider genuinely on-brand**, spread across channels and audiences:

- a LinkedIn or social post
- a customer or prospect email
- an internal Slack or chat message
- a deck, one-pager, or proposal
- a landing-page or website section
- a support or community reply

Then ask for **1 to 2 they consider off**, so you can calibrate what a flag looks like, not just what good looks like. Diversity matters: it lets you separate the constant (their voice and values) from the variable (the channel). One LinkedIn post tells you their LinkedIn format. Six pieces across six channels tell you who they are. Method is in `references/voice-extraction.md`.

### If they have no visual doc
Ask for **5 to 10 shipped designed assets** (links or screenshots): thumbnails, slides, a page, a one-pager, an ad. You will extract palette, type, and layout tokens. If they have no designed output at all, ship the universal craft slice only and mark the brand slice not configured.

### Company facts intake (always, short)
Whether or not they have a strategy doc, confirm the canon with a quick pass. These are the values the Company-fit check will catch errors against, so they have to be exact:

- What do you sell, and the exact prices.
- Who is the audience, and is there anyone you explicitly do not target.
- Which offers are live, and which are retired (so the gate flags a retired one stated as live).
- Your real, current metrics worth checking copy against (subscriber or user counts, and similar).
- Your domains, and any that are not yours.
- A never-say list: claims, words, or framings that are off-brand or off-strategy for you.

## After the interview

You should now have: scope and roster, a locked log location, and for each of the three personalized files either a doc to distill or a set of examples to extract from. Proceed to build (SKILL.md Step 4), then generate (Step 5).
