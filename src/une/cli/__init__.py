import argparse
from ..une_atomic_library import (
    unified_effective_power, 
    unified_power_acceleration,
    global_grid_mass,
    transmission_loss_mass
)

def main():
    parser = argparse.ArgumentParser(prog="une", description="UNE Unified Efficiency Framework")
    subparsers = parser.add_subparsers(dest="cmd")

    p = subparsers.add_parser("power", help="Calculate effective power")
    p.add_argument("--energy", type=float, required=True)
    p.add_argument("--time", type=float, default=3600)
    p.add_argument("--N", type=int, default=50)
    p.add_argument("--resonance", type=float, default=0.9)
    p.add_argument("--fractal", type=float, default=1.5)

    a = subparsers.add_parser("accelerate", help="Calculate acceleration")
    a.add_argument("--energy", type=float, required=True)
    a.add_argument("--time", type=float, default=3600)
    a.add_argument("--N", type=int, default=50)
    a.add_argument("--epochs", type=int, default=5)

    g = subparsers.add_parser("grid", help="Global grid mass")
    g.add_argument("--twh", type=float, default=29000)

    args = parser.parse_args()

    if args.cmd == "power":
        print(unified_effective_power(args.energy, args.time, args.N, args.resonance, args.fractal))
    elif args.cmd == "accelerate":
        print(unified_power_acceleration(args.energy, args.time, args.N, epochs=args.epochs))
    elif args.cmd == "grid":
        print(global_grid_mass(args.twh))
