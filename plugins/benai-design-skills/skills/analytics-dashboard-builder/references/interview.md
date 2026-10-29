# Interview

The goal is not a list of metrics. It is shared understanding: by the end, you and the user should both be able to describe the same dashboard and arrive at the same numbers.

Ask one question at a time. Acknowledge the answer, then either dig or move on. There is no target question count. Ten focused questions on a simple business beats thirty on autopilot.

## Work top down

Start at the number that matters most and reverse into what drives it. Most people, asked to list metrics, produce whatever their tools happen to show. Asked what number they would look at first, they say something true.

### The apex

1. If you could see one number every morning before anything else, what is it?
2. How do you define it exactly? Recurring revenue, cash collected, net profit, revenue booked? Which currency?
3. What target does it have, and by when?
4. What are the two or three things that move it?

Question 2 is where most of the value is. "Revenue" is four different numbers and people rarely notice they mean a specific one. Push until the definition is one you could compute.

### The drivers

For each thing they named in question 4, ask what they would need to see to know it was working. This is how the sections get discovered rather than assumed, and it keeps the page anchored to their model of the business rather than to a template.

Then sweep the functions, skipping any that do not apply:

- **Revenue:** recurring versus one-off, new versus expansion, failed payments, discounts given away
- **Retention:** churn, cancellations, where in the lifecycle people leave
- **Sales:** calls booked, show rate, proposals out, win rate, deal size
- **Marketing:** reach, traffic, conversion, list growth, cost per acquisition
- **Delivery and operations:** engagement, support load, delivery against plan
- **Finance:** refunds, renewals coming up, margin
- **Team:** only if they actually manage against it

### The reality check

5. What do you check today, and where?
6. Which of those tools do you not have a login for?
7. Who else reads this?

Question 6 matters more than it looks. The most valuable thing a dashboard often does is give someone sight of a number they currently have to ask a colleague for.

### The two questions that separate must-know from nice-to-know

8. Tell me about a decision you made in the last week or two where better numbers would have changed what you did.
9. If one of these numbers went bad tomorrow, what would you actually do differently?

These are the best questions in the set. Anything that survives question 9 belongs on the page. Anything that does not is interesting rather than useful, and it is what makes dashboards unreadable.

### Shape

10. What window do you think in? Yesterday, last 7 days, last 30, month to date?
11. One screen you scan in thirty seconds, or something you sit with?
12. Is this a morning briefing you read once, or a monitor you leave open?

The last one has real consequences. A once-a-day briefing can be a static page refreshed on a schedule, which is far cheaper and gives numbers stable enough to reason about. A monitor needs live data and a different build.

## Pushing back is part of the job

When someone asks for something that will not help, say so once, with the reason, and then do what they decide. Common cases:

- **A metric with no target and no owner.** It cannot be good or bad, only present. Ask what number would make them act.
- **Lifetime totals.** Total views ever, total members ever. They only go up, so they carry no information.
- **A metric that duplicates a tool that answers it better.** Link to that tool instead of copying a worse version of its chart.
- **A metric whose only possible response is to message someone else.** Then the useful signal is "this needs a conversation", not the underlying chart.

## Close the interview properly

Before moving to step 3, read back what you heard: the apex metric and its definition, the drivers, the sections, the window, and anything explicitly excluded. Ask them to correct it. Cheap here, expensive after the page is built.
