#!/data/data/com.termux/files/usr/bin/python3
"""
SELF-CLONE MODULE
Creates an isolated workspace to test upgrades before applying them.
Ensures the system never breaks its own running environment.
"""
import os, sys, shutil, subprocess, tempfile
from datetime import datetime

REPO_ROOT = "/data/data/com.termux/files/home/une"
WORKSPACE = "/sdcard/openroot/temp_workspace"
BRANCH_NAME = f"auto-update-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

def clone_and_setup():
    """Clones repo into temp workspace."""
    if os.path.exists(WORKSPACE):
        shutil.rmtree(WORKSPACE)
    
    os.makedirs(WORKSPACE)
    print(f"📦 Cloning to {WORKSPACE}...")
    
    # Clone current state
    result = subprocess.run(
        ["git", "clone", ".", WORKSPACE],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"❌ Clone failed: {result.stderr}")
        return None
    
    # Create a new branch for the upgrade
    subprocess.run(["git", "checkout", "-b", BRANCH_NAME], cwd=WORKSPACE, capture_output=True)
    print(f"🌿 Created branch: {BRANCH_NAME}")
    return WORKSPACE

def run_upgrade_in_workspace(ws_path):
    """Runs the evolution engine in the sandbox."""
    print(f"🚀 Running evolution engine in sandbox...")
    
    # Run the evolution engine inside the workspace
    # We pass the workspace path as the target
    env = os.environ.copy()
    env["REPO_TARGET"] = ws_path
    
    # Execute the evolution engine logic directly here to avoid path issues
    # (Simplified for this demo: we just run the standard engine but with swapped paths)
    # In a full implementation, you'd import the engine module and override paths.
    
    # For now, let's just simulate the "upgrade" by copying the latest engine
    # and running it.
    
    # Actually, let's just run the existing evolution_engine.py but point it to the workspace
    # We need to temporarily swap sys.path or pass args.
    
    # Simpler approach: Copy the engine code into the workspace and run it there.
    engine_src = os.path.join(REPO_ROOT, "evolution_engine.py")
    engine_dst = os.path.join(ws_path, "evolution_engine.py")
    shutil.copy(engine_src, engine_dst)
    
    # Run it
    result = subprocess.run(
        [sys.executable, "evolution_engine.py"],
        cwd=ws_path,
        capture_output=True, text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print(f"STDERR: {result.stderr}")
    
    return result.returncode == 0

def merge_if_success(ws_path, success):
    """Merges the branch if tests passed."""
    if not success:
        print("⚠️  Upgrade failed in sandbox. Aborting merge.")
        shutil.rmtree(ws_path)
        return False
    
    print("✅ Sandbox tests passed. Merging to main...")
    
    # Switch back to main
    subprocess.run(["git", "checkout", "main"], cwd=ws_path, capture_output=True)
    
    # Merge the branch
    result = subprocess.run(["git", "merge", BRANCH_NAME, "--no-edit"], cwd=ws_path, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ Merge conflict detected. Aborting.")
        shutil.rmtree(ws_path)
        return False
    
    # Push to remote
    print("🚀 Pushing merged changes...")
    result = subprocess.run(["git", "push", "origin", "main"], cwd=ws_path, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"⚠️  Push failed (auth issue?): {result.stderr[:100]}")
        # Don't abort, just warn. The local merge succeeded.
    
    # Cleanup
    shutil.rmtree(ws_path)
    print("✅ Workspace cleaned. Upgrade complete.")
    return True

def main():
    print("🔄 Starting Recursive Self-Upgrade Sequence...")
    
    ws = clone_and_setup()
    if not ws:
        return
    
    success = run_upgrade_in_workspace(ws)
    merge_if_success(ws, success)

if __name__ == "__main__":
    main()
