#!/usr/bin/env python3
"""Absorb durable memory + current session state into wisdom_corpus.json"""
import json, os, datetime

WISDOM = "/data/data/com.termux/files/home/une/wisdom/wisdom_corpus.json"
os.makedirs(os.path.dirname(WISDOM), exist_ok=True)

entry = {
  "ts": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
  "source": "grok_full_memory_absorb",
  "type": "durable_memory_plus_session",
  "durable_memory": {
    "name": "Jesse McMillen",
    "github": "jesseray718",
    "location": "Saxton / Sikeston area, Missouri",
    "core_projects": ["OpenRoot", "AeroCement", "Agape-UNE", "ACRE PoPW"],
    "key_preferences": [
      "Never use tilde (\~) in commands — always absolute paths or $HOME",
      "One atomic paste-ready command preferred",
      "Joule-native accounting",
      "Open-source, CC-BY-SA docs + GPL-3.0 code, no patents",
      "Local-first AI, Termux + Kai9000 + Alpine"
    ],
    "major_threads": [
      "AeroCement / OpenCell thermal cascade + φ-vortex",
      "Black Locust RMH as parallel draft",
      "Thermodynamic ledger (now SQLite)",
      "η = useful_joules / human_joules",
      "ACRE mints only from measured ledger",
      "Fractal swarm with n_max reliability bound",
      "UNE 3-letter primitives + cooperation axiom (still to be restated)",
      "Context bridge canonical location: /data/data/com.termux/files/home/une/wisdom/wisdom_corpus.json"
    ]
  },
  "this_session_locked": [
    "φ-vortex is master air-flow",
    "Micro-Node geometric targets defined",
    "Black Locust RMH parallel valved integration",
    "Discrete Stirling + flywheel architecture",
    "Zero-energy cooling path specified",
    "SQLite joule-only ledger",
    "Universal absorber now points only at wisdom_corpus.json",
    "Defensive publication + clean open licenses as protection strategy"
  ],
  "pending": [
    "Restate compounding-cooperation equation and Jesus-translation axiom",
    "Lock exact Micro-Node dimensions",
    "Instrument first prototype",
    "Wire ledger → ACRE",
    "Continue feeding every AI delta into wisdom_corpus.json only"
  ]
}

if os.path.exists(WISDOM):
    try:
        with open(WISDOM) as f:
            data = json.load(f)
    except Exception:
        data = {"entries": []}
else:
    data = {"entries": [], "meta": {"canonical": True, "project": "Agape-UNE / OpenRoot"}}

if "entries" not in data:
    data["entries"] = []

data["entries"].append(entry)
data["last_updated"] = entry["ts"]

with open(WISDOM, "w") as f:
    json.dump(data, f, indent=2)

print("Full durable memory + session state absorbed into:")
print(WISDOM)
print("Total entries:", len(data["entries"]))
