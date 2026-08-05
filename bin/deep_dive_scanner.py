#!os.path.expanduser("~") + "/"une/bin/python3
"""
OpenRoot Deep Dive Scanner v3.0 - Full Systems Go
Extracts: purpose, docstrings, imports, cross-references, connections.
Builds: dependency graph, interconnection map, leverage analysis.
Calculates: efficiency coefficient (Output / (Time × Joules))^3
"""
import os, sys, json, hashlib, re, ast
from datetime import datetime
from collections import defaultdict

HOME = os.path.expanduser("~")
OUTPUT_FILE = os.path.join(HOME, "openroot/context_bridge/foundation_map.json")
ENERGY_PER_LINE_J = 0.000001

SKIP_DIRS = {
    'node_modules', '__pycache__', '.git', '.cache', '.npm',
    '.termux', '.config', '.local', '.gnupg', '.ssh',
    'backups', 'tmp', 'models', '.ollama', 'storage',
    '.python', '.gradle', '.android', '.clangd', '. bark'
}

CODE_EXTENSIONS = ('.py', '.sh', '.json', '.md', '.js', '.html', '.css', '.ts')

def sha256(data):
    return hashlib.sha256(str(data).encode()).hexdigest()

def extract_purpose(filepath, content):
    """Extract the real purpose from docstrings, comments, or first meaningful lines."""
    purpose = ""
    
    # Python docstrings
    if filepath.endswith('.py'):
        try:
            tree = ast.parse(content)
            doc = ast.get_docstring(tree)
            if doc:
                purpose = doc.strip()[:300]
        except:
            pass
        if not purpose:
            for line in content.splitlines()[:5]:
                if line.strip().startswith('#') and len(line.strip()) > 5:
                    purpose = line.strip('# ').strip()[:300]
                    break
    
    # Shell comments
    elif filepath.endswith('.sh'):
        for line in content.splitlines()[:10]:
            if line.strip().startswith('#') and len(line.strip()) > 5 and not line.strip().startswith('#!'):
                purpose = line.strip('# ').strip()[:300]
                break
    
    # Markdown headers
    elif filepath.endswith('.md'):
        for line in content.splitlines()[:20]:
            if line.strip().startswith('#') and not line.strip().startswith('#!'):
                purpose = line.strip('# ').strip()[:300]
                break
    
    # JSON - look for description or name field
    elif filepath.endswith('.json'):
        try:
            data = json.loads(content)
            if isinstance(data, dict):
                for key in ['description', 'name', 'title', 'purpose', 'meta']:
                    if key in data:
                        val = data[key]
                        if isinstance(val, dict):
                            val = val.get('description', str(val))[:200]
                        purpose = f"{key}: {str(val)[:200]}"
                        break
        except:
            pass
    
    return purpose or "(no purpose extracted)"

def extract_imports(filepath, content):
    """Extract imports/requires/sources with full detail."""
    imports = []
    
    if filepath.endswith('.py'):
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
        except:
            for line in content.splitlines():
                stripped = line.strip()
                if stripped.startswith('import ') or stripped.startswith('from '):
                    parts = stripped.split()
                    if len(parts) > 1:
                        imports.append(parts[1].split('.')[0])
    
    elif filepath.endswith('.sh'):
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith('source ') or stripped.startswith('. '):
                parts = stripped.split()
                if len(parts) > 1:
                    imports.append(parts[1])
    
    elif filepath.endswith('.js'):
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith('import ') or stripped.startswith('const ') and 'require(' in stripped:
                imports.append(stripped[:60])
    
    return list(set(imports))[:20]

def extract_cross_refs(filepath, content, all_files_set):
    """Find references to OTHER files in the ecosystem."""
    refs = []
    basename = os.path.basename(filepath)
    dirname = os.path.basename(os.path.dirname(filepath))
    
    # Look for references to other project names in content
    project_names = ['openroot', 'une', 'wisdom', 'cannonball', 'bridge', 
                     'absorber', 'merkle', 'energy', 'hive', 'seed', 'context']
    
    for name in project_names:
        if name in content.lower() and name not in basename.lower():
            refs.append(name)
    
    # Look for file path references
    path_patterns = re.findall(r'[\w/\-]+/(?:une|openroot|context_bridge|skills|projects)/[\w/\-]+\.\w+', content)
    refs.extend(path_patterns[:5])
    
    return list(set(refs))[:15]

