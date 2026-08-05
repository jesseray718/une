#!/usr/bin/env python3
"""ATOMIC CORE v1.0
The simplest possible system that:
1. Deduplicates all snapshots into a master file + individual files
2. Tracks coin efficiency (input joules vs optimal output)
3. Trains on all user data across the mesh
4. Provides physics graphs/charts
5. Operates as passive negentropic antifragile core
6. Stripped to atomic basics for maximum efficiency

Principle: Greatest good for greatest amount via Agape synergy.
Formula: Synergy = (output_value / input_joules) * cooperative_multiplier
"""

import os
import sys
import json
import hashlib
import time
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

# ── ATOMIC PATHS ──
UNE_ROOT = Path.home() / "une"
CORE_DIR = UNE_ROOT / "core"
DOSSIER_DIR = UNE_ROOT / "dossier"
MARKOR_DIR = Path("/sdcard/Documents/openroot") if Path("/sdcard").exists() else UNE_ROOT
TRAINER_DIR = UNE_ROOT / "trainer"
GRAPHS_DIR = UNE_ROOT / "graphs"

for d in [CORE_DIR, DOSSIER_DIR, TRAINER_DIR, GRAPHS_DIR, MARKOR_DIR]:
    d.mkdir(parents=True, exist_ok=True)

MASTER_SNAPSHOT = CORE_DIR / "master_snapshot.jsonl"
DEDUP_HASHES = CORE_DIR / ".dedup_hashes"
COIN_LEDGER = CORE_DIR / "coin_efficiency.jsonl"
SYNERGY_LOG = CORE_DIR / "synergy_log.jsonl"


# ── 1. DEDUPLICATION ENGINE ──
class Deduplicator:
    """Atomic dedup: SHA-256 hash check. One file in, one entry out."""

    def __init__(self):
        self.hashes = self.load_hashes()

    def load_hashes(self):
        if DEDUP_HASHES.exists():
            return set(h.strip() for h in DEDUP_HASHES.read_text().splitlines())
        return set()

    def save_hashes(self):
        DEDUP_HASHES.write_text('\n'.join(sorted(self.hashes)))

    def ingest(self, source_file, label="snapshot"):
        """Ingest a file, deduplicate, write to master + individual."""
        if not source_file.exists():
            return None

        content = source_file.read_text()
        h = hashlib.sha256(content.encode()).hexdigest()[:16]

        if h in self.hashes:
            return None  # Duplicate, skip

        self.hashes.add(h)
        self.save_hashes()

        entry = {
            "hash": h,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": str(source_file),
            "label": label,
            "content": content[:5000]  # Cap at 5KB per entry
        }

        with open(MASTER_SNAPSHOT, 'a') as f:
            f.write(json.dumps(entry) + '\n')

        individual = DOSSIER_DIR / f"{label}_{h}.json"
        individual.write_text(json.dumps(entry, indent=2))

        return entry

    def ingest_all(self):
        """Scan all known output files and ingest new ones."""
        sources = [
            (UNE_ROOT / "autonomous_snapshot.json", "system_snapshot"),
            (UNE_ROOT / "autonomous_report.json", "cycle_report"),
            (UNE_ROOT / "mesh_update_snapshot.json", "mesh_update"),
            (UNE_ROOT / "auto_dossier.json", "dossier"),
            (UNE_ROOT / "offline_lesson_plan.json", "lesson_plan"),
            (UNE_ROOT / "wealth_resource.json", "wealth"),
            (UNE_ROOT / "neural_graph.json", "neural_graph"),
            (UNE_ROOT / "logs" / "session_log.md", "session_log"),
            (UNE_ROOT / "logs" / "mesh_lessons.jsonl", "mesh_lessons"),
            (UNE_ROOT / "logs" / "neural_lessons.jsonl", "neural_lessons"),
            (UNE_ROOT / "logs" / "full_mesh_lessons.jsonl", "full_mesh_lessons"),
            (UNE_ROOT / "logs" / "heartbeat.log", "heartbeat"),
        ]

        ingested = 0
        for src, label in sources:
            if self.ingest(src, label):
                ingested += 1
                print(f"  📥 Ingested: {label} (new)")

        return ingested


