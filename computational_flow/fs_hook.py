#!/data/data/com.termux/files/usr/bin/env python3
"""Filesystem awareness module for Agape engine."""
import os, json
from pathlib import Path
from collections import defaultdict
from state_utils import load_ckpt, save_ckpt

import os
try:
    from paths import OPENROOT
except ImportError:
    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))

UNE_ROOT = Path("os.path.expanduser("~") + "/"une")
KB_PATH = Path(os.path.join(OPENROOT, "agape_kb/repo_snapshot.json"))

def snapshot(root=UNE_ROOT):
    files_by_ext = defaultdict(list)
    files_by_dir = defaultdict(int)
    total_size = 0
    file_count = 0
    
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ('__pycache__', '.git', 'node_modules')]
        for fn in filenames:
            fp = Path(dirpath) / fn
            try:
                size = fp.stat().st_size
            except: continue
            total_size += size
            file_count += 1
            ext = fp.suffix or '(noext)'
            files_by_ext[ext].append(str(fp.relative_to(root)))
            files_by_dir[str(Path(dirpath).relative_to(root))] += 1
    
    snap = {
        "root": str(root),
        "file_count": file_count,
        "total_bytes": total_size,
        "by_extension": {k: len(v) for k, v in sorted(files_by_ext.items())},
        "by_directory": dict(sorted(files_by_dir.items(), key=lambda x: -x[1])[:20]),
        "files": {k: v for k, v in files_by_ext.items()}
    }
    
    KB_PATH.parent.mkdir(parents=True, exist_ok=True)
    KB_PATH.write_text(json.dumps(snap, indent=2))
    return snap

if __name__ == "__main__":
    ckpt = load_ckpt()
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "snap"
    if cmd == "snap":
        s = snapshot()
        print(f"📊 Snapshot: {s['file_count']} files, {s['total_bytes']:,} bytes")
        print(f"Top extensions: {dict(list(s['by_extension'].items())[:5])}")
        print(f"Saved to {KB_PATH}")
    elif cmd == "json":
        print(json.dumps(snapshot(), indent=2))
