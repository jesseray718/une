#!/data/data/com.termux/files/usr/bin/python3
"""
Re-Scorer v1.0: Classifies files by semantic meaning, not literal word match.
Scores based on: extension, directory context, project membership, and filename keywords.
"""
import json
import os
import re

IMMORTAL = "/sdcard/openroot/context_bridge/immortal_context.json"

# === CLASSIFICATION RULES ===

# Kingdom Core: Your actual work — code, docs, wisdom, engineering
KINGDOM_EXTENSIONS = {
    ".py", ".sh", ".js", ".ts", ".json", ".yaml", ".yml", ".toml",
    ".md", ".txt", ".rst", ".csv", ".sql", ".html", ".css",
    ".c", ".cpp", ".h", ".rs", ".go", ".rb", ".lua", ".php",
    ".drawio", ".svg", ".scad", ".stl",
}

KINGDOM_DIRS = {
    "openroot", "une", "wisdom", "agape", "kai", "skills", "docs",
    "research", "scripts", "src", "computational_flow", "universical",
    "openroot-ecosystem", "agape-une", "renaissance", "aerocement",
    "volumetric", "opencell", "thermal", "economic", "syn-fuel",
    "projects", "github-repos",
}

KINGDOM_KEYWORDS = {
    "governor", "wiring", "hub", "spoke", "build", "absorber",
    "bridge", "context", "seed", "wisdom", "prime", "universical",
    "permaculture", "eta", "cooperation", "node", "mesh",
    "sensor", "flow", "thermal", "cell", "aero", "cement",
    "openroot", "agape", "une", "kai",
}

# Neutral: System files, configs, caches — not parasitic, just infrastructure
NEUTRAL_DIRS = {
    ".git", "node_modules", "vendor", "__pycache__", ".cache",
    "cache", "tmp", "temp", ".npm", ".config",
}

NEUTRAL_EXTENSIONS = {
    ".log", ".lock", ".pid", ".sock", ".db", ".sqlite",
    ".nomedia", ".uuid", ".bak",
}

# Parasitic: Actual waste — duplicates, trash, orphaned media thumbnails
PARASITIC_PATTERNS = [
    r"\.thumbnails/", r"\.Trash/", r"is_legacy_not_exist",
    r"\.database_uuid$", r"/\.nomedia$",
    r"/Android/obb/", r"/Android/data/com\.",
]

PARASITIC_EXTENSIONS = {
    ".apk", ".dex", ".so", ".ttf", ".woff", ".woff2",
}


def classify_file(path, size):
    """Classify a file based on path, extension, and directory context."""
    ext = os.path.splitext(path)[1].lower()
    path_lower = path.lower()
    parts = re.split(r'[/\\]', path_lower)
    dirs = set(parts)

    # Check parasitic first (trash/thumbnails = delete candidates)
    for pattern in PARASITIC_PATTERNS:
        if re.search(pattern, path_lower):
            return 0.0, "PARASITIC_WASTE", ["matched: " + pattern]

    if ext in PARASITIC_EXTENSIONS:
        # APKs in repos might be needed, but standalone are waste
        if "repo" not in path_lower and "openroot" not in path_lower:
            return 0.05, "PARASITIC_WASTE", [f"ext:{ext}"]

    # Check neutral (infrastructure)
    if dirs & NEUTRAL_DIRS:
        if ext in NEUTRAL_EXTENSIONS:
            return 0.3, "NEUTRAL_NOISE", ["infra"]
        return 0.35, "NEUTRAL_NOISE", ["infra_dir"]

    # Check Kingdom Core (your actual work)
    score = 0.0
    keywords_hit = []

    # Kingdom directory match
    if dirs & KINGDOM_DIRS:
        score = max(score, 0.7)
        keywords_hit.append("kingdom_dir")

    # Kingdom extension match
    if ext in KINGDOM_EXTENSIONS:
        score = max(score, 0.6)
        keywords_hit.append(f"ext:{ext}")

    # Kingdom keyword in filename
    filename = os.path.basename(path_lower)
    for kw in KINGDOM_KEYWORDS:
        if kw in filename or kw in path_lower:
            score = max(score, 0.8)
            keywords_hit.append(kw)

    # Large code/doc files = high value
    if ext in KINGDOM_EXTENSIONS and size > 1000:
        score = max(score, 0.75)
        keywords_hit.append("substantial_content")

    # Empty files = low value (unless .gitkeep)
    if size == 0 and not filename.startswith(".gitkeep"):
        score = min(score, 0.2)
        keywords_hit.append("empty")

    if score >= 0.7:
        category = "KINGDOM_CORE"
    elif score >= 0.5:
        category = "ALIGNMENT_BUILD"
    elif score >= 0.2:
        category = "NEUTRAL_NOISE"
    else:
        category = "PARASITIC_WASTE"

    return round(score, 4), category, keywords_hit


def main():
    print("=== RE-SCORER v1.0 ===")
    print("Loading immortal context...")

    with open(IMMORTAL, 'r') as f:
        data = json.load(f)

    files = data.get("file_index", [])
    print(f"Re-scoring {len(files)} files...")

    stats = {"KINGDOM_CORE": 0, "ALIGNMENT_BUILD": 0, "NEUTRAL_NOISE": 0, "PARASITIC_WASTE": 0}

    for entry in files:
        path = entry.get("path", "")
        size = entry.get("size", 0)

        score, category, keywords = classify_file(path, size)

        entry["alignment_score"] = score
        entry["category"] = category
        entry["keywords"] = keywords
        entry["essence_chain"] = f"Score: {score} | {category}"

        stats[category] += 1

        processed = sum(stats.values())
        if processed % 10000 == 0:
            total = sum(stats.values())
            print(f"   Processed {total}/{len(files)}...")

    data["statistics"] = stats
    data["meta"]["rescore_version"] = "1.0_semantic_classification"

    print(f"\nSaving to {IMMORTAL}...")
    with open(IMMORTAL, 'w') as f:
        json.dump(data, f, indent=2)

    print("\n=== RE-SCORING COMPLETE ===")
    print(f"KINGDOM_CORE (Your real work):     {stats['KINGDOM_CORE']:6d}")
    print(f"ALIGNMENT_BUILD (Supporting work): {stats['ALIGNMENT_BUILD']:6d}")
    print(f"NEUTRAL_NOISE (Infrastructure):    {stats['NEUTRAL_NOISE']:6d}")
    print(f"PARASITIC_WASTE (Delete candidates): {stats['PARASITIC_WASTE']:6d}")

    total_kingdom = stats['KINGDOM_CORE'] + stats['ALIGNMENT_BUILD']
    total_waste = stats['PARASITIC_WASTE']
    print(f"\nSignal ratio: {total_kingdom}:{total_waste}")
    print(f"Kingdom percentage: {(total_kingdom/len(files)*100):.1f}%")
    print(f"Waste percentage: {(total_waste/len(files)*100):.1f}%")


if __name__ == "__main__":
    main()
