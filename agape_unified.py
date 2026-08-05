"""Agape Unified: Clones all jesseray718 repos, analyzes structure,
wires them into a fractal node network, auto-optimizes each repo,
and proposes a unified theory of integration."""
import json, os, sys, subprocess, time, hashlib, math, re
from pathlib import Path
from datetime import datetime, timezone
from state_utils import load_ckpt, save_ckpt, stamp, append_lesson

UNE = Path(os.environ.get("UNE_DIR", str(Path.home() / "une")))
GITHUB_USER = os.environ.get("GITHUB_USER", "jesseray718")
ECOSYSTEM_DIR = Path(os.environ.get("ECOSYSTEM_DIR", str(Path.home() / "ecosystem")))
MANIFEST_FILE = UNE / "ecosystem_manifest.json"
UNIFIED_THEORY_FILE = UNE / "unified_theory.md"
NODE_MAP_FILE = UNE / "node_map.json"

REPOS = ["une", "openroot", "wisdom-scaffold", "canonical", "aerocement", "jesseray718"]

def cmd(args, cwd=None, timeout=120):
    try:
        r = subprocess.run(args, capture_output=True, text=True, cwd=str(cwd) if cwd else None, timeout=timeout)
        return r.returncode == 0, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", "TIMEOUT"
    except Exception as e:
        return False, "", str(e)[:200]

def clone_all_repos():
    ECOSYSTEM_DIR.mkdir(parents=True, exist_ok=True)
    repo_status = {}
    for repo in REPOS:
        repo_path = ECOSYSTEM_DIR / repo
        url = f"https://github.com/{GITHUB_USER}/{repo}.git"
        if repo_path.exists():
            print(f"  [PULL] {repo}")
            ok, out, err = cmd(["git", "pull", "--rebase"], cwd=repo_path, timeout=60)
            status = "updated" if ok and "Already up to date" not in out else "pulled"
            if not ok:
                status = f"pull_failed: {err[:50]}"
        else:
            print(f"  [CLONE] {repo}")
            ok, out, err = cmd(["git", "clone", url, str(repo_path)], timeout=120)
            status = "cloned" if ok else f"clone_failed: {err[:50]}"
        repo_status[repo] = {"path": str(repo_path), "status": status, "url": url, "ts": stamp()}
    return repo_status

def analyze_repo(repo_name, repo_path):
    repo_path = Path(repo_path)
    info = {
        "name": repo_name, "path": str(repo_path), "ts": stamp(),
        "python_files": [], "shell_scripts": [], "json_files": [],
        "markdown_files": [], "total_lines": 0, "imports": set(),
        "functions": set(), "classes": set(), "has_git": False,
        "git_branch": "unknown", "file_count": 0, "size_bytes": 0,
        "readme_summary": "", "potential_node_role": [],
        "integration_points": [], "health": "unknown", "optimization_findings": []
    }
    if not repo_path.exists():
        info["health"] = "missing"
        return info
    ok, branch, _ = cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_path)
    if ok:
        info["has_git"] = True
        info["git_branch"] = branch
    for f in repo_path.rglob("*"):
        if ".git" in f.parts:
            continue
        info["file_count"] += 1
        try: info["size_bytes"] += f.stat().st_size
        except: pass
        if f.suffix == ".py":
            info["python_files"].append(str(f.relative_to(repo_path)))
            try:
                content = f.read_text(errors="replace")
                info["total_lines"] += content.count("\n")
                for line in content.split("\n"):
                    s = line.strip()
                    if s.startswith("import ") or s.startswith("from "):
                        parts = s.split()
                        info["imports"].add(parts[1] if len(parts) > 1 else s)
                    if s.startswith("def "):
                        info["functions"].add(s.split("(")[0].replace("def ", ""))
                    if s.startswith("class "):
                        info["classes"].add(s.split("(")[0].replace("class ", "").split(":")[0])
            except: pass
        elif f.suffix == ".sh": info["shell_scripts"].append(str(f.relative_to(repo_path)))
        elif f.suffix == ".json": info["json_files"].append(str(f.relative_to(repo_path)))
        elif f.suffix in [".md", ".txt"]: info["markdown_files"].append(str(f.relative_to(repo_path)))
    info["imports"] = sorted(info["imports"])[:50]
    info["functions"] = sorted(info["functions"])[:50]
    info["classes"] = sorted(info["classes"])[:20]
    readme_path = repo_path / "README.md"
    if readme_path.exists():
        try: info["readme_summary"] = readme_path.read_text(errors="replace")[:500]
        except: pass
    # Classify
    nl = repo_name.lower()
    funcs = " ".join(info["functions"]).lower()
    files = " ".join(info["python_files"]).lower()
    imports = " ".join(info["imports"]).lower()
    roles = []
    if "une" in nl or "energy" in funcs or "joules" in imports: roles.append("energy_accounting")
    if "open" in nl and "root" in nl: roles.append("system_kernel")
    if "wisdom" in nl or "scripture" in files or "theology" in funcs: roles.append("wisdom_engine")
    if "cannon" in nl: roles.append("deployment_launcher")
    if "aero" in nl or "cement" in nl: roles.append("physical_systems")
    if "jesseray718" == nl: roles.append("profile_hub")
    if not roles:
        if info["python_files"]: roles.append("compute_node")
        else: roles.append("passive_node")
    info["potential_node_role"] = roles
    # Integration points
    points = []
    if "state_utils" in imports or "load_ckpt" in funcs or "save_ckpt" in funcs: points.append("shared_checkpoint")
    if "json" in imports: points.append("json_state_bus")
    if "subprocess" in imports: points.append("process_orchestration")
    if "hashlib" in imports or "merkle" in funcs: points.append("merkle_anchoring")
    if "math" in imports: points.append("computational_math")
    if "ollama" in imports.lower() or "brain" in funcs: points.append("ai_integration")
    if not points: points.append("standalone")
    info["integration_points"] = points
    # Health
    if info["file_count"] == 0: info["health"] = "empty"
    elif not info["python_files"] and not info["shell_scripts"]: info["health"] = "inactive"
    elif info["python_files"] and info["total_lines"] > 50: info["health"] = "active"
    else: info["health"] = "minimal"
    return info

