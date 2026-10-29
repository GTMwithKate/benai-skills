---
name: analytics-dashboard-builder
description: 'Builds one business analytics dashboard from the tools a business already pays for, then writes a companion skill and scheduled task so it refreshes itself every morning. Covers the path: interview the owner on what matters, audit which connectors respond, shortlist the data points that drive decisions, agree a layout as a wireframe, build a self-contained page in their branding with light and dark modes, deploy it to a live shareable URL, have a second agent audit the design before anyone sees it, iterate until the owner is happy, then set up the daily refresh. Use this skill whenever someone wants a dashboard, a business overview, a morning report, or KPIs and metrics in one place, wants to "see my whole business", is tired of opening many tools to work out what is happening, asks to connect Stripe or Circle or YouTube or Google Analytics to see their numbers, or wants an existing dashboard to update itself on a schedule. Use it even when they only describe the problem and never say the word dashboard.'
---

# Analytics dashboard builder

Take someone from "I open sixteen tools every morning and still cannot tell you how the business is doing" to one page that answers it, and that rebuilds itself before they wake up.

## How to talk while running this skill

Short. Plain words. Simplified Technical English, the ELI5 kind. One idea per sentence. Active voice.

The owner of a hardware shop is not an analyst and does not want a briefing. Ask one question, wait. Report what you did, whether it worked, and what they need to decide next. Nothing else.

When you need a decision, give two options maximum, the context needed to pick fast, and which one you would go with. Keep file paths, URLs and numbers exact. Cut everything else.

Verbose output was the loudest complaint from the first real run of this skill. A wall of prose after every step makes an owner stop reading, and an owner who stops reading cannot hold up a gate.

## The shape of the work

Eleven steps. Each one is a gate: get agreement, then move.

Skipping a gate is how dashboards end up with forty tiles nobody reads, and how numbers end up on a page nobody can defend. A gate is a question you asked and they answered. Deciding they would probably say yes is not a gate, and it is the specific failure the first run made twice.

## Why the order matters

Most people jump to charts. That fails predictably. A chart with no agreed metric is decoration. A metric with no reachable source is a wish. A source with no daily refresh is a screenshot. A dashboard nobody agreed the layout of gets rejected on sight, after all the expensive work is done. And a page published without a review round gets rejected on its design, which is the cheapest thing to have fixed and the most annoying to find at the end.

So: decide what matters, find out what is reachable, agree the picture, build, let a machine review it, let the owner review it, then automate.

## The steps

### 1. Environment check

Establish where this is running and what it can reach, before promising anything.

- Which surface: Claude on the web, Cowork, or a local terminal
- Which connectors respond right now. Call them, do not read the docs and assume
- Which sources will only ever work locally
- **Whether the scheduler on this surface can carry these connectors.** This is a different question from whether the sources answer now, and it is the one that actually bites. A scheduled run wakes up as a fresh session. If it cannot see Stripe, it fails every morning at seven

Test the last point rather than assuming it. On a surface where scheduled runs cannot carry connectors, say so now and offer the alternatives: a local schedule on their own machine, or a manual run of the refresh skill. Finding this out after the page is built means step 11 produces a job that looks scheduled and is not.

### 2. Interview

Read `references/interview.md` before starting.

Work top down: the one number they would look at every morning, then what moves it, then the functions underneath. One question at a time. No fixed question count. Keep each question to one or two lines.

The interview is over when both sides could independently describe the same dashboard and arrive at the same numbers. Close with a short read-back and get a yes.

### 3. Direction

Output broad categories with candidates in brackets. Nothing else, at this stage:

```
- Revenue (MRR, quarterly revenue, net profit, failed payments)
- Retention (churn rate, cancellations, churn by tenure)
- Audience (subscribers, last video performance, email list)
```

No sources, no chart types, no reasoning. The point is to agree the shape of the page before tools get a chance to narrow it. Iterate until they say yes.

### 4. Connector deep dive

Read `references/connectors.md`.

