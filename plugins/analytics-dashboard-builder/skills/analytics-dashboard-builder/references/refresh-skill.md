# The refresh skill

Step 11 writes a second, smaller skill whose only job is to put today's numbers into the page that already exists. This file is what that skill has to carry.

Author it with the `benai-skill-creator-skill` bundled in this plugin, on its Build branch: the dashboard build that just happened in this chat is the finished task it extracts the process from. The structure below holds either way.

## The split that makes this reliable

An agent fetches. Deterministic code computes and patches. Every number on the page comes from a stored pull put through the same arithmetic every day, so a run can be repeated, diffed and checked.

The alternative, an agent doing the arithmetic conversationally each morning, produces numbers nobody can verify and that change for no reason.

## What the skill has to contain

Not a summary. The actual working detail, because in a month nobody will remember any of it and the agent running the job will have none of the context that produced it.

1. **Where the page lives** and the exact call that updates it in place
2. **Every metric definition**: each numerator, each denominator, and the population both come from
3. **The reconciliation line** that has to close before publishing
4. **The connector map**: per data point, the exact call, the shape returned, the freshness lag, any cap
5. **The traps file**: every way this specific business's data has produced a wrong number, each with the wrong answer it produced. This is the most valuable file in the skill. A trap without its wrong answer is advice; a trap with its wrong answer is recognisable
6. **Reference values** for the day it was built, so a future run can sanity-check itself

## Where the skill has to live

A skill that is not installed somewhere durable does not exist. This has already gone wrong once: a refresh skill was written to a container path that died with the container, and pushed to a git branch, which is storage and not installation. Neither survived to the next session.

So, before writing it:

1. Ask the owner where their skills live. Common answers are a personal skills directory on their machine, a plugin they already install, or a shared internal repository the team syncs from
2. Write it there
3. Say in the close-out report the exact final path, and say plainly whether a fresh session will find it

If the only writable place is temporary, say so rather than reporting success. Then either hand the owner the files to install themselves, or agree a durable home first. A refresh skill the morning job cannot load is the same as no refresh skill, and it fails silently.

## Efficiency

**Rolling windows append, they do not re-pull.** A 14-day series needs today's value, the oldest entry dropped, and the new one added. Re-pulling fourteen days every morning costs fourteen times as much for the same answer.

The figures that genuinely need a full window are the ones whose denominator *is* the window: churn rates, tenure hazard rates, cohort comparisons. Those move slowly, so refreshing them weekly is honest as long as the card says when they were last computed.

**Large pulls go in a subagent** that returns only aggregates. Hundreds of records at hundreds of kilobytes a page should never reach the main context.

**Start from yesterday's data object** and change only what needs changing, rather than rebuilding it.

## Snapshot first

Before computing anything, save the current published data object to a dated file.

That snapshot is what makes tomorrow's deltas real rather than invented, and it is what the guardrails compare against. Without it, every arrow on the page is a guess.

If the page cannot be read, stop. Patching a page you could not read means rebuilding it from scratch, which is the exact outcome this skill exists to prevent.

## Guardrails

Stop rather than publish when any of these trip, and report which one:

- The headline revenue figure moved more than 10% in a day
- The member or user count moved more than 5% in a day
- Any headline number came back zero. A zero is almost never real: it means a source returned an empty list and the arithmetic collapsed quietly
- A required source returned something unusable
- A key the page reads has gone missing from the data object

Set them loose. They exist to catch a broken pull, not a bad week. A genuinely bad week should reach the user; a source silently returning empty should not reach them dressed as a real number.

Being a morning late is recoverable. A wrong number that gets acted on is not.

## When a source will not answer

Leave its values untouched and render the affected card as not tracked, with the reason.

Never age a number forward as though it were today's. A stale figure presented as current is the one failure mode that actually costs money, because it is the one that gets acted on.

The instinct to fill a gap is the thing to resist. A blank prompts a fix; a plausible number prompts a decision.

## Patch, do not rebuild

The design is finished. Replace the data object and touch nothing else: no CSS, no chart options, no markup.

A patch script that brace-matches the object, refuses if any key the page reads has disappeared, and reports what changed is worth writing once. It makes an unattended morning job safe.

If a number needs a new card, that is a conversation with the user, not a morning job.

## Log every run

One line per run, appended to a file: the date, the headline figures, which sources answered, which were left untouched, and any guard that tripped. Two mornings should be diffable.

## Reporting back

The user reads the dashboard, not the message. Keep the report to what the page cannot tell them:

- What moved and by how much, in percentage points for rates
- Anything rendered as not tracked, and why
- Any guard that tripped, and what happened instead
- Anything that looks like a data problem rather than a business change

If everything refreshed cleanly and nothing moved much, one line. Do not restate the numbers they are about to look at.

## The scheduled task

One line of prompt, because the skill carries the whole procedure.

**Ask cloud or local before creating anything.** Step 11 in the skill file carries the wording. The two answers behave differently and the difference is not cosmetic:

- **A cloud schedule** fires whether or not their machine is on. It only works if every required source is reachable from a fresh session with no local credentials
- **A local schedule** reaches anything their laptop can reach, including local files and local credentials. It needs the machine awake at the scheduled time, and a missed run happens at next launch instead

**Test that the schedule can carry its connectors, before you report success.** This is the failure that stopped a real run after every other step had gone right: the platform created the job happily, and a fired session would have woken with no billing connector, no database and no email platform, and failed every single morning.

A job that looks scheduled and cannot reach its data is worse than no job, because nobody notices for weeks. If the credentials cannot travel, do not leave it enabled. Disable it, say exactly why in one line, and offer the two real options: a local schedule on their machine, or running the skill by hand.

Two more things to tell the user when it is set up:

- **The first run should be started by hand**, so connector permission prompts get approved once rather than stalling an unattended run
- **Where the skill is installed**, and whether that path survives a fresh session
