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

def checkpoint_tip(path):
    tip = ZERO_HASH
    count = 0

    if not path.exists():
        return tip, count

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
        tip = record.get("current_hash", tip)
        count += 1

    return tip, count

def main():
    parser = argparse.ArgumentParser(
        description="Create a local immutable-style Newton Chain seal receipt."
    )
    parser.add_argument("--ledger", default="data/thermoledger.jsonl")
    parser.add_argument(
        "--checkpoint-ledger",
        default="data/newton_checkpoints.jsonl",
    )
    parser.add_argument("--output-dir", default="data/newton_seals")
    parser.add_argument("--label", default="manual-seal")
    args = parser.parse_args()

    ledger = Path(args.ledger)
    checkpoints = Path(args.checkpoint_ledger)
    output_dir = Path(args.output_dir)

    if not ledger.is_file():
        raise SystemExit(f"ledger not found: {ledger}")

    output_dir.mkdir(parents=True, exist_ok=True)

    checkpoint_hash, checkpoint_count = checkpoint_tip(checkpoints)

    payload = {
        "schema_version": "1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "label": args.label,
        "ledger_path": str(ledger),
        "ledger_sha256": sha256_file(ledger),
        "checkpoint_ledger_path": str(checkpoints),
        "checkpoint_count": checkpoint_count,
        "checkpoint_tip_hash": checkpoint_hash,
    }

    receipt = dict(payload)
    receipt["seal_hash"] = hashlib.sha256(
        canonical_json(payload).encode("utf-8")
    ).hexdigest()

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = output_dir / f"newton_seal_{stamp}.json"
    output.write_text(
        json.dumps(receipt, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"seal: {output}")
    print(f"seal_hash: {receipt['seal_hash']}")
    print(f"ledger_sha256: {receipt['ledger_sha256']}")
    print(f"checkpoint_tip_hash: {checkpoint_hash}")

if __name__ == "__main__":
    main()
