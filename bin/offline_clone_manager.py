#!/usr/bin/env python3
"""
OFFLINE-FIRST CLONE + SYNC MANAGER
η-maximizing: clone once, operate fully offline, push only when online and ahead.
Maintains immutable ledger backup on every cycle.
"""
import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

UNE_ROOT = Path.home() / "une"
META_HUB = UNE_ROOT / "meta_hub"
LEDGER_DIR = UNE_ROOT / "ledger"
SYNC_LOG = UNE_ROOT / "logs" / "offline_sync.log"
CACHE = UNE_ROOT / "repo_list_cache.json"
USER = "jesseray718"

META_HUB.mkdir(parents=True, exist_ok=True)
(LEDGER_DIR / "offline_backup").mkdir(parents=True, exist_ok=True)
SYNC_LOG.parent.mkdir(parents=True, exist_ok=True)

def log(msg: str):
    ts = datetime.now(timezone.utc).isoformat()
    line = f"[{ts}] {msg}"
    print(line)
    with open(SYNC_LOG, "a") as f:
        f.write(line + "\n")

def run(cmd, cwd=None, timeout=45):
    try:
        r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    except subprocess.TimeoutExpired:
        return "", "Timeout", -1
    except Exception as e:
        return "", str(e), -1

def is_online() -> bool:
    _, _, rc = run("ping -c 1 -W 2 github.com", timeout=6)
    return rc == 0

def detect_branch(path: Path) -> str:
    out, _, rc = run("git rev-parse --abbrev-ref HEAD", cwd=path)
    if rc == 0 and out:
        return out
    for candidate in ("main", "master"):
        _, _, rc = run(f"git show-ref --verify --quiet refs/heads/{candidate}", cwd=path)
        if rc == 0:
            return candidate
    return "main"

def get_repo_list():
    if is_online():
        log("Online: fetching repo list via gh")
        out, err, rc = run(f"gh repo list {USER} --limit 100 --json name,url")
        if rc == 0:
            try:
                repos = json.loads(out)
                CACHE.write_text(json.dumps(repos, indent=2))
                return repos
            except Exception:
                log("Failed to parse gh output")
        else:
            log(f"gh failed: {err[:80]}")
    if CACHE.exists():
        log("Offline: using cached repo list")
        try:
            return json.loads(CACHE.read_text())
        except Exception:
            pass
    log("Scanning local meta_hub as last resort")
    repos = []
    for item in sorted(META_HUB.iterdir()):
        if item.is_dir() and (item / ".git").exists():
            repos.append({"name": item.name, "url": f"https://github.com/{USER}/{item.name}.git"})
    return repos

def clone_or_update(repo: dict) -> bool:
    name = repo.get("name")
    url = repo.get("url")
    path = META_HUB / name
    if path.exists() and (path / ".git").exists():
        log(f"Updating {name}")
        branch = detect_branch(path)
        _, ferr, frc = run("git fetch origin", cwd=path)
        if frc != 0:
            log(f"  fetch failed: {ferr[:60]}")
            return False
        out, perr, prc = run(f"git pull --no-edit origin {branch}", cwd=path)
        if prc == 0 or "Already up to date" in (out + perr):
            log(f"  OK {name}")
            return True
        log(f"  pull conflict-ish, trying rebase")
        run(f"git pull --rebase origin {branch}", cwd=path)
        return True
    else:
        log(f"Cloning {name}")
        _, err, rc = run(f"git clone {url} {path}", cwd=META_HUB, timeout=90)
        if rc == 0:
            log(f"  cloned {name}")
            return True
        log(f"  clone failed: {err[:100]}")
        return False

def push_local_ahead(repos):
    if not is_online():
        log("Offline: local commits stay local")
        return
    log("Online: checking for local ahead commits")
    for repo in repos:
        name = repo.get("name")
        path = META_HUB / name
        if not path.exists():
            continue
        branch = detect_branch(path)
        out, _, _ = run(f"git rev-list --count origin/{branch}..HEAD 2>/dev/null", cwd=path)
        try:
            ahead = int(out) if out.isdigit() else 0
        except Exception:
            ahead = 0
        if ahead > 0:
            log(f"  pushing {name} ({ahead} ahead)")
            _, err, rc = run(f"git push origin {branch}", cwd=path)
            if rc == 0:
                log(f"  pushed {name}")
            else:
                log(f"  push failed: {err[:80]}")
        else:
            log(f"  {name} even")

def backup_ledger():
    if not LEDGER_DIR.exists():
        return
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = LEDGER_DIR / "offline_backup" / ts
    dest.mkdir(parents=True, exist_ok=True)
    for f in list(LEDGER_DIR.glob("*.jsonl")) + list(LEDGER_DIR.glob("*.json")):
        if f.is_file():
            run(f"cp '{f}' '{dest}/'")
    log(f"Ledger backup → {dest}")

def sync_all():
    log("=== OFFLINE-FIRST SYNC START ===")
    backup_ledger()
    repos = get_repo_list()
    if not repos:
        log("No repos found")
        return
    ok = fail = 0
    for r in repos:
        if clone_or_update(r):
            ok += 1
        else:
            fail += 1
    log(f"Clone/Update: {ok} ok, {fail} failed")
    push_local_ahead(repos)
    log("=== SYNC COMPLETE ===")

if __name__ == "__main__":
    sync_all()
