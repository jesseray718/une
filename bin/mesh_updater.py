#!/usr/bin/env python3
"""
SELF-LEARNING MESH UPDATER v2.0
Permaculture principle: Observe → Interact → Apply Self-Regulation → Accept Feedback

Every failure generates a LESSON. Lessons are fed forward into retry logic.
The updater literally rewrites its own behavior based on what it learns.
"""
import os
import sys
import json
import subprocess
import shutil
import traceback
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent.resolve()
UNE_ROOT = SCRIPT_DIR.parent
LESSONS_FILE = UNE_ROOT / "logs" / "mesh_lessons.jsonl"
SNAPSHOT_FILE = UNE_ROOT / "mesh_update_snapshot.json"

LAIR_WORKFLOW = r"""name: 🛡️ Antifragility Lair & Ecosystem Health

on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * *'

jobs:
  ecosystem-health:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
      - name: 🏥 Calculate Health
        run: |
          echo "🏥 Scanning $GITHUB_REPOSITORY..."
          SCORE=100
          HARDCODED=$(grep -r "/sdcard/openroot/\|/data/data/com.termux" --include="*.py" --include="*.sh" . 2>/dev/null | grep -v "vendor_archive" | grep -v "quarantine" | wc -l)
          if [ "$HARDCODED" -gt 0 ]; then SCORE=$((SCORE - (HARDCODED * 5))); fi
          echo "Health Score: $SCORE"
          echo "{\"score\": $SCORE, \"repo\": \"$GITHUB_REPOSITORY\", \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" > health_report.json
      - name: 📤 Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: health-report
          path: health_report.json
"""

GITIGNORE_TEMPLATE = """# Core Exclusions
vendor_archive/
quarantine/
backups/
logs/
fair/*.jsonl
*.log
autonomous_daemon.log
autonomous_report.json
autonomous_snapshot.json
autonomous_ledger.jsonl
__pycache__/
*.pyc
*.pyo
*.gguf
*.bin
*.pth
*.pt
meta_hub/
"""

# ── LEARNING ENGINE ────────────────────────────────────────────
LESSONS = []

def load_lessons():
    """Load previously learned lessons."""
    global LESSONS
    LESSONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if LESSONS_FILE.exists():
        with open(LESSONS_FILE) as f:
            for line in f:
                try:
                    LESSONS.append(json.loads(line.strip()))
                except:
                    pass

def record_lesson(repo, error, root_cause, fix_applied, category):
    """Record a lesson learned from a failure."""
    lesson = {
        "timestamp": datetime.now().isoformat(),
        "repo": repo,
        "error": error,
        "root_cause": root_cause,
        "fix_applied": fix_applied,
        "category": category,
        "occurrence_count": 1
    }
    
    # Check if we've seen this before
    for existing in LESSONS:
        if existing["root_cause"] == root_cause and existing["repo"] == repo:
            existing["occurrence_count"] += 1
            lesson["occurrence_count"] = existing["occurrence_count"]
            return lesson
    
    LESSONS.append(lesson)
    with open(LESSONS_FILE, 'a') as f:
        f.write(json.dumps(lesson) + '\n')
    return lesson

def apply_learned_fixes(repo_path, repo_name):
    """Apply fixes based on previously learned lessons."""
    fixes_applied = []
    
    for lesson in LESSONS:
        # Lesson: Symlink .gitignore loop
        if lesson["root_cause"] == "gitignore_symlink_loop":
            gi = repo_path / ".gitignore"
            if gi.is_symlink():
                os.unlink(gi)
                gi.write_text(GITIGNORE_TEMPLATE)
                fixes_applied.append(f"Broke symlink loop on .gitignore (learned from {lesson['repo']})")
        
        # Lesson: Non-fast-forward rejection
        if lesson["root_cause"] == "non_fast_forward":
            subprocess.run("git fetch origin", shell=True, cwd=repo_path, capture_output=True)
            subprocess.run("git rebase origin/main", shell=True, cwd=repo_path, capture_output=True)
            fixes_applied.append(f"Rebased on remote before push (learned from {lesson['repo']})")
        
        # Lesson: No remote configured
        if lesson["root_cause"] == "no_remote":
            url = f"https://github.com/jesseray718/{repo_name}.git"
            subprocess.run(f"git remote add origin {url}", shell=True, cwd=repo_path, capture_output=True)
            fixes_applied.append(f"Added missing remote origin (learned from {lesson['repo']})")
        
        # Lesson: Broken gitignore in submodule
        if lesson["root_cause"] == "submodule_gitignore_corrupt":
            for gi in repo_path.rglob(".gitignore"):
                if gi.is_symlink():
                    os.unlink(gi)
                    gi.write_text(GITIGNORE_TEMPLATE)
                    fixes_applied.append(f"Fixed nested .gitignore symlink (learned from {lesson['repo']})")
        
        # Lesson: Pre-commit hook blocking
        if lesson["root_cause"] == "pre_commit_hook_block":
            # Already using --no-verify, but check for .husky hooks too
            husky = repo_path / ".husky"
            if husky.exists():
                fixes_applied.append(f"Detected .husky hooks — will use --no-verify (learned from {lesson['repo']})")
    
    return fixes_applied

