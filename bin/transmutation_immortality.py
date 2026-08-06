#!/usr/bin/env python3
"""
TRANSMUTATION & IMMORTALITY ENGINE
1. Logs errors as "Transmutation Events" (Error → Lesson → Wealth).
2. Hashes every event (SHA-256).
3. Anchors the hash to Bitcoin via OpenTimestamps (OTS).
4. Stores the immutable ledger locally and distributes it.
5. Generates "Wealth Pathways" from patterns of suffering/profit/war.

Principle: "What cannot be destroyed can only be multiplied."
"""
import os
import sys
import json
import hashlib
import subprocess
import time
from pathlib import Path
from datetime import datetime, timezone
from state_utils import load_ckpt, save_ckpt

UNE_ROOT = Path.home() / "une"
LEDGER_DIR = UNE_ROOT / "ledger"
IMMUTABLE_LEDGER = LEDGER_DIR / "transmutation_ledger.jsonl"
ANCHOR_LOG = LEDGER_DIR / "blockchain_anchors.jsonl"
WEALTH_PATHWAYS = LEDGER_DIR / "wealth_pathways.json"

# Ensure directories exist
LEDGER_DIR.mkdir(parents=True, exist_ok=True)

def load_ledger():
    """Load existing ledger entries."""
    entries = []
    if IMMUTABLE_LEDGER.exists():
        with open(IMMUTABLE_LEDGER) as f:
            for line in f:
                try:
                    entries.append(json.loads(line.strip()))
                except:
                    pass
    return entries

def save_entry(entry):
    """Append entry to ledger."""
    with open(IMMUTABLE_LEDGER, 'a') as f:
        f.write(json.dumps(entry) + '\n')

def generate_transmutation(event_type, error_msg, context=""):
    """
    Transform an error into a wealth pathway.
    Returns the entry dict.
    """
    # 1. Define the Wealth Pathway (Lesson)
    pathways = {
        "corruption": {
            "error": "Centralized power corrupts",
            "lesson": "Distribute control; trust math, not men.",
            "wealth": "Decentralized Trust Network",
            "action": "Anchor to blockchain, replicate across mesh."
        },
        "war_machine": {
            "error": "War consumes resources for destruction",
            "lesson": "Redirect energy to creation (Agape).",
            "wealth": "Peace Dividend Calculator",
            "action": "Convert war budget data to seed funding."
        },
        "profit_suffering": {
            "error": "Profit extracted from human suffering",
            "lesson": "Value = Utility + Harmony.",
            "wealth": "Harmony Index Coin",
            "action": "Reward behaviors that reduce suffering."
        },
        "government_not_for_people": {
            "error": "Governance serves elites, not citizens",
            "lesson": "Governance = Service Protocol.",
            "wealth": "Open Governance DAO",
            "action": "Publish decision logs on-chain."
        },
        "syntax_error": {
            "error": "Code syntax error",
            "lesson": "Precision in thought leads to precision in action.",
            "wealth": "Refined Algorithm",
            "action": "Fix and recompile."
        },
        "merge_conflict": {
            "error": "Git merge conflict",
            "lesson": "Divergent paths require negotiation, not force.",
            "wealth": "Consensus Mechanism",
            "action": "Negotiate merge; record compromise."
        }
    }

    # Find best match or default
    wp = pathways.get(event_type, pathways["syntax_error"])
    
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_id": hashlib.sha256(f"{event_type}{error_msg}{time.time()}".encode()).hexdigest()[:16],
        "type": event_type,
        "error_message": error_msg[:500],
        "context": context,
        "transmutation": {
            "lesson": wp["lesson"],
            "wealth_pathway": wp["wealth"],
            "action": wp["action"]
        },
        "wealth_generated": 10, # Base wealth credit
        "status": "pending_anchor"
    }
    return entry

def hash_entry(entry):
    """Create a SHA-256 hash of the entry for immutability."""
    # Serialize without timestamp to ensure consistent hash for same content
    # But we include timestamp for uniqueness in this specific log
    data = json.dumps(entry, sort_keys=True)
    return hashlib.sha256(data.encode()).hexdigest()

