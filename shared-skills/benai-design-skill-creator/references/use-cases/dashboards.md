# Use case: dashboards

One page that answers "how is the business doing" every morning, built from the tools the user already pays for, refreshing itself on a schedule. The generated skill carries the user's own agreed metrics, sources, and layout as its defaults.

## Dashboard types to offer

Ask which the user wants (AskUserQuestion): a **morning briefing** (static page, refreshed on a schedule, numbers stable enough to reason about - the cheap default), a **monitor** (left open all day, needs live data, a different build), or a **function page** (one department: sales, marketing, retention). Briefing versus monitor has real build consequences; do not assume.

## The process (each step is a gate: get agreement, then move)

1. **Interview.** Top down: the one number they would check every morning, then what moves it, then the functions underneath. One question at a time. Push on definitions - "revenue" is four different numbers. The two best questions: "tell me about a recent decision better numbers would have changed" and "if this number went bad tomorrow, what would you actually do differently?" Anything that survives the second belongs on the page. Close by reading back the apex metric, drivers, sections, and window, and let them correct it.
2. **Data sources.** Probe every connector the interview implies - call them, do not read docs and assume. Record per source: the exact call, the shape returned, its freshness lag. Stay read-only: billing systems, email platforms, and communities are production. If a scheduled refresh is wanted, also test whether a fresh scheduled session can reach each source.
3. **Shortlist.** One options table: 15-20 candidate metrics maximum, 5-15 ticked as the recommendation, each row carrying its source, chart form, window/comparison, and the decision it drives. Apply the cut test yourself first (below). Unreachable metrics go in their own block with the reason, never quietly dropped.
4. **/design layout variations.** 2-3 structurally distinct layouts on a /design canvas - different hierarchy, grouping, or hero number, not the same grid recolored. Wireframe fidelity, placeholders visibly blank (never invented numbers - a mocked figure gets believed, then quoted). Always light AND dark. The user picks or mixes.
5. **Build.** One self-contained page, data separated from render so one number changing changes its chart with no other edit.
6. **Audit.** A fresh reviewer pass (a sub-agent when available): screenshot both modes, read the screenshots, check every number against the agreed list, verify flows close. You cannot review your own page - you read your intention instead of the pixels.
7. **Review with the owner, then scheduled refresh.** Iterate on the /design canvas until they call it done. Then ask: do you want this on a schedule, and where should the schedule live? Write the refresh routine and install it somewhere that survives.

## The cut test (step 3)

A metric earns a slot only if the user would do something differently because it moved. Cut on sight: lifetime totals (they only go up), counts with no comparison and no target, follower counts with no direction, anything a dedicated tool answers better (link out instead), anything whose only response is to message somebody else.

## Design rules (the ones that decide whether the page gets opened twice)

**House style**: a modern developer-platform instrument panel. Near-neutral surfaces from the token ramp, hairline 1px borders, one accent used sparingly, thin geometric icons at a consistent stroke, tight spacing from one scale, one radius everywhere. Restraint is the default: a dashboard is a tool, not a poster. A louder brand kit applies its character at the quietest setting that still reads as the brand, on top of this structure, never instead of it.

**Hard bans** - break one and the page reads as machine-made:

- No text below 14px anywhere: labels, axes, tooltips, notes. If it does not fit at 14px, shorten the words or grow the box.
- No horizontal rule under a section name, and no decorative divider lines at all. Sections separate with vertical space (~40px) and a bigger heading.
- No transparent cards. Solid fill from the token ramp plus a visible hairline border, on every card.
- No small grey subtitle beside a section heading, no freshness text paragraph in the header (one icon, detail on hover), no narration on a card face - noun labels, not sentences.
- No badge/pill spam (two on the whole page, max), no info marker on every title (four max), no empty box (fill it or shrink it).
- No italics, no serif anywhere, no hard offset shadow on a dark ground.
- Do not force the page into one viewport height - that single decision causes shrunken labels, sliver bars, and voids. Dense and landscape; a page and a half of scroll is fine.

**Typography**: hero number 48-60px, section headers 20-24px, card titles 15px uppercase, card values 28-36px, notes at the 14px floor. Numerals in a monospace face so values do not change width every morning. Three sizes per card, maximum; hierarchy by weight (400/600/700), not by adding sizes. Muted text still measures at least 4.5:1 against its ground.

**Layout**: landscape, full width before another row. Twelve-column grid, every card spanning whole columns. Most important number biggest, top left. Page max ~1400px, centred. Uniform card heights inside every row; nest small cards beside a large one rather than stretching.