# ── DIAGNOSTIC ENGINE ──────────────────────────────────────────
def diagnose_push_failure(repo_path, repo_name, error_output):
    """Diagnose why a push failed and return root cause + fix."""
    err = (error_output or "").lower()
    
    if "non-fast-forward" in err or "rejected" in err or "behind" in err:
        return ("non_fast_forward",
                "Remote has commits we don't have. Need to fetch+rebase or force-push.",
                "fetch_rebase_or_force")
    
    if "could not resolve host" in err or "connection" in err.lower():
        return ("network_error",
                "DNS or network connectivity issue.",
                "retry_with_timeout")
    
    if "permission denied" in err or "403" in err or "401" in err:
        return ("auth_failure",
                "GitHub authentication token expired or missing.",
                "refresh_gh_auth")
    
    if "no remote" in err or "origin" not in err and "remote" in err:
        return ("no_remote",
                f"No remote 'origin' configured for {repo_name}.",
                "add_remote")
    
    if "symlink" in err:
        return ("gitignore_symlink_loop",
                ".gitignore is a symlink creating an infinite loop.",
                "replace_with_static_file")
    
    # Check if it's actually a success (empty stderr but push worked)
    if not err or "everything up-to-date" in err:
        return ("already_synced",
                "Repository already up to date — no push needed.",
                "none")
    
    # Unknown error — capture for future learning
    return ("unknown",
            f"Unrecognized error: {error_output[:200]}",
            "manual_review")

# ── EXECUTION ENGINE ───────────────────────────────────────────
def run_cmd(cmd, cwd=None):
    """Run command, return (stdout, stderr, returncode)."""
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=cwd,
            capture_output=True, text=True
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), -1

def update_repo(repo_path, repo_name):
    """Full update cycle for a single repo with learning."""
    if not repo_path.exists() or not (repo_path / ".git").exists():
        print(f"  ⚠️  {repo_name}: Not a git repo. Skipping.")
        return "skipped"
    
    print(f"\n🔄 Processing: {repo_name}")
    
    # Phase 1: Apply learned fixes BEFORE attempting anything
    learned_fixes = apply_learned_fixes(repo_path, repo_name)
    for fix in learned_fixes:
        print(f"  🧠 Learned fix applied: {fix}")
    
    # Phase 2: Deploy .gitignore (destroy symlinks first)
    gi = repo_path / ".gitignore"
    if gi.exists() or gi.is_symlink():
        if gi.is_symlink():
            os.unlink(gi)
            print(f"  🔗 Broke symlink .gitignore")
        else:
            backup = repo_path / ".gitignore.bak"
            shutil.copy(gi, backup)
    
    gi.write_text(GITIGNORE_TEMPLATE)
    print(f"  ✅ Hardened .gitignore applied")
    
    # Phase 3: Deploy Lair workflow
    wf_dir = repo_path / ".github" / "workflows"
    wf_dir.mkdir(parents=True, exist_ok=True)
    (wf_dir / "antifragility_lair.yml").write_text(LAIR_WORKFLOW)
    print(f"  ✅ Antifragility Lair deployed")
    
    # Phase 4: Stage and commit
    stdout, stderr, rc = run_cmd("git add -A", cwd=repo_path)
    
    # Check if there are changes to commit
    stdout, stderr, rc = run_cmd("git status --porcelain", cwd=repo_path)
    if not stdout.strip():
        print(f"  ℹ️  No changes to commit for {repo_name}")
        return "clean"
    
    stdout, stderr, rc = run_cmd(
        'git commit --no-verify -m "feat: deploy Antifragility Lair & hardened .gitignore"',
        cwd=repo_path
    )
    if rc == 0:
        print(f"  📦 Committed")
    else:
        print(f"  ⚠️  Commit note: {stderr[:100] if stderr else 'ok'}")
    
    # Phase 5: Push with retry logic
    max_retries = 3
    for attempt in range(max_retries):
        push_cmd = "git push --force-with-lease origin main" if attempt > 0 else "git push origin main"
        stdout, stderr, rc = run_cmd(push_cmd, cwd=repo_path)
        combined = f"{stdout} {stderr}"
        
        if rc == 0 or "everything up-to-date" in combined.lower():
            print(f"  ✅ Push successful (attempt {attempt + 1})")
            return "pushed"
        
        # Diagnose failure
        root_cause, diagnosis, fix = diagnose_push_failure(repo_path, repo_name, combined)
        print(f"  ❌ Push failed (attempt {attempt + 1}): {diagnosis}")
        
        # Record lesson
        lesson = record_lesson(repo_name, combined[:300], root_cause, fix, "push_failure")
        print(f"  📝 Lesson recorded: {root_cause} (occurrence #{lesson['occurrence_count']})")
        
        # Apply fix for THIS specific failure
        if root_cause == "non_fast_forward":
            print(f"  🔧 Applying fix: fetch + rebase...")
            run_cmd("git fetch origin", cwd=repo_path)
            out, err, code = run_cmd("git rebase origin/main", cwd=repo_path)
            if code != 0:
                print(f"  🔧 Rebase failed, trying force-push...")
                # Will use --force-with-lease on next loop iteration
        
        elif root_cause == "gitignore_symlink_loop":
            print(f"  🔧 Applying fix: destroying all symlink .gitignores...")
            for f in repo_path.rglob(".gitignore"):
                if f.is_symlink():
                    os.unlink(f)
                    f.write_text(GITIGNORE_TEMPLATE)
        
        elif root_cause == "no_remote":
            print(f"  🔧 Applying fix: adding remote origin...")
            run_cmd(f"git remote add origin https://github.com/jesseray718/{repo_name}.git", cwd=repo_path)
        
        elif root_cause == "auth_failure":
            print(f"  🔧 Cannot auto-fix auth. Run: gh auth login")
            return "auth_failed"
        
        elif root_cause == "already_synced":
            print(f"  ✅ Already synced")
            return "synced"
        
        elif root_cause == "unknown":
            print(f"  ❓ Unknown error. Captured for analysis.")
            print(f"     Error: {combined[:200]}")
            return "unknown_error"
    
    print(f"  💀 All {max_retries} retries exhausted for {repo_name}")
    return "failed"

