---
type: check
layer: 1-universal
status: active
source: the humanizer skill (blader/humanizer), based on Wikipedia "Signs of AI writing" (WikiProject AI Cleanup). Embedded here, not referenced.
---

# Check: AI writing tells

Detect signs of AI-generated text. Flag each instance with the exact quote and a natural rewrite. This is layer 1, it is the same for everyone. Flag and suggest, do not rewrite on your own. The mechanical ones (em-dash overuse, AI vocabulary, boldface, Title Case, emojis, curly quotes, filler) bundle into a single "clean the mechanical stuff" approval.

Two jobs: remove the patterns below, and make sure what is left has a pulse (see the end). Clean but soulless is still slop.

## Content patterns

1. Significance inflation. Watch: stands/serves as, a testament/reminder, a vital/pivotal/crucial/key role or moment, underscores/highlights its importance, reflects broader, symbolizing its ongoing/lasting, setting the stage for, marks a shift, key turning point, evolving landscape, indelible mark, deeply rooted. Fix: state the plain fact, drop the importance puffery.
2. Notability name-dropping. Watch: cited in [list of outlets], active social media presence, written by a leading expert. Fix: one concrete, sourced instance instead of a list.
3. Superficial -ing analyses. Watch: highlighting, underscoring, ensuring, reflecting, symbolizing, contributing to, fostering, showcasing tacked on the end of a sentence. Fix: cut it or replace with an actual source or fact.
4. Promotional language. Watch: boasts a, vibrant, rich (figurative), nestled, in the heart of, renowned, breathtaking, must-visit, stunning, groundbreaking (figurative), commitment to. Fix: neutral, factual description.
5. Vague attributions. Watch: experts believe, observers have cited, industry reports, some critics argue, studies show (with no named source). Fix: name the source or cut the claim.
6. Formulaic challenges. Watch: "Despite challenges... continues to thrive," "Challenges and Future Prospects." Fix: specific facts about the actual situation.

## Language and grammar patterns

7. AI vocabulary. Watch: additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate, key (adj), landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore (verb), valuable, vibrant. Fix: plain equivalents, or cut.
8. Copula avoidance. Watch: serves as, stands as, marks, represents, boasts, features, offers (where "is" or "has" would do). Fix: use is, are, has.
9. Negative parallelisms. Watch: "not only X but also Y," "it's not just X, it's Y." Fix: state the point directly.
10. Rule of three. Watch: ideas forced into groups of three (innovation, inspiration, and insights). Fix: use the natural number of items.
11. Synonym cycling. Watch: protagonist / main character / central figure / hero for the same thing. Fix: repeat the clearest word.
12. False ranges. Watch: "from the Big Bang to dark matter," "from X to Y" where X and Y are not on a real scale. Fix: list the items directly.

## Style patterns

13. Em dash overuse. Watch for em dashes used where a comma, a period, or a restructure would do. Some brands ban them outright; if yours does, that hard rule lives in `voice.md` as a guardrail, not here.
14. Boldface overuse. Watch: mechanically bolded terms. Fix: remove the bolding.
15. Inline-header lists. Watch: "**Thing:** sentence about the thing." Fix: convert to prose or a clean list.
16. Title Case headings. Fix: sentence case.
17. Emojis. Watch: emojis decorating headings or bullets. Fix: remove them.
18. Curly quotes. Fix: straight quotes.

## Communication patterns

19. Chatbot artifacts. Watch: "I hope this helps," "let me know if," "here is a," "of course!," "certainly!" Fix: remove entirely.
20. Knowledge-cutoff disclaimers. Watch: "as of my last update," "while details are limited in available sources." Fix: find the fact or cut.
21. Sycophantic tone. Watch: "great question," "you're absolutely right," "excellent point." Fix: respond directly.

## Filler and hedging

22. Filler phrases. "In order to" to "to." "Due to the fact that" to "because." "At this point in time" to "now." "Has the ability to" to "can." "It is important to note that" deleted.
23. Excessive hedging. "Could potentially possibly" to "may." Cut stacked qualifiers.
24. Generic positive conclusions. Watch: "the future looks bright," "exciting times ahead." Fix: a specific plan or fact, or cut.

## Add a pulse (soul)

Removing patterns is only half the job. Also flag writing that is technically clean but dead: every sentence the same length, no opinion, no first person where it fits, no acknowledgment of complexity, reads like a press release. The fix is not mechanical, note it as a Drift and suggest injecting a real opinion, varied rhythm, or a specific reaction.

## Grading

- Aligned: none of patterns 1 to 24, and it has a pulse.
- Drift: a few soft tells, or clean-but-soulless, no hard guardrail break.
- Misaligned: an AI-vocabulary word, chatbot artifact, or sycophancy in outward copy, or em-dash overuse. (If the brand bans em dashes outright in `voice.md`, a single one is Misaligned.)
