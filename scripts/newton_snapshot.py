#!/usr/bin/env python3
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def read_tip(path):
    if not path.exists():
        return "0" * 64, 0

    tip = "0" * 64
    blocks = 0

    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        tip = record.get("current_hash", tip)
        blocks += 1

    return tip, blocks

def main():
    parser = argparse.ArgumentParser(
        description="Create a local SHA-256 snapshot receipt for the Newton Chain ledger."
    )
    parser.add_argument("--ledger", default="data/thermoledger.jsonl")
    parser.add_argument("--output-dir", default="data/newton_snapshots")
    args = parser.parse_args()

    ledger = Path(args.ledger)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not ledger.exists():
        raise SystemExit(f"ledger not found: {ledger}")

    tip_hash, block_count = read_tip(ledger)
    ledger_hash = sha256_file(ledger)

    receipt = {
        "schema_version": "1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "ledger_path": str(ledger),
        "ledger_sha256": ledger_hash,
        "block_count": block_count,
        "tip_hash": tip_hash,
    }

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = output_dir / f"newton_snapshot_{stamp}.json"
    output.write_text(
        json.dumps(receipt, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"snapshot: {output}")
    print(f"blocks: {block_count}")
    print(f"ledger_sha256: {ledger_hash}")
    print(f"tip_hash: {tip_hash}")

if __name__ == "__main__":
    main()
