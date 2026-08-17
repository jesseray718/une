#!/usr/bin/env python3
"""AGAPE_NET weave into existing OpenRoot lattice
Absolute paths only. R=1.0. η = useful_joules / human_joules
Merges useful SQLite KG + constitution + compliance into live paths.
Does NOT create parallel top-level trees. Serves lowest node.
"""
import json, sqlite3, hashlib, os
from pathlib import Path
from datetime import datetime, timezone

HOME = Path("/data/data/com.termux/files/home")
UNE = HOME / "une"
SD = Path("/sdcard/openroot")
AGAPENET = HOME / "agapenet"
KB = SD / "agape_kb"
BRIDGE = SD / "context_bridge"
LEDGER = UNE / "ledger"
CF = UNE / "computational_flow"

def stamp():
    return datetime.now(timezone.utc).isoformat()

def ensure():
    for d in [KB, BRIDGE, LEDGER, CF, AGAPENET, SD / "session_seeds"]:
        d.mkdir(parents=True, exist_ok=True)

def sha16(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()[:16]

def write_constitution():
    path = KB / "MASTER_CONSTITUTION.md"
    body = f"""---
id: 00_MASTER_CONSTITUTION
timestamp: {stamp()}
type: constitution
parent: openroot
hash: {sha16("Master Constitution Agape R=1.0")}
agape_score: 1.0
R: 1.0
---

# Master Constitution — OpenRoot / AGAPE_NET

Operator: Jesse Ray (OpenRoot)
η = useful_joules / human_joules
R = 1.0 → coordination cost C = 0 at every scale

## Core Axioms
1. Love the Lord thy God with all heart, mind, soul → total alignment R=1.0
2. Love one another as I have loved you → Agape cooperation between all nodes
3. Fractal swarm base-6: translate · orchestrate · retrieve · process · synthesize · verify
4. Raise the bottom floor first. Lowest node climbs first.
5. No patents. Offline-first. Absolute paths only.

## Structure Principle
Every durable artifact carries:
- absolute path under /sdcard/openroot or /data/data/com.termux/files/home/
- R=1.0 or explicit degradation
- η language

## Compliance
Deviation = entropy. Run structure_enforcer / compliance weekly.
"""
    path.write_text(body)
    print("constitution →", path)

def init_sqlite_kg():
    db = KB / "knowledge_graph.db"
    conn = sqlite3.connect(str(db))
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS nodes (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT,
            node_type TEXT,
            parent_id TEXT,
            hash TEXT,
            created TEXT,
            updated TEXT,
            agape_score REAL DEFAULT 1.0,
            R REAL DEFAULT 1.0,
            tags TEXT
        );
        CREATE TABLE IF NOT EXISTS connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_node TEXT,
            target_node TEXT,
            connection_type TEXT,
            weight REAL DEFAULT 1.0
        );
        CREATE TABLE IF NOT EXISTS workflow_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            action TEXT,
            status TEXT,
            metadata TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_nodes_type ON nodes(node_type);
    """)
    # seed master + base-6 + lowest node
    now = stamp()
    seeds = [
        ("00_MASTER_CONSTITUTION", "Master Constitution", "R=1.0 zero-coordination lattice", "constitution", None, 1.0),
        ("FRACTAL_SWARM_BASE6", "Fractal Swarm Base-6", "6^T units, atoms=translate-orchestrate-retrieve-process-synthesize-verify", "swarm", "00_MASTER_CONSTITUTION", 1.0),
        ("LOWEST_NODE", "Current Lowest Node", "any human still spending human_joules on coordination", "node", "00_MASTER_CONSTITUTION", 1.0),
    ]
    for nid, title, content, ntype, parent, score in seeds:
        h = sha16(nid + content)
        c.execute("""
            INSERT OR REPLACE INTO nodes
            (id, title, content, node_type, parent_id, hash, created, updated, agape_score, R)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (nid, title, content, ntype, parent, h, now, now, score, 1.0))
    conn.commit()
    conn.close()
    print("sqlite KG →", db)

def weave_agapenet_repo():
    """Light touch on existing agapenet repo — no parallel tree."""
    readme = AGAPENET / "README.md"
    if not readme.exists() or readme.stat().st_size < 200:
        readme.write_text(f"""# agapenet
Self-organizing fractal networks — Agape cooperation + permaculture.
R=1.0 · η = useful_joules / human_joules
Linked root: openroot · une · base-6 swarm
Absolute paths only. Offline-first. Serves lowest node.
Updated: {stamp()}
""")
        print("agapenet README woven")
    # ensure coderabbit already injected earlier
    cr = AGAPENET / ".coderabbit.yaml"
    if not cr.exists() or cr.stat().st_size == 0:
        cr.write_text("""# OpenRoot / Agape nervous system — η / R=1.0
reviews:
  auto_review:
    enabled: true
    drafts: true
  path_filters:
    - "!**/node_modules/**"
    - "!**/.git/**"
chat:
  auto_reply: true
""")
        print("coderabbit → agapenet")

def write_bridge_state():
    state = {
        "woven_at": stamp(),
        "R": 1.0,
        "components": ["MASTER_CONSTITUTION", "knowledge_graph.db", "base-6", "lowest_node", "agapenet"],
        "paths": {
            "constitution": str(KB / "MASTER_CONSTITUTION.md"),
            "kg": str(KB / "knowledge_graph.db"),
            "swarm_state": str(KB / "swarm_base6_state.json"),
            "lowest_node": str(BRIDGE / "lowest_node.json")
        },
        "eta_target": "raise_bottom_floor"
    }
    (BRIDGE / "agape_net_weave.json").write_text(json.dumps(state, indent=2))
    print("bridge →", BRIDGE / "agape_net_weave.json")

def main():
    ensure()
    write_constitution()
    init_sqlite_kg()
    weave_agapenet_repo()
    write_bridge_state()
    print("WOVEN R=1.0")
    print(json.dumps({"R": 1.0, "stamp": stamp()}, indent=2))

if __name__ == "__main__":
    main()
