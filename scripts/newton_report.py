#!/usr/bin/env python3
import argparse
import json
from collections import Counter
from pathlib import Path

def load_records(path):
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
            records.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise SystemExit(f"invalid JSON at ledger line {line_number}: {error}")
    return records

def main():
    parser = argparse.ArgumentParser(
        description="Generate a local Newton Chain telemetry summary."
    )
    parser.add_argument("--ledger", default="data/thermoledger.jsonl")
    args = parser.parse_args()

    records = load_records(Path(args.ledger))

    if not records:
        print("status: empty")
        print("blocks: 0")
        print("joules: 0.00")
        print("kwh: 0.000000")
        raise SystemExit(0)

    joules = [float(record.get("joules_generated", 0.0)) for record in records]
    power = [float(record.get("average_power_w", 0.0)) for record in records]
    sources = Counter(
        record.get("telemetry_payload", {}).get("source", "unknown")
        for record in records
    )

    total_joules = sum(joules)
    total_kwh = total_joules / 3600000.0

    print("status: summary")
    print(f"blocks: {len(records)}")
    print(f"first_timestamp: {records[0].get('timestamp', '')}")
    print(f"last_timestamp: {records[-1].get('timestamp', '')}")
    print(f"total_joules: {total_joules:.2f}")
    print(f"total_kwh: {total_kwh:.6f}")
    print(f"average_power_w: {sum(power) / len(power):.2f}")
    print(f"minimum_power_w: {min(power):.2f}")
    print(f"maximum_power_w: {max(power):.2f}")
    print("sources:")
    for source, count in sorted(sources.items()):
        print(f"  {source}: {count}")

if __name__ == "__main__":
    main()