Probe every tool that step 3 implies. Record, per source: the exact call, the shape that comes back, its freshness lag, and any cap on the pull. Recommend a meta connector for the awkward ones, accept native connectors, and stay read only throughout.

### 5. Options table

One table. Three caps, and they interact, so state all three to the user at once:

- **Offer fifteen to twenty rows.** Never forty. A table nobody reads cannot be filtered, so the pre-filtering is the skill's job, not the user's
- **Tick five to fifteen as your recommendation**, and count the ticks before you send it
- **If the user states their own cap, your recommendation fits inside it.** Ticking sixteen rows against a stated cap of fifteen wastes a round

| Column | Purpose |
|---|---|
| Section | How the page groups |
| Metric | The number |
| Connector | Where it comes from |
| Chart | How it gets shown |
| Window and comparison | What period, measured against what |
| The decision it drives | The cut test, stated per row |
| Confirmed | Yes if pulled and seen, no if unreachable, partial if incomplete |

Sort by section, money first. Anything unreachable goes in its own block at the bottom with the reason, never quietly dropped.

`references/metric-patterns.md` holds the must-know versus nice-to-know test that decides what earns a row.

### 6. Layout

Read `references/wireframe.md`. Present the layout as a monospace box-drawing wireframe in a fenced code block, landscape, before writing any code.

This is the cheapest review round available: the user sees the real hierarchy, the card proportions and the copy length while everything is still free to change. Iterate to agreement.

State the date source in the wireframe header. See the date rule below, because a wireframe header a day behind the real date has already happened.

### 7. Brand

Ask, in this order:

1. Do they have brand guidelines or a brand kit? Use them.
2. A brand but no written guidelines? Extract the palette from their website and get as close as possible.
3. Neither? Ask for two or three references they like and build a scheme from those.

Ask for their logo as a file or a URL, in every one of the three cases above. It goes in the header of the page. If they cannot supply one, say plainly that the page will carry a text wordmark until they do, rather than shipping the placeholder quietly.

Always produce light and dark. Dark tends to be the one people actually keep open, and it needs its own elevation treatment rather than the light one inverted. `references/design.md` carries that.

**When the requested branding is not their own.** If they ask for another company's logo, name or typeface on a page of their own numbers, stop and ask what the page is for. There are legitimate answers: a client demo, a white-labelled report, an agency deliverable, a mock for a pitch. There is also the case where the page will circulate as though that company produced it, which misrepresents whose business the numbers describe.

So: ask, do not assume, and do not quietly comply. If it is a demo or a client deliverable, use the mark and say so on the page. If they cannot say what it is for, do not put another company's mark on it, and offer their own branding or a neutral scheme instead. Check the licence on any display typeface before shipping it: a trial licence does not cover a published page.

### 8. Build

Read `references/design.md` and follow it rather than improvising. It opens with the house style, which is the look to aim for: a modern developer-platform dashboard, near-neutral, hairline borders, thin geometric icons, one accent, interactions that respond. Clean and technical, never decorative. Invoke the `dataviz` skill and read it before choosing any chart mark or fixing any palette. Then `references/deploy.md` for publishing.

`dataviz` is not optional and it is not a footnote. On the first real run of this skill it was skipped, its own colour validator was never run, and the exact colour-vision fault the design file warns about shipped to a live page. Run it before you publish, not after somebody asks.

The build is a single self-contained page with the data separated from the render, so changing one number changes its chart with no other edit.

Before you publish, run the pre-publish audit at the bottom of `references/design.md`, all twenty checks, and report the result in the chat as a short pass or fail list. Do not publish with a fail.

### 9. Self review by sub-agent

Read `references/self-review.md`.

Before the owner sees anything, hand the page to a fresh sub-agent and have it review the page against `references/design.md`. It runs the twenty point audit, screenshots both modes and reads the screenshots, checks every number against the agreed metric list, and returns findings with a PASS or FAIL verdict.

You fix what it finds. Then you spawn a new reviewer, not the same one, and go again. Loop until the verdict is PASS.

Three rules make this work, and they are all in the reference file:

