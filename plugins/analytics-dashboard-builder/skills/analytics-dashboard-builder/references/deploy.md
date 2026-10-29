# Deploy

## Build shape

One self-contained HTML file. No external requests: no CDN scripts, no remote stylesheets, no remote fonts, no remote images. Vendor the charting library into the file and inline any asset as a data URI.

Two reasons this matters more than it looks. A page with an external dependency breaks the day that host changes, usually silently. And a single file can be opened from disk, emailed, or published anywhere without a build step.

## Separate the data from the render

Every number the page shows lives in one data object near the top. Every card and chart reads from it. Nothing is hardcoded into markup or chart options.

```js
const D = { mrr: { net: 65076, target: 100000 }, members: { count: 667 } };
```

This is what makes the refresh cheap: changing one value in that object changes its card and its chart with no other edit. It also means the refresh can patch a single object rather than regenerating a page, which is what stops a morning job from quietly redesigning things.

Give every figure that needs explaining a tooltip string in the same object, so the definitions travel with the numbers.

## Ask where it goes

Two good answers, and the choice is the user's:

**A live artifact.** Published straight from the conversation, private until shared, and updatable in place. Best when the audience is a small team and nobody wants to own hosting.

**A static host.** More control, a custom domain, and access control if the platform offers it. Best when it needs to sit behind a login or live on a company domain.

Either way the page is the same file.

## Updating in place

The rule that matters most: **an update must target the existing published item.**

Publishing without the existing identifier creates a second copy. The user keeps reading the first one, which has quietly stopped updating, while a fresher version exists somewhere they never look. This failure is silent and it can run for weeks.

So record, in the refresh skill:

- The exact identifier or URL of the published page
- The call that updates it in place
- The title and icon, which must stay stable across republishes, because that is how people find the page again

## Sharing

Published pages are usually private to their owner. Sharing is a separate, manual step. Say so explicitly rather than letting the user assume their team can already see it: a dashboard nobody else can open is a common and quietly frustrating outcome.

## Before publishing

- No external references anywhere in the file. Check rather than assume
- Both light and dark render correctly
- No horizontal scrollbar at a normal desktop width
- Every chart draws when the page is opened in a background tab
- No text below 14px. The floor is 14px, set in `design.md`. Any older reference to 13px is out of date
- Every number traces to a real pull, and anything missing says so
- The full twenty point audit in `design.md` has been run and reported. This short list is not a substitute for it
