---
name: reverse-engineer-skill
description: Builds a new Claude skill from examples of finished work instead of written instructions. You give it your best (and ideally worst) examples of an output, such as newsletters, LinkedIn posts, proposals, reports, reels or ad copy. It finds the patterns that separate the good ones from the bad ones, tags each finding as seen, inferred or unknown, waits for your approval, then builds the skill and tests it against your own examples. Use when someone says "reverse engineer a skill", "build a skill from my examples", "turn my best posts into a skill", "learn from my best and worst", "make a skill that writes like these", or shares a folder of examples and wants a skill that repeats what works. Also use it when someone wants to reverse engineer a feature of an app or website: it points them to the open-source REA (Reverse Engineer Anything) repo and turns what REA finds into a skill.
---

# Reverse Engineer a Skill

Build a skill by showing Claude what good looks like, not by describing the steps.

Three steps, one approval:

1. **Gather** good examples of the output, and bad ones if there is data.
2. **Find the winning patterns.** Every finding is tagged seen, inferred or unknown. Stop here and wait for the user to approve.
3. **Build the skill and test it** against examples the analysis never saw.

## When not to use it

This works when the task ends in a clear finished output you can point at. If it does not (email triage, a messy research process, a judgment call with no artifact), say so. Suggest doing the task once with Claude and turning that chat into a skill instead. Do not force it.

## When the example is an app, not a document

