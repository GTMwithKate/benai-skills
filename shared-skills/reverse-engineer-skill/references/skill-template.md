# Skill template

The shape of the skill you build in step 3. Replace everything in angle brackets.

---

## SKILL.md

```markdown
---
name: <short-kebab-name>
description: <What it makes, in one sentence.> Rules are reverse-engineered from <n> best and <n> worst <outputs> by <metric>. Input is <what the user gives it>. Use when the user says "<phrase 1>", "<phrase 2>", "<phrase 3>", or <the situation that should trigger it>.
---

# <Skill name>

Makes ONE <output>. The rules in `references/rules.md` come from <n> real examples (<n> best, <n> worst by <metric>). The full findings are in `references/analysis.md`.

## The one idea behind every rule

<The headline finding, in one or two sentences, and what it means for the writing.>

## Hard limits (always)

- Never invent numbers, results, names or dates. A fact comes from the input or the user. Otherwise write `[check]`.
- Never copy whole sentences from the examples. Copy the shape.
- Numbers from the examples are not facts about the user. Never reuse them as the user's results.
- <Two to four rules that must never break, taken from rules.md.>

## Steps

1. **Read the input.** <What to collect, including the author's name if the output has one. What to ask if it is missing.>
2. **Read the examples.** Read two best and one worst in `references/examples/` before writing. Start with <file>, <file> and <file>.
3. **<Decide the key choice the analysis found matters>,** e.g. the angle, the offer or the hook. Say which you chose.
4. **Write it** in the shape of `references/template.md`.
5. **Check it.** Save the draft and run `python3 references/check.py <draft-file>` (if it exists). Fix every FAIL and run again. Then go through the rules in `references/rules.md`.
6. **Output** exactly in the template. Put the check result and any open `[check]` items in the reply, not in the output file.

## When it goes wrong

- <A case the examples did not cover, and what to do.>
```

---

## references/rules.md

One rule per line, numbered, each traced to findings:

```markdown
# Rules

1. <Rule.> (findings 1, 2)
2. <Rule.> (finding 5)

## Words and phrases to avoid
- <phrase> (from the worst set, finding 9)
```

## references/template.md

The exact output shape to fill in: the parts in order, with the length and position rules written into the placeholders. Use plain section headings that `check.py` can find. End it with a checklist of the rules that cannot be measured.

## references/check.py

Write it only when three or more rules can be measured. Keep it in plain Python with no extra installs.

```python
"""Check a draft against the measurable rules in rules.md.

Usage: python3 check.py <draft-file>
"""
import re
import sys

BANNED = ["<phrase from the worst set>"]


def main(path):
    text = open(path, encoding="utf-8").read()
    words = text.split()
    results = []

    def check(ok, label, detail=""):
        results.append(("PASS" if ok else "FAIL", label, detail))

    LIMIT = 300  # replace with the upper limit from your analysis table
    check(len(words) <= LIMIT, f"{LIMIT} words or less", f"{len(words)} words")
    hits = [b for b in BANNED if b.lower() in text.lower()]
    check(not hits, "No banned phrases", ", ".join(hits))
    # Add one check per measurable rule: a link position, a required section, a line count.

    for status, label, detail in results:
        print(f"{status}  {label}  {detail}".rstrip())
    sys.exit(1 if any(r[0] == "FAIL" for r in results) else 0)


if __name__ == "__main__":
    main(sys.argv[1])
```
