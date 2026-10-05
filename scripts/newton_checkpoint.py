#!/usr/bin/env python3
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ZERO_HASH = "0" * 64

def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))

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
        description="Create a hash-linked local Newton Chain checkpoint."
    )
    parser.add_argument("--ledger", default="data/thermoledger.jsonl")
    parser.add_argument("--checkpoint-ledger",
                        default="data/newton_checkpoints.jsonl")
    parser.add_argument("--label", default="manual")
    args = parser.parse_args()

    ledger = Path(args.ledger)
    checkpoint_ledger = Path(args.checkpoint_ledger)

    if not ledger.is_file():
        raise SystemExit(f"ledger not found: {ledger}")

    checkpoint_ledger.parent.mkdir(parents=True, exist_ok=True)

    previous_checkpoint_hash = ZERO_HASH
    if checkpoint_ledger.exists():
        for line in checkpoint_ledger.read_text(encoding="utf-8").splitlines():
            if line.strip():
                previous_checkpoint_hash = json.loads(line)["current_hash"]

    tip_hash, block_count = read_tip(ledger)

    payload = {
        "schema_version": "1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "label": args.label,
        "previous_checkpoint_hash": previous_checkpoint_hash,
        "ledger_path": str(ledger),
        "ledger_sha256": sha256_file(ledger),
        "ledger_block_count": block_count,
        "ledger_tip_hash": tip_hash,
    }

    record = dict(payload)
    record["current_hash"] = hashlib.sha256(
        canonical_json(payload).encode("utf-8")
    ).hexdigest()

    with checkpoint_ledger.open("a", encoding="utf-8") as handle:
        handle.write(canonical_json(record) + "\n")

    print(f"checkpoint_ledger: {checkpoint_ledger}")
    print(f"checkpoint_hash: {record['current_hash']}")
    print(f"ledger_blocks: {block_count}")
    print(f"ledger_tip_hash: {tip_hash}")

if __name__ == "__main__":
    main()