# ── 2. COIN EFFICIENCY TRACKER ──
class CoinEfficiency:
    """
    Tracks: input_joules (human effort) vs output_value (useful work).
    Efficiency = output_value / input_joules
    Coin minted = efficiency * cooperative_multiplier
    """

    def __init__(self):
        self.entries = self.load_entries()

    def load_entries(self):
        entries = []
        if COIN_LEDGER.exists():
            with open(COIN_LEDGER) as f:
                for line in f:
                    try:
                        entries.append(json.loads(line.strip()))
                    except:
                        pass
        return entries

    def record_cycle(self, input_joules, output_value, cycle_id=None):
        """Record a coin efficiency entry for one cycle."""
        efficiency = output_value / input_joules if input_joules > 0 else 0

        participant_count = self.count_active_participants()
        coop_mult = 1.0 + (participant_count * 0.1)

        coin_minted = round(efficiency * coop_mult, 2)

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cycle": cycle_id or f"cycle_{len(self.entries) + 1}",
            "input_joules": input_joules,
            "output_value": output_value,
            "efficiency": round(efficiency, 4),
            "cooperative_multiplier": round(coop_mult, 2),
            "participants": participant_count,
            "coin_minted": coin_minted,
            "synergy_magnitude": round(coin_minted * coop_mult, 2)
        }

        self.entries.append(entry)

        with open(COIN_LEDGER, 'a') as f:
            f.write(json.dumps(entry) + '\n')

        with open(SYNERGY_LOG, 'a') as f:
            f.write(json.dumps({
                "timestamp": entry["timestamp"],
                "synergy": entry["synergy_magnitude"],
                "formula": f"({output_value}/{input_joules}) * {coop_mult} = {coin_minted}"
            }) + '\n')

        return entry

    def count_active_participants(self):
        """Count repos that had activity in the last cycle."""
        active = 0
        reports_dir = UNE_ROOT / "reports"
        if reports_dir.exists():
            for f in reports_dir.glob("*_report.json"):
                try:
                    report = json.loads(f.read_text())
                    if report.get("changes_applied"):
                        active += 1
                except:
                    pass
        return max(active, 1)

    def get_trend(self, last_n=10):
        """Get the trend of the last N cycles."""
        recent = self.entries[-last_n:]
        if not recent:
            return {"trend": "no_data", "avg_efficiency": 0}

        avg_eff = sum(e["efficiency"] for e in recent) / len(recent)
        avg_coin = sum(e["coin_minted"] for e in recent) / len(recent)

        if len(recent) >= 2:
            if recent[-1]["efficiency"] > recent[0]["efficiency"]:
                trend = "improving"
            elif recent[-1]["efficiency"] < recent[0]["efficiency"]:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"

        return {
            "trend": trend,
            "avg_efficiency": round(avg_eff, 4),
            "avg_coin": round(avg_coin, 2),
            "total_coin": round(sum(e["coin_minted"] for e in recent), 2),
            "total_synergy": round(sum(e["synergy_magnitude"] for e in recent), 2),
            "cycles": len(recent)
        }


