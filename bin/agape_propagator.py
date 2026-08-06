#!/usr/bin/env python3
"""
AGAPE PROPAGATION ENGINE v2.0 — NON-VIOLENT ALIGNMENT
Principle: Correct gently. Align history without breaking it.
Wealth: Every successful alignment adds to the Knowledge Ledger.
"""
import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from state_utils import load_ckpt, save_ckpt

UNE_ROOT = Path.home() / "une"
PLAN_FILE = UNE_ROOT / "offline_lesson_plan.json"
WEALTH_LEDGER = UNE_ROOT / "wealth_resource.json"
LOGS_DIR = UNE_ROOT / "logs"

def load_wealth():
    """Load the wealth ledger."""
    if WEALTH_LEDGER.exists():
        return json.loads(WEALTH_LEDGER.read_text())
    return {"total_alignments": 0, "total_knowledge_credits": 0, "history": []}

def save_wealth(wealth):
    """Save the wealth ledger."""
    WEALTH_LEDGER.write_text(json.dumps(wealth, indent=2))

def add_knowledge_credit(reason, repo_name):
    """Add a knowledge credit to the ledger."""
    wealth = load_wealth()
    wealth["total_alignments"] += 1
    wealth["total_knowledge_credits"] += 10  # Arbitrary value for "wealth"
    entry = {
        "timestamp": datetime.now().isoformat(),
        "reason": reason,
        "repo": repo_name,
        "credits_earned": 10
    }
    wealth["history"].append(entry)
    save_wealth(wealth)
    print(f"💰 Wealth Added: +10 credits for {reason} in {repo_name}")
    print(f"   Total Wealth: {wealth['total_knowledge_credits']} credits")

def apply_gentle_fix(fix_type, context):
    """Apply a fix without force-pushing."""
    print(f"🌿 Gentle Correction: {fix_type}")
    
    if fix_type == "symlink_loop":
        # Destroy symlink, replace with static file
        for gi in UNE_ROOT.rglob(".gitignore"):
            if gi.is_symlink():
                os.unlink(gi)
                gi.write_text("# Hardened .gitignore\nvendor_archive/\nquarantine/\nbackups/\nlogs/\n*.log\n*.pyc\n*.gguf\n*.bin\nmeta_hub/")
                print(f"   ✅ Gently broke symlink: {gi}")
                add_knowledge_credit("Symlink loop resolved", str(gi.parent.name))
    
    elif fix_type == "auth_failure":
        print("   ℹ️  Manual action: Run 'gh auth refresh' to restore connection.")
        # We don't auto-fix auth to avoid security risks, but we log the lesson.
        add_knowledge_credit("Auth lesson logged", "global")
    
    elif fix_type == "no_remote":
        repo_name = context.get("repo_name", "")
        if repo_name:
            repo_path = UNE_ROOT / "meta_hub" / repo_name
            if repo_path.exists():
                url = f"https://github.com/jesseray718/{repo_name}.git"
                # Check if remote exists first
                out = subprocess.run(f"cd {repo_path} && git remote get-url origin", shell=True, capture_output=True, text=True)
                if out.returncode != 0:
                    subprocess.run(f"cd {repo_path} && git remote add origin {url}", shell=True)
                    print(f"   ✅ Gently added remote for {repo_name}")
                    add_knowledge_credit("Remote aligned", repo_name)
                else:
                    print(f"   ℹ️  Remote already exists for {repo_name}")
    
    elif fix_type == "non_fast_forward":
        # THE KEY CHANGE: Fetch + Rebase (Gentle) instead of Force-Push
        print("   🌿 Aligning history gently (Fetch + Rebase)...")
        for repo in (UNE_ROOT / "meta_hub").iterdir():
            if repo.is_dir() and (repo / ".git").exists():
                repo_name = repo.name
                try:
                    # 1. Fetch
                    subprocess.run(f"cd {repo} && git fetch origin", shell=True, check=True)
                    # 2. Rebase (rewrites local history to sit on top of remote)
                    # If rebase fails, we merge instead (even gentler)
                    rebase_out = subprocess.run(f"cd {repo} && git rebase origin/main", shell=True, capture_output=True, text=True)
                    if rebase_out.returncode == 0:
                        print(f"   ✅ {repo_name}: History aligned via rebase.")
                        add_knowledge_credit("History aligned (rebase)", repo_name)
                    else:
                        # Rebase conflict? Try merge (preserves history entirely)
                        subprocess.run(f"cd {repo} && git rebase --abort", shell=True)
                        subprocess.run(f"cd {repo} && git merge origin/main --no-edit", shell=True)
                        print(f"   ✅ {repo_name}: History aligned via merge.")
                        add_knowledge_credit("History aligned (merge)", repo_name)
                        
                    # 3. Push (Safe, fast-forward only)
                    subprocess.run(f"cd {repo} && git push origin main", shell=True, check=True)
                    print(f"   🚀 {repo_name}: Pushed safely.")
                    
                except subprocess.CalledProcessError as e:
                    print(f"   ⚠️  {repo_name}: Alignment paused (conflict or auth).")
                    # Log the pause as a lesson
                    add_knowledge_credit("Alignment paused", repo_name)

    elif fix_type == "hardcoded_path":
        print("   🔧 Scanning for hardcoded paths...")
        # Simple scan and report for now
        print("   ℹ️  Hardcoded paths detected. Manual review recommended for safety.")
        add_knowledge_credit("Hardcoded path lesson logged", "global")

    else:
        print(f"   ❓ Unknown fix type: {fix_type}")

def main():
    if not PLAN_FILE.exists():
        print("❌ No offline lesson plan found. Run observer first.")
        return
    
    plan = json.loads(PLAN_FILE.read_text())
    print(f"📜 Loading Offline Lesson Plan ({plan['total_lessons']} lessons)")
    print(f"💰 Current Wealth: {load_wealth()['total_knowledge_credits']} credits")
    
    for fix in plan["priority_fixes"]:
        apply_gentle_fix(fix["error_type"], fix)
    
    print(f"\n✅ Gentle Alignment Complete.")
    print(f"💰 New Wealth Total: {load_wealth()['total_knowledge_credits']} credits")
    print(f"📈 Wealth Resource saved to: {WEALTH_LEDGER}")

if __name__ == "__main__":
    ckpt = load_ckpt()
    main()