def calculate_leverage(lines, deps, refs, purpose):
    """Calculate the leverage coefficient: how much influence this file has.
    High leverage = many references + many dependencies + meaningful purpose + significant size.
    """
    connectivity = len(deps) + len(refs)
    density = lines / max(connectivity, 1)
    purpose_weight = 1.0 if purpose and "(no purpose" not in purpose else 0.1
    size_factor = min(lines / 100, 10)  # Cap at 10x
    
    # Leverage = connectivity × purpose × size (cubed for compounding)
    base = (connectivity * purpose_weight * size_factor)
    leverage = base ** 1.5 if base > 0 else 0
    return round(leverage, 4)

def scan_deep():
    files_data = []
    dir_tree = defaultdict(lambda: {
        "files": 0, "lines": 0, "joules": 0.0, "size": 0,
        "purposes": [], "imports_summary": [], "cross_refs": []
    })
    total_lines = 0
    total_size = 0
    errors = 0
    
    all_filepaths = set()
    
    # First pass: collect all file paths for cross-reference checking
    for root, dirs, files in os.walk(HOME):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        depth = root.replace(HOME, '').count(os.sep)
        if depth > 5:
            dirs[:] = []
            continue
        for f in files:
            if f.endswith(CODE_EXTENSIONS):
                all_filepaths.add(os.path.relpath(os.path.join(root, f), HOME))
    
    # Second pass: deep scan
    for root, dirs, files in os.walk(HOME):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        depth = root.replace(HOME, '').count(os.sep)
        if depth > 5:
            dirs[:] = []
            continue
        
        for file in files:
            if not file.endswith(CODE_EXTENSIONS):
                continue
                
            fpath = os.path.join(root, file)
            rel_path = os.path.relpath(fpath, HOME)
            parts = rel_path.split(os.sep)
            group = parts[0] if len(parts) > 1 else "~ (root)"
            subdir = "/".join(parts[:2]) if len(parts) > 2 else group
            
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = len(content.splitlines())
                    size = os.path.getsize(fpath)
                    
                    purpose = extract_purpose(fpath, content)
                    imports = extract_imports(fpath, content)
                    xrefs = extract_cross_refs(fpath, content, all_filepaths)
                    leverage = calculate_leverage(lines, imports, xrefs, purpose)
                    
                    entry = {
                        "path": rel_path,
                        "group": group,
                        "subdir": subdir,
                        "lines": lines,
                        "size_bytes": size,
                        "estimated_joules": round(lines * ENERGY_PER_LINE_J, 6),
                        "purpose": purpose,
                        "imports": imports,
                        "cross_references": xrefs,
                        "leverage_coefficient": leverage,
                        "extension": os.path.splitext(file)[1]
                    }
                    files_data.append(entry)
                    total_lines += lines
                    total_size += size
                    
                    dir_tree[subdir]["files"] += 1
                    dir_tree[subdir]["lines"] += lines
                    dir_tree[subdir]["joules"] += round(lines * ENERGY_PER_LINE_J, 6)
                    dir_tree[subdir]["size"] += size
                    if purpose and "(no purpose" not in purpose:
                        dir_tree[subdir]["purposes"].append(purpose[:80])
                    dir_tree[subdir]["imports_summary"].extend(imports)
                    dir_tree[subdir]["cross_refs"].extend(xrefs)
                    
            except Exception as e:
                errors += 1

    # Build interconnection graph
    graph = defaultdict(list)
    for f in files_data:
        for ref in f["cross_references"]:
            graph[f["group"]].append(ref)
    
    # Find highest-leverage files
    leverage_sorted = sorted(files_data, key=lambda x: x["leverage_coefficient"], reverse=True)
    
    # Find most connected groups
    connectivity = {g: len(set(refs)) for g, refs in graph.items()}
    
    # Global Merkle Root
    all_hashes = [sha256(f["path"] + str(f["lines"])) for f in files_data]
    global_merkle = sha256("".join(all_hashes))
    
    # Efficiency coefficient (cubed)
    total_output = len(files_data)
    total_time_est = total_lines / 100  # Rough: 100 lines per hour
    total_joules = total_lines * ENERGY_PER_LINE_J
    base_coeff = total_output / max(total_time_est * total_joules, 0.000001)
    efficiency_cubed = round(base_coeff ** 3, 6)
    
    return {
        "scan_timestamp": datetime.now().isoformat(),
        "scanner_version": "3.0-full-systems-go",
        "scan_root": HOME,
        "total_files": len(files_data),
        "total_lines": total_lines,
        "total_size_bytes": total_size,
        "estimated_total_joules": round(total_joules, 6),
        "global_merkle_root": global_merkle,
        "efficiency_coefficient_cubed": efficiency_cubed,
        "errors": errors,
        "directory_tree": dict(dir_tree),
        "interconnection_graph": dict(graph),
        "connectivity_ranking": sorted(connectivity.items(), key=lambda x: x[1], reverse=True)[:20],
        "top_leverage_files": [{
            "path": f["path"],
            "leverage": f["leverage_coefficient"],
            "lines": f["lines"],
            "purpose": f["purpose"][:100],
            "cross_refs": f["cross_references"][:5]
        } for f in leverage_sorted[:30]],
        "files": files_data
    }

