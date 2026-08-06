#!/usr/bin/env python3
"""
GITHUB AGAPE SCANNER
Searches for repos that match Permaculture/Antifragile principles.
Identifies potential targets for "Golden Merges".
"""
import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from state_utils import load_ckpt, save_ckpt

# Configuration
KEYWORDS = [
    "antifragile", "permaculture", "self-healing", "modular-system",
    "regenerative-code", "decentralized-compute", "agape-engine",
    "mesh-network", "fractal-software", "bio-inspired-code"
]
USER = "jesseray718"
OUTPUT_FILE = Path.home() / "une" / "agape_opportunities.json"

def search_github(keyword):
    """Search GitHub for a keyword using gh cli."""
    try:
        # Search for public repos matching the keyword
        cmd = f"gh search repos '{keyword}' --limit 20 --sort=updated --json name,description,stars,forks,updatedAt,url"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return json.loads(result.stdout)
        return []
    except Exception as e:
        print(f"Error searching {keyword}: {e}")
        return []

def analyze_potential(repos, keyword):
    """Analyze repos for 'unified potential'."""
    opportunities = []
    for repo in repos:
        name = repo.get("name", "")
        desc = repo.get("description", "") or ""
        stars = repo.get("stars", 0)
        forks = repo.get("forks", 0)
        updated = repo.get("updatedAt", "")
        
        # Heuristic: High stars + Recent update + Low forks = Good candidate for merge/collab
        # Or: High forks = Community interest but fragmented (needs unification)
        score = 0
        reason = ""
        
        if stars > 100:
            score += 20
            reason += "High popularity. "
        if forks > 10:
            score += 15
            reason += "Fragmented community (needs unification). "
        if "fork" in name.lower() or "fork" in desc.lower():
            score += 10
            reason += "Already a fork. "
        if "permaculture" in desc.lower() or "antifragile" in desc.lower():
            score += 25
            reason += "Direct thematic match. "
        
        if score > 30:
            opportunities.append({
                "repo": name,
                "url": repo.get("url"),
                "stars": stars,
                "forks": forks,
                "score": score,
                "reason": reason,
                "match_keyword": keyword,
                "strategy": "Merge Fork" if forks > 10 else "Collaborate"
            })
    
    return opportunities

def main():
    print("🔍 Scanning GitHub for Agape/Permaculture Opportunities...")
    all_opportunities = []
    
    for kw in KEYWORDS:
        print(f"   Searching: {kw}...")
        repos = search_github(kw)
        found = analyze_potential(repos, kw)
        all_opportunities.extend(found)
    
    # Sort by score
    all_opportunities.sort(key=lambda x: x["score"], reverse=True)
    
    # Save results
    OUTPUT_FILE.write_text(json.dumps(all_opportunities, indent=2))
    
    print(f"\n✅ Scan Complete. Found {len(all_opportunities)} high-potential targets.")
    print(f"📄 Saved to: {OUTPUT_FILE}")
    
    # Display top 5
    print("\n🏆 TOP 5 OPPORTUNITIES FOR UNIFIED IMPLEMENTATION:")
    for i, opp in enumerate(all_opportunities[:5], 1):
        print(f"  {i}. {opp['repo']} (Score: {opp['score']})")
        print(f"     URL: {opp['url']}")
        print(f"     Strategy: {opp['strategy']}")
        print(f"     Reason: {opp['reason']}")
        print("-" * 40)

if __name__ == "__main__":
    ckpt = load_ckpt()
    # Check if gh is authenticated
    auth_check = subprocess.run("gh auth status", shell=True, capture_output=True, text=True)
    if auth_check.returncode != 0:
        print("❌ GitHub CLI not authenticated. Run: gh auth login")
        sys.exit(1)
    main()
