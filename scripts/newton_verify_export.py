#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path

FIELDS = (
    "block_number",
    "timestamp",
    "previous_hash",
    "current_hash",
    "joules_generated",
    "average_power_w",
    "source",
    "tin_c",
    "tout_c",
    "mass_flow_kg_s",
    "interval_s",
    "delta_t_c",
)

def records_from_ledger(path):
    if not path.exists():
        return []

    records = []
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

        payload = record.get("telemetry_payload", {})
        records.append({
            "block_number": str(len(records) + 1),
            "timestamp": str(record.get("timestamp", "")),
            "previous_hash": str(record.get("previous_hash", "")),
            "current_hash": str(record.get("current_hash", "")),
            "joules_generated": str(record.get("joules_generated", "")),
            "average_power_w": str(record.get("average_power_w", "")),
            "source": str(payload.get("source", "")),
            "tin_c": str(payload.get("tin_c", "")),
            "tout_c": str(payload.get("tout_c", "")),
            "mass_flow_kg_s": str(payload.get("mass_flow_kg_s", "")),
            "interval_s": str(payload.get("interval_s", "")),
            "delta_t_c": str(payload.get("delta_t_c", "")),
        })
    return records

def records_from_csv(path):
    if not path.exists():
        raise SystemExit(f"export file not found: {path}")

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)

        if tuple(reader.fieldnames or []) != FIELDS:
            raise SystemExit("export CSV header does not match the expected format")

        return [
            {field: str(row.get(field, "")) for field in FIELDS}
            for row in reader
        ]

def main():
    parser = argparse.ArgumentParser(
        description="Verify CSV export matches the local Newton Chain ledger."
    )
    parser.add_argument("--ledger", default="data/thermoledger.jsonl")
    parser.add_argument("--export", dest="export_path",
                        default="data/newton_telemetry_export.csv")
    args = parser.parse_args()

    ledger_records = records_from_ledger(Path(args.ledger))
    export_records = records_from_csv(Path(args.export_path))

    if len(ledger_records) != len(export_records):
        raise SystemExit(
            f"mismatch: ledger has {len(ledger_records)} blocks; "
            f"export has {len(export_records)} rows"
        )

    for index, (ledger_record, export_record) in enumerate(
        zip(ledger_records, export_records),
        start=1,
    ):
        if ledger_record != export_record:
            raise SystemExit(
                f"mismatch at block {index}: "
                f"{ledger_record['current_hash'][:12]}"
            )

    print("status: export-valid")
    print(f"blocks: {len(ledger_records)}")
    print(f"ledger: {args.ledger}")
    print(f"export: {args.export_path}")

if __name__ == "__main__":
    main()
