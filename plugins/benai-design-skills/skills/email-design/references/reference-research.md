# Reference research - finding the right emails to steal from

The goal of this step is 2-3 references that match the user's **product** and the email's **goal**, shown to the user before any design work. A reference that matches neither axis pulls the design toward someone else's brand and someone else's job-to-be-done.

## Step 0 - Ask the user first

Before researching, ask: "Do you have emails you like? Links, screenshots, or forwards from your own inbox all work." User-supplied references outrank researched ones - they encode taste you cannot infer. If they supply some, you may still add 1-2 researched references to fill gaps (e.g. they gave a vibe reference but nothing for this email's goal).

## Step 1 - Define the two axes

Write both down before searching:

- **Product axis**: industry, price point, audience sophistication, visual temperature (a fintech tool, a DTC candle brand, and a developer platform want different worlds).
- **Goal axis**: what this specific email must do. Common goals and what their best references look like:

| Goal | What good references demonstrate |
|---|---|
| Launch / announcement | One hero moment, one CTA, drama above the fold |
| Newsletter / digest | Scannable modular sections, clear rhythm, restrained per-item styling |
| Promo / sale | Offer legibility - the deal readable in 2 seconds, urgency without clutter |
| Onboarding / welcome | Warmth + a single next step; progressive feature reveal |
| Product update / changelog | Dense information made calm; typography doing the work |
| Winback / re-engagement | Emotional reopening line, low-pressure CTA |
| Transactional-plus (receipt, confirmation) | Utility first, brand moments at the edges |

Search both axes: one query set for "[industry] + email," one for "[goal] email."

## Step 2 - The sources

### milled.com - the large searchable archive of real brand emails

What it is: a searchable archive of actual sends from thousands of brands - not curated design showcases, but what brands really send, at real cadence.

How to use it:
- Search by brand name when the user names competitors or aspirational brands ("show me what Notion / Glossier / Linear send").
- Search by keyword for the goal axis: "launch," "40% off," "welcome," "you're in."
- Browse a relevant brand's timeline to see their *system* - how their promo differs from their newsletter - which is more instructive than one pretty email.
- Strength: reality. Weakness: no design filtering; expect to sift. Use it to answer "what do brands like this actually send," then quality-filter yourself.

### reallygoodemails.com

What it is: the curated design-quality gallery, categorized by email type.

How to use it:
- Browse by category matching the goal axis directly (Announcement, Newsletter, Promotion, Welcome, etc.).
- Many entries include the actual HTML - when a reference's build technique matters (how did they do that dark hero?), open the code view and read it.
- Strength: everything is well-designed and categorized. Weakness: it skews toward design-forward tech/DTC; a traditional-industry user may need milled for realism.

### Pinterest

What it is: the moodboard engine - strongest for visual language, weakest for email realism.

How to use it:
- Query pattern: "[industry] email design," "[goal] email design," plus aesthetic modifiers ("glassmorphism email," "dark gradient email," "editorial newsletter design").
- Follow the "more like this" trail from any strong hit - Pinterest's similarity engine is the actual tool here.
- Treat results as *visual direction* (palette, density, type attitude), not as literal email layouts - many pins are concept shots that would never survive an email client.

### Supplementary

- The user's own inbox and competitors' signup flows (subscribe and see what arrives) when the engagement allows time.
- Web search for "[brand] email design case study" when a named brand's system is the target.

## Step 3 - Select and present

From everything gathered, pick **2-3** references. Selection criteria:

1. At least one matches the goal axis strongly (right email *type*).
2. At least one matches the product axis strongly (right *world*).
3. Ideally one carries the aspirational visual language (this is where a glass/gradient reference belongs, if the brand suits it).
4. Every pick must be *achievable in email-safe HTML after degradation* - a reference whose entire appeal is a video background or heavy interactivity will only disappoint. Check each pick against the degradation map in `liquid-glass.md` and the rules in `email-client-constraints.md` before showing it.

Present to the user as a short list - link or screenshot, plus one line each: "what we'd steal from this one" (e.g. "the modular card rhythm," "the offer typography," "the dark gradient hero"). Ask which resonates. Their answer shapes the /design variations in the next step - each variation should be traceable to a reference the user reacted to.

## Anti-patterns

- Researching before asking the user for references.
- Picking three references that are all the same layout (no real choice for the user).
- Picking by prettiness while ignoring the goal axis - a gorgeous launch email is a bad reference for a weekly digest.
- Showing 8 references; more than 3 shifts the decision burden back onto the user.
- Referencing an email whose signature effect cannot degrade gracefully.
