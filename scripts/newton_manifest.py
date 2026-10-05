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

def latest_receipt(directory, pattern):
    files = sorted(directory.glob(pattern), key=lambda item: item.stat().st_mtime)
    return files[-1] if files else None

def main():
    parser = argparse.ArgumentParser(
        description="Create a local Newton Chain release manifest."
    )
    parser.add_argument("--ledger", default="data/thermoledger.jsonl")
    parser.add_argument("--output-dir", default="data/newton_manifests")
    parser.add_argument("--label", default="manual-manifest")
    args = parser.parse_args()

    ledger = Path(args.ledger)
    output_dir = Path(args.output_dir)

    if not ledger.is_file():
        raise SystemExit(f"ledger not found: {ledger}")

    snapshot = latest_receipt(
        Path("data/newton_snapshots"),
        "newton_snapshot_*.json",
    )
    seal = latest_receipt(
        Path("data/newton_seals"),
        "newton_seal_*.json",
    )

    if snapshot is None:
        raise SystemExit("no snapshot receipt found")

    if seal is None:
        raise SystemExit("no seal receipt found")

    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "schema_version": "1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "label": args.label,
        "ledger_path": str(ledger),
        "ledger_sha256": sha256_file(ledger),
        "snapshot_path": str(snapshot),
        "snapshot_sha256": sha256_file(snapshot),
        "seal_path": str(seal),
        "seal_sha256": sha256_file(seal),
    }

    encoded = json.dumps(
        manifest,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    receipt = dict(manifest)
    receipt["manifest_hash"] = hashlib.sha256(encoded).hexdigest()

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output = output_dir / f"newton_manifest_{stamp}.json"
    output.write_text(
        json.dumps(receipt, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"manifest: {output}")
    print(f"manifest_hash: {receipt['manifest_hash']}")
    print(f"ledger_sha256: {receipt['ledger_sha256']}")
    print(f"snapshot: {snapshot}")
    print(f"seal: {seal}")

if __name__ == "__main__":
    main()
