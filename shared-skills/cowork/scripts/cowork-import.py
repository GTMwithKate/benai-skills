#!/usr/bin/env python3
"""
Cowork Session Importer
Imports a .zip archive exported by cowork-export.py into Claude Desktop.

Usage:
  python3 cowork-import.py <archive.zip>                        # Import a session
  python3 cowork-import.py <archive.zip> --copy                 # Force import as copy (new UUID)
  python3 cowork-import.py <archive.zip> --assets-dir /path     # Custom assets directory
  python3 cowork-import.py --from-dir /path/to/extracted        # Import from extracted folder

Default assets directory: ~/Documents/CoworkImports/<session-title>/
"""

import argparse
import json
import os
import platform
import shutil
import sys
import uuid as uuid_mod


def get_app_support():
    system = platform.system()
    if system == "Darwin":
        return os.path.expanduser("~/Library/Application Support/Claude")
    elif system == "Windows":
        return os.path.join(os.environ.get("APPDATA", ""), "Claude")
    else:  # Linux
        return os.path.expanduser("~/.config/Claude")


def consolidate_transcript(session_dir):
    """Merge all context segments into one so Claude Desktop renders the full chat.

    Claude Desktop only renders from the last context boundary. When a session
    ran out of context and was continued, 'system' entries mark the boundaries
    and only the final segment is shown. This function removes those boundaries
    so the entire conversation appears as one continuous chat.
    """
    claude_projects = os.path.join(session_dir, ".claude", "projects")
    if not os.path.isdir(claude_projects):
        return 0
    consolidated = 0
    for root, dirs, files in os.walk(claude_projects):
        for fname in files:
            if fname.endswith(".jsonl") and "subagents" not in root:
                fpath = os.path.join(root, fname)
                with open(fpath) as f:
                    lines = f.readlines()

                # Check if there are multiple context segments
                system_lines = []
                for i, line in enumerate(lines):
                    try:
                        entry = json.loads(line.strip())
                    except json.JSONDecodeError:
                        continue
                    if entry.get("type") == "system":
                        system_lines.append(i)

                if not system_lines:
                    continue  # No context boundaries — nothing to consolidate

                # Rebuild: keep first enqueue+dequeue, drop system entries and
                # subsequent enqueue/dequeue pairs (context restarts), keep all
                # user/assistant messages
                new_lines = []
                seen_first_enqueue = False
                seen_first_dequeue = False
                for line in lines:
                    line_stripped = line.strip()
                    if not line_stripped:
                        continue
                    try:
                        entry = json.loads(line_stripped)
                    except json.JSONDecodeError:
                        new_lines.append(line)
                        continue

                    entry_type = entry.get("type", "")

                    # Drop system continuation entries
                    if entry_type == "system":
                        continue

                    # Keep first enqueue/dequeue, drop subsequent ones
                    if entry_type == "queue-operation":
                        op = entry.get("operation", "")
                        if op == "enqueue":
                            if not seen_first_enqueue:
                                seen_first_enqueue = True
                                new_lines.append(line)
                            # Skip subsequent enqueues
                            continue
                        elif op == "dequeue":
                            if not seen_first_dequeue:
                                seen_first_dequeue = True
                                new_lines.append(line)
                            continue
                        elif op == "remove":
                            continue
                        else:
                            new_lines.append(line)
                            continue
                    else:
                        new_lines.append(line)

                # Write consolidated transcript
                with open(fpath, "w") as f:
                    f.writelines(new_lines)
                removed = len(lines) - len(new_lines)
                consolidated += removed

    return consolidated


def extract_first_user_message(session_dir):
    """Extract the first user message from the .jsonl transcript."""
    claude_projects = os.path.join(session_dir, ".claude", "projects")
    if not os.path.isdir(claude_projects):
        return None
    for root, dirs, files in os.walk(claude_projects):
        for fname in files:
            if fname.endswith(".jsonl") and "subagents" not in root:
                fpath = os.path.join(root, fname)
                with open(fpath) as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            entry = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        entry_type = entry.get("type") or entry.get("role", "")
                        if entry_type != "user":
                            continue
                        msg = entry.get("message", entry)
                        content = msg.get("content", "")
                        if isinstance(content, str) and len(content) > 5:
                            return content
                        elif isinstance(content, list):
                            for part in content:
                                if isinstance(part, dict) and part.get("type") == "text" and len(part.get("text", "")) > 5:
                                    return part["text"]
    return None


