#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path

def load_records(ledger_path):
    if not ledger_path.exists():
        return []
    records = []
    for line_number, line in enumerate(
        ledger_path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if line.strip():
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise SystemExit(f"invalid JSON at ledger line {line_number}: {error}")
    return records

def main():
    parser = argparse.ArgumentParser(
        description="Export local Newton Chain records to CSV."
    )
    parser.add_argument("--ledger", default="data/thermoledger.jsonl")
    parser.add_argument("--output", default="data/newton_telemetry_export.csv")
    args = parser.parse_args()

    ledger_path = Path(args.ledger)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    records = load_records(ledger_path)

    fields = [
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
    ]

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()

        for block_number, record in enumerate(records, start=1):
            payload = record.get("telemetry_payload", {})
            writer.writerow({
                "block_number": block_number,
                "timestamp": record.get("timestamp", ""),
                "previous_hash": record.get("previous_hash", ""),
                "current_hash": record.get("current_hash", ""),
                "joules_generated": record.get("joules_generated", ""),
                "average_power_w": record.get("average_power_w", ""),
                "source": payload.get("source", ""),
                "tin_c": payload.get("tin_c", ""),
                "tout_c": payload.get("tout_c", ""),
                "mass_flow_kg_s": payload.get("mass_flow_kg_s", ""),
                "interval_s": payload.get("interval_s", ""),
                "delta_t_c": payload.get("delta_t_c", ""),
            })

    print(f"exported_blocks: {len(records)}")
    print(f"output: {output_path}")

if __name__ == "__main__":
    main()
