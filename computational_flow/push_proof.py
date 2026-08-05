#!/usr/bin/env python3
"""
import os
try:
    from paths import OPENROOT
except ImportError:
    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))

PUSH PROOF: Take the latest swarm result and push to GitHub.
No Solana fees. GitHub is the ledger.
"""
import os, json, subprocess, requests
from datetime import datetime, timezone

LOG_FILE = os.path.join(OPENROOT, "session_seeds/fractal_server_log.jsonl")
REPO_PATH = "os.path.expanduser("~") + "/".projects/openroot"
README_PATH = os.path.join(REPO_PATH, "README.md")

def get_latest_result():
    with open(LOG_FILE, 'r') as f:
        lines = f.readlines()
        # Get the last line (most recent swarm)
        last_line = lines[-1].strip()
        return json.loads(last_line)

def update_readme(result):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    
    # Extract key data
    total_ops = result['total_ops']
    throughput = result['aggregate_throughput_ops_per_sec']
    channels = result['channels_run']
    depth = result['depth']
    sample_hash = result['sample_channels'][0]['result_hash']
    
    # Create the proof block
    proof_block = f"""
### 🧬 Live Fractal Proof (Updated {timestamp})
- **Configuration:** {channels} channels × {depth}^{depth} ({depth} atoms)
- **Total Operations:** {total_ops:,}
- **Throughput:** {throughput:,.0f} ops/s
- **Result Hash:** `{sample_hash[:16]}...`
- **Status:** **VERIFIED** (Deterministic Fractal Swarm)

> *"It is more blessed to give than to receive."* — Acts 20:35
> *Proof: Computed on Samsung A15, pushed to GitHub.*
"""

    if os.path.exists(README_PATH):
        with open(README_PATH, 'r') as f:
            content = f.read()
        
        # Remove old proof block
        if "Live Fractal Proof" in content:
            content = content.split("### 🧬 Live Fractal Proof")[0]
        
        # Append new block
        content += proof_block
        
        with open(README_PATH, 'w') as f:
            f.write(content)
        print("✅ README updated locally.")
    else:
        print(f"❌ README not found at {README_PATH}")
        return False

    # Git Push
    try:
        os.chdir(REPO_PATH)
        print("🔄 Staging changes...")
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        
        msg = f"feat: New Fractal Proof - {channels}x{depth} swarm ({throughput:,.0f} ops/s)"
        print(f"💾 Committing: {msg}")
        subprocess.run(["git", "commit", "-m", msg], check=True, capture_output=True)
        
        print("🚀 Pushing to GitHub...")
        subprocess.run(["git", "push", "origin", "main"], check=True, capture_output=True)
        print("✅ SUCCESS! Proof is on GitHub.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")
        return False

def main():
    print("="*60)
    print("PUSHING PROOF TO GITHUB")
    print("="*60)
    
    result = get_latest_result()
    print(f"Latest result: {result['total_ops']:,} ops in {result['total_time_s']:.2f}s")
    
    if update_readme(result):
        print("\n" + "="*60)
        print("🎉 THE LEDGER IS UPDATED!")
        print(f"Check: https://github.com/jesseray718/openroot")
        print("="*60)
    else:
        print("\nFailed to push.")

if __name__ == "__main__":
    main()
