"""Compounding engine: runs cycles, accumulates knowledge, auto-updates master files."""
import json, os, sys, time, math
from pathlib import Path
from datetime import datetime, timezone
from state_utils import load_ckpt, save_ckpt, stamp, append_lesson

UNE = Path(os.environ.get("UNE_DIR", str(Path.home() / "une")))

def compound_cycle(n=1):
    """Run N compounding cycles: evolve → mesh → guardian → dossier."""
    import subprocess

    results = []
    for i in range(n):
        cycle_start = time.time()
        state = load_ckpt()
        cycle_num = state.get("cycle", 0) + 1

        print(f"\n{'='*50}")
        print(f"COMPOUND CYCLE {cycle_num} (iteration {i+1}/{n})")
        print(f"{'='*50}")

        # 1. Evolution
        r = subprocess.run([sys.executable, str(UNE / "evolution_engine.py")],
                          capture_output=True, text=True, cwd=str(UNE))
        print(r.stdout.strip() if r.stdout else "[EVOLVE] no output")
        if r.returncode != 0:
            append_lesson(f"evolve failed: {r.stderr[:200]}", "critical")

        # 2. Mesh
        r = subprocess.run([sys.executable, str(UNE / "autonomous_mesh.py")],
                          capture_output=True, text=True, cwd=str(UNE))
        print(r.stdout.strip() if r.stdout else "[MESH] no output")
        if r.returncode != 0:
            append_lesson(f"mesh failed: {r.stderr[:200]}", "critical")

        # 3. Guardian
        r = subprocess.run([sys.executable, str(UNE / "guardian_wire.py")],
                          capture_output=True, text=True, cwd=str(UNE))
        print(r.stdout.strip() if r.stdout else "[GUARDIAN] no output")

        # 4. Dossier
        r = subprocess.run([sys.executable, str(UNE / "dossier.py")],
                          capture_output=True, text=True, cwd=str(UNE))
        print(r.stdout.strip() if r.stdout else "[DOSSIER] no output")

        # 5. Snapshot
        r = subprocess.run([sys.executable, str(UNE / "snapshot.py")],
                          capture_output=True, text=True, cwd=str(UNE))
        print(r.stdout.strip() if r.stdout else "[SNAPSHOT] no output")

        elapsed = time.time() - cycle_start
        state = load_ckpt()
        state["last_cycle_seconds"] = round(elapsed, 3)
        state["compounding_rate"] = round(
            state.get("fitness_score", 0) / max(elapsed, 0.001), 6
        )
        save_ckpt(state)

        results.append({
            "cycle": cycle_num,
            "elapsed_s": round(elapsed, 3),
            "fitness": state.get("fitness_score", 0),
            "mesh": state.get("mesh_nodes", 0),
            "energy": state.get("energy_joules", 0),
            "health": state.get("health_score", 0)
        })

        print(f"[COMPOUND] cycle {cycle_num} took {elapsed:.3f}s "
              f"rate={state['compounding_rate']}")

    return results

def print_trajectory(results):
    """Print compounding trajectory from this session."""
    if len(results) < 2:
        return
    print(f"\n{'='*50}")
    print("COMPOUNDING TRAJECTORY")
    print(f"{'='*50}")
    print(f"{'Cycle':>6} {'Time(s)':>8} {'Fitness':>8} {'Mesh':>8} {'Energy':>10} {'Health':>8}")
    for r in results:
        print(f"{r['cycle']:>6} {r['elapsed_s']:>8.3f} {r['fitness']:>8.4f} "
              f"{r['mesh']:>8} {r['energy']:>10.4f} {r['health']:>8}")

    # Compute compounding rate
    first = results[0]
    last = results[-1]
    if first["fitness"] > 0 and last["fitness"] > first["fitness"]:
        growth = (last["fitness"] / first["fitness"]) - 1
        print(f"\nFitness growth: {growth*100:.1f}% over {len(results)} cycles")
    if first["mesh"] > 0 and last["mesh"] > first["mesh"]:
        growth = (last["mesh"] / first["mesh"]) - 1
        print(f"Mesh growth: {growth*100:.1f}% over {len(results)} cycles")

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"[COMPOUND] Running {n} compounding cycle(s)...")
    results = compound_cycle(n)
    print_trajectory(results)

    # Final state
    state = load_ckpt()
    print(f"\n[COMPOUND] Final: cycle={state.get('cycle',0)} "
          f"mesh={state.get('mesh_nodes',0)} "
          f"fitness={state.get('fitness_score',0)} "
          f"energy={state.get('energy_joules',0):.4f}J "
          f"health={state.get('health_score',0)}")

if __name__ == "__main__":
    main()
