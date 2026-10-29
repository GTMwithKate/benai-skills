# Analysis template

Fill this in during step 2. Save it as `<new-skill-name>/references/analysis.md`.

---

```markdown
---
type: analysis
status: awaiting-approval
output: <what the output is>
mode: <performance / inspiration / style>
metric: <the number used to rank, or "none">
examples: <n> best, <n> worst, <n> holdout
created: <YYYY-MM-DD>
---

# <Output>: <n> best vs <n> worst by <metric>

Source: the files in `examples/best/` and `examples/worst/`. Holdout examples were not read.
Tags: **seen** = I can point to it in the examples or numbers. **inferred** = my best reading of why. **unknown** = the examples cannot tell.

## The headline

<One or two sentences: the biggest difference between best and worst, with its numbers.>

| Measure | Best (avg) | Worst (avg) | Tag |
|---|---|---|---|
| <metric> | | | seen |
| <length> | | | seen |
| <position of the key element> | | | seen |

## Findings

### <Dimension, e.g. Opening>
1. **<Finding in one line.>** <Count it: "4 of 6 best ... 0 of 6 worst".> **seen**
2. **<Why that likely matters.>** **inferred**

### <Dimension, e.g. Structure>
3. ...

## Rules for the skill

| # | Rule | From findings | Tag |
|---|---|---|---|
| R1 | <Do this, in one line> | 1, 2 | seen |
| R2 | <Never do this> | 5 | inferred |

## Open questions

- <Unknown>: <what data would settle it>.

## Dropped examples

- <file>: <why it was left out of the comparison>.
```

---

## Checks before showing it to the user

- Every finding has exactly one tag.
- Every count matches the files. Recount anything that decides a rule.
- No finding says "always" or "never" unless every example agrees.
- Each rule points at the findings behind it.
- The headline uses the numbers from the table, not new ones.
