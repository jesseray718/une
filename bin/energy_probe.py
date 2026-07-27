#!/data/data/com.termux/files/usr/bin/python3
"""Energy Probe - Snapshot joules before/after an operation."""
import json, os, sys, time
sys.path.insert(0, "/sdcard/openroot/bin")
from rish_wrapper import get_battery_telemetry

CACHE_PATH = "/data/data/com.termux/files/home/une/storage/joule_cache.json"

def load_cache():
    try:
        with open(CACHE_PATH, "r") as f: return json.load(f)
    except: return {"total_joules": 0.0}

def snapshot():
    """Return current joule count + power reading."""
    telem = get_battery_telemetry()
    cache = load_cache()
    return {
        "joules_at_snapshot": cache.get("total_joules", 0.0),
        "power_w": telem.get("power_watts", 0) if telem else 0,
        "voltage_mV": telem.get("voltage_mV", 0) if telem else 0,
        "current_uA": telem.get("current_uA", 0) if telem else 0,
        "level": telem.get("level", 0) if telem else 0,
        "timestamp": time.time()
    }

def cost(before, after):
    """Calculate joules consumed between two snapshots."""
    delta = after["joules_at_snapshot"] - before["joules_at_snapshot"]
    dt = after["timestamp"] - before["timestamp"]
    return {
        "joules_consumed": round(delta, 6),
        "duration_s": round(dt, 4),
        "avg_power_mW": round((delta / dt * 1000) if dt > 0 else 0, 2),
        "before_level": before.get("level"),
        "after_level": after.get("level")
    }

if __name__ == "__main__":
    # Standalone: snapshot current state
    s = snapshot()
    print(json.dumps(s, indent=2))
