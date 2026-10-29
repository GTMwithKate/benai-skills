# Metric patterns

Definitions that hold across businesses, the test that decides what earns a slot, and the traps that produce numbers which look right and are not.

## Contents

- The cut test
- Core definitions
- The reconciliation
- Traps, with the wrong answer each one produces
- Presenting a rate honestly

## The cut test

A metric earns a slot only if the user would do something differently because it moved. Everything else is interesting.

Apply it yourself before showing anything. Handing over a long list and asking the user to filter looks collaborative and is actually offloading the hard part.

**Cut on sight:**

- Lifetime totals. They only go up.
- Any count with no comparison and no target. It cannot be good or bad.
- Follower counts with no direction.
- Anything a dedicated tool already answers better. Link out instead.
- Anything where the only possible response is to message somebody else.

**Nice to know versus must know** is the distinction to hold in mind while building the options table. A must-know changes an action this week. A nice-to-know changes a conversation. Both are real, only one belongs on a page read in thirty seconds.

## Core definitions

### Customers versus subscriptions

Count **people**, not billing objects. A customer holding two plans is one member and two subscriptions. Decide which one a card means, say so on the card, and make every breakdown of that card sum to the same number.

For an active paying base: distinct customers holding at least one live subscription that is not already scheduled to end. The ones scheduled to end are worth showing separately, because they are a leading indicator that moves before churn does.

### Recurring revenue

Normalise every plan to one month before summing:

- Yearly divided by twelve
- Any plan with an interval count divided by that count. A quarterly plan is commonly stored as a monthly interval with a count of three, which is the single most expensive gotcha in this whole area
- Tiered prices often carry a null unit amount. Reading that field scores them as zero without erroring
- Apply recurring discounts; do not apply one-off discounts, which by definition do not recur
- Floor each subscription at zero. A coupon can be larger than the plan it discounts

### Annualised revenue

Two different numbers, and showing only the flattering one is misleading:

- **Contracted:** excludes anything already scheduled to end
- **If nobody leaves:** monthly recurring times twelve, which is a ceiling

Show the honest one large and the ceiling small beside it.

### Net new

Joins minus leaves. A gross join count reads as growth during a month of decline, which is exactly when the number matters most.

### Churn

Members lost in the window over members active at the **start** of the window, with both sides drawn from the same population. Report movement in percentage points, never as a percent of a percent.

Churn by tenure has to be a **rate per band**, not a share of total cancellations. A share chart only tells you most members are new. The useful version is cancellations in a band over the members who reached that band.

### Multi-currency

If the account settles in one currency, the provider's own reporting will present everything in that currency, including charges taken in another. Pick the currency the user thinks in, convert with a **sourced and dated** rate shown on the card, and keep the original visible. Never carry an unsourced rate.

## The reconciliation

```
members at period start + new + reactivated - churned = members today
```

Run this before publishing. If it does not close, one of the terms is wrong, and it is usually churn.

Reactivations are the term people forget. Someone who left and came back breaks a naive start-plus-new-minus-lost, and the resulting mismatch is often blamed on the churn definition instead.

Put the working in a tooltip on the churn card. A number whose arithmetic is visible gets trusted; one that is asserted gets questioned every month.

## Traps, with the wrong answer each one produces

Each trap below has produced a wrong figure on a real dashboard. They are written with the wrong answer attached, because the wrong answer is what makes the trap recognisable. Every one of them looks like ordinary correct reasoning right up to the number it produces.

**When building for a specific business, write its own version of this list**, with that business's actual wrong answers in it. That file is the single most valuable thing the refresh skill inherits.

### Counting subscriptions when you mean people
Produces a member count noticeably higher than reality, and every per-member rate comes out low.

### Deduplicating on the wrong key
A join key that is null on most rows collapses the count silently. Deduplicate on something guaranteed present: a customer id or an email.