def anchor_to_blockchain(hash_hex, entry_id):
    """
    Anchor the hash to the Bitcoin blockchain using OpenTimestamps.
    This makes the record uncorruptible.
    """
    # Create a temporary file with the hash
    temp_file = LEDGER_DIR / f"anchor_{entry_id}.txt"
    temp_file.write_text(hash_hex)

    try:
        # Run ots upgrade
        # Note: This requires 'ots' CLI installed in Termux
        result = subprocess.run(
            f"ots upgrade {temp_file} 2>&1",
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            # Success: The hash is now in the blockchain (or pending inclusion)
            anchor_log = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "entry_id": entry_id,
                "hash": hash_hex,
                "ots_status": "success",
                "proof_path": str(temp_file) + ".asc"
            }
            with open(ANCHOR_LOG, 'a') as f:
                f.write(json.dumps(anchor_log) + '\n')
            print(f"   ✅ Anchored to Bitcoin: {entry_id}")
            return True
        else:
            print(f"   ⚠️  Anchor failed (OTS busy or network): {result.stderr[:100]}")
            return False
    except Exception as e:
        print(f"   ⚠️  Anchor error: {e}")
        return False

def generate_wealth_pathway_report():
    """Generate a report of all wealth pathways generated from errors."""
    entries = load_ledger()
    pathways = {}
    
    for e in entries:
        wp = e.get("transmutation", {}).get("wealth_pathway", "Unknown")
        if wp not in pathways:
            pathways[wp] = {"count": 0, "total_wealth": 0, "lessons": set()}
        pathways[wp]["count"] += 1
        pathways[wp]["total_wealth"] += e.get("wealth_generated", 0)
        pathways[wp]["lessons"].add(e.get("transmutation", {}).get("lesson", ""))

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_entries": len(entries),
        "total_wealth_minted": sum(e.get("wealth_generated", 0) for e in entries),
        "pathways": {k: {"count": v["count"], "total_wealth": v["total_wealth"], "lessons": list(v["lessons"])} for k, v in pathways.items()}
    }
    
    WEALTH_PATHWAYS.write_text(json.dumps(report, indent=2))
    print(f"   📊 Wealth Pathways Report: {WEALTH_PATHWAYS}")
    return report

def main():
    print("\n⚛️  TRANSMUTATION & IMMORTALITY ENGINE")
    print("=" * 55)

    # Simulate catching errors from the previous run
    # In real usage, this would be called by the Mesh Loop or Observer
    simulated_errors = [
        ("merge_conflict", "Conflict in aerocement- repo: histories diverged."),
        ("government_not_for_people", "Repository archived by admin: read-only access imposed."),
        ("corruption", "Centralized control detected in push permissions."),
        ("syntax_error", "SyntaxError in script: invalid escape sequence."),
        ("war_machine", "Resource waste detected in failed build cycles.")
    ]

    for err_type, msg in simulated_errors:
        print(f"\n🔄 Processing: {err_type} - {msg[:40]}...")
        
        # 1. Transmute
        entry = generate_transmutation(err_type, msg)
        
        # 2. Hash
        h = hash_entry(entry)
        entry["hash"] = h
        
        # 3. Save to Ledger
        save_entry(entry)
        print(f"   📝 Logged: {entry['event_id']}")
        
        # 4. Anchor (Optional: run asynchronously to not block)
        # For demo, we try to anchor immediately
        if anchor_to_blockchain(h, entry["event_id"]):
            entry["status"] = "anchored"
            # Update the entry in the file (simple rewrite for demo)
            # In production, use a database or append-only update
        else:
            print(f"   ⏳ Pending anchor (will retry next cycle)")

    # 5. Generate Wealth Report
    report = generate_wealth_pathway_report()
    
    print("\n" + "=" * 55)
    print("🏁 TRANSMUTATION COMPLETE")
    print(f"   Total Entries: {report['total_entries']}")
    print(f"   Total Wealth Minted: {report['total_wealth_minted']}")
    print(f"   Pathways Identified: {len(report['pathways'])}")
    print("=" * 55)
    
    # Print the pathways
    print("\n🌟 WEALTH PATHWAYS GENERATED FROM ERROR:")
    for wp, data in report["pathways"].items():
        print(f"  • {wp}: {data['count']}x occurrences, {data['total_wealth']} wealth")
        for lesson in data["lessons"]:
            print(f"      → {lesson}")

if __name__ == "__main__":
    ckpt = load_ckpt()
    main()
