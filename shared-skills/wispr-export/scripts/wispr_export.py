#!/usr/bin/env python3
"""
Wispr Flow Transcript Exporter

Find and export your Wispr Flow voice transcripts from the local flow.sqlite
database. STRICTLY READ-ONLY — the database is opened in read-only mode and is
never modified.

The transcripts live in the `History` table. Each entry has three text columns:
  - asrText        raw speech-to-text
  - formattedText  cleaned / punctuated version
  - editedText     your manual edits (if any)
By default the exporter picks the best available text per entry:
  editedText > formattedText > asrText.

Usage:
  # Quick overview (counts, date range, top apps) — the default when no command
  python3 wispr_export.py stats

  # One big file grouped by date
  python3 wispr_export.py export --mode single --output transcripts.md

  # One markdown file per day in a folder
  python3 wispr_export.py export --mode daily --output ./wispr-flow/

  # One file per app (Warp, Chrome, Slack, ...)
  python3 wispr_export.py export --mode by-app --output ./wispr-by-app/

  # Run your own read-only SQL (SELECT only) and get CSV back
  python3 wispr_export.py query --sql "SELECT timestamp, app, formattedText FROM History LIMIT 20"

  # Print a ready-to-edit starter query and exit
  python3 wispr_export.py query --print-template

Common filters (apply to stats and export):
  --today                only today's entries (shortcut for --since <today>)
  --this-week            only this week's entries (since Monday)
  --since YYYY-MM-DD     only entries on/after this date (UTC)
  --until YYYY-MM-DD     only entries on/before this date (UTC)
  --app SUBSTR           only apps whose bundle-id or friendly name contains SUBSTR
  --text auto|formatted|asr|edited   which text column to export (default: auto)
  --min-words N          skip entries with fewer than N words (default: 1)
  --include-archived     include rows where isArchived = 1 (default: excluded)
  --db PATH              override the database location
"""

import argparse
import csv
import datetime
import glob
import os
import platform
import re
import sqlite3
import sys
from collections import defaultdict, Counter


# Map macOS bundle IDs (and a few others) to friendly, filename-safe names.
APP_NAMES = {
    "dev.warp.Warp-Stable": "Warp",
    "com.google.Chrome": "Chrome",
    "com.brave.Browser": "Brave",
    "com.tinyspeck.slackmacgap": "Slack",
    "com.anthropic.claudefordesktop": "Claude Desktop",
    "md.obsidian": "Obsidian",
    "notion.id": "Notion",
    "net.whatsapp.WhatsApp": "WhatsApp",
    "tv.parsec.www": "Parsec",
    "com.google.antigravity": "Antigravity",
    "com.apple.ScreenContinuity": "Screen Continuity",
    "com.apple.Safari": "Safari",
    "com.microsoft.VSCode": "VS Code",
}


def app_data_roots():
    """Per-platform directories where app data (and Wispr Flow) live."""
    system = platform.system()
    if system == "Darwin":
        return [os.path.expanduser("~/Library/Application Support")]
    if system == "Windows":
        return [os.environ[v] for v in ("APPDATA", "LOCALAPPDATA") if os.environ.get(v)]
    return [os.path.expanduser("~/.config"), os.path.expanduser("~/.local/share")]


def default_db_path():
    """The standard flow.sqlite location for this platform (no username
    hardcoded — derived from the current user's home via expanduser)."""
    roots = app_data_roots()
    base = roots[0] if roots else os.path.expanduser("~")
    return os.path.join(base, "Wispr Flow", "flow.sqlite")


def discover_db_path():
    """Find flow.sqlite without assuming a fixed path. Use the standard
    location if present; otherwise shallow-glob the app-data roots for any
    Wispr-named folder containing flow.sqlite (handles different usernames,
    OSes, and folder-name variants). Falls back to the standard path so the
    "not found" error still points somewhere sensible."""
    standard = default_db_path()
    if os.path.isfile(standard):
        return standard
    for root in app_data_roots():
        for pattern in ("*Wispr*/flow.sqlite", "*Wispr*/*/flow.sqlite"):
            matches = sorted(glob.glob(os.path.join(root, pattern)))
            if matches:
                return matches[0]
    return standard


def friendly_app(app):
    """Human-readable app name from a bundle id (or '(unknown)' when blank)."""
    if not app:
        return "(unknown)"
    if app in APP_NAMES:
        return APP_NAMES[app]
    # Fall back to the last dotted segment, title-cased.
    tail = app.split(".")[-1]
    return tail or app


def safe_filename(name):
    """Filename-safe slug for app/day file names."""
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_") or "untitled"


def connect_readonly(db_path):
    """Open the database strictly read-only so it can never be modified."""
    if not os.path.isfile(db_path):
        sys.exit(f"Error: Wispr Flow database not found at:\n  {db_path}\n"
                 f"Pass --db PATH if it lives elsewhere.")
    uri = f"file:{db_path}?mode=ro"
    return sqlite3.connect(uri, uri=True)