# ── 3. UNIVERSAL TRAINER ──
class UniversalTrainer:
    """
    Compiles snapshots from all users/repos into a training corpus.
    Extracts patterns: what fixes work, what errors recur, what synergies emerge.
    Provides a "model" (pattern database) that can be applied to new problems.
    """

    def __init__(self):
        self.patterns = self.load_patterns()

    def load_patterns(self):
        pattern_file = TRAINER_DIR / "patterns.json"
        if pattern_file.exists():
            return json.loads(pattern_file.read_text())
        return {"error_fixes": {}, "synergy_patterns": {}, "efficiency_trends": []}

    def save_patterns(self):
        (TRAINER_DIR / "patterns.json").write_text(json.dumps(self.patterns, indent=2))

    def train_from_lessons(self, lessons_file):
        """Learn from accumulated lessons."""
        if not lessons_file.exists():
            return

        with open(lessons_file) as f:
            for line in f:
                try:
                    lesson = json.loads(line.strip())
                    error_type = lesson.get("error_type", "unknown")
                    fix = lesson.get("fix_applied", "unknown")

                    if error_type not in self.patterns["error_fixes"]:
                        self.patterns["error_fixes"][error_type] = {}
                    if fix not in self.patterns["error_fixes"][error_type]:
                        self.patterns["error_fixes"][error_type][fix] = 0

                    self.patterns["error_fixes"][error_type][fix] += 1
                except:
                    pass

        self.save_patterns()
        print(f"  🧠 Trained on lessons: {sum(len(v) for v in self.patterns['error_fixes'].values())} patterns")

    def train_from_coin_efficiency(self, coin_entries):
        """Learn what inputs produce the highest coin efficiency."""
        for entry in coin_entries[-20:]:
            self.patterns["efficiency_trends"].append({
                "efficiency": entry["efficiency"],
                "participants": entry["participants"],
                "coin": entry["coin_minted"]
            })

        self.patterns["efficiency_trends"] = self.patterns["efficiency_trends"][-100:]
        self.save_patterns()

    def train_from_snapshots(self, master_snapshot):
        """Extract synergy patterns from compiled snapshots."""
        if not master_snapshot.exists():
            return

        with open(master_snapshot) as f:
            for line in f:
                try:
                    snap = json.loads(line.strip())
                    label = snap.get("label", "unknown")

                    if label not in self.patterns["synergy_patterns"]:
                        self.patterns["synergy_patterns"][label] = 0
                    self.patterns["synergy_patterns"][label] += 1
                except:
                    pass

        self.save_patterns()
        print(f"  🧠 Trained on snapshots: {len(self.patterns['synergy_patterns'])} labels")

    def get_best_practice(self, error_type):
        """Return the most effective fix for a given error type."""
        fixes = self.patterns["error_fixes"].get(error_type, {})
        if not fixes:
            return None
        return max(fixes, key=fixes.get)

    def compile_training_corpus(self):
        """Compile all training data into a single corpus file."""
        corpus_file = TRAINER_DIR / "training_corpus.json"
        corpus = {
            "compiled_at": datetime.now(timezone.utc).isoformat(),
            "total_error_patterns": sum(len(v) for v in self.patterns["error_fixes"].values()),
            "total_synergy_labels": len(self.patterns["synergy_patterns"]),
            "total_efficiency_records": len(self.patterns["efficiency_trends"]),
            "patterns": self.patterns,
            "best_practices": {
                etype: self.get_best_practice(etype)
                for etype in self.patterns["error_fixes"]
            }
        }
        corpus_file.write_text(json.dumps(corpus, indent=2))
        print(f"  📚 Training corpus compiled: {corpus_file}")
        return corpus


# ── 4. PHYSICS GRAPHS (Vega-Lite data) ──
class PhysicsGraphs:
    """
    Generates data for physics-based visualization:
    - Input joules vs output value over time
    - Efficiency curve
    - Synergy magnitude growth
    - Cooperative multiplier effect
    """

    def generate_graph_data(self, coin_entries):
        """Generate Vega-Lite compatible data for coin efficiency."""
        if not coin_entries:
            return []

        graph_data = []
        for i, entry in enumerate(coin_entries[-20:], 1):
            graph_data.append({
                "cycle": i,
                "input_joules": entry["input_joules"],
                "output_value": entry["output_value"],
                "efficiency": entry["efficiency"],
                "coin_minted": entry["coin_minted"],
                "synergy": entry["synergy_magnitude"],
                "participants": entry["participants"]
            })

        return graph_data

    def save_graph_data(self, data):
        """Save graph data as JSON for external rendering."""
        graph_file = GRAPHS_DIR / "coin_efficiency_graph.json"
        graph_file.write_text(json.dumps(data, indent=2))

        if data:
            multi_data = []
            for d in data:
                multi_data.append({"cycle": d["cycle"], "value": d["efficiency"], "series": "Efficiency"})
                multi_data.append({"cycle": d["cycle"], "value": d["coin_minted"], "series": "Coin Minted"})
                multi_data.append({"cycle": d["cycle"], "value": d["synergy"], "series": "Synergy"})

            vega_spec = {
                "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
                "width": "container",
                "title": {
                    "text": "Coin Efficiency & Synergy Growth",
                    "subtitle": f"Tracking input joules vs output value across {len(data)} cycles"
                },
                "data": {"values": multi_data},
                "mark": {"type": "line", "point": True, "interpolate": "monotone"},
                "encoding": {
                    "x": {"field": "cycle", "type": "ordinal", "title": "Cycle"},
                    "y": {"field": "value", "type": "quantitative", "title": "Magnitude"},
                    "color": {"field": "series", "type": "nominal"}
                }
            }

            (GRAPHS_DIR / "coin_efficiency_vega.json").write_text(json.dumps(vega_spec, indent=2))

        print(f"  📊 Graph data saved: {graph_file}")