**Cards - a delta with every number.** Label, value, delta against a named window, at most one factual note pinned to the bottom. A number with no comparison cannot be good or bad. Counting metrics get two or three windows (24h / 7d / 30d) rather than whitespace; a genuinely single-window metric fills the box with key-value facts (population, window, target), never an invented second window. The window sits in the title row, not in small grey text at the bottom.

**Charts** - pick the mark from the question, not from variety:

| Question | Mark |
|---|---|
| Compare across categories | Horizontal bars, sorted, value labels outside the bar end |
| Movement over time | Line, or area for a single series |
| Composition of a whole | Stacked bar; donut only for 2-3 well-separated parts |
| Value against a target | Progress bar or meter, target marked |
| Distribution | Histogram with real bands |

Every axis labeled at 14px, time axes in date order, missing data drawn as a hatch or dashed outline (never a colour that reads as a real low value), no hover shadows, chart text drawn at 1:1 so it cannot silently rescale below the floor.

**Colour**: direction, not sign - every metric declares whether up is good, and delta colour comes from that declaration (churn rising is bad even though it rose). One accent hue for emphasis; status colours a separate small set; two categories that are not good-and-bad get accent-plus-neutral, never green-and-red. Confounded comparisons render neutral with the reason on the card.

**Light and dark, both, always.** Same data, structure, geometry, and spacing; only surfaces, ink, and elevation change. Light mode may use a soft or brand shadow; dark mode separates by background lift plus hairline border, never an offset shadow (it reads as a rendering fault). Dark is the mode people keep open - check contrast there specifically.

**Never invent a number.** A missing figure renders as an honest "missing because X" card, never a plausible placeholder. Real dates from the machine. Population stated on every card.

## Metric rules that go into the generated skill

- Count **people**, not billing objects: a customer with two plans is one member, two subscriptions. Say which a card means, and make its breakdowns sum to it.
- Numerator and denominator from the same population - the most common source of a wrong rate. Churn = lost in window over active at the **start** of the window; movement in percentage points, never percent-of-a-percent.
- Normalise recurring revenue to one month before summing (yearly / 12; watch interval counts - a quarterly plan is often stored as monthly-times-three).
- Net new = joins minus leaves; a gross join count reads as growth during a month of decline.
- Run the reconciliation before publishing: start + new + reactivated - churned = today. If it does not close, a term is wrong, usually churn. Put the working in a tooltip.
- Recompute every supplied ratio from its own inputs, and check the definition, not just the arithmetic - a rate can recompute perfectly and still use the wrong denominator.
- Classic traps: cancellation-request dates read as end dates, lagging mirrors used for recent windows, zeros that are really collection gaps, the team's own activity counted as engagement, rounded public counters used for deltas. When a source cannot support an agreed definition, re-open the definition with the owner - never deliver the nearest computable thing under the agreed label.

## The review checklist (before the owner sees anything, every round)

1. Render both modes at 1440px, screenshot, and read the screenshots - every fault that ever got published was visible in the render and invisible in the source.
2. Grep the mechanical bans: smallest font size, italics, rules/dividers outside cards, transparent card fills, external requests.
3. Every number traces to a real pull; every ratio recomputed; the reconciliation closes; every card label matches the definition behind its number.
4. One radius, one spacing scale, one icon set at one weight; owner's logo in the header; section headings carry icons.
5. Then ask the owner five short questions in one message: anything too small? any number wrong or surprising? anything you would never look at, or missing? does it look like your brand? anything cluttered? Patch what they name, republish in place (never a second copy), and keep design rounds separate from number rounds.

## /design delivery

The final dashboard lands on a /design canvas for edit rounds (live HTML/CSS artboards, both modes), and the live page is republished in place after each round. The canvas is where the owner marks changes; they should never have to describe a visual change in prose.

**Live artboards only.** Every artboard is live HTML/CSS with real editable text on brand tokens - never a flattened PNG mock, which the owner could not edit and the gate could not do its job with.

## Sources

Reference material for dashboard and app-UI patterns lives in `../sources.md`. A screenshot of a dashboard the user already loves outranks all of it.

## Self-improvement

Every owner correction - a metric they cut, a layout they mix, a definition they sharpen, a trap their data springs - gets written into this file (or the generated skill's copy, especially its own traps list) in the same session. The business-specific traps list is the single most valuable thing the refresh routine inherits.