def build_where(args):
    """Build a WHERE clause + params from the common filters."""
    clauses = []
    params = []
    if not args.include_archived:
        clauses.append("COALESCE(isArchived, 0) = 0")
    clauses.append("COALESCE(numWords, 0) >= ?")
    params.append(args.min_words)
    if args.since:
        clauses.append("substr(timestamp, 1, 10) >= ?")
        params.append(args.since)
    if args.until:
        clauses.append("substr(timestamp, 1, 10) <= ?")
        params.append(args.until)
    if args.app:
        # Match either the raw bundle id or a known friendly name.
        matched_bundles = [b for b, n in APP_NAMES.items()
                           if args.app.lower() in n.lower()]
        like = f"%{args.app.lower()}%"
        sub = ["LOWER(COALESCE(app,'')) LIKE ?"]
        params.append(like)
        for b in matched_bundles:
            sub.append("app = ?")
            params.append(b)
        clauses.append("(" + " OR ".join(sub) + ")")
    where = " WHERE " + " AND ".join(clauses) if clauses else ""
    return where, params


def pick_text(row, mode):
    """Choose the text column for a row given the --text mode."""
    asr, formatted, edited = row["asrText"], row["formattedText"], row["editedText"]
    if mode == "asr":
        return asr or ""
    if mode == "formatted":
        return formatted or ""
    if mode == "edited":
        return edited or ""
    # auto: best available
    return (edited or formatted or asr or "").strip()


def fetch_entries(conn, args):
    """Yield filtered History rows ordered by time."""
    conn.row_factory = sqlite3.Row
    where, params = build_where(args)
    sql = (f"SELECT timestamp, app, url, asrText, formattedText, editedText, "
           f"numWords FROM History{where} ORDER BY timestamp ASC")
    return conn.execute(sql, params)


def day_of(timestamp):
    """YYYY-MM-DD (UTC) from a Wispr timestamp string."""
    return (timestamp or "")[:10] or "unknown-date"


def time_of(timestamp):
    """HH:MM (UTC) from a Wispr timestamp string."""
    return (timestamp or "")[11:16]


def format_entry(row, text):
    """One transcript block in markdown."""
    app = friendly_app(row["app"])
    t = time_of(row["timestamp"])
    ctx = f"`{t}` · **{app}**"
    if row["url"]:
        ctx += f" · {row['url']}"
    return f"{ctx}\n\n{text}\n"


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_stats(conn, args):
    where, params = build_where(args)
    total, words = conn.execute(
        f"SELECT COUNT(*), COALESCE(SUM(numWords),0) FROM History{where}", params
    ).fetchone()
    if total == 0:
        print("No transcripts match the current filters.")
        return
    dmin, dmax = conn.execute(
        f"SELECT MIN(substr(timestamp,1,10)), MAX(substr(timestamp,1,10)) "
        f"FROM History{where}", params
    ).fetchone()
    top = conn.execute(
        f"SELECT app, COUNT(*) c FROM History{where} GROUP BY app "
        f"ORDER BY c DESC LIMIT 10", params
    ).fetchall()

    print(f"Database : {args.db}")
    print(f"Transcripts (filtered) : {total:,}")
    print(f"Total words            : {words:,}")
    print(f"Date range (UTC)       : {dmin} → {dmax}")
    print("Top apps:")
    for app, c in top:
        print(f"  {friendly_app(app):<18} {c:,}")


def cmd_export_single(conn, args):
    rows = fetch_entries(conn, args)
    by_day = defaultdict(list)
    count = 0
    for row in rows:
        text = pick_text(row, args.text)
        if not text.strip():
            continue
        by_day[day_of(row["timestamp"])].append(format_entry(row, text))
        count += 1

    out = args.output or "wispr-flow-transcripts.md"
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write("# Wispr Flow Transcripts\n\n")
        for day in sorted(by_day):
            f.write(f"\n## {day}\n\n")
            f.write("\n---\n\n".join(by_day[day]))
            f.write("\n")
    print(f"Wrote {count:,} transcripts across {len(by_day)} day(s) -> {out}")


def cmd_export_daily(conn, args):
    rows = fetch_entries(conn, args)
    by_day = defaultdict(list)
    count = 0
    for row in rows:
        text = pick_text(row, args.text)
        if not text.strip():
            continue
        by_day[day_of(row["timestamp"])].append(format_entry(row, text))
        count += 1

    out_dir = args.output or "./wispr-flow/"
    os.makedirs(out_dir, exist_ok=True)
    for day, blocks in sorted(by_day.items()):
        path = os.path.join(out_dir, f"{day}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# {day}\n\n")
            f.write("\n---\n\n".join(blocks))
            f.write("\n")
    print(f"Wrote {count:,} transcripts into {len(by_day)} daily file(s) -> {out_dir}")


