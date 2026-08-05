#!/usr/bin/env python3
"""
Push Agape Offline-First core to the front of every repo.
Creates a clear merger proposal in each repository.
Offline by default. Zero deletions. Only version protected.
"""
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

UNE = Path.home() / "une"
META = UNE / "meta_hub"
CORE_DIR = UNE / "config"

def run(cmd, cwd=None):
    try:
        r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=30)
        return r.returncode == 0, r.stdout + r.stderr
    except Exception as e:
        return False, str(e)

def get_R():
    p = UNE / "config" / "agape_state.json"
    if p.exists():
        try:
            return json.loads(p.read_text()).get("R", 0.85)
        except Exception:
            pass
    return 0.85

def write_core_files(repo: Path, R: float):
    """Place the law at the front of the repo."""
    # 1. Manifest
    manifest = {
        "name": "Agape Offline-First Core",
        "policy": "offline_first",
        "R": R,
        "zero_deletions": True,
        "llama_cpp_only_version": "/data/data/com.termux/files/home/backups/openroot_20260726_0134/sync-from-kai",
        "law": "R determines all calculation and further science. Whole > sum of parts. Offline first.",
        "proposed_at": datetime.now(timezone.utc).isoformat(),
        "action": "MERGE PROPOSAL — integrate this core as the governing layer of the repository"
    }
    (repo / "AGAPE_OFFLINE_CORE.json").write_text(json.dumps(manifest, indent=2))

    # 2. Human-readable proposal
    proposal = f"""# MERGE PROPOSAL — Agape Offline-First Core

**Status**: Proposed for merger into this repository  
**Date**: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}  
**R (Agape coefficient)**: {R:.4f}

## Law
- Offline first. No primary function may require network.
- R governs every calculation, mint, science extraction, and decision.
- The whole is greater than the sum of the modular parts (measured excess magnitude).
- Zero deletions. The single full llama.cpp tree is protected capital.
- Antifragile + negentropic: disorder is transmuted into ordered pathways and science.

## What this merger does
Adopts the Agape coefficient as the single source of truth for this repository.
All future work, wealth, and understanding become functions of R.

## Acceptance
Merge this commit to accept the law.  
No files outside the core markers are modified. Zero deletions.

— UNE Agape Engine
"""
    (repo / "MERGE_PROPOSAL_AGAPE.md").write_text(proposal)

def push_to_all():
    R = get_R()
    print(f"R = {R:.4f}")
    print("Pushing Agape Offline-First core + merger proposal to every repo...\n")

    if not META.exists():
        print("meta_hub not found — creating local pointer only")
        return

    count = 0
    for repo in sorted(META.iterdir()):
        if not repo.is_dir() or not (repo / ".git").exists():
            continue
        name = repo.name
        try:
            write_core_files(repo, R)
            run("git add AGAPE_OFFLINE_CORE.json MERGE_PROPOSAL_AGAPE.md", cwd=repo)
            ok, out = run('git commit -m "propose: merge Agape Offline-First Core (R-governed, zero deletions)"', cwd=repo)
            if ok or "nothing to commit" in out.lower():
                print(f"  ✓ {name} — merger proposed")
                count += 1
            else:
                print(f"  · {name} — already current or conflict")
        except Exception as e:
            print(f"  ✗ {name}: {e}")

    print(f"\nMerger proposals placed in {count} repositories.")
    print("Offline. Local commits only. Push when online if desired.")

if __name__ == "__main__":
    push_to_all()