def build_node_map(repo_infos):
    node_map = {}
    active = [r for r in repo_infos if r["health"] != "missing"]
    for i, repo in enumerate(sorted(active, key=lambda r: r["name"])):
        node_id = f"node_{i:04d}"
        node_map[node_id] = {
            "repo": repo["name"], "role": repo["potential_node_role"],
            "integration_points": repo["integration_points"], "health": repo["health"],
            "file_count": repo["file_count"], "lines_of_code": repo["total_lines"],
            "children": [], "parent": "root",
            "synced": repo["health"] == "active", "ts": stamp()
        }
    nodes = sorted(node_map.keys())
    for i, nid in enumerate(nodes):
        child_start = (i + 1) * 6 - 5
        child_end = (i + 1) * 6
        node_map[nid]["children"] = [f"node_{j:04d}" for j in range(child_start, min(child_end + 1, len(nodes))) if f"node_{j:04d}" in node_map]
    total = len(nodes)
    max_depth = int(math.log(total, 6)) + 1 if total >= 6 else 1
    return {"nodes": node_map, "total_nodes": total, "max_depth": max_depth,
            "base_degree": 6, "capacity": 6 ** max_depth if max_depth > 0 else 1, "ts": stamp()}

def optimize_repo(repo_name, repo_path):
    repo_path = Path(repo_path)
    findings = []
    if not (repo_path / ".gitignore").exists():
        findings.append({"type": "missing_gitignore", "severity": "low", "fix": "Add .gitignore"})
    if not (repo_path / "README.md").exists():
        findings.append({"type": "missing_readme", "severity": "medium", "fix": f"Add README.md"})
    for py in repo_path.glob("*.py"):
        ok, _, err = cmd(["python3", "-m", "py_compile", str(py)], timeout=10)
        if not ok:
            findings.append({"type": "syntax_error", "severity": "critical", "fix": f"Fix {py.name}: {err[:80]}"})
    return findings

def generate_unified_theory(repo_infos, node_map):
    active = [r for r in repo_infos if r["health"] == "active"]
    total_files = sum(r["file_count"] for r in repo_infos)
    total_lines = sum(r["total_lines"] for r in repo_infos)
    roles = {}
    for r in repo_infos:
        for role in r["potential_node_role"]:
            roles.setdefault(role, []).append(r["name"])
    theory = f"""# Unified Theory of JesseRay718 Ecosystem
Generated: {stamp()}

## Overview
| Metric | Value |
|--------|-------|
| Total repos | {len(repo_infos)} |
| Active nodes | {len(active)} |
| Total files | {total_files} |
| Total lines | {total_lines} |
| Mesh depth | {node_map['max_depth']} |
| Capacity | {node_map['capacity']} |

## Ecosystem Roles
"""
    for role, repos in sorted(roles.items()):
        theory += f"### {role}\n"
        for r in repos: theory += f"- `{r}`\n"
        theory += "\n"
    theory += f"""## Integration Architecture
Shared checkpoint bus connects all repos via `state_checkpoint.json`.

## Fractal Scaling Path
Current: {node_map['total_nodes']} nodes at depth {node_map['max_depth']}
Next depth: {node_map['capacity'] * 6} capacity

## Node Cooperation Thru Agape
"It is more blessed to give than to receive" (Acts 20:35)
- Nodes give: heartbeat, lessons, computed results to checkpoint
- Nodes receive: shared state context before acting
- Nodes cooperate: no duplicated logic — each repo owns its domain

## Optimization Findings
"""
    for repo in repo_infos:
        if repo.get("optimization_findings"):
            theory += f"### {repo['name']}\n"
            for f in repo["optimization_findings"]:
                theory += f"- [{f['severity']}] {f['type']}: {f['fix']}\n"
            theory += "\n"
    theory += "\n---\n*Auto-generated by agape_unified.py*\n"
    return theory

