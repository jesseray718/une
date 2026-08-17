#!/usr/bin/env python3
"""state_utils — absolute-path checkpoint + merkle for Agape swarm
η = useful_joules / human_joules
Never tilde. Offline-first. Serves lowest node.
"""
import json
import os
import hashlib
from pathlib import Path
from datetime import datetime, timezone

UNE = Path("/data/data/com.termux/files/home/une")
SD = Path("/sdcard/openroot")
_CKPT_PATH = UNE / "state_checkpoint.json"
_ALT_CKPT = SD / "context_bridge" / "state_checkpoint.json"

def load_ckpt(path=None):
    p = Path(path) if path else _CKPT_PATH
    if not p.exists():
        p = _ALT_CKPT
    if not p.exists():
        return {
            "cycle": 0,
            "fitness_score": 0.0,
            "mesh_nodes": [],
            "energy_joules": 10.0,
            "lessons": [],
            "merkle_root": None,
            "health_score": 1.0,
            "R": 1.0,
            "ts": datetime.now(timezone.utc).isoformat()
        }
    try:
        return json.loads(p.read_text())
    except Exception:
        return {
            "cycle": 0,
            "fitness_score": 0.0,
            "mesh_nodes": [],
            "energy_joules": 10.0,
            "lessons": [],
            "merkle_root": None,
            "health_score": 1.0,
            "R": 1.0
        }

def save_ckpt(data, path=None):
    p = Path(path) if path else _CKPT_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    data = dict(data)
    data["ts"] = datetime.now(timezone.utc).isoformat()
    data.setdefault("R", 1.0)
    p.write_text(json.dumps(data, indent=2, default=str))
    # mirror to sdcard bridge
    try:
        _ALT_CKPT.parent.mkdir(parents=True, exist_ok=True)
        _ALT_CKPT.write_text(p.read_text())
    except Exception:
        pass

def calc_merkle(items):
    if not items:
        return hashlib.sha256(b"empty").hexdigest()
    hashes = [hashlib.sha256(str(i).encode()).hexdigest() for i in items]
    while len(hashes) > 1:
        nxt = []
        for i in range(0, len(hashes) - 1, 2):
            nxt.append(hashlib.sha256((hashes[i] + hashes[i + 1]).encode()).hexdigest())
        if len(hashes) % 2:
            nxt.append(hashlib.sha256(hashes[-1].encode()).hexdigest())
        hashes = nxt
    return hashes[0]
