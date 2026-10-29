---
type: log
status: active
tags: [de-slop, quality-gate, output-review, supervisory]
---

> [!info] What this is
> Append-only log of de-slop quality-gate runs, sectioned by person. One entry per output checked: date, what it was, the verdict, and the findings. This is the supervisory view: how each teammate is using the gate, and the patterns that keep showing up in their copy. Within each person, newest at the bottom. Starts empty and fills from real runs only.

# Supervisory read

> [!abstract] The pattern across the team
> Once there are enough runs, summarize here: total runs, the findings that fire most across the team, and a one-line read per person. Update as it fills.

| Person | Runs | Blockers | What keeps showing up |
|--------|------|----------|-----------------------|
{{One row per teammate. Counts start at 0. Fill the pattern column once a person has a few runs.}}

---

{{One section per teammate, in this shape. Repeat the block for each name on the roster.}}

# {{Name}}

> [!summary] {{Name}} · 0 runs
> No runs yet. Once there are a few, summarize the recurring pattern here: the kind of output they check most, and what their copy keeps getting flagged for.

### Runs

{{Entries append here, oldest first. Entry shape:}}
{{**YYYY-MM-DD · what the output was (modality, audience)**}}
{{Verdict: ✅ / ✅⚠️ / ❌ + one line.}}
{{- Check (Source) · severity · what's off.}}