def get_local_claude_json(sessions_base):
    """Read oauthAccount and userID from the most recent native session's .claude.json."""
    best = None
    best_mtime = 0
    for root, dirs, files in os.walk(sessions_base):
        if ".claude" in dirs:
            claude_json_path = os.path.join(root, ".claude", ".claude.json")
            if os.path.exists(claude_json_path):
                try:
                    mtime = os.path.getmtime(claude_json_path)
                    if mtime > best_mtime:
                        with open(claude_json_path) as f:
                            data = json.load(f)
                        if data.get("oauthAccount"):
                            best = data
                            best_mtime = mtime
                except (json.JSONDecodeError, OSError):
                    continue
    return best


def detect_local_account(sessions_base):
    """Read accountName and emailAddress from the most recently active local session."""
    best = None
    best_activity = 0
    for org_id in os.listdir(sessions_base):
        org_path = os.path.join(sessions_base, org_id)
        if not os.path.isdir(org_path):
            continue
        for ws_id in os.listdir(org_path):
            ws_path = os.path.join(org_path, ws_id)
            if not os.path.isdir(ws_path):
                continue
            for fname in os.listdir(ws_path):
                if fname.startswith("local_") and fname.endswith(".json"):
                    try:
                        with open(os.path.join(ws_path, fname)) as f:
                            data = json.load(f)
                        name = data.get("accountName")
                        email = data.get("emailAddress")
                        activity = data.get("lastActivityAt") or data.get("createdAt") or 0
                        if name and email and activity > best_activity:
                            best_activity = activity
                            best = {"accountName": name, "emailAddress": email, "org_id": org_id, "ws_id": ws_id}
                    except (json.JSONDecodeError, OSError):
                        continue
    return best


