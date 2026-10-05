#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import argparse
import csv
from pathlib import Path
from newton_chain.ledger import NewtonChain

REQUIRED_COLUMNS = {
    "tin_c",
    "tout_c",
    "mass_flow_kg_s",
    "interval_s",
}

def number(row, name, line_number):
    try:
        value = float(row[name])
    except (KeyError, TypeError, ValueError) as error:
        raise SystemExit(f"invalid {name} at CSV row {line_number}: {error}")
    return value

def main():
    parser = argparse.ArgumentParser(
        description="Append validated thermal measurements from CSV to the Newton Chain."
    )
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--ledger", default="data/thermoledger.jsonl")
    parser.add_argument("--source", default="csv-import")
    parser.add_argument("--specific-heat-j-kg-k", type=float, default=1005.0)
    args = parser.parse_args()

    if not args.csv_file.is_file():
        parser.error(f"CSV file not found: {args.csv_file}")

    appended = 0
    total_joules = 0.0
    chain = NewtonChain(args.ledger)

    with args.csv_file.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)

        if not reader.fieldnames:
            raise SystemExit("CSV has no header row")

        missing = REQUIRED_COLUMNS - set(reader.fieldnames)
        if missing:
            raise SystemExit(
                "CSV missing required columns: " + ", ".join(sorted(missing))
            )

        for line_number, row in enumerate(reader, start=2):
            tin_c = number(row, "tin_c", line_number)
            tout_c = number(row, "tout_c", line_number)
            mass_flow_kg_s = number(row, "mass_flow_kg_s", line_number)
            interval_s = number(row, "interval_s", line_number)

            if mass_flow_kg_s < 0:
                raise SystemExit(
                    f"mass_flow_kg_s cannot be negative at CSV row {line_number}"
                )

            if interval_s <= 0:
                raise SystemExit(
                    f"interval_s must be greater than zero at CSV row {line_number}"
                )

            delta_t_c = tout_c - tin_c
            power_w = mass_flow_kg_s * args.specific_heat_j_kg_k * delta_t_c
            joules = power_w * interval_s

            block = chain.append(
                joules_generated=joules,
                average_power_w=power_w,
                telemetry_payload={
                    "source": args.source,
                    "csv_row": line_number,
                    "tin_c": tin_c,
                    "tout_c": tout_c,
                    "mass_flow_kg_s": mass_flow_kg_s,
                    "interval_s": interval_s,
                    "specific_heat_j_kg_k": args.specific_heat_j_kg_k,
                    "delta_t_c": delta_t_c,
                },
            )

            appended += 1
            total_joules += joules
            print(
                f"row={line_number} "
                f"hash={block['current_hash'][:12]} "
                f"joules={joules:.2f}"
            )

    print(f"appended: {appended}")
    print(f"total_joules: {total_joules:.2f}")

if __name__ == "__main__":
    main()
