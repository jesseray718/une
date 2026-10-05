#!/usr/bin/env python3
import argparse
from newton_chain.ledger import NewtonChain

def main():
    parser = argparse.ArgumentParser(
        description="Append a manual thermal measurement to the Newton Chain."
    )
    parser.add_argument("--ledger", default="data/thermoledger.jsonl")
    parser.add_argument("--tin-c", type=float, required=True)
    parser.add_argument("--tout-c", type=float, required=True)
    parser.add_argument("--mass-flow-kg-s", type=float, required=True)
    parser.add_argument("--interval-s", type=float, required=True)
    parser.add_argument("--specific-heat-j-kg-k", type=float, default=1005.0)
    parser.add_argument("--source", default="manual")
    args = parser.parse_args()

    delta_t = args.tout_c - args.tin_c
    power_w = args.mass_flow_kg_s * args.specific_heat_j_kg_k * delta_t
    joules = power_w * args.interval_s

    if args.interval_s <= 0:
        parser.error("--interval-s must be greater than zero")
    if args.mass_flow_kg_s < 0:
        parser.error("--mass-flow-kg-s cannot be negative")

    block = NewtonChain(args.ledger).append(
        joules_generated=joules,
        average_power_w=power_w,
        telemetry_payload={
            "source": args.source,
            "tin_c": args.tin_c,
            "tout_c": args.tout_c,
            "mass_flow_kg_s": args.mass_flow_kg_s,
            "interval_s": args.interval_s,
            "specific_heat_j_kg_k": args.specific_heat_j_kg_k,
            "delta_t_c": delta_t,
        },
    )

    print(f"hash: {block['current_hash']}")
    print(f"power_w: {power_w:.2f}")
    print(f"joules: {joules:.2f}")

if __name__ == "__main__":
    main()
