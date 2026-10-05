#!/usr/bin/env python3
import argparse
from .ledger import NewtonChain

def main():
    parser = argparse.ArgumentParser(description="Append a simulated telemetry block.")
    parser.add_argument("--ledger", default="data/thermoledger.jsonl")
    parser.add_argument("--tin-c", type=float, default=21.4)
    parser.add_argument("--tout-c", type=float, default=58.7)
    parser.add_argument("--mass-flow-kg-s", type=float, default=0.045)
    parser.add_argument("--interval-s", type=float, default=5.0)
    parser.add_argument("--specific-heat-j-kg-k", type=float, default=1005.0)
    args = parser.parse_args()

    delta_t = args.tout_c - args.tin_c
    power_w = args.mass_flow_kg_s * args.specific_heat_j_kg_k * delta_t
    joules = power_w * args.interval_s

    block = NewtonChain(args.ledger).append(
        joules_generated=joules,
        average_power_w=power_w,
        telemetry_payload={
            "source": "simulation",
            "tin_c": args.tin_c,
            "tout_c": args.tout_c,
            "mass_flow_kg_s": args.mass_flow_kg_s,
            "interval_s": args.interval_s,
            "delta_t_c": delta_t,
        },
    )
    print(f"hash: {block['current_hash']}")
    print(f"power_w: {power_w:.2f}")
    print(f"joules: {joules:.2f}")

if __name__ == "__main__":
    main()