- **The reviewer is blind.** It gets the file, the design rules and the agreed metrics. Not your reasoning and not what you were going for
- **The reviewer never edits.** It reads and reports. You make every change
- **Every finding cites a rule, or it is labelled taste.** Rule-backed findings enter the fix loop. Taste gets forwarded to the owner at step 10 as options. This is what stops the loop running forever

Three rounds maximum on the same finding. If it survives three, take it to the owner with both positions in a line each.

You cannot review your own page. You read your intention instead of the pixels, which is exactly how every design fault this skill has shipped got past the agent that built it.

### 10. Review with the owner, and iterate

This is a gate, and it is the step the first run of this skill did not have.

Step 9 already cleared everything a rule can catch, so this round is about the things only the owner knows: whether the page answers their question, whether it looks like their business, and whether they would open it tomorrow. Start by handing them the sub-agent's TASTE list as options, in one short message.

Publishing is not finishing. Show the owner the live page and ask directly whether the layout, the type sizes, the icons, the colours and the copy are right. Then fix what they name, republish in place, and ask again. Loop until they say it is done.

Read `references/review.md`. It carries the questions to ask, how to run a round without breaking the data, and the faults to look for yourself before you ask.

Expect three to six rounds. This is the longest step in the skill by wall-clock time and that is correct: it is the step that decides whether the page gets used or closed. Do not treat a round as a setback or apologise for it.

Two things to do yourself at the start of every round, before you ask the owner anything:

- **Look at the rendered page.** Render it, screenshot it, and read the screenshot. Every design fault that has ever shipped from this skill was visible in a screenshot and invisible in the source
- **Re-run the audit.** A fix in round two commonly reintroduces a fault that passed in round one

Do not move to step 11 until they say the page is right.

### 11. Ask about updating, then write the refresh skill

Two questions, both asked, both answered, before any file is written. The first run of this skill skipped both and simply built a scheduled job. It worked, and it was still wrong: nobody had said yes.

**Question one: do you want this updating on a schedule?**

- **Yes:** go to question two.
- **No:** say plainly that everything needed to build the updater has been captured, and offer to write the skill anyway so they can run it by hand or schedule it later. A skill they run manually is still worth having, because it is what holds the metric definitions.

**Question two: where should the schedule live?**

Give them the two options and a recommendation. Step 1 already established which of these actually works here, so lead with that.

- **A cloud schedule**, run by the platform. Fires whether or not their machine is on. Only works if every required source is reachable from a fresh session with no local credentials, which step 1 tested
- **A local schedule** on their own machine, such as cron. Reaches anything their laptop can reach, including local files and local credentials. Needs the machine awake at the scheduled time, and a missed run happens at next launch instead

Then read `references/refresh-skill.md` for what the child skill has to carry. Author it with the `benai-skill-creator-skill` bundled in this plugin, and see the note under Companion skills about making sure you load that copy.

**Install the child skill somewhere that survives.** A skill written into a container path dies with the container, and a skill on a git branch is not installed. Ask the owner where their skills live and put it there. State the final path in your close-out report, and say plainly whether a future session will find it. This is a required line in the report, because the first run left the skill in two places and neither of them persisted.

Then report: where the dashboard lives, where the skill is installed, whether that path survives, what the task is called, whether the schedule is cloud or local, and what needs one manual run so connector permission prompts get approved once rather than stalling an unattended run at 8am.

## Rules that hold at every step

These are the ones that, when broken, produce a number somebody acts on, or a mess somebody has to undo.

**Never invent a number.** A missing figure renders as a card stating what is missing and why. Not a placeholder styled at the size and weight of a real value. An honest blank prompts a fix; a plausible wrong number prompts a decision.

**Numerator and denominator come from the same population.** This is the single most common source of a wrong rate. If the numerator counts people who cancelled and the denominator counts subscriptions, the rate is meaningless and will look plausible.

**Flows have to close.** Members at period start, plus new, plus reactivated, minus churned, equals members today. If that line does not add up, one of its terms is wrong. This check catches more errors than every other one combined, so run it before publishing and put the working on the page's tooltip.

