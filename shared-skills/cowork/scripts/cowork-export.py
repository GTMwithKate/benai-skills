#!/usr/bin/env python3
"""
Cowork Session Exporter
Exports Claude Desktop Cowork sessions into portable archives.

Each export contains:
  - Session metadata (local_<uuid>.json)
  - Conversation data & audit logs (local_<uuid>/ directory)
  - Assets from referenced project folders (userSelectedFolders)
  - VM-reconstructed files (extracted from audit log Write calls)
  - A manifest.json for import on the target machine
  - A bundled cowork-import.py for the recipient

Usage:
  python3 cowork-export.py --list                      # List sessions (human-readable table)
  python3 cowork-export.py --list-json                 # List sessions (JSON with UUIDs)
  python3 cowork-export.py --session UUID              # Export one session by UUID
  python3 cowork-export.py --session UUID --output DIR # Export to a custom directory
  python3 cowork-export.py --all                       # Export all sessions
  python3 cowork-export.py --all --output DIR          # Export all to a custom directory

Default output directory: ~/Documents
"""

import argparse
import json
import os
import shutil
import sys
import datetime
import platform


def get_app_support():
    """Get Claude Desktop app support directory (cross-platform)."""
    system = platform.system()
    if system == "Darwin":
        return os.path.expanduser("~/Library/Application Support/Claude")
    elif system == "Windows":
        return os.path.join(os.environ.get("APPDATA", ""), "Claude")
    else:  # Linux
        return os.path.expanduser("~/.config/Claude")


APP_SUPPORT = get_app_support()
SESSIONS_BASE = os.path.join(APP_SUPPORT, "local-agent-mode-sessions")
DEFAULT_EXPORT_DIR = os.path.expanduser("~/Documents")


def find_all_workspaces():
    """Find all org/workspace directories containing sessions."""
    workspaces = []
    if not os.path.exists(SESSIONS_BASE):
        return workspaces
    for org_id in os.listdir(SESSIONS_BASE):
        org_path = os.path.join(SESSIONS_BASE, org_id)
        if not os.path.isdir(org_path):
            continue
        for ws_id in os.listdir(org_path):
            ws_path = os.path.join(org_path, ws_id)
            if os.path.isdir(ws_path):
                # Check if workspace has any session files
                has_sessions = any(
                    f.startswith("local_") and f.endswith(".json")
                    for f in os.listdir(ws_path)
                )
                if has_sessions:
                    workspaces.append((ws_path, org_id, ws_id))
    return workspaces


def load_sessions_from_all():
    """Load all session metadata from all workspaces."""
    sessions = []
    workspaces = find_all_workspaces()
    for ws_path, org_id, ws_id in workspaces:
        for fname in sorted(os.listdir(ws_path)):
            if fname.startswith("local_") and fname.endswith(".json") and fname != "cowork_settings.json":
                fpath = os.path.join(ws_path, fname)
                try:
                    with open(fpath) as f:
                        data = json.load(f)
                    uuid = data["sessionId"].replace("local_", "")
                    sessions.append({
                        "uuid": uuid,
                        "title": data.get("title", "Untitled"),
                        "model": data.get("model", "unknown"),
                        "created_at": data.get("createdAt"),
                        "last_activity": data.get("lastActivityAt"),
                        "folders": data.get("userSelectedFolders", []),
                        "is_archived": data.get("isArchived", False),
                        "initial_message": data.get("initialMessage", ""),
                        "meta_path": fpath,
                        "dir_path": os.path.join(ws_path, f"local_{uuid}"),
                        "ws_path": ws_path,
                        "org_id": org_id,
                        "ws_id": ws_id,
                    })
                except (json.JSONDecodeError, OSError, KeyError):
                    continue
    return sessions


def format_timestamp(ts):
    if ts is None:
        return "N/A"
    return datetime.datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M")


def print_sessions(sessions):
    """Print sessions as a human-readable table."""
    print(f"\n{'#':<4} {'Title':<40} {'UUID':<12} {'Created':<18} {'Folders'}")
    print("-" * 120)
    for i, s in enumerate(sessions, 1):
        folders_str = ", ".join(os.path.basename(f) for f in s["folders"]) or "(none)"
        title = s["title"][:38]
        uuid_short = s["uuid"][:8] + "..."
        print(f"{i:<4} {title:<40} {uuid_short:<12} {format_timestamp(s['created_at']):<18} {folders_str}")
    print()