def main():
    print("=" * 75)
    print("  OPENROOT DEEP DIVE SCANNER v3.0 — FULL SYSTEMS GO")
    print("  Purpose × Connection × Leverage × Efficiency³")
    print("=" * 75)
    
    result = scan_deep()
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n>>> FOUNDATION MAP: {OUTPUT_FILE}")
    print(f"  Files: {result['total_files']}")
    print(f"  Lines: {result['total_lines']:,}")
    print(f"  Size: {result['total_size_bytes']/1024/1024:.1f} MB")
    print(f"  Merkle: {result['global_merkle_root'][:16]}...")
    print(f"  Errors: {result['errors']}")
    print(f"  Efficiency Coefficient³: {result['efficiency_coefficient_cubed']}")
    
    # Directory summary
    print(f"\n>>> DIRECTORY BREAKDOWN (Top 20 by LOC):")
    print(f"{'Subdir':<35} {'Files':<7} {'Lines':<8} {'Joules':<10} {'Purposes':<9}")
    print("-" * 70)
    sorted_dirs = sorted(result["directory_tree"].items(),
        key=lambda x: x[1]["lines"], reverse=True)[:20]
    for dirname, stats in sorted_dirs:
        n_purposes = len(stats["purposes"])
        print(f"{dirname:<35} {stats['files']:<7} {stats['lines']:<8,} {stats['joules']:<10.4f} {n_purposes:<9}")
    
    # Connectivity ranking
    print(f"\n>>> INTERCONNECTION RANKING (Most Connected Groups):")
    print(f"{'Group':<25} {'Unique Connections':<20}")
    print("-" * 45)
    for group, count in result["connectivity_ranking"][:15]:
        print(f"{group:<25} {count:<20}")
    
    # Top leverage files
    print(f"\n>>> TOP 20 LEVERAGE FILES (Highest Impact per Joule):")
    print(f"{'File':<45} {'Lev':<8} {'Lines':<7} {'Purpose':<40}")
    print("-" * 100)
    for f in result["top_leverage_files"][:20]:
        print(f"{f['path'][:45]:<45} {f['leverage']:<8.2f} {f['lines']:<7} {f['purpose'][:40]:<40}")
    
    print(f"\n>>> SCAN COMPLETE. Merkle {result['global_merkle_root'][:16]}...")
    print(f"    Efficiency³: {result['efficiency_coefficient_cubed']}")

if __name__ == "__main__":
    main()
