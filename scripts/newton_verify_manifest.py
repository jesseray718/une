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
        description="Verify a Newton Chain release manifest."
    )
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--ledger", default="data/thermoledger.jsonl")
    args = parser.parse_args()

    if not args.manifest.is_file():
        raise SystemExit(f"manifest not found: {args.manifest}")

    ledger = Path(args.ledger)
    if not ledger.is_file():
        raise SystemExit(f"ledger not found: {ledger}")

    try:
        receipt = json.loads(args.manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SystemExit(f"invalid manifest JSON: {error}")

    stored_hash = receipt.pop("manifest_hash", None)
    calculated_hash = hashlib.sha256(
        canonical_json(receipt).encode("utf-8")
    ).hexdigest()

    if not stored_hash or stored_hash != calculated_hash:
        raise SystemExit("manifest hash mismatch")

    snapshot = Path(receipt.get("snapshot_path", ""))
    seal = Path(receipt.get("seal_path", ""))

    if not snapshot.is_file():
        raise SystemExit(f"snapshot referenced by manifest not found: {snapshot}")

    if not seal.is_file():
        raise SystemExit(f"seal referenced by manifest not found: {seal}")

    checks = {
        "ledger_sha256": (
            receipt.get("ledger_sha256"),
            sha256_file(ledger),
        ),
        "snapshot_sha256": (
            receipt.get("snapshot_sha256"),
            sha256_file(snapshot),
        ),
        "seal_sha256": (
            receipt.get("seal_sha256"),
            sha256_file(seal),
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

    print("status: manifest-valid")
    print(f"manifest: {args.manifest}")
    print(f"manifest_hash: {stored_hash}")
    print(f"ledger_sha256: {checks['ledger_sha256'][1]}")
    print(f"snapshot: {snapshot}")
    print(f"seal: {seal}")

if __name__ == "__main__":
    main()
