#!/usr/bin/env python3
"""Distributed immutable ledger replicator. Only commits when content actually changed."""
import shutil
import subprocess
from pathlib import Path

UNE_ROOT = Path.home() / "une"
LEDGER_DIR = UNE_ROOT / "ledger"
META_HUB = UNE_ROOT / "meta_hub"

LEDGER_FILES = [
    "transmutation_ledger.jsonl",
    "blockchain_anchors.jsonl",
    "wealth_pathways.json",
]

def run(cmd, cwd):
    return subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)

def replicate():
    if not LEDGER_DIR.exists():
        print("Ledger not found")
        return
    replicated = failed = 0
    for repo in sorted(META_HUB.iterdir()):
        if not repo.is_dir() or not (repo / ".git").exists():
            continue
        name = repo.name
        dest = repo / "ledger"
        dest.mkdir(exist_ok=True)
        changed = False
        try:
            for lf in LEDGER_FILES:
                src = LEDGER_DIR / lf
                dst = dest / lf
                if src.exists():
                    if not dst.exists() or src.read_bytes() != dst.read_bytes():
                        shutil.copy2(src, dst)
                        changed = True
            if changed:
                run("git add ledger/", repo)
                run("git commit -m 'feat: replicate immutable ledger'", repo)
                run("git push origin HEAD", repo)
                print(f"  replicated + pushed {name}")
            else:
                print(f"  already current {name}")
            replicated += 1
        except Exception as e:
            failed += 1
            print(f"  failed {name}: {e}")
    print(f"\nReplicated {replicated} repos. Failed: {failed}")

if __name__ == "__main__":
    replicate()