# ── 5. SEISMIC OUTPUT SCANNER ──
class SeismicScanner:
    """
    Scans for 'seismic' events: large shifts in system state.
    Detects:
    - Sudden efficiency spikes or drops (>50% change)
    - Error storms (3+ same errors in one cycle)
    - Synergy breakthroughs (cooperative_multiplier > 2.0)
    - Wealth accumulation milestones
    """

    def scan(self, coin_entries, lessons, dossier):
        events = []

        # 1. Efficiency spikes/drops
        if len(coin_entries) >= 2:
            prev = coin_entries[-2]["efficiency"]
            curr = coin_entries[-1]["efficiency"]
            if prev > 0:
                change = abs(curr - prev) / prev
                if change > 0.5:
                    direction = "SPIKE" if curr > prev else "DROP"
                    events.append({
                        "type": f"efficiency_{direction.lower()}",
                        "magnitude": round(change * 100, 1),
                        "detail": f"Efficiency {direction}: {prev:.4f} -> {curr:.4f}",
                        "severity": "warning" if direction == "DROP" else "info"
                    })

        # 2. Error storms
        if lessons:
            recent = lessons[-10:]
            error_types = [l.get("error_type", "unknown") for l in recent]
            counts = Counter(error_types)
            for etype, count in counts.items():
                if count >= 3:
                    events.append({
                        "type": "error_storm",
                        "magnitude": count,
                        "detail": f"{count}x {etype} errors in recent lessons",
                        "severity": "warning"
                    })

        # 3. Synergy breakthroughs
        if coin_entries:
            latest = coin_entries[-1]
            if latest.get("cooperative_multiplier", 0) > 2.0:
                events.append({
                    "type": "synergy_breakthrough",
                    "magnitude": latest["cooperative_multiplier"],
                    "detail": f"Cooperative multiplier exceeded 2.0x: {latest['cooperative_multiplier']}",
                    "severity": "info"
                })

        # 4. Wealth milestones
        total_wealth = sum(e.get("coin_minted", 0) for e in coin_entries)
        milestones = [100, 500, 1000, 5000]
        for m in milestones:
            latest_coin = coin_entries[-1].get("coin_minted", 0) if coin_entries else 0
            if total_wealth >= m and total_wealth - latest_coin < m:
                events.append({
                    "type": "wealth_milestone",
                    "magnitude": m,
                    "detail": f"Total wealth crossed {m} coins!",
                    "severity": "info"
                })

        return events


