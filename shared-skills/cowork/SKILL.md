---
name: cowork
description: Export and import Claude Desktop Cowork sessions as portable archives, and diagnose/clean Claude Desktop cache and storage issues.
  Use this skill whenever the user says "export session", "import session", "backup cowork",
  "transfer session", "share cowork session", "save my chat", "move session to another machine",
  "portable session", "export cowork", "import cowork", "clear cache", "disk space", "storage full",
  "ENOSPC", "no space left", "clean up claude", "vm cache", or wants to archive, share, migrate
  Claude Desktop Cowork conversations, or troubleshoot Claude Desktop storage problems.
allowed-tools: Bash, Read, Write, AskUserQuestion
---

# Cowork Porter — Export & Import Desktop Sessions

Tools for exporting and importing Claude Desktop Cowork sessions as portable zip archives. Each archive contains: metadata, conversation history, audit logs, referenced project files, and VM-reconstructed files.

## Scripts

Both scripts are non-interactive CLI tools. Always call them with explicit flags — never run without arguments.

### cowork-export.py

**Path:** `python3 skills/cowork/scripts/cowork-export.py`

| Flag | Purpose |
|------|---------|
| `--list` | Print sessions as human-readable table (for display) |
| `--list-json` | Print sessions as JSON array (for parsing — includes UUIDs) |
| `--session UUID` | Export a specific session by its full UUID |
| `--all` | Export all sessions |
| `--output DIR` | Output directory (default: `~/Documents`) |

`--list-json` returns entries with: `number`, `uuid`, `title`, `model`, `created_at`, `last_activity`, `folders`, `is_archived`.

Use `--list-json` to look up UUIDs, then pass them to `--session`.

### cowork-import.py

**Path:** `python3 skills/cowork/scripts/cowork-import.py`

| Flag | Purpose |
|------|---------|
| `<archive.zip>` | Path to the zip archive to import |
| `--copy` | Force import as copy with new UUID |
| `--from-dir DIR` | Import from an extracted directory instead of zip |
| `--assets-dir DIR` | Custom directory for assets (default: `~/Documents/CoworkImports/<title>`) |

If the session already exists locally, the script auto-imports as a copy with "(Copy)" in the title.

### Previewing an archive before import

To inspect a zip without importing:
```bash
python3 -c "
import zipfile, json, sys
with zipfile.ZipFile(sys.argv[1]) as zf:
    manifest_name = [n for n in zf.namelist() if n.endswith('manifest.json')][0]
    m = json.loads(zf.read(manifest_name))
    s = m['session']
    print(f\"Session: {s['title']}\")
    print(f\"From: {m.get('source_machine', 'unknown')}\")
    print(f\"Model: {s['model']}\")
    print(f\"Exported: {m.get('exported_at', 'unknown')}\")
    print(f\"Assets: {len(s.get('original_folders', []))} folder(s)\")
    print(f\"VM files: {s.get('vm_file_count', 0)}\")
" <archive.zip>
```

## Cache & Storage Diagnostics

Claude Desktop stores data in a platform-specific directory. Over time, VM bundles and caches can consume significant disk space (20GB+).

### Data directory locations

| Platform | Path |
|----------|------|
| macOS | `~/Library/Application Support/Claude/` |
| Linux | `~/.config/Claude/` |
| Windows | `%APPDATA%\Claude\` |

### Storage breakdown

To diagnose, run `du -d1 -h` on the data directory and show the user the results sorted by size:

```bash
du -d1 -h "$HOME/Library/Application Support/Claude/" 2>/dev/null | sort -rh
```

### Common space hogs

| Directory | Typical Size | Safe to Delete | What It Is |
|-----------|-------------|----------------|------------|
| `vm_bundles/` | 10-20GB+ | Yes | Cowork VM images, re-downloaded on demand |
| `Cache/` | 500MB-1GB | Yes | Electron browser cache |
| `Code Cache/` | 100-200MB | Yes | V8 compiled code cache |
| `claude-code-vm/` | 100-300MB | Yes | Claude Code VM state |
| `GPUCache/` | ~500KB | Yes | GPU shader cache |
| `DawnWebGPUCache/` | ~500KB | Yes | WebGPU cache |
| `DawnGraphiteCache/` | ~500KB | Yes | Graphite render cache |

### Additional cache locations (outside data dir)

| Path | What It Is |
|------|------------|
| `~/Library/Caches/com.anthropic.claudefordesktop/` | App-level cache |
| `~/Library/Caches/com.anthropic.claudefordesktop.ShipIt/` | Auto-updater cache |
| `~/Library/Caches/claude-cli-nodejs/` | Claude Code CLI cache |
| `~/Library/Logs/Claude/` | App logs |
| `~/Library/Logs/CoworkScheduler/` | Cowork scheduler logs |
| `~/Library/Logs/CoworkWebhook/` | Cowork webhook logs |

### Cleaning

**Important:** User should quit Claude Desktop before cleaning. Check with `pgrep -la "Claude"`.

To clear all caches and VM bundles:
```bash
rm -rf "$HOME/Library/Application Support/Claude/vm_bundles"
rm -rf "$HOME/Library/Application Support/Claude/Cache"
rm -rf "$HOME/Library/Application Support/Claude/Code Cache"
rm -rf "$HOME/Library/Application Support/Claude/claude-code-vm"
rm -rf "$HOME/Library/Application Support/Claude/GPUCache"
rm -rf "$HOME/Library/Application Support/Claude/DawnWebGPUCache"
rm -rf "$HOME/Library/Application Support/Claude/DawnGraphiteCache"
rm -rf "$HOME/Library/Caches/com.anthropic.claudefordesktop"
rm -rf "$HOME/Library/Caches/com.anthropic.claudefordesktop.ShipIt"
rm -rf "$HOME/Library/Caches/claude-cli-nodejs"
rm -rf "$HOME/Library/Logs/Claude"
rm -rf "$HOME/Library/Logs/CoworkScheduler"
rm -rf "$HOME/Library/Logs/CoworkWebhook"
```

**Do NOT delete:** `claude-code-sessions/`, `local-agent-mode-sessions/`, `Claude Extensions/`, `Claude Extensions Settings/`, `IndexedDB/`, `Local Storage/`, `Session Storage/` — these contain user data and settings.

## Domain Knowledge

- **Cross-platform paths** — Scripts auto-detect: macOS (`~/Library/Application Support/Claude`), Linux (`~/.config/Claude`), Windows (`%APPDATA%\Claude`). Don't hardcode paths.
- **After import, restart Claude Desktop** to see the session in Cowork.
- **Imported session history is viewable** but VM state is ephemeral — it may not be resumable.
- **Data integrity** — the scripts handle UUID remapping, asset copying, and metadata updates. Don't modify archives or session files manually.
- **Default export location:** `~/Documents`
- **Default import assets location:** `~/Documents/CoworkImports/<title>/`
- **Confirm before acting** — export and import are significant operations. Confirm the user's selection before running.
