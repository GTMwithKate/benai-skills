# business-analytics

Build a business analytics dashboard from the tools you already pay for, then keep it updating itself every morning.

## What it does

One skill, `analytics-dashboard-builder`, walks the whole path:

1. **Environment check.** What can actually be reached from here, and what only works locally.
2. **Interview.** The one number you look at every morning, then what drives it, then the functions underneath.
3. **Direction.** Broad categories agreed before any tool gets touched.
4. **Connector deep dive.** Every source probed for real, not read from documentation.
5. **Options table.** Fifteen to twenty candidates, pre-filtered on whether they change a decision. You pick five to fifteen.
6. **Layout.** A wireframe you approve before a line of code exists.
7. **Brand.** Your guidelines, or your website's palette, or references you like.
8. **Build and deploy.** One self-contained page, light and dark, on a live shareable URL.
9. **Machine review.** A second agent audits the page against every design rule, blind, and it gets fixed before you ever see it.
10. **Your review.** You look at the live page and say what is wrong. Repeat until it is right.
11. **Refresh.** A companion skill and a scheduled task, so it rebuilds before you wake up.

## Install

Three ways in. Pick the one that matches where you work.

**As a plugin in Claude Code.** Unzip `analytics-dashboard-builder-plugin.zip`, then point Claude Code at the folder as a local marketplace and install it. This is the full package: both skills, the slash command, and the bundled icons.

```
/plugin marketplace add /path/to/analytics-dashboard-builder-plugin
/plugin install analytics-dashboard-builder
```

**As a single skill, uploaded.** Use `analytics-dashboard-builder.skill`. Upload it in your Claude settings under Capabilities, or add it to a Claude Code project. This is the whole dashboard skill including all nine reference files and the icons. It does not include the BenAI skill creator, which the skill handles: it writes your refresh skill by hand instead, from the same reference file.

**By hand.** Unzip and drop `analytics-dashboard-builder/` into `~/.claude/skills/`. Restart Claude Code.

Then either run the command:

```
/dashboard
```

Or just say what you want:

```
I want one page that shows me what is happening across my whole business every morning.
```

## What makes it different

Most dashboard builds fail in one of four ways. This skill is built around all four.

- **Forty tiles nobody reads.** Every metric has to pass one test: would you do something differently because it moved? If not, it does not get a slot.
- **Numbers nobody can defend.** Every count states what it counts, every rate states its population, and the member flow has to reconcile before anything publishes.
- **A page that looks fine in a screenshot.** The design rules are a named house style, fourteen hard bans and a twenty-point audit, and they exist because real builds shipped 9px labels, no logos at all, transparent cards and cards with holes in them.
- **Shipped without a review round.** Publishing is not finishing. A blind sub-agent audits the page against every rule first, and then a second gate keeps looping on your feedback until you say it is right.
- **A screenshot pretending to be a dashboard.** It is not finished until it refreshes itself, on a schedule that can actually reach your data.

## What is in the box

- `analytics-dashboard-builder`, the main skill, plus nine reference files: the interview, connector probing, metric definitions and traps, the wireframe format, the design rules, deployment, the machine review, your review, and the refresh skill
- `assets/icons/`, thirty three Lucide glyphs (ISC), already re-stroked to the 1.5px the design rules require, so the icon rule cannot break on a machine with no web access
- `commands/dashboard.md`, a `/dashboard` slash command
- `benai-skill-creator-skill`, the BenAI skill creator, bundled, used to author your refresh skill at step 11. It reverse-engineers the refresh skill from the build that just happened in the chat, instead of writing one from memory

**What it expects to already be there.** `dataviz` is built into Claude, so it is always available, and the skill leans on it for chart choice and palette validation. `design-system-creator` gets used if you happen to have it. Neither is bundled, because you cannot bundle a built-in and the skill does not depend on the optional one.

Everything else is in the reference files rather than in a dependency, because a build that assumed a missing skill would be installed once improvised the whole design layer and got it wrong.

## Connectors

Native connectors where they are clean. [Composio](https://composio.dev) for the awkward ones: analytics, ad platforms and social networks, where one link covers what would otherwise be a dozen integrations.

Read only throughout. Nothing in this plugin writes to a billing system, an email list or a community.

Built by [Ben AI](https://benai.co).