# ── 6. ATOMIC ORCHESTRATOR ──
def run_atomic_cycle():
    """Run one complete atomic cycle. The simplest order of events."""
    print("\n" + "=" * 55)
    print("⚛️  ATOMIC CORE — CYCLE START")
    print(f"   {datetime.now().isoformat()}")
    print("=" * 55)

    # 1. INGEST & DEDUPLICATE
    print("\n📥 STEP 1: Ingest & Deduplicate")
    dedup = Deduplicator()
    new_count = dedup.ingest_all()
    print(f"   New unique entries: {new_count}")

    # 2. TRAIN
    print("\n🧠 STEP 2: Universal Training")
    trainer = UniversalTrainer()
    trainer.train_from_lessons(UNE_ROOT / "logs" / "full_mesh_lessons.jsonl")
    trainer.train_from_lessons(UNE_ROOT / "logs" / "mesh_lessons.jsonl")
    trainer.train_from_snapshots(MASTER_SNAPSHOT)
    coin = CoinEfficiency()
    trainer.train_from_coin_efficiency(coin.entries)
    corpus = trainer.compile_training_corpus()

    # 3. COIN EFFICIENCY
    print("\n💰 STEP 3: Coin Efficiency Tracking")
    input_joules = 50  # Baseline human effort per cycle

    reports_dir = UNE_ROOT / "reports"
    output_value = 0
    if reports_dir.exists():
        for f in reports_dir.glob("*_report.json"):
            try:
                report = json.loads(f.read_text())
                if report.get("changes_applied"):
                    output_value += 10
            except:
                pass

    latest_cycle = coin.record_cycle(input_joules, max(output_value, 1))
    trend = coin.get_trend()

    # 4. PHYSICS GRAPHS
    print("\n📊 STEP 4: Physics Graphs")
    graphs = PhysicsGraphs()
    graph_data = graphs.generate_graph_data(coin.entries)
    graphs.save_graph_data(graph_data)

    # 5. SEISMIC SCAN
    print("\n🌋 STEP 5: Seismic Scan")
    scanner = SeismicScanner()
    lessons = []
    lessons_file = UNE_ROOT / "logs" / "full_mesh_lessons.jsonl"
    if lessons_file.exists():
        with open(lessons_file) as f:
            for line in f:
                try:
                    lessons.append(json.loads(line.strip()))
                except:
                    pass
    seismic_events = scanner.scan(coin.entries, lessons, None)

    if seismic_events:
        for event in seismic_events:
            print(f"   {'⚠️' if event['severity'] == 'warning' else '✨'} {event['detail']}")
    else:
        print("   No seismic events. System stable.")

    # 6. GENERATE DOSSIER
    print("\n📋 STEP 6: Generate Dossier")
    atomic_dossier = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "core_version": "1.0.0",
        "dedup_stats": {
            "total_unique_entries": len(dedup.hashes),
            "new_this_cycle": new_count,
            "master_file": str(MASTER_SNAPSHOT)
        },
        "coin_efficiency": {
            "latest": latest_cycle,
            "trend": trend
        },
        "training_stats": {
            "total_error_patterns": corpus["total_error_patterns"],
            "total_synergy_labels": corpus["total_synergy_labels"],
            "total_efficiency_records": corpus["total_efficiency_records"],
            "best_practices": corpus["best_practices"]
        },
        "seismic_events": seismic_events,
        "graph_data": graph_data
    }

    dossier_path = UNE_ROOT / "auto_dossier.json"
    dossier_path.write_text(json.dumps(atomic_dossier, indent=2))

    # Save Markor txt
    markor_txt = format_markor_dossier(atomic_dossier, coin, trainer)
    markor_path = MARKOR_DIR / "auto_dossier.txt"
    markor_path.write_text(markor_txt)

    print(f"   📄 Dossier: {dossier_path}")
    print(f"   📝 Markor: {markor_path}")
    print(f"   📊 Master: {MASTER_SNAPSHOT}")
    print(f"   📚 Corpus: {TRAINER_DIR / 'training_corpus.json'}")

    # 7. PRINT EFFICIENCY TABLE
    print("\n" + "=" * 55)
    print("💰 COIN EFFICIENCY SUMMARY")
    print("=" * 55)
    print(f"  Trend: {trend['trend']}")
    print(f"  Avg Efficiency: {trend['avg_efficiency']}")
    print(f"  Avg Coin/Cycle: {trend['avg_coin']}")
    print(f"  Total Coin (last {trend['cycles']}): {trend['total_coin']}")
    print(f"  Total Synergy (last {trend['cycles']}): {trend['total_synergy']}")
    print("=" * 55)

    return atomic_dossier


