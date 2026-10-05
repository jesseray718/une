#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

ZERO_HASH = "0" * 64

def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def read_tip(path):
    tip_hash = ZERO_HASH
    block_count = 0

    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise SystemExit(f"invalid ledger JSON at line {line_number}: {error}")

        tip_hash = record.get("current_hash", tip_hash)
        block_count += 1

    return tip_hash, block_count

def main():
    parser = argparse.ArgumentParser(
        description="Verify a Newton Chain snapshot receipt against a local ledger."
    )
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--ledger", default="data/thermoledger.jsonl")
    args = parser.parse_args()

    ledger = Path(args.ledger)

    if not ledger.is_file():
        raise SystemExit(f"ledger not found: {ledger}")

    if not args.snapshot.is_file():
        raise SystemExit(f"snapshot not found: {args.snapshot}")

    try:
        receipt = json.loads(args.snapshot.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SystemExit(f"invalid snapshot JSON: {error}")

    ledger_hash = sha256_file(ledger)
    tip_hash, block_count = read_tip(ledger)

    checks = {
        "ledger_sha256": (
            receipt.get("ledger_sha256"),
            ledger_hash,
        ),
        "block_count": (
            receipt.get("block_count"),
            block_count,
        ),
        "tip_hash": (
            receipt.get("tip_hash"),
            tip_hash,
        ),
    }

    failed = False

    for name, (expected, actual) in checks.items():
        if expected != actual:
            print(f"mismatch: {name}")
            print(f"expected: {expected}")
            print(f"actual: {actual}")
            failed = True

    if failed:
        raise SystemExit(1)

    print("status: snapshot-valid")
    print(f"snapshot: {args.snapshot}")
    print(f"blocks: {block_count}")
    print(f"ledger_sha256: {ledger_hash}")
    print(f"tip_hash: {tip_hash}")

if __name__ == "__main__":
    main()
