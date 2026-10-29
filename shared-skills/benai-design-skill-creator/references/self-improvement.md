# Self-improvement: the update-yourself contract

A skill that only reads its files is a template. A skill that also writes them is a system that compounds. This contract applies to this creator skill itself AND to every skill it generates - copy this file into each generated skill's `references/` folder and cite it from its SKILL.md.

## The trigger list

Update your own files, in the same session, when the user gives any of these:

1. **Layout-changing feedback.** They moved, resized, restructured, or removed something structural on the canvas, or said the equivalent in chat ("the logo should always sit bottom-right", "two columns, not three"). Cosmetic one-offs (a word swap for this post, a nudged margin) stay local to the run.
2. **A new reference.** They pasted a link or screenshot of something they want to look like. Add it (or a one-line description plus the link) to the skill's references/sources file so the next run starts from it.
3. **A hard rule.** "Never X", "always Y", "stop doing Z". These are the most valuable words a user ever says to a skill. They go into the skill's rules verbatim, with a one-line note on what prompted them.
4. **A corrected fact.** A brand value, a wrong assumption about their audience, an input type you mishandled. Fix the file that carried the wrong belief.

## Where each kind of feedback lands

| Feedback | File to update |
|---|---|
| Structural layout change | The template file itself (and its light/dark twin, so the modes never drift apart) |
| New reference or example | The skill's sources/references file |
| Hard rule ("never X") | The skill's rules section or rules file |
| Taste answer (density, mood, ...) | The skill's defaults, recorded as an answered question |
| Input-handling correction | The input contract |

## How to do it without breaking things

- **Re-tokenize before saving.** If the user edited a canvas, their concrete values (a hex, a font name) go back into the template as tokens, not literals - the template must stay brand-portable.
- **One source, both modes.** When light and dark variants exist, fold the change into the shared source so a fix in one mode cannot silently miss the other.
- **Say what you changed.** End the session by naming each file you updated and the one-line reason. Silent self-edits erode trust; narrated ones build it.
- **Never weaken a gate.** Feedback can change templates, references, rules, and defaults. It cannot remove the design-system gate, the /design variation gate, or the canvas delivery - those are the framework, not preferences.

## The clause to bake into generated skills

Include this (adapted to the skill's own file names) in every generated SKILL.md:

> **This skill improves itself.** When the user gives layout-changing feedback, a new reference, or a hard rule ("never X"), update the matching file in this skill - templates, references, or rules - in the same session, then say what changed. The skill you run next month should be better than the one you run today, because of what happened in between.
