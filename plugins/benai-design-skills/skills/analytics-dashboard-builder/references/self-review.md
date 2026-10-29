# Self review by sub-agent

Step 9. A fresh agent reviews the page before the owner ever sees it. You fix what it finds. Repeat until it passes. Only then does the owner get a link.

## Why this is not optional

You cannot review your own page. You know what you intended, so you read the intention instead of the pixels. Every design fault that has ever gone out from this skill was plainly visible in a screenshot, and the agent that built it looked straight past it.

A fresh reviewer has no intention to read. It sees what is actually there. This is the same reason the two test builds of this skill found contradictions the author of the rules could not see.

It is also cheap. One sub-agent round costs a fraction of one round of the owner's attention, and the owner's attention is the scarce thing. Spend the machine's first.

## The split that makes it work

Three rules, and the loop breaks without any of them.

**The reviewer is blind.** Give it the file path, `design.md`, and the agreed metric list. Do not give it the build conversation, your reasoning, or what you were going for. A reviewer that knows your intention will forgive it.

**The reviewer never edits.** It reads, measures, screenshots and reports. You make every change. Separation of duties is what stops a reviewer quietly rewriting the page into its own taste and then approving its own work.

**Every finding cites a rule, or it is labelled taste.** A finding must point at a ban number or an audit row in `design.md`. Anything else is a preference, and preferences are labelled as such and forwarded to the owner rather than fixed. This single rule is what makes the loop terminate. Without it a reviewer generates fresh opinions forever and the page never gets published.

## The prompt to spawn it

Send a fresh sub-agent roughly this. Fill in the paths and the metric list.

```
You are reviewing a dashboard someone else built. You did not build it and you
must not change it. Read only.

The page: <absolute path, or the published URL>
The rules: <absolute path to design.md>
The metrics that were agreed: <paste the ticked options table>

Do this, in order.

1. Read design.md in full.
2. Run the twenty point audit at the bottom of it. Grep the file for the
   mechanical checks. Report the measured value wherever a check asks for one,
   not just pass or fail.
3. Open the page at 1440 wide, in both light and dark. Screenshot each and
   actually read the screenshots. Hover something and confirm the interaction
   rules hold.
4. Check every number on the page against the agreed metric list. Flag anything
   present that was not agreed, anything agreed that is missing, and any label
   that does not match the definition it was agreed under.
5. Recompute every rate, share and average on the page from its own numerator
   and denominator. Report any that do not agree. Then check each one against
   the definition it was agreed under, not only against its own inputs.
6. Read back the computed font-family on a heading and on a numeral, in the
   browser, and report both. What a stack asks for and what actually rendered
   are different facts.

Then report:

- The audit, twenty rows, with measured values.
- Every finding, most serious first. For each one: the file location, what is
  wrong, and the ban number or audit row it breaks.
- Separately, under a heading called TASTE, anything you think is weak that no
  rule in design.md actually covers. Do not mix these in with the findings.
- The three weakest things on the page, even if everything passed. Never reply
  that it looks good and stop there.
- One verdict: PASS or FAIL. FAIL if any rule-backed finding stands.

Do not edit any file. Do not publish anything. Do not call any data connector.
```

Reviewing the local file is usually easier than the published URL, and the two are identical. Review whichever you can screenshot.

## The loop

1. Spawn the reviewer
2. Fix every rule-backed finding
3. Spawn a **new** reviewer, not the same one. A reviewer that has already approved a page is anchored to its own verdict
4. Repeat until the verdict is PASS

**Three rounds, then stop.** If the same finding survives three rounds, it is not a fix you are failing to apply, it is a disagreement or a genuine constraint. Take it to the owner with both positions stated in a line each and let them decide. Grinding a fourth round on the same point wastes real time.

**Fix findings. Forward taste.** Everything under the reviewer's TASTE heading goes to the owner as a short list at the start of step 10, phrased as options. Do not act on it alone. Taste is the owner's call, and acting on a sub-agent's preference is how a page drifts away from the brand you were given.

**Report the loop honestly.** When you hand the page over, say how many rounds it took and what the last reviewer still flagged. An owner who knows the page passed a machine review reads it differently, and hiding a surviving finding is how it becomes their discovery instead of yours.

## What a good finding looks like

> `design-test-02.html:412`. The tenure chart's value labels sit inside the fill on the two longest bars and outside on the two shortest. Charts section, value labels sit outside the end of the bar, always.

Location, the fault, the rule. Actionable in one read.

## What a bad finding looks like

> The colour palette could be more cohesive and the visual hierarchy could be strengthened to better guide the eye.

No location, no rule, no action. If a reviewer sends findings like that, tell it to cite rules and locations, and run it again.

## When you cannot spawn a sub-agent

Some surfaces have no sub-agent. Then run the audit yourself, in a deliberately fresh pass: read `design.md` again from the top rather than from memory, screenshot the page, and check the screenshot against the ban list one ban at a time.

Say plainly in your report that you ran the weaker self-check because no sub-agent was available. It genuinely is weaker, and the owner should know which one they got.