Sometimes the "good output" is software: a feature in an app or website you like. Claude cannot read that from a file. The open-source tool for this is **REA (Reverse Engineer Anything)**, an MCP and skill at [github.com/morluto/rea](https://github.com/morluto/rea) (MIT licence). It studies how an app behaves and reports what it found with evidence. It does not copy the source code.

1. **Check whether REA is set up.** If its tools are not available, point the user to the official repo or rea.tools for the setup steps. Let them install it themselves, from those official sources only, then restart their agent.
2. **Have REA investigate**, in the user's words, for example: "Understand how <feature> works in <app>, show me the evidence, and build a similar feature for my project."
3. **Treat REA's report like an analysis.** Tag its findings seen (evidence shown), inferred or unknown, and stop for approval as in step 2.
4. **Then pick what to build.** For a one-off feature, let REA's own workflow build and test it. For a repeatable job, such as "rebuild this kind of feature for each client", build a skill from the approved findings with step 3 below.

Only inspect apps the user is allowed to inspect, and remind them to check the app's terms. Advise against rebuilding a whole paid tool to save its price: maintenance and bug fixing usually cost more than the subscription.

## Hard rules

- **Never invent a reason, number or result.** Every finding carries a tag:
  - **seen**: you can point to it in the examples or their numbers.
  - **inferred**: your best reading of why it worked. Say it is a guess.
  - **unknown**: the examples cannot tell. Say what would settle it.
- **Never build before the user approves the patterns.** The analysis is a checkpoint, not a formality.
- **Copy the shape, never the sentences.** The built skill must not reuse whole sentences from the examples.
- **Keep the examples private.** They stay in the skill's own `references/examples/` folder. Nothing goes anywhere else.
- **Know your metric.** If the number is a mix (a "score", an index), work out how it is built before comparing. The part that moves most is often the real finding.
- **Small is fine.** Three liked examples can build a style skill. Say what the skill can and cannot know from that little.

## Step 1: Gather the examples

Ask only what you cannot find out yourself. Ask it in one message:

1. **What is the output?** One line, for example "my weekly newsletter" or "client proposals".
2. **Where are the examples?** Files, a folder, pasted text, links, screenshots or a connected tool.
3. **Is there a performance number?** For example click rate, replies, reactions per follower, deals won, watch time. If yes, which one counts.

Then pick the mode:

| What the user has | Mode | What to collect |
|---|---|---|
| Their own outputs with numbers | **Performance** | Their best 5 to 10 and worst 5 to 10 by the chosen number |
| No outputs of their own, but a creator or competitor they admire | **Inspiration** | That person's best and worst by public numbers (reactions, views). Credit them, never copy them |
| Outputs they like, no numbers at all | **Style** | 3 to 10 examples they like. No worst set, so the skill learns a style, not what performs |

Rules for a fair comparison:

- **Rank by a rate, not a total**, when audience size changed over time. Click rate beats clicks. Reactions per follower beat reactions. If there is no audience number to make a rate, use the user's metric and say so.
- **Compare like with like.** Same format, same channel, same kind of ask. Drop the odd ones out and say which ones you dropped and why.
- **Hold back one or two of the best examples** for the test in step 3, but not the very best one. Do not read them in step 2. Each test round needs a fresh one. If there are fewer than four best examples, skip the holdout and say the test will be weaker.

Save each example as its own file with its numbers at the top:

```
<new-skill-name>/references/examples/best/01-<short-name>.md
<new-skill-name>/references/examples/worst/01-<short-name>.md
holdout/01-<short-name>.md      outside the skill folder until the test is done
```

Put the numbers in frontmatter: the metric, its value, the date (or the age, if that is all there is) and the format. Images and screenshots go next to the file with the same name. The holdout stays outside the skill folder so the test cannot read its own answer. Move it into `references/examples/holdout/` after the last test round.

## Step 2: Find the winning patterns

Read every best and worst example end to end, images included. Not samples, all of them. If an image or page cannot be read, leave that example out of the format findings and say so.

Compare them on the dimensions that fit this output. Start with these and drop what does not apply:

- **Topic and offer**: what the reader gets.
- **Opening**: the first line or the first three seconds.
- **Structure**: the order of the parts, and where the key element sits (a link, a price, the demo).
- **Length**: in words, slides or seconds.
- **The ask**: how many there are, where they sit, and how they are worded.
- **Tone and voice**: person, warmth, hype words, jargon.
- **Format**: images, lists, line breaks, visual style, pacing.
- **Anything the numbers point at.** If one number barely moves between best and worst but another does, say so. That tells you which part of the output decides the result.

Write the analysis using `references/analysis-template.md`:

- A headline: the one thing that most separates best from worst, with its numbers.
- A table of measurable differences (averages for best against worst), each row tagged.
- Numbered findings grouped by dimension, each tagged seen, inferred or unknown. Count them: "4 of 6 best do this, 0 of 6 worst do".
- Rules you would put in the skill, each traced to the finding numbers behind it.
- Open questions: the unknowns, and what data would settle them.

**Style mode has no worst set.** Describe what the examples share instead: the headline is the style in one line, the table lists shared measures (length, pace, colours, structure) as ranges, and counts read "3 of 3 do this". Things only one example does are options, not rules. Say plainly that the skill will copy a style, not what performs.

Save it as `<new-skill-name>/references/analysis.md`, show the headline and the proposed rules, and **stop**. Ask the user to approve, correct or cut rules. Their corrections beat your inferences. Write a correction into the analysis as **seen (user)**, and an inferred rule they approve unchanged as **inferred (approved)**.

## Step 3: Build the skill and test it

### Build

After approval, build the skill with `references/skill-template.md`:

```
<new-skill-name>/
├── SKILL.md            the steps, hard limits and output shape
└── references/
    ├── analysis.md     the approved findings (from step 2)
    ├── rules.md        the rules, each one traced to its findings
    ├── template.md     the exact output shape to fill in
    ├── check.py        optional: checks the rules that can be measured
    └── examples/       best, worst and holdout
```

- The SKILL.md description says what the skill makes and the phrases a person would use to trigger it.
- Put the single biggest finding at the top of SKILL.md as "the one idea behind every rule".
- Turn **seen** findings into rules. Turn **inferred** findings into rules only when they are **inferred (approved)**. Leave **unknown** findings out, or list them as things to test.
- Write a rule as "always" only when every best example follows it. Otherwise write "usually" and give the count, for example "6 of 8 best".
- If the output has an author, the skill asks for their name and voice instead of borrowing the examples' author.
- Tell the skill to read two best and one worst example before each run, not all of them.
- **Write `check.py` when three or more rules can be measured**, such as a word limit, banned words, a link position or a required section. Plain Python, no extra installs. It prints PASS or FAIL per rule, and the skill runs it on every draft.

### Test

1. **Pick a fresh input.** Use the topic or brief behind a holdout example. If there is no holdout, ask the user for one real upcoming task.
2. **Run the new skill on it in a clean context.** Use a fresh chat or a subagent that only gets the new skill folder and the input. It must not get this conversation.
3. **Score the draft.** Run `check.py` if there is one, then go through every rule and mark it followed or broken.
4. **Compare it with the holdout example** the analysis never saw. Is it the same shape, length and kind of ask? Where is it worse?
5. **Fix the skill**, not the draft, when a rule is broken or the draft misses something the holdout has. Run the test again with a fresh holdout, because the one you fixed against is no longer a fair test. Stop when you run out of fresh holdouts or after three rounds, and report what is still off.

## Output

At the end, report:

1. The skill folder and how to install it: zip the folder, then upload it in Claude under Customize, then Skills. In Claude Code, put the folder in `~/.claude/skills/`.
2. The approved headline finding and the number of rules.
3. The test result: rules passed against total, `check.py` output, and how the draft compared with the holdout.
4. What the skill cannot know yet (the unknowns), and what data would improve it.

## Worked example (short)

Someone wanted a better newsletter skill. They gave Claude their 6 best and 6 worst newsletters, ranked by click rate. The analysis found that opens were almost the same for best and worst, but clicks from people who opened were far higher for the best (**seen**). So the body and the ask decide the result, not the subject line (**inferred**, approved). The best emails also reached the link sooner and were shorter (**seen**). The built skill wrote shorter emails, put the link earlier and held back part of the content for the click. A word count and link-position check went into `check.py`.
