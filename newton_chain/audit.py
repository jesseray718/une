#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from .ledger import ZERO_HASH, block_hash

def audit(path):
    path = Path(path)
    if not path.exists():
        print(f"ledger not found: {path}")
        return 0

    expected_previous = ZERO_HASH
    total_joules = 0.0
    count = 0

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        record = json.loads(line)
        stored_hash = record.pop("current_hash", None)

        if record.get("previous_hash") != expected_previous:
            raise SystemExit(f"broken chain at line {line_number}")

        if not stored_hash or block_hash(record) != stored_hash:
            raise SystemExit(f"hash mismatch at line {line_number}")

        expected_previous = stored_hash
        total_joules += float(record.get("joules_generated", 0))
        count += 1

    print(f"status: valid")
    print(f"blocks: {count}")
    print(f"joules: {total_joules:.2f}")
    print(f"kwh: {total_joules / 3600000:.6f}")
    return count

def main():
    parser = argparse.ArgumentParser(description="Audit a local Newton Chain ledger.")
    parser.add_argument("--ledger", default="data/thermoledger.jsonl")
    args = parser.parse_args()
    audit(args.ledger)

if __name__ == "__main__":
    main()
