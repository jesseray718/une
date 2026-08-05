"""Master dossier: health check, trajectory projection, compounding state summary."""
import json, os, sys, math, subprocess
from pathlib import Path
from datetime import datetime, timezone
from state_utils import load_ckpt, save_ckpt, stamp, append_lesson

UNE = Path(os.environ.get("UNE_DIR", str(Path.home() / "une")))
DOSSIER_FILE = UNE / "dossier.json"
MASTER_FILE = UNE / "master.md"
HEALTH_FILE = UNE / "health_report.json"

def collect_system_stats():
    """Gather Android/Termux system metrics via shell."""
    stats = {}
    try:
        # Disk usage
        df = subprocess.run(["df", "-h", "/data"], capture_output=True, text=True)
        stats["disk"] = df.stdout.strip().split("\n")[-1].split() if df.returncode == 0 else []
        # Memory
        mem = subprocess.run(["free", "-m"], capture_output=True, text=True)
        lines = mem.stdout.strip().split("\n") if mem.returncode == 0 else []
        if len(lines) >= 2:
            stats["mem_mb"] = lines[1].split()
        # CPU temp
        temp_paths = ["/sys/class/thermal/thermal_zone0/temp", "/sys/class/thermal/thermal_zone1/temp"]
        for tp in temp_paths:
            try:
                t = int(Path(tp).read_text().strip()) / 1000.0
                stats["cpu_temp_c"] = round(t, 1)
                break
            except Exception:
                continue
        # Uptime
        uptime = subprocess.run(["uptime"], capture_output=True, text=True)
        stats["uptime"] = uptime.stdout.strip() if uptime.returncode == 0 else "unknown"
        # Python file count
        stats["py_files"] = len(list(UNE.rglob("*.py")))
        # Total repo size
        du = subprocess.run(["du", "-sh", str(UNE)], capture_output=True, text=True)
        stats["repo_size"] = du.stdout.strip().split()[0] if du.returncode == 0 else "unknown"
    except Exception as e:
        stats["error"] = str(e)
    return stats

def health_check(state, sys_stats):
    """Score system health 0-100."""
    checks = []
    score = 100
    # Energy efficiency
    energy = state.get("energy_joules", 0.0)
    cycle = max(state.get("cycle", 0), 1)
    energy_per_cycle = energy / cycle
    if energy_per_cycle > 1.0:
        score -= 20
        checks.append({"check": "energy_per_cycle", "status": "warn", "value": f"{energy_per_cycle:.4f} J/cycle"})
    else:
        checks.append({"check": "energy_per_cycle", "status": "ok", "value": f"{energy_per_cycle:.4f} J/cycle"})
    # Fitness trending
    fitness = state.get("fitness_score", 0.0)
    if fitness < 0.1:
        score -= 15
        checks.append({"check": "fitness_score", "status": "warn", "value": fitness})
    else:
        checks.append({"check": "fitness_score", "status": "ok", "value": fitness})
    # Lesson accumulation
    lessons = state.get("lessons", [])
    if len(lessons) < cycle:
        score -= 10
        checks.append({"check": "lesson_rate", "status": "warn", "value": f"{len(lessons)}/{cycle}"})
    else:
        checks.append({"check": "lesson_rate", "status": "ok", "value": f"{len(lessons)}/{cycle}"})
    # Mesh growth
    mesh = state.get("mesh_nodes", 0)
    if mesh == 0 and cycle > 0:
        score -= 15
        checks.append({"check": "mesh_growth", "status": "warn", "value": mesh})
    else:
        checks.append({"check": "mesh_growth", "status": "ok", "value": mesh})
    # System temperature
    temp = sys_stats.get("cpu_temp_c")
    if temp and temp > 55:
        score -= 20
        checks.append({"check": "cpu_temp", "status": "warn", "value": temp})
    elif temp:
        checks.append({"check": "cpu_temp", "status": "ok", "value": temp})
    # Last error
    last_err = state.get("last_error")
    if last_err:
        score -= 25
        checks.append({"check": "last_error", "status": "error", "value": last_err})
    else:
        checks.append({"check": "last_error", "status": "ok", "value": None})

    return {"score": max(0, score), "checks": checks}

