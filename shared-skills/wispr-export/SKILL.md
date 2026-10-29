---
name: wispr-export
description: Find and export your Wispr Flow voice transcripts from the local flow.sqlite database.
  Use this skill whenever the user says "export wispr", "wispr flow", "wispr transcripts",
  "voice transcripts", "export my dictation", "what did I say", "speech to text history",
  "dump my wispr", "wispr export", "find my transcripts", or wants to pull, browse, search,
  or back up their Wispr Flow dictation history. Strictly read-only — never modifies the
  Wispr database.
allowed-tools: Bash, Read, Write, AskUserQuestion
---

# Wispr Flow Transcript Exporter

Find and export Wispr Flow voice transcripts from the local SQLite database. The
script is **strictly read-only** — it opens the database in `mode=ro` and never
writes to it.

## Where the data lives

The script **auto-discovers** `flow.sqlite` — never hardcode a path. It checks
the standard per-platform location and, if not found there, shallow-globs the
app-data roots for any Wispr-named folder containing `flow.sqlite`. This works
across machines and usernames. Pass `--db PATH` only to override.

| Platform | Standard location (auto-detected) |
|----------|-----------------------------------|
| macOS | `~/Library/Application Support/Wispr Flow/flow.sqlite` |
| Windows | `%APPDATA%\Wispr Flow\flow.sqlite` (also checks `%LOCALAPPDATA%`) |
| Linux | `~/.config/Wispr Flow/flow.sqlite` (also `~/.local/share`) |

Transcripts are in the `History` table. The three text columns, in order of
preference, are `editedText` (your manual edits) → `formattedText` (cleaned) →
`asrText` (raw speech-to-text). Each row also carries `timestamp` (UTC),
`app` (bundle id), `url`, `numWords`, and `isArchived`.

## Workflow

1. **Always start with `stats`** to show the user what's there (counts, date
   range, top apps) before exporting anything large.
2. **FIRST question — how much to export (time range).** Use AskUserQuestion
   with these options:
   - **Everything** — all transcripts (no date filter)
   - **This week** — `--this-week` (since Monday)
   - **Today** — `--today`
   - (the auto-provided free-text "Other" lets them type any range, e.g.
     "since May 1" → `--since 2026-05-01`, or "Slack only last month")

   Interpret whatever they type into the right `--since/--until/--app` flags.
3. **Then pick the shape** if not obvious (defaults to `--mode single`). The
   four shapes map to the `--mode`/`query` choices below; only ask if unclear.
4. Run the export. Confirm the resolved DB path and the output path back.

> Do not hardcode output paths either. Default to a clearly-named file in the
> user's home/Documents (or wherever they ask), and echo the final path.

## wispr_export.py

**Path:** `python3 scripts/wispr_export.py`

| Command | Purpose |
|---------|---------|
| `stats` | Counts, total words, date range, top apps (default if no command) |
| `export --mode single` | One big markdown file grouped by date |
| `export --mode daily` | One `.md` per day in a folder (easy to browse) |
| `export --mode by-app` | One file per app (Warp, Chrome, Slack, …) |
| `query --sql "SELECT …"` | Run a read-only SELECT, get CSV on stdout |
| `query --print-template` | Print a ready-to-edit starter query |

### Common filters (work on `stats` and `export`)

| Flag | Purpose |
|------|---------|
| `--today` | Shortcut: only today's entries |
| `--this-week` | Shortcut: entries since Monday of this week |
| `--since YYYY-MM-DD` | Only entries on/after this date (UTC) |
| `--until YYYY-MM-DD` | Only entries on/before this date (UTC) |
| `--app SUBSTR` | Match bundle-id or friendly name (e.g. `--app slack`, `--app Warp`) |
| `--text auto\|formatted\|asr\|edited` | Which text column to export (default `auto`) |
| `--min-words N` | Skip entries below N words (default 1) |
| `--include-archived` | Include archived rows (default: excluded) |
| `--db PATH` | Override the database location |

### Examples

```bash
# Overview first
python3 scripts/wispr_export.py stats

# Everything, one file grouped by date
python3 scripts/wispr_export.py export --mode single \
  --output ~/wispr-flow-transcripts.md

# Just today
python3 scripts/wispr_export.py export --mode single --today \
  --output ~/wispr-today.md

# This week, one file per day
python3 scripts/wispr_export.py export --mode daily --this-week \
  --output ~/wispr-flow/

# Just what you dictated into Slack
python3 scripts/wispr_export.py export --mode by-app --app slack \
  --output ~/wispr-by-app/

# Pull a custom subset yourself
python3 scripts/wispr_export.py query \
  --sql "SELECT substr(timestamp,1,10) d, COUNT(*) FROM History GROUP BY d ORDER BY d"
```

## Domain knowledge

- **Read-only, always.** The DB is the user's live Wispr Flow store. The script
  enforces `mode=ro` and the `query` command refuses anything but `SELECT`/`WITH`.
  Do not move, copy-over, or delete `flow.sqlite`.
- **Text precedence** is `editedText > formattedText > asrText` in `auto` mode.
  Use `--text asr` to see exactly what was heard vs. the cleaned output.
- **Timestamps are UTC** with a `+00:00` offset; day grouping uses the UTC date.
- **Archived entries are excluded by default** (`isArchived = 1`) — add
  `--include-archived` to see them.
- **`app` is a bundle id** (e.g. `com.tinyspeck.slackmacgap`); the script maps the
  common ones to friendly names and falls back to the last dotted segment.
- **Audio/screenshot BLOBs** exist per row but are not exported — this skill is
  about text. Pull them via a custom `query` if ever needed.
- **Confirm before large dumps** — 4k+ transcripts / ~78k words is a lot; show
  `stats` and let the user pick the shape first.
