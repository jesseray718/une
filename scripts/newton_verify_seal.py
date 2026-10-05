#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))

def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def main():
    parser = argparse.ArgumentParser(
        description="Verify a local Newton Chain seal receipt."
    )
    parser.add_argument("seal", type=Path)
    parser.add_argument("--ledger", default="data/thermoledger.jsonl")
    args = parser.parse_args()

    if not args.seal.is_file():
        raise SystemExit(f"seal not found: {args.seal}")

    ledger = Path(args.ledger)
    if not ledger.is_file():
        raise SystemExit(f"ledger not found: {ledger}")

    try:
        receipt = json.loads(args.seal.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SystemExit(f"invalid seal JSON: {error}")

    stored_seal_hash = receipt.pop("seal_hash", None)
    calculated_seal_hash = hashlib.sha256(
        canonical_json(receipt).encode("utf-8")
    ).hexdigest()

    if not stored_seal_hash or stored_seal_hash != calculated_seal_hash:
        raise SystemExit("seal hash mismatch")

    current_ledger_hash = sha256_file(ledger)

    if receipt.get("ledger_sha256") != current_ledger_hash:
        raise SystemExit("ledger hash does not match seal")

    print("status: seal-valid")
    print(f"seal: {args.seal}")
    print(f"seal_hash: {stored_seal_hash}")
    print(f"ledger_sha256: {current_ledger_hash}")
    print(f"checkpoint_tip_hash: {receipt.get('checkpoint_tip_hash', '')}")

if __name__ == "__main__":
    main()
