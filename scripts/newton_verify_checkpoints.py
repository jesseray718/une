#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

ZERO_HASH = "0" * 64

def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))

def main():
    parser = argparse.ArgumentParser(
        description="Verify hash continuity for Newton Chain checkpoints."
    )
    parser.add_argument(
        "--checkpoint-ledger",
        default="data/newton_checkpoints.jsonl",
    )
    args = parser.parse_args()

    path = Path(args.checkpoint_ledger)

    if not path.exists():
        print("status: no-checkpoints")
        print("checkpoints: 0")
        raise SystemExit(0)

    expected_previous_hash = ZERO_HASH
    checkpoint_count = 0

    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not line.strip():
            continue

        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise SystemExit(
                f"invalid checkpoint JSON at line {line_number}: {error}"
            )

        stored_hash = record.pop("current_hash", None)

        if record.get("previous_checkpoint_hash") != expected_previous_hash:
            raise SystemExit(
                f"broken checkpoint link at line {line_number}"
            )

        calculated_hash = hashlib.sha256(
            canonical_json(record).encode("utf-8")
        ).hexdigest()

        if not stored_hash or calculated_hash != stored_hash:
            raise SystemExit(
                f"checkpoint hash mismatch at line {line_number}"
            )

        expected_previous_hash = stored_hash
        checkpoint_count += 1

    print("status: checkpoints-valid")
    print(f"checkpoints: {checkpoint_count}")
    print(f"tip_hash: {expected_previous_hash}")

if __name__ == "__main__":
    main()
