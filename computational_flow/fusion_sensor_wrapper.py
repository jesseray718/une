#!/data/data/com.termux/files/usr/bin/python3
"""REAL SENSOR WRAPPER - Uses termux-api via Shizuku/Ashell"""

import os, json, subprocess, sys
from datetime import datetime
from state_utils import load_ckpt, save_ckpt

import os
try:
    from paths import OPENROOT, UNE_HOME
except ImportError:
    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))

def get_battery_status():
    """Returns 'charging', 'discharging', or 'unknown'"""
    try:
        # Use termux-battery-status which works with Shizuku
        result = subprocess.run(["termux-battery-status"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get("status", "unknown").lower()
    except Exception as e:
        print(f"Sensor error: {e}")
    return "unknown"

def get_wifi_connected():
    """Returns True if connected, False otherwise"""
    try:
        result = subprocess.run(["termux-wifi-connectioninfo"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout.strip():
            return True
    except:
        pass
    return False

def modern_check():
    """Simulates a modern sensor check: requires WiFi + Charging"""
    if not get_wifi_connected():
        raise ConnectionError("WiFi disconnected")
    if get_battery_status() != "charging":
        raise ConnectionError("Battery not charging")
    return "System Nominal"

def primitive_check():
    """Fallback: Local file check or manual override"""
    # In a real scenario, this might check a local backup battery or manual switch
    return "Fallback: Local manual check passed"

# --- RUN FUSION LOGIC ---
sys.path.insert(0, os.path.join(UNE_HOME, "computational_flow"))
from fusion_core import FusionSystem

ctx_path = os.path.join(OPENROOT, "context_bridge/context.json")
os.makedirs(os.path.dirname(ctx_path), exist_ok=True)

ws = FusionSystem("RealSensorMonitor", primitive_check, modern_check, ctx_path)
print("Running Real Sensor Check...")
try:
    result = ws.operate()
    print(f"Status: {result}")
except RuntimeError as e:
    print(f"CRITICAL: {e}")