**Read only, always.** Billing systems, email platforms and communities are production. There is no figure on a dashboard worth the risk of a write, and a mistake there is not recoverable by editing a file. At the end, give a straight accounting of every call that changed any state anywhere, including connection records and permission grants, without waiting to be asked.

**When a source cannot support an agreed definition, re-open the definition.** Do not ship the nearest thing you can compute with a footnote admitting the gap. If step 2 agreed revenue net of discounts and the source has no discount field, go back to the owner with the two honest options: ship list price under a different label, or leave the card blank until the data exists. Their call, not yours. A card labelled with the agreed definition and carrying a different number is a wrong number, however honest the footnote.

**Ask before writing to a repository.** Committing, branching or pushing is a visible act in someone else's project and it is not implied by "build me a dashboard". Ask where files should live before you write any, and never open a pull request unless they asked for one. On the first run a branch was pushed before git had been mentioned at all.

**Get the date from the machine, not from your head.** Read the real current date and the owner's timezone, state both in the header, and use them everywhere. A header one day behind is the kind of small wrongness that makes an owner distrust every other number on the page.

**Check significance before calling something a finding.** Two rates a few points apart on samples in the low hundreds are noise. Drawing noise in red and green asserts a conclusion the data cannot support.

**State the population on the card.** Every count carries what it counts. "667 members" and "756 subscriptions" describing the same business is not a contradiction if both say which they are, and is a bug if neither does.

**Correct yourself out loud, immediately.** If you notice you miscounted, misread a field or broke one of these rules, say so in one line and fix it. Every self-caught error on the first run was worth more than the thing it corrected.

## Reference files

| File | Read it when |
|---|---|
| `references/interview.md` | Step 2, before the first question |
| `references/connectors.md` | Step 4, and again at step 1 for reachability |
| `references/metric-patterns.md` | Step 5, and again at step 8 before computing anything. Definitions, the cut test, and the traps that produce wrong numbers |
| `references/wireframe.md` | Step 6 |
| `references/design.md` | Step 8, before writing any CSS, and again before every republish for the audit |
| `references/deploy.md` | Step 8, for publishing and updating in place |
| `references/self-review.md` | Step 9, every round of the machine review |
| `references/review.md` | Step 10, every round with the owner |
| `references/refresh-skill.md` | Step 11 |
| `assets/icons/` | Step 8. Thirty three Lucide glyphs, ISC licensed, already at the 1.5px stroke the design file requires. Use these before fetching anything |

Read `metric-patterns.md` twice, as the table says. Reading it once at step 5 and working from memory at step 8 is how a definition drifts between what was agreed and what was built.

## Companion skills

**Bundled with this plugin:**

- `benai-skill-creator-skill`, the BenAI skill creator. Use it at step 11 to author the refresh skill, rather than writing one by hand. Run its **Build** branch: the dashboard build that just happened in this chat is exactly the "task you just finished" it extracts from, so the refresh skill gets built from what actually happened rather than from memory. It keeps the result small, modular and single-purpose, which is the shape a refresh skill needs. Ignore its Plan branch here; the task is never "just an idea" by step 11.

  A container often has a generic `skill-creator` already installed, and the Skill tool may load that one instead of this plugin's copy. Check which copy you loaded. If it is not this plugin's `benai-skill-creator-skill`, read this plugin's copy from disk and follow it, because this is the version the plugin pins.

**Built into Claude, so always available:**

- `dataviz`. Required at step 8, before any chart mark or palette is chosen. Its colour validator catches pairs that collapse under colour-vision deficiency, and pale tints that fall below contrast on a dark ground. Both have shipped on a real dashboard because this skill was treated as optional.

**Useful if the user happens to have it:**

- `design-system-creator`, when they have a brand but nothing written down.

Everything else this skill needs is in its own reference files, deliberately. A build that assumed a missing skill would be present once improvised the entire design layer and got it wrong, so the references carry the rules directly rather than pointing at something that may not be installed.