def print_sessions_json(sessions):
    """Print sessions as JSON for programmatic use."""
    output = []
    for i, s in enumerate(sessions, 1):
        output.append({
            "number": i,
            "uuid": s["uuid"],
            "title": s["title"],
            "model": s["model"],
            "created_at": format_timestamp(s["created_at"]),
            "last_activity": format_timestamp(s["last_activity"]),
            "folders": [os.path.basename(f) for f in s["folders"]],
            "is_archived": s["is_archived"],
        })
    print(json.dumps(output, indent=2))


def export_session(session, ws_path, org_id, ws_id, export_dir):
    """Export a single session to a .zip archive."""
    uuid = session["uuid"]
    safe_title = "".join(c if c.isalnum() or c in "-_ " else "_" for c in session["title"])[:50].strip()
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"cowork_{safe_title}_{ts}"
    staging_dir = os.path.join(export_dir, f".staging_{uuid}")

    # Clean up any previous staging
    if os.path.exists(staging_dir):
        shutil.rmtree(staging_dir)
    os.makedirs(staging_dir, exist_ok=True)

    session_staging = os.path.join(staging_dir, "session")
    assets_staging = os.path.join(staging_dir, "assets")
    os.makedirs(session_staging)
    os.makedirs(assets_staging)

    # 1. Copy session metadata JSON
    meta_dest = os.path.join(session_staging, os.path.basename(session["meta_path"]))
    shutil.copy2(session["meta_path"], meta_dest)
    print(f"  Copied metadata: {os.path.basename(session['meta_path'])}")

    # 2. Copy session directory (conversation, audit, etc.)
    def ignore_temp_files(directory, files):
        return [f for f in files if f.startswith("~$") or f == ".DS_Store"]

    dir_name = f"local_{uuid}"
    dir_src = session["dir_path"]
    if os.path.isdir(dir_src):
        dir_dest = os.path.join(session_staging, dir_name)
        shutil.copytree(dir_src, dir_dest, symlinks=False, ignore_dangling_symlinks=True, ignore=ignore_temp_files)
        dir_size = sum(
            os.path.getsize(os.path.join(dp, f))
            for dp, dn, filenames in os.walk(dir_dest)
            for f in filenames
        )
        print(f"  Copied session data: {dir_name}/ ({dir_size / 1024:.1f} KB)")

    # 3. Copy assets from userSelectedFolders
    folder_map = {}
    for folder_path in session["folders"]:
        folder_name = os.path.basename(folder_path)
        folder_map[folder_path] = folder_name
        if os.path.isdir(folder_path):
            dest = os.path.join(assets_staging, folder_name)
            shutil.copytree(folder_path, dest, symlinks=False, ignore_dangling_symlinks=True, ignore=ignore_temp_files)
            file_count = sum(len(files) for _, _, files in os.walk(dest))
            assets_size = sum(
                os.path.getsize(os.path.join(dp, f))
                for dp, dn, filenames in os.walk(dest)
                for f in filenames
            )
            print(f"  Copied assets: {folder_name}/ ({file_count} files, {assets_size / 1024:.1f} KB)")
        else:
            print(f"  Warning: Folder not found, skipping assets: {folder_path}")

    # 4. Reconstruct VM-only files from audit log
    vm_files_staging = os.path.join(staging_dir, "vm-files")
    os.makedirs(vm_files_staging)
    vm_file_count = 0
    vm_files_size = 0

    audit_path = os.path.join(dir_src, "audit.jsonl")
    if os.path.exists(audit_path):
        with open(audit_path) as af:
            for line in af:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg = entry.get("message", {})
                content = msg.get("content", "")
                if not isinstance(content, list):
                    continue
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    if block.get("type") != "tool_use":
                        continue
                    name = block.get("name", "")
                    inp = block.get("input", {})
                    if name == "Write":
                        file_path = inp.get("file_path", "")
                        file_content = inp.get("content", "")
                        # Skip files in mnt/ (already captured via userSelectedFolders)
                        if "/mnt/" in file_path:
                            continue
                        if not file_path or not file_content:
                            continue
                        parts = file_path.split("/")
                        try:
                            sessions_idx = parts.index("sessions")
                            rel_path = os.path.join(*parts[sessions_idx + 2:])
                        except (ValueError, IndexError):
                            rel_path = os.path.basename(file_path)
                        dest_path = os.path.join(vm_files_staging, rel_path)
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        with open(dest_path, "w") as wf:
                            wf.write(file_content)
                        vm_file_count += 1
                        vm_files_size += len(file_content.encode("utf-8"))

    if vm_file_count > 0:
        print(f"  Reconstructed VM files: {vm_file_count} files ({vm_files_size / 1024:.1f} KB)")
    else:
        shutil.rmtree(vm_files_staging)

    # 5. Create manifest for import
    manifest = {
        "export_version": "1.0",
        "exported_at": datetime.datetime.now().isoformat(),
        "source_machine": platform.node(),
        "source_os": f"{platform.system()} {platform.release()}",
        "source_home": os.path.expanduser("~"),
        "org_id": org_id,
        "workspace_id": ws_id,
        "session": {
            "uuid": uuid,
            "title": session["title"],
            "model": session["model"],
            "created_at": session["created_at"],
            "last_activity": session["last_activity"],
            "initial_message": session["initial_message"],
            "original_folders": session["folders"],
            "folder_map": folder_map,
            "vm_file_count": vm_file_count,
        },
        "import_instructions": {
            "step_1": "Install Claude Desktop on the target machine and sign in with the same account.",
            "step_2": "Close Claude Desktop completely.",
            "step_3": "Run: python3 cowork-import.py <archive_file>",
            "step_4": "Reopen Claude Desktop. The session should appear in Cowork.",
            "note": "The session will be viewable but may not be resumable (VM state is ephemeral)."
        }
    }
    manifest_path = os.path.join(staging_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    # 6. Bundle the import script
    import_script_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cowork-import.py")
    if os.path.exists(import_script_src):
        shutil.copy2(import_script_src, os.path.join(staging_dir, "cowork-import.py"))

    # 7. Create .zip archive
    archive_path = os.path.join(export_dir, f"{archive_name}.zip")
    import zipfile
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(staging_dir):
            for fname in files:
                full_path = os.path.join(root, fname)
                arcname = os.path.join(archive_name, os.path.relpath(full_path, staging_dir))
                zf.write(full_path, arcname)

    # Cleanup staging
    shutil.rmtree(staging_dir)

    archive_size = os.path.getsize(archive_path)
    print(f"  Archive created: {archive_path} ({archive_size / 1024 / 1024:.1f} MB)")
    return archive_path


def main():
    parser = argparse.ArgumentParser(description="Export Cowork sessions")
    parser.add_argument("--all", action="store_true", help="Export all sessions")
    parser.add_argument("--session", help="Export a specific session by UUID")
    parser.add_argument("--list", action="store_true", help="List sessions (human-readable table)")
    parser.add_argument("--list-json", action="store_true", help="List sessions as JSON (for programmatic use)")
    parser.add_argument("--output", default=DEFAULT_EXPORT_DIR, help="Output directory (default: ~/Documents)")
    args = parser.parse_args()

    sessions = load_sessions_from_all()
    if not sessions:
        print("Error: No Cowork sessions found.")
        sys.exit(1)

    if args.list:
        print_sessions(sessions)
        return

    if args.list_json:
        print_sessions_json(sessions)
        return

    if args.session:
        to_export = [s for s in sessions if s["uuid"] == args.session]
        if not to_export:
            print(f"Error: Session {args.session} not found.")
            print_sessions(sessions)
            sys.exit(1)
    elif args.all:
        to_export = sessions
    else:
        print("Error: Specify --list, --list-json, --session UUID, or --all")
        sys.exit(1)

    os.makedirs(args.output, exist_ok=True)

    print(f"\nExporting {len(to_export)} session(s) to {args.output}/\n")

    for session in to_export:
        print(f"Exporting: {session['title']} ({session['uuid'][:8]}...)")
        export_session(session, session["ws_path"], session["org_id"], session["ws_id"], args.output)
        print()

    print("Done! Archives ready for transfer.")


if __name__ == "__main__":
    main()