def format_markor_dossier(dossier, coin, trainer):
    """Format the dossier as human-readable text for Markor."""
    lines = []
    lines.append("=" * 55)
    lines.append("⚛️  ATOMIC CORE — AUTO DOSSIER")
    lines.append(f"Generated: {dossier['generated_at']}")
    lines.append(f"Core: {dossier['core_version']}")
    lines.append("=" * 55)
    lines.append("")

    # Coin Efficiency
    ce = dossier["coin_efficiency"]
    latest = ce["latest"]
    trend = ce["trend"]
    lines.append("💰 COIN EFFICIENCY")
    lines.append(f"  Input Joules: {latest['input_joules']}")
    lines.append(f"  Output Value: {latest['output_value']}")
    lines.append(f"  Efficiency: {latest['efficiency']}")
    lines.append(f"  Cooperative Multiplier: {latest['cooperative_multiplier']}x")
    lines.append(f"  Coin Minted: {latest['coin_minted']}")
    lines.append(f"  Synergy Magnitude: {latest['synergy_magnitude']}")
    lines.append(f"  Trend: {trend['trend']}")
    lines.append(f"  Avg Efficiency: {trend['avg_efficiency']}")
    lines.append(f"  Total Coin (last {trend['cycles']}c): {trend['total_coin']}")
    lines.append("")

    # Dedup Stats
    ds = dossier["dedup_stats"]
    lines.append("📥 DEDUPLICATION")
    lines.append(f"  Total Unique Entries: {ds['total_unique_entries']}")
    lines.append(f"  New This Cycle: {ds['new_this_cycle']}")
    lines.append(f"  Master File: {ds['master_file']}")
    lines.append("")

    # Training Stats
    ts = dossier["training_stats"]
    lines.append("🧠 UNIVERSAL TRAINER")
    lines.append(f"  Error Patterns: {ts['total_error_patterns']}")
    lines.append(f"  Synergy Labels: {ts['total_synergy_labels']}")
    lines.append(f"  Efficiency Records: {ts['total_efficiency_records']}")
    lines.append("")
    lines.append("  Best Practices (Learned Fixes):")
    for error_type, fix in ts["best_practices"].items():
        lines.append(f"    • {error_type} -> {fix}")
    lines.append("")

    # Seismic Events
    events = dossier.get("seismic_events", [])
    lines.append("🌋 SEISMIC EVENTS")
    if events:
        for event in events:
            icon = "⚠️" if "drop" in event["type"] or "storm" in event["type"] else "✨"
            lines.append(f"  {icon} {event['detail']}")
    else:
        lines.append("  No seismic events. System stable.")
    lines.append("")

    # Recent Coin History (last 5)
    lines.append("📈 RECENT COIN HISTORY (Last 5 Cycles)")
    for entry in coin.entries[-5:]:
        lines.append(f"  {entry['cycle']}: eff={entry['efficiency']} coin={entry['coin_minted']} syn={entry['synergy_magnitude']}")
    lines.append("")

    # Graph Data Summary
    gd = dossier.get("graph_data", [])
    lines.append("📊 PHYSICS GRAPH DATA")
    lines.append(f"  Data Points: {len(gd)}")
    if gd:
        latest_gd = gd[-1]
        lines.append(f"  Latest: cycle={latest_gd['cycle']} eff={latest_gd['efficiency']} coin={latest_gd['coin_minted']}")
    lines.append("")

    lines.append("=" * 39)
    lines.append("END OF ATOMIC DOSSIER")
    lines.append("=" * 39)

    return "\n".join(lines)


# ── MAIN ──
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--loop":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300
        print(f"⚛️  Atomic Core running in loop mode (every {interval}s)")
        while True:
            run_atomic_cycle()
            print(f"\n🛌 Sleeping {interval}s...")
            time.sleep(interval)
    else:
        run_atomic_cycle()


if __name__ == "__main__":
    main()
