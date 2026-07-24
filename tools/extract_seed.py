#!/usr/bin/env python3
import json, os
from datetime import datetime
from pathlib import Path

UNE = Path(os.environ.get('HOME', '')) / 'une'
CONTEXT_FILE = UNE / 'context_bridge' / 'context.json'
SENSOR_LOG = UNE / 'logs' / 'sensor_flow.log'
SEED_DIR = UNE / 'seeds'
SEED_DIR.mkdir(exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
seed_file = SEED_DIR / f'session_{timestamp}.json'

context_data = {}
if CONTEXT_FILE.exists():
    with open(CONTEXT_FILE) as f:
        context_data = json.load(f)

sensor_lines = []
if SENSOR_LOG.exists():
    with open(SENSOR_LOG) as f:
        lines = f.readlines()
        sensor_lines = [l.strip() for l in lines[-50:]]

seed = {
    "meta": {
        "type": "openroot_session_seed",
        "created": timestamp,
        "source": "Samsung A15 Termux"
    },
    "context_snapshot": context_data,
    "recent_sensor_log": sensor_lines,
    "session_stats": {
        "total_lessons": len(context_data.get('lessons', [])),
        "confirmed_anchors": len(context_data.get('system_state', {}).get('bitcoin_anchors', {}))
    }
}

with open(seed_file, 'w') as f:
    json.dump(seed, f, indent=2)

print(f"Seed created: {seed_file}")
print(f"  Lessons: {seed['session_stats']['total_lessons']}")
print(f"  Anchors: {seed['session_stats']['confirmed_anchors']}")
