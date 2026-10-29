# Review and iterate

Step 10. The step that decides whether the page gets opened every morning or closed and forgotten.

Step 9 has already run: a sub-agent reviewed the page against every rule in `design.md` and it passed. So this round is not about faults a rule can catch. It is about the things only the owner knows.

Publishing is not finishing. The first version of a dashboard is a proposal. Nobody has read it yet at full size, in their own browser, in the mode they actually use, with their own numbers in it. That reading always produces changes, and the changes are usually about design rather than data.

Budget for three to six rounds. That is not a sign the build went badly. It is the step working.

## Before you ask them anything

Every round, in this order.

0. **Hand over the sub-agent's TASTE list**, from step 9, as a short list of options. Those are the judgement calls a rule could not settle, and they belong to the owner.
1. **Render the page and look at it.** Screenshot it and read the screenshot. Both modes, at 1440px wide. Every design fault that has gone out from this skill was plainly visible in a screenshot and invisible in the source.
2. **Re-run the audit** at the bottom of `design.md`, all twenty checks. A fix in round two routinely reintroduces a fault that passed in round one. Small type in particular comes back, because the fix for a cramped card is nearly always to shrink something.
3. **Fix what you found yourself** before you ask them. Do not spend the owner's round on a fault you could see.

## The questions

Ask these, short, in one message. Not one at a time: this is a review, not an interview, and they are looking at the page while they answer.

1. Is anything on the page too small to read comfortably?
2. Is any number wrong, or does any number surprise you?
3. Is anything here you would never look at? What is missing that you would?
4. Does it look like your brand? Do you have a logo file I should use?
5. Anything that just looks bad or feels cluttered?

Then stop talking and let them answer. Do not pre-defend the design.

## Running a round

**Patch, do not rebuild.** Change what they named and nothing else. A round that quietly restyles three other things makes the next round about the things they did not ask for.

**Publish in place.** Update the existing published page, never create a second copy. A second copy is silent: they keep reading the first one, which has stopped changing, while the fixed version sits somewhere they never look.

**Do not touch the data object unless the change is a data change.** Design rounds and number rounds are different rounds. Mixing them is how a layout fix silently changes a figure.

**One reply per round, short.** What you changed, one line each. Not a summary of the design philosophy.

## Faults an owner names, and what they actually mean

These come up nearly every time. Recognising them saves a round.

| What they say | What it is | The fix |
|---|---|---|
| "The text is tiny" | Something is under 14px, usually a note or an axis label | Raise it. If it no longer fits, cut the words or grow the box. Never shrink it back |
| "It looks cluttered" | Too many pills, too many info markers, too many note lines, or a subtitle beside a heading | Delete. Cards carry a label, a number, a delta and at most one note |
| "It looks AI-generated" | Section rule lines, a gradient stripe, or narration copy on the cards | Remove the lines, remove the stripe, rewrite every card string as a noun label |
| "It looks unfinished" | Transparent cards, ragged card heights, or a void inside a tall card | Solid fills and visible borders on every card, uniform heights per row, fill the box or shrink the box |
| "It does not look like us" | Their own logo is missing from the header, or the palette was guessed | Put their logo in the header. Ask for the file if you do not have it. Go back to the brand kit |
| "The icons look cartoonish" | A bold or filled icon set | Switch to a thin geometric set at light or regular weight. One set for the whole page |
| "The dark mode looks bad" | Almost always a light hard offset shadow behind dark cards, reading as a double edge | Dark mode separates surfaces with background lift and a hairline border. No offset shadow |
| "It does not look professional" | Italics, mixed icon sets, or more than one radius | Remove every italic. One icon set, one radius, one spacing scale |
| "It looks like a printed report" | The font stack fell through to a serif, because the brand face is not installed and remote fonts are banned | Embed the brand face as a data URI, or append a system sans before the serif. Read back the computed font family to confirm |
| "It feels dead" | No hover states, no transitions, an instant tab switch | Add hover, a focus ring, 120 to 160ms transitions on colour only, and a sliding tab indicator |
| "There is too much here" | More cards than the cut test allows | Cut to the ones that change a decision. Offer the cut list rather than deciding alone |
| "This number looks wrong" | Usually a real population mismatch, occasionally a real business surprise | Re-run the reconciliation before you defend the number. Check numerator and denominator share a population |

## When they name a number

Treat it as probably right until you have re-derived it. An owner who says a figure looks wrong is usually reading it against something they know that is not on the page.

Re-run the reconciliation line first. Then check the numerator and the denominator come from the same population. Then check the window. Most surprises are one of those three, and all three are cheap to check.

If the number turns out to be correct, say so plainly and put the working in the tooltip so the same question does not come back next week.

## When to stop

Stop when they say it is done. Not when you think it is done, and not when the audit passes. The audit passing is the floor, not the finish line.

If they go quiet after a round, ask once, plainly, whether the page is right or whether there is more to change. Silence is not agreement, and step 11 writes files, so it needs a real yes.

## What not to do in this step

- Do not defend a design choice. If they do not like it, it is wrong for them, which is the only test that matters here
- Do not ask for feedback as a numbered form. Ask the five questions and let them talk
- Do not batch changes across rounds. Fix, republish, show, ask
- Do not start the refresh skill. That is step 11 and it needs its own two questions answered
- Do not add anything they did not ask for, however good the idea. Suggest it in one line instead, and let them say yes
