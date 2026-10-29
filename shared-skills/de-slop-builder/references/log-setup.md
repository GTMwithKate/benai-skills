---
type: reference
status: active
tags: [de-slop-builder, log, setup]
---

# Log setup

The slop log is the memory of the gate. For a team it is the supervisory layer: who runs it, what keeps showing up in each person's work. For an individual it is a personal record of recurring mistakes. Either way it is only useful if it is in **one consistent place, addressed the same way every run**. A log that lands in whatever folder the user happened to work in that day is not a log. Settle the location before generating, because the generated Step F hardcodes it.

## Decide the location, best case first

Work down this list and stop at the first that fits.

### 1. Obsidian vault (best case)
Detect an `.obsidian` folder at or above the working directory. If present, the log lives at a fixed path inside it, for example `<vault>/Intelligence/de-slop-log.md` or a folder the user names. A vault is ideal: it is one rooted place, the user is always in it, wikilinks and callouts render, and the file is easy to read as a dashboard. Write the absolute vault-relative path into the generated Step F.

### 2. A fixed local folder or repo
No vault, but a stable project folder or git repo they work in consistently. Put the log there at an absolute path. Warn the user of the catch: this is only consistent if they always invoke the gate from that project. If they work across many folders, this will fragment, so prefer option 3.

### 3. A cloud doc via MCP
No single local home, or they work across many machines and folders. Put the log somewhere cloud that the skill can reach by a fixed address from anywhere. This is the right default for a roaming user.

- Detect what is connected. Look for a Google Docs, Google Drive, or Notion MCP among the available tools (search the tool list for docs, drive, sheets, or notion). Use whatever the user actually has.
- Create one canonical doc (for example a Google Doc titled "De-Slop Log") and capture its document id or URL.
- The generated Step F appends to **that id** every run, regardless of which folder the skill is invoked from. The fixed address is the doc id, not a path.
- A Google Sheet is a fine alternative if they prefer rows: one row per run. Same principle, fixed spreadsheet id.

### 4. Nothing stable exists
Do not generate a skill that logs to a moving target. Instead, tell the user to either create a dedicated folder they will always invoke the gate in (for example `~/de-slop`), or connect a Google Docs or Drive MCP so option 3 becomes available. Pick one with them, set it up, then generate. A consistent home is a precondition, not a nice-to-have.

## Team vs individual: the log shape

This is the one place scope changes the output.

### Team
Use `references/assets/log/log-team.template.md`. The log is segmented by person. Each teammate has a section with a short recurring-pattern summary, sitting under one supervisory read at the top (a per-person scorecard table: runs, blockers, the pattern that keeps showing up). The generated Step F routes each run to the right person's section by the active profile or the name the user gives, and updates that person's summary over time.

The value, in the user's framing: an owner opens the log and sees, per person, how often they run the gate and what their copy keeps getting flagged for, so coaching is specific. One person tends to ship hype, another leaves placeholders, another writes run-ons. That is the alignment dividend.

You never pre-fill this with invented entries. It starts empty under each name and fills from real runs.

### Individual
Use `references/assets/log/log-individual.template.md`. One chronological stream, newest at the bottom, no per-person sections, no supervisory table. Same entry format otherwise.

## What the generated Step F must contain

Whichever location and shape you chose, the generated skill's Step F is explicit and fixed:

- The exact destination: a vault-relative path, an absolute folder path, or a cloud doc id.
- For a team, the routing rule (which person's section this run appends to) and the instruction to refresh that person's summary line.
- The entry format: date, person (for a team), what the output was, the verdict, and each finding as check, source, severity. One line of context plus the findings. Never the whole output.
- The append-only discipline: add an entry, never rewrite past ones.

Write the destination in literally. The generated skill should never have to guess where its log is.