def main():
    print("=" * 60)
    print("AGAPE UNIFIED — Ecosystem Controller")
    print("=" * 60)
    print("\n[1/6] Cloning/pulling repos...")
    repo_status = clone_all_repos()
    for repo, s in repo_status.items(): print(f"  {repo}: {s['status']}")
    print("\n[2/6] Analyzing repos...")
    repo_infos = []
    for name, s in repo_status.items():
        if "failed" in s["status"]:
            repo_infos.append({"name": name, "path": s["path"], "health": "clone_failed",
                "python_files": [], "total_lines": 0, "file_count": 0,
                "potential_node_role": ["failed"], "integration_points": [],
                "optimization_findings": []})
            continue
        print(f"  Analyzing {name}...")
        info = analyze_repo(name, s["path"])
        repo_infos.append(info)
        print(f"    files={info['file_count']} py={len(info['python_files'])} "
              f"lines={info['total_lines']} health={info['health']} role={info['potential_node_role']}")
    print("\n[3/6] Building fractal node map...")
    node_map = build_node_map(repo_infos)
    print(f"  Nodes: {node_map['total_nodes']} Depth: {node_map['max_depth']} Capacity: {node_map['capacity']}")
    NODE_MAP_FILE.write_text(json.dumps(node_map, indent=2, default=str))
    print("\n[4/6] Optimizing repos...")
    for repo in repo_infos:
        if repo["health"] in ["active", "minimal"]:
            repo["optimization_findings"] = optimize_repo(repo["name"], repo["path"])
            if repo["optimization_findings"]:
                print(f"  {repo['name']}: {len(repo['optimization_findings'])} findings")
    print("\n[5/6] Generating unified theory...")
    theory = generate_unified_theory(repo_infos, node_map)
    UNIFIED_THEORY_FILE.write_text(theory)
    print(f"  Written: {UNIFIED_THEORY_FILE.name} ({len(theory)} chars)")
    print("\n[6/6] Updating manifest and checkpoint...")
    manifest = {"generated": stamp(), "github_user": GITHUB_USER,
        "repos": {r["name"]: {"health": r["health"], "role": r["potential_node_role"],
            "files": r["file_count"], "lines": r["total_lines"]} for r in repo_infos},
        "node_map": {"total_nodes": node_map["total_nodes"], "max_depth": node_map["max_depth"]}}
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2, default=str))
    state = load_ckpt()
    state["ecosystem_nodes"] = node_map["total_nodes"]
    state["ecosystem_depth"] = node_map["max_depth"]
    state["ecosystem_capacity"] = node_map["capacity"]
    state["last_agape_sync"] = stamp()
    save_ckpt(state)
    append_lesson(f"Agape sync: {node_map['total_nodes']} nodes, depth {node_map['max_depth']}", "info")
    print("\n[COMMIT] Pushing ecosystem state...")
    cmd(["git", "add", "-A"], cwd=UNE)
    ok, out, err = cmd(["git", "commit", "-m", f"agape: {node_map['total_nodes']} nodes depth {node_map['max_depth']}"], cwd=UNE)
    if ok: cmd(["git", "push", "origin", "main"], cwd=UNE, timeout=60)
    print(f"\n{'='*60}")
    print("AGAPE UNIFIED — COMPLETE")
    print(f"{'='*60}")
    print(f"Manifest: {MANIFEST_FILE}")
    print(f"Theory: {UNIFIED_THEORY_FILE}")
    print(f"Node map: {NODE_MAP_FILE}")
    print(f"Active repos: {len([r for r in repo_infos if r['health'] == 'active'])}")
    print(f"Total nodes: {node_map['total_nodes']}")
    print(f"Max depth: {node_map['max_depth']}")
    print(f"Capacity: {node_map['capacity']}")

if __name__ == "__main__":
    main()