### Counting a churn when one of two plans ended
A customer who cancelled one plan and kept another is not lost. A member is lost only when nothing live remains.

### Reading a cancellation request date as an end date
Most systems stamp the moment someone asks. Billing counts them as gone when the paid period ends. Those fall in different months, which shifts churn by several points and makes a daily loss series run days ahead of the truth.

### Trusting a mirror or warehouse for recent windows
A replicated copy lags. Anything for a window shorter than a few days comes from the live source. A mirror reporting zero new members while the live system had three is the usual first symptom.

### Zeros that are really gaps
A source returning no records for a date is usually a collection gap, not a quiet day. Plotting it as zero drags averages down and makes a normal day look like a good one. Drop those points rather than plotting them.

### Averages polluted by outlier days
One deliberate purge, one outage, one launch. Isolate it and report it separately rather than smoothing it away or letting it set the baseline.

### Including your own team in engagement
Community activity that counts the team's own posts flatters itself. Exclude authors on the company domain.

### Rounded public counters
Some platforms round a public total to the nearest thousand. A delta built from two rounded totals can be wrong by the whole rounding unit. Show the total with no delta until an exact source exists.

### Reporting lag treated as a decline
Several analytics platforms report a few days behind and return nothing for recent days. End every window at the last day actually returned, and print that date on the section.

### Comparing a young thing to a finished thing
A one-day-old item against the median of completed ones always looks like a failure. Either compare at the same age, or show the series with the newest marked and its age labelled, and say the total is still climbing.

### Attribution tags that are not where you expect
Campaign identifiers often hide inside another field, such as a stored URL, rather than in a dedicated property. Extract from every place they appear, decode, normalise case, and match carefully: similar slugs frequently belong to different things.

### An event that quietly stopped firing
Compare any event count against a second source before building on it. An event logging a handful of occurrences where another system logs dozens is broken, not quiet.

### A missing API scope
When a provider's own reporting endpoints refuse, say so plainly and leave the card as not tracked. Reconstructing a substitute from raw records once produced a chart trending up while the provider reported the same month down. Worse than no chart.

### Two counts from one provider that both look official
Platforms commonly expose several subscriber or member counts covering different states. They will not agree. Choose one endpoint, note which, and stay on it so the number does not move for no reason.

## Presenting a rate honestly

- State the population on the card
- Movement in percentage points for anything already a percentage
- Colour from a declared direction per metric, never from the sign of the change. A rising churn number is bad even though it went up
- Where a comparison is confounded, render it neutral and say why. A bounce rate falling because all traffic fell is not good news
- Sample size on anything cohort-based, and no red-versus-green on a difference that a significance check does not support

## A supplied ratio that disagrees with its own inputs

Recompute every rate, average and share from its own numerator and denominator, even when the owner or the source hands you the figure directly.

They disagree more often than you would expect, usually by a rounding step. A real case: ARPU was supplied as 121.98 while the supplied revenue and customer count divide to 121.97. Both numbers were "from a real pull" and they still contradicted each other.

When they disagree:

- Say so, in one line, and ask which the owner wants on the page
- Show one of them, never both. A card showing a supplied ratio beside the two inputs that produce a different answer invites the reader to do the arithmetic and lose trust in the page
- If you cannot ask, show your recomputed figure and state the inputs on the card

**Check the definition, not only the arithmetic.** A supplied rate can recompute perfectly from its own inputs and still be defined the wrong way round. A real case: churn supplied as 61 leavers over 1,216 customers at period end recomputes exactly, and the definition above uses customers at period *start*, which gives 61 over 1,183 and a different answer. The arithmetic check passes and the number is still not the metric that was agreed.

So state the denominator on the card, and when the supplied rate uses a different one from the agreed definition, name both figures and ask which the owner wants. Do not put two rates for the same thing on one card.

This is the same rule as "flows have to close", applied one level down. A page whose numbers do not agree with each other gets distrusted as a whole, including the fifteen figures that were right.
