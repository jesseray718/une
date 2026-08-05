#!/data/data/com.termux/files/usr/bin/python3
import json, os, sys, time, signal
from datetime import datetime, timezone

import os
try:
    from paths import OPENROOT, UNE_HOME
except ImportError:
    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))

BIN_DIR = os.path.join(OPENROOT, "bin")
LOG_FILE = os.path.join(UNE_HOME, "logs/energy/stream.jsonl")
CACHE_FILE = os.path.join(UNE_HOME, "storage/joule_cache.json")
CONTEXT_FILE = os.path.join(UNE_HOME, "context_bridge/context.json")

sys.path.insert(0, BIN_DIR)
from rish_wrapper import get_battery_telemetry

def ensure_dirs():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    os.makedirs(os.path.dirname(CONTEXT_FILE), exist_ok=True)

def append_log(entry):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
        f.flush()
        os.fsync(f.fileno())

def load_cache():
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"total_joules": 0.0, "last_sample_time": 0, "start_time": None}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)
        f.flush()
        os.fsync(f.fileno())

def save_context_summary(session_data):
    ensure_dirs()
    try:
        if os.path.exists(CONTEXT_FILE):
            with open(CONTEXT_FILE, "r") as f:
                context = json.load(f)
        else:
            context = {"sessions": []}
        if not isinstance(context, dict): context = {"sessions": []}
        if "sessions" not in context: context["sessions"] = []
        context["sessions"].append(session_data)
        if len(context["sessions"]) > 10: context["sessions"] = context["sessions"][-10:]
        with open(CONTEXT_FILE, "w") as f:
            json.dump(context, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        print(f"\n[INFO] Session summary saved to {CONTEXT_FILE}")
    except Exception as e:
        print(f"\n[ERROR] Failed to save context: {e}")

def handle_stop(signum, frame):
    global running
    running = False
    print("\n[STOP] Shutting down logger...")

def main():
    global running
    running = True
    signal.signal(signal.SIGINT, handle_stop)
    signal.signal(signal.SIGTERM, handle_stop)

    cache = load_cache()
    sample_interval = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
    session_start = time.time()
    cache["start_time"] = session_start

    print(f"[INFO] OpenRoot Energy Logger started. Interval: {sample_interval}s")
    print(f"[INFO] Target: {LOG_FILE}")
    print(f"[INFO] Context Bridge: Enabled")

    while running:
        start = time.time()
        telem = get_battery_telemetry()

        if not telem or "error" in telem:
            append_log({"type": "error", "msg": str(telem)})
            time.sleep(sample_interval)
            continue

        last_t = cache.get("last_sample_time", start)
        dt = start - last_t
        power_w = telem.get("power_watts", 0.0)
        delta_joules = power_w * dt

        cache["total_joules"] += delta_joules
        cache["last_sample_time"] = start

        entry = {
            "type": "sample",
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "power_w": power_w,
            "delta_joules": delta_joules,
            "cumulative_joules": cache["total_joules"],
            "raw": {
                "current_uA": telem.get("current_uA"),
                "voltage_mV": telem.get("voltage_mV"),
                "level": telem.get("level"),
                "temp_dC": telem.get("temp_dC")
            }
        }

        append_log(entry)
        save_cache(cache)
        print(f"[J] {cache['total_joules']:.4f} J | P: {power_w*1000:.2f} mW | Lvl: {telem.get('level')}%", flush=True)

        elapsed = time.time() - start
        if elapsed < sample_interval:
            time.sleep(sample_interval - elapsed)

    end_time = time.time()
    duration_sec = end_time - session_start
    avg_power_w = cache["total_joules"] / duration_sec if duration_sec > 0 else 0

    session_summary = {
        "timestamp_end": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "duration_seconds": round(duration_sec, 2),
        "total_joules": round(cache["total_joules"], 4),
        "avg_power_mW": round(avg_power_w * 1000, 2),
        "end_level": telem.get("level", "N/A"),
        "notes": "Auto-generated via Context Bridge"
    }

    save_context_summary(session_summary)
    print(f"[DONE] Session ended. Total: {session_summary['total_joules']} J over {session_summary['duration_seconds']}s.")

if __name__ == "__main__":
    main()