def cmd_export_by_app(conn, args):
    rows = fetch_entries(conn, args)
    by_app = defaultdict(list)
    count = 0
    for row in rows:
        text = pick_text(row, args.text)
        if not text.strip():
            continue
        by_app[friendly_app(row["app"])].append(format_entry(row, text))
        count += 1

    out_dir = args.output or "./wispr-by-app/"
    os.makedirs(out_dir, exist_ok=True)
    for app, blocks in sorted(by_app.items()):
        path = os.path.join(out_dir, f"{safe_filename(app)}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# {app}\n\n")
            f.write("\n---\n\n".join(blocks))
            f.write("\n")
    print(f"Wrote {count:,} transcripts into {len(by_app)} app file(s) -> {out_dir}")


TEMPLATE_QUERY = """\
-- Read-only starter query. Edit freely, then run:
--   python3 wispr_export.py query --sql "<your query>"
SELECT
  substr(timestamp, 1, 19)              AS time,
  app,
  url,
  numWords,
  COALESCE(editedText, formattedText, asrText) AS text
FROM History
WHERE COALESCE(isArchived, 0) = 0
  AND COALESCE(numWords, 0) > 0
  -- AND substr(timestamp,1,10) >= '2026-06-01'
  -- AND app = 'com.tinyspeck.slackmacgap'
ORDER BY timestamp DESC
LIMIT 100;
"""


def cmd_query(conn, args):
    if args.print_template:
        print(TEMPLATE_QUERY)
        return
    if not args.sql:
        sys.exit("Provide --sql \"SELECT ...\" or use --print-template.")
    stripped = args.sql.lstrip().lower()
    if not (stripped.startswith("select") or stripped.startswith("with")):
        sys.exit("Refusing to run: only SELECT/WITH (read-only) queries are allowed.")
    cur = conn.execute(args.sql)
    writer = csv.writer(sys.stdout)
    if cur.description:
        writer.writerow([d[0] for d in cur.description])
    for r in cur:
        writer.writerow(r)


def main():
    parser = argparse.ArgumentParser(description="Export Wispr Flow transcripts (read-only)")
    parser.add_argument("--db", default=discover_db_path(),
                        help="Path to flow.sqlite (auto-discovered if omitted)")
    sub = parser.add_subparsers(dest="command")

    def add_filters(p):
        p.add_argument("--since", help="Only entries on/after YYYY-MM-DD (UTC)")
        p.add_argument("--until", help="Only entries on/before YYYY-MM-DD (UTC)")
        p.add_argument("--today", action="store_true", help="Shortcut: only today's entries")
        p.add_argument("--this-week", action="store_true",
                       help="Shortcut: entries since Monday of this week")
        p.add_argument("--app", help="Filter by app bundle-id or friendly name substring")
        p.add_argument("--text", choices=["auto", "formatted", "asr", "edited"],
                       default="auto", help="Which text column to export (default: auto)")
        p.add_argument("--min-words", type=int, default=1, help="Skip entries below N words")
        p.add_argument("--include-archived", action="store_true",
                       help="Include archived rows (default: excluded)")

    p_stats = sub.add_parser("stats", help="Show counts, date range, top apps")
    add_filters(p_stats)

    p_export = sub.add_parser("export", help="Export transcripts to markdown")
    p_export.add_argument("--mode", choices=["single", "daily", "by-app"],
                          default="single", help="Export layout (default: single)")
    p_export.add_argument("--output", help="Output file (single) or directory (daily/by-app)")
    add_filters(p_export)

    p_query = sub.add_parser("query", help="Run a read-only SELECT and get CSV")
    p_query.add_argument("--sql", help="A SELECT/WITH query to run")
    p_query.add_argument("--print-template", action="store_true",
                         help="Print a starter query and exit")

    args = parser.parse_args()
    # Default command is stats when none given.
    if not args.command:
        args.command = "stats"
        for attr, val in (("since", None), ("until", None), ("app", None),
                          ("text", "auto"), ("min_words", 1), ("include_archived", False),
                          ("today", False), ("this_week", False)):
            setattr(args, attr, val)

    # Resolve the --today / --this-week shortcuts into a --since date (local).
    if getattr(args, "today", False) and not args.since:
        args.since = datetime.date.today().isoformat()
    if getattr(args, "this_week", False) and not args.since:
        today = datetime.date.today()
        args.since = (today - datetime.timedelta(days=today.weekday())).isoformat()

    conn = connect_readonly(args.db)
    try:
        if args.command == "stats":
            cmd_stats(conn, args)
        elif args.command == "export":
            {"single": cmd_export_single,
             "daily": cmd_export_daily,
             "by-app": cmd_export_by_app}[args.mode](conn, args)
        elif args.command == "query":
            cmd_query(conn, args)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