def project_trajectory(state):
    """Project forward N cycles based on current growth rates."""
    cycle = max(state.get("cycle", 0), 1)
    energy = state.get("energy_joules", 0.0)
    mesh = max(state.get("mesh_nodes", 1), 1)
    fitness = state.get("fitness_score", 0.0)
    lessons = len(state.get("lessons", []))

    # Rates per cycle
    energy_rate = energy / cycle
    mesh_rate = mesh / cycle if cycle > 0 else 0
    lesson_rate = lessons / cycle

    projections = []
    for n in [10, 50, 100, 500, 1000]:
        future_cycle = cycle + n
        projected = {
            "cycles_ahead": n,
            "future_cycle": future_cycle,
            "projected_energy_j": round(energy + (energy_rate * n), 4),
            "projected_mesh_nodes": int(mesh * (6 ** min(n // 10, 8))) if mesh_rate > 0 else mesh,
            "projected_lessons": int(lessons + (lesson_rate * n)),
            "projected_fitness": round(min(fitness + (0.001 * n), 1.0), 4) if fitness > 0 else 0.0,
            "projected_depth": int(math.log(max(mesh * (6 ** min(n // 10, 8)), 1), 6)) if mesh_rate > 0 else 0
        }
        projections.append(projected)
    return projections

def build_dossier(state, sys_stats, health, projections):
    """Compile full dossier JSON."""
    return {
        "generated": stamp(),
        "system": {
            "device": "Samsung SM-A156U",
            "environment": "Termux + Shizuku",
            "py_files": sys_stats.get("py_files", 0),
            "repo_size": sys_stats.get("repo_size", "?"),
            "cpu_temp_c": sys_stats.get("cpu_temp_c", "?"),
            "uptime": sys_stats.get("uptime", "?")[:120]
        },
        "checkpoint": state,
        "health": health,
        "trajectory": projections,
        "axioms_active": [
            "observe_and_interact",
            "catch_and_store_energy",
            "apply_self_regulation_and_accept_feedback",
            "produce_no_waste",
            "integrate_rather_than_segregate"
        ]
    }

def write_master_md(dossier):
    """Human-readable master file."""
    h = dossier["health"]
    s = dossier["system"]
    c = dossier["checkpoint"]
    t = dossier["trajectory"]
    md = f"""# UNE Master Dossier
Generated: {dossier['generated']}

## System
| Metric | Value |
|--------|-------|
| Device | {s['device']} |
| Environment | {s['environment']} |
| Python files | {s['py_files']} |
| Repo size | {s['repo_size']} |
| CPU temp | {s['cpu_temp_c']}°C |

## Checkpoint State
| Metric | Value |
|--------|-------|
| Cycle | {c.get('cycle', 0)} |
| Fitness | {c.get('fitness_score', 0)} |
| Mesh nodes | {c.get('mesh_nodes', 0)} |
| Energy | {c.get('energy_joules', 0):.4f} J |
| Lessons | {len(c.get('lessons', []))} |
| Merkle root | {c.get('merkle_root', '')[:24]}... |

## Health Score: {h['score']}/100
"""
    for chk in h["checks"]:
        icon = "✅" if chk["status"] == "ok" else "⚠️" if chk["status"] == "warn" else "❌"
        md += f"| {icon} {chk['check']} | {chk['status']} | {chk['value']} |\n"

    md += "\n## Trajectory Projection\n"
    md += "| Cycles ahead | Future cycle | Energy (J) | Mesh nodes | Depth | Lessons | Fitness |\n"
    md += "|-------------|-------------|-----------|------------|-------|---------|----------|\n"
    for p in t:
        md += f"| {p['cycles_ahead']} | {p['future_cycle']} | {p['projected_energy_j']} | {p['projected_mesh_nodes']} | {p['projected_depth']} | {p['projected_lessons']} | {p['projected_fitness']} |\n"

    md += f"\n## Active Axioms\n"
    for a in dossier.get("axioms_active", []):
        md += f"- {a}\n"
    md += f"\n---\n*Auto-generated by dossier.py*\n"

    MASTER_FILE.write_text(md)
    return md

def main():
    state = load_ckpt()
    sys_stats = collect_system_stats()
    health = health_check(state, sys_stats)
    projections = project_trajectory(state)
    dossier = build_dossier(state, sys_stats, health, projections)

    # Write all outputs
    DOSSIER_FILE.write_text(json.dumps(dossier, indent=2, default=str))
    HEALTH_FILE.write_text(json.dumps(health, indent=2))
    md = write_master_md(dossier)

    # Record health in checkpoint
    state["health_score"] = health["score"]
    state["last_health_check"] = stamp()
    if health["score"] < 70:
        append_lesson(f"Health degraded to {health['score']}/100", "warning")
    save_ckpt(state)

    print(f"[DOSSIER] health={health['score']}/100 mesh={state.get('mesh_nodes',0)} "
          f"cycle={state.get('cycle',0)} fitness={state.get('fitness_score',0)}")
    print(f"[DOSSIER] files: {DOSSIER_FILE.name}, {HEALTH_FILE.name}, {MASTER_FILE.name}")
    print(f"[DOSSIER] trajectory: {len(projections)} projections written")

if __name__ == "__main__":
    main()
