#!/usr/bin/env python3
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ZERO_HASH = "0" * 64

def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))

def block_hash(payload):
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()

class NewtonChain:
    def __init__(self, path="data/thermoledger.jsonl"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def latest_hash(self):
        if not self.path.exists():
            return ZERO_HASH
        last = None
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                last = json.loads(line)
        return last["current_hash"] if last else ZERO_HASH

    def append(self, joules_generated, average_power_w, telemetry_payload):
        payload = {
            "previous_hash": self.latest_hash(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "joules_generated": float(joules_generated),
            "average_power_w": float(average_power_w),
            "telemetry_payload": telemetry_payload,
        }
        record = dict(payload)
        record["current_hash"] = block_hash(payload)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(canonical_json(record) + "\n")
        return record
