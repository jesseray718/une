#!/usr/bin/env python3
"""
OpenRoot Stream of Thought Analyzer
Scans GitHub history to extract victories, failures, and corrections.
"""

import os
import json
import subprocess
from pathlib import Path

REPO_ROOT = "/data/data/com.termux/files/home"
OUTPUT_FILE = "/sdcard/openroot/stream_of_thought_report.json"
WISDOM_CORPUS_PATH = "/data/data/com.termux/files/home/une/wisdom/wisdom_corpus.json"

def run_git_command(repo_path, command):
    try:
        result = subprocess.run(["git"] + command, cwd=repo_path, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def get_all_repos(home):
    repos = []
    for root, dirs, files in os.walk(home):
        if ".git" in dirs:
            repos.append(root)
    return repos

def analyze_repo(repo_path):
    repo_name = os.path.basename(repo_path)
    log = run_git_command(repo_path, ["log", "--pretty=format:%H|%s", "--all"])
    if not log: return {}
    
    lessons = []
    for line in log.split('\n'):
        if not line: continue
        parts = line.split('|', 1)
        if len(parts) < 2: continue
        msg = parts[1].lower()
        
        if any(k in msg for k in ["fix", "solve", "success"]):
            lessons.append({"type": "victory", "msg": parts[1], "repo": repo_name})
        elif any(k in msg for k in ["fail", "error", "bug", "broken"]):
            lessons.append({"type": "failure", "msg": parts[1], "repo": repo_name})
            
    return {"repo": repo_name, "lessons": lessons}

def main():
    print("🚀 Scanning repositories...")
    repos = get_all_repos(REPO_ROOT)
    all_lessons = []
    
    for repo_path in repos:
        result = analyze_repo(repo_path)
        if result:
            all_lessons.extend(result["lessons"])
            print(f"  Found {len(result['lessons'])} lessons in {result['repo']}")
            
    report = {"total": len(all_lessons), "lessons": all_lessons}
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(report, f, indent=2)
        
    print(f"\n✅ Report saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