def main():
    parser = argparse.ArgumentParser(description="Import a Cowork session archive")
    parser.add_argument("archive", nargs="?", help="Path to the .zip archive")
    parser.add_argument("--from-dir", help="Import directly from extracted directory (used by install.sh)")
    parser.add_argument("--copy", action="store_true", help="Import as a copy with new UUID (keeps original intact)")
    parser.add_argument("--assets-dir", help="Directory to place asset folders (default: ~/Documents/CoworkImports/<title>)")
    args = parser.parse_args()

    if not args.archive and not args.from_dir:
        print("Error: Provide an archive path or use --from-dir")
        sys.exit(1)

    app_support = get_app_support()
    sessions_base = os.path.join(app_support, "local-agent-mode-sessions")

    if not os.path.exists(sessions_base):
        print(f"Error: Claude Desktop sessions directory not found at {sessions_base}")
        print("Make sure Claude Desktop is installed and you've used Cowork at least once.")
        sys.exit(1)

    # Detect local account for remapping
    local_account = detect_local_account(sessions_base)
    if local_account:
        print(f"Detected local account: {local_account['accountName']} ({local_account['emailAddress']})")
    else:
        print("Warning: Could not detect local account from existing sessions")

    tmp_dir = None

    if args.from_dir:
        extracted = args.from_dir
    else:
        if not os.path.exists(args.archive):
            print(f"Error: Archive not found: {args.archive}")
            sys.exit(1)

        tmp_dir = os.path.join(app_support, ".cowork-import-tmp")
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)

        print(f"Extracting archive...")
        if args.archive.endswith(".zip"):
            import zipfile
            with zipfile.ZipFile(args.archive, "r") as zf:
                zf.extractall(tmp_dir)
        else:
            import tarfile
            with tarfile.open(args.archive, "r:gz") as tar:
                tar.extractall(tmp_dir)

        extracted_dirs = os.listdir(tmp_dir)
        if len(extracted_dirs) != 1:
            print("Error: Unexpected archive structure")
            sys.exit(1)
        extracted = os.path.join(tmp_dir, extracted_dirs[0])

    # Read manifest
    manifest_path = os.path.join(extracted, "manifest.json")
    with open(manifest_path) as f:
        manifest = json.load(f)

    session_info = manifest["session"]
    orig_uuid = session_info["uuid"]
    print(f"\nSession: {session_info['title']}")
    print(f"Originally from: {manifest.get('source_machine', 'unknown')}")

    # Find target workspace directory
    # Prefer the local account's workspace over the one from the manifest
    org_id = manifest["org_id"]
    ws_id = manifest["workspace_id"]
    target_ws = os.path.join(sessions_base, org_id, ws_id)

    if local_account:
        local_ws = os.path.join(sessions_base, local_account["org_id"], local_account["ws_id"])
        if os.path.exists(local_ws) and local_ws != target_ws:
            target_ws = local_ws
            print(f"Note: Using local account workspace at {local_account['org_id']}/{local_account['ws_id']}")

    if not os.path.exists(target_ws):
        # Find the workspace with the most content (most likely the active one)
        best_ws, best_count, best_oid, best_wid = None, -1, None, None
        for oid in os.listdir(sessions_base):
            op = os.path.join(sessions_base, oid)
            if not os.path.isdir(op):
                continue
            for wid in os.listdir(op):
                wp = os.path.join(op, wid)
                if os.path.isdir(wp):
                    count = len(os.listdir(wp))
                    if count > best_count:
                        best_ws, best_count = wp, count
                        best_oid, best_wid = oid, wid
        if best_ws:
            target_ws = best_ws
            print(f"Note: Using existing workspace at {best_oid}/{best_wid}")
        else:
            os.makedirs(target_ws, exist_ok=True)
            print(f"Created new workspace directory: {org_id}/{ws_id}")

    # Check if session already exists — if so, import as copy
    existing_meta = os.path.join(target_ws, f"local_{orig_uuid}.json")
    is_copy = args.copy or os.path.exists(existing_meta)
    if is_copy:
        new_uuid = str(uuid_mod.uuid4())
        print(f"  Session already exists or --copy flag set, importing as copy")
        print(f"  New UUID: {new_uuid}")
    else:
        new_uuid = orig_uuid

    # Copy session files with UUID remapping
    session_src = os.path.join(extracted, "session")
    for item in os.listdir(session_src):
        src = os.path.join(session_src, item)
        if is_copy:
            dst_name = item.replace(orig_uuid, new_uuid)
        else:
            dst_name = item
        dst = os.path.join(target_ws, dst_name)
        if os.path.exists(dst):
            print(f"  Skipping (already exists): {dst_name}")
            continue
        if os.path.isdir(src):
            shutil.copytree(src, dst, symlinks=False, dirs_exist_ok=False)
        else:
            shutil.copy2(src, dst)
        print(f"  Imported: {dst_name}")

    # Consolidate context segments so full chat renders in Claude Desktop
    new_session_dir_early = os.path.join(target_ws, f"local_{new_uuid}")
    removed = consolidate_transcript(new_session_dir_early)
    if removed > 0:
        print(f"  Consolidated transcript: removed {removed} context boundary lines")

    # Update sessionId and title in metadata if copy
    meta_path = os.path.join(target_ws, f"local_{new_uuid}.json")
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            meta = json.load(f)
        if is_copy:
            meta["sessionId"] = f"local_{new_uuid}"
            if "(Copy)" not in meta.get("title", ""):
                meta["title"] = meta.get("title", "") + " (Copy)"

        # Handle assets
        original_folders = session_info.get("original_folders", [])
        folder_map = session_info.get("folder_map", {})
        assets_src = os.path.join(extracted, "assets")
        safe_title = "".join(c if c.isalnum() or c in "-_ " else "_" for c in session_info.get("title", "session"))[:50].strip()
        import_base = args.assets_dir or os.path.join(os.path.expanduser("~/Documents/CoworkImports"), safe_title)
        os.makedirs(import_base, exist_ok=True)

        def copy_tree_merge(src_dir, dst_dir):
            """Copy files from src to dst, skip existing files. Returns count."""
            count = 0
            for root, dirs, files in os.walk(src_dir):
                for fname in files:
                    s = os.path.join(root, fname)
                    rel = os.path.relpath(s, src_dir)
                    d = os.path.join(dst_dir, rel)
                    os.makedirs(os.path.dirname(d), exist_ok=True)
                    if not os.path.exists(d):
                        shutil.copy2(s, d)
                        count += 1
            return count

        folder_remap = {}
        if os.path.isdir(assets_src):
            for orig_path, folder_name in folder_map.items():
                src = os.path.join(assets_src, folder_name)
                if not os.path.isdir(src):
                    continue

                target_folder = os.path.join(import_base, folder_name)
                os.makedirs(target_folder, exist_ok=True)

                file_count = copy_tree_merge(src, target_folder)
                print(f"  Assets -> {target_folder} ({file_count} new files)")
                folder_remap[orig_path] = target_folder

        # Ensure all original folders have a remap, even without exported assets
        for orig_path in original_folders:
            if orig_path not in folder_remap:
                folder_name = os.path.basename(orig_path)
                target_folder = os.path.join(import_base, folder_name)
                os.makedirs(target_folder, exist_ok=True)
                folder_remap[orig_path] = target_folder
        for orig_path, folder_name in folder_map.items():
            if orig_path not in folder_remap:
                target_folder = os.path.join(import_base, folder_name)
                os.makedirs(target_folder, exist_ok=True)
                folder_remap[orig_path] = target_folder

        # Handle VM-reconstructed files
        vm_files_src = os.path.join(extracted, "vm-files")
        if os.path.isdir(vm_files_src) and os.listdir(vm_files_src):
            vm_target = os.path.join(import_base, "_vm-workspace-files")
            os.makedirs(vm_target, exist_ok=True)
            vm_count = copy_tree_merge(vm_files_src, vm_target)
            print(f"  VM workspace files -> {vm_target} ({vm_count} new files)")

        # Build all old session directory prefixes for path remapping
        # Sessions may be referenced via different org/workspace IDs, so collect all variants
        # Pattern: .../local-agent-mode-sessions/<any-org>/<any-ws>/local_<uuid>
        session_suffix = f"/local_{orig_uuid}"
        source_session_prefixes = set()
        all_paths = [e.get("hostPath", "") for e in meta.get("fsDetectedFiles", [])]
        all_paths += meta.get("userApprovedFileAccessPaths", [])
        for hp in all_paths:
            idx = hp.find(session_suffix)
            if idx >= 0 and "local-agent-mode-sessions/" in hp:
                source_session_prefixes.add(hp[:idx + len(session_suffix)])

        # New session directory on this machine
        new_session_dir = os.path.join(target_ws, f"local_{new_uuid}")

        def remap_path(path):
            """Remap a single path using folder_remap or session prefix matching."""
            for orig_folder, new_folder in folder_remap.items():
                if path.startswith(orig_folder):
                    return new_folder + path[len(orig_folder):], True
            for prefix in source_session_prefixes:
                if path.startswith(prefix):
                    return new_session_dir + path[len(prefix):], True
            return path, False

        # Update folder paths in metadata
        new_folders = []
        for fp in meta.get("userSelectedFolders", []):
            new_folders.append(folder_remap.get(fp, fp))
        meta["userSelectedFolders"] = new_folders

        # Remap hostPath in fsDetectedFiles
        for entry in meta.get("fsDetectedFiles", []):
            entry["hostPath"], _ = remap_path(entry.get("hostPath", ""))

        # Remap userApprovedFileAccessPaths
        new_approved = []
        for path in meta.get("userApprovedFileAccessPaths", []):
            new_path, _ = remap_path(path)
            new_approved.append(new_path)
        meta["userApprovedFileAccessPaths"] = new_approved

        if folder_remap or source_session_prefixes:
            print(f"  Remapped file paths to local machine")

        # Remap account to local account
        if local_account:
            old_account = meta.get("accountName", "")
            old_email = meta.get("emailAddress", "")
            if old_account != local_account["accountName"] or old_email != local_account["emailAddress"]:
                meta["accountName"] = local_account["accountName"]
                meta["emailAddress"] = local_account["emailAddress"]
                print(f"  Remapped account: {old_account} -> {local_account['accountName']}")

        # Fix initialMessage — extract the real first user message from transcript
        first_msg = extract_first_user_message(new_session_dir)
        if first_msg:
            meta["initialMessage"] = first_msg
            print(f"  Fixed initialMessage from transcript")

        # Write updated metadata
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2)
        if is_copy:
            print(f"  Updated metadata (new UUID + title)")

        # Patch .claude/.claude.json — add oauthAccount and userID from local account
        inner_claude_json = os.path.join(new_session_dir, ".claude", ".claude.json")
        if os.path.exists(inner_claude_json):
            local_claude_json = get_local_claude_json(sessions_base)
            if local_claude_json:
                with open(inner_claude_json) as f:
                    inner_data = json.load(f)
                patched = False
                if local_claude_json.get("oauthAccount") and inner_data.get("oauthAccount") != local_claude_json["oauthAccount"]:
                    inner_data["oauthAccount"] = local_claude_json["oauthAccount"]
                    patched = True
                if local_claude_json.get("userID") and inner_data.get("userID") != local_claude_json["userID"]:
                    inner_data["userID"] = local_claude_json["userID"]
                    patched = True
                if patched:
                    with open(inner_claude_json, "w") as f:
                        json.dump(inner_data, f, indent=2)
                    print(f"  Patched .claude.json (oauthAccount + userID)")

        # Remove stale credentials from source machine
        stale_creds = os.path.join(new_session_dir, ".claude", ".credentials.json")
        if os.path.exists(stale_creds):
            os.remove(stale_creds)
            print(f"  Removed stale .credentials.json")

    # Cleanup
    if tmp_dir and os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

    print(f"\nImport complete! Restart Claude Desktop to see the session.")


if __name__ == "__main__":
    main()