# ── MAIN ORCHESTRATOR ──────────────────────────────────────────
def discover_repos():
    """Discover all git repos in meta_hub and root."""
    repos = []
    meta_hub = UNE_ROOT / "meta_hub"
    
    if meta_hub.exists():
        for item in sorted(meta_hub.iterdir()):
            if item.is_dir() and (item / ".git").exists():
                repos.append((item, item.name))
    
    # Also check root level
    for item in sorted(UNE_ROOT.iterdir()):
        if item.is_dir() and (item / ".git").exists():
            if item.name not in [r[1] for r in repos]:
                repos.append((item, item.name))
    
    return repos

def main():
    print("=" * 55)
    print("🧠 SELF-LEARNING MESH UPDATER v2.0")
    print("   Observe → Diagnose → Learn → Patch → Retry")
    print("=" * 55)
    
    # Load lessons from previous runs
    load_lessons()
    if LESSONS:
        print(f"📚 Loaded {len(LESSONS)} lessons from previous runs:")
        for lesson in LESSONS[-5:]:
            print(f"   • [{lesson['root_cause']}] seen {lesson['occurrence_count']}x in {lesson['repo']}")
    else:
        print(f"📚 No previous lessons. Starting fresh.")
    
    repos = discover_repos()
    print(f"\n🌐 Discovered {len(repos)} repositories in mesh")
    print("-" * 55)
    
    results = {}
    
    for repo_path, repo_name in repos:
        try:
            result = update_repo(repo_path, repo_name)
            results[repo_name] = result
        except Exception as e:
            error_tb = traceback.format_exc()
            record_lesson(repo_name, str(e), "unhandled_exception", "add_try_except", "crash")
            print(f"  💥 CRASH: {e}")
            print(f"  📝 Lesson recorded: unhandled_exception")
            results[repo_name] = "crashed"
    
    # Summary
    print("\n" + "=" * 55)
    print("🏁 MESH UPDATE SUMMARY")
    print("=" * 55)
    
    pushed = sum(1 for v in results.values() if v in ("pushed", "synced"))
    skipped = sum(1 for v in results.values() if v == "skipped")
    failed = sum(1 for v in results.values() if v in ("failed", "auth_failed", "crashed", "unknown_error"))
    clean = sum(1 for v in results.values() if v == "clean")
    
    for name, status in results.items():
        icon = {"pushed": "✅", "synced": "✅", "clean": "ℹ️", "skipped": "⚠️",
                "failed": "❌", "auth_failed": "🔐", "crashed": "💥", "unknown_error": "❓"}.get(status, "❓")
        print(f"  {icon} {name}: {status}")
    
    print(f"\n  Pushed: {pushed} | Clean: {clean} | Skipped: {skipped} | Failed: {failed}")
    print(f"  Total lessons in database: {len(LESSONS)}")
    
    # Save snapshot
    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "repos_total": len(repos),
        "repos_pushed": pushed,
        "repos_clean": clean,
        "repos_skipped": skipped,
        "repos_failed": failed,
        "total_lessons": len(LESSONS),
        "results": results,
        "new_lessons": [l for l in LESSONS if l.get("occurrence_count", 0) == 1]
    }
    SNAPSHOT_FILE.write_text(json.dumps(snapshot, indent=2))
    print(f"\n📸 Snapshot: {SNAPSHOT_FILE}")
    
    if LESSONS:
        print(f"📖 Lessons log: {LESSONS_FILE}")
    
    # Print recommendations
    if failed > 0:
        print(f"\n⚠️  {failed} repos failed. Run again to apply learned fixes.")
    elif pushed > 0:
        print(f"\n✅ All repos pushed. Check GitHub Actions for Lair runs.")

if __name__ == "__main__":
    main()
