#!/usr/bin/env python3
"""Benchmark: Fractal Swarm vs Monolithic Model on Samsung A15."""
import os, sys, time, json, subprocess, statistics
from datetime import datetime

import os
try:
    from paths import UNE_HOME
except ImportError:
    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))

ARM_SCRIPT = os.path.join(UNE_HOME, "computational_flow/arm_energy.py")
LOG_FILE = os.path.join(UNE_HOME, "computational_flow/logs/benchmark_results.jsonl")

def get_freq():
    try:
        with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq") as f:
            return int(f.read().strip())/1000.0
    except: return 0

def run_test(name, duration, simulate_load=True):
    print(f"\n>>> Running {name}...")
    start = time.time()
    freqs = []
    while time.time() - start < duration:
        if simulate_load:
            # Simulate work (replace with real ollama call later)
            _ = sum(range(10000)) 
        freqs.append(get_freq())
        time.sleep(0.1)
    
    dur = time.time() - start
    avg_f = statistics.mean(freqs) if freqs else 0
    # Simple energy estimate
    energy = 0.5 * ((avg_f/650)**1.5) * dur
    eta = 1.0 / energy if energy > 0 else 0
    
    res = {"test": name, "duration": round(dur,2), "avg_mhz": round(avg_f,1), "energy": round(energy,4), "eta": round(eta,4)}
    print(f"   Done: {dur:.2f}s, {avg_f:.1f}MHz, {energy:.4f}J, Eta={eta:.4f}")
    
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f: f.write(json.dumps(res)+"\n")
    return res

if __name__ == "__main__":
    print("=== AGAPE-UNE BENCHMARK ===")
    run_test("Monolithic_Sim", 2.0)
    run_test("Swarm_Sim", 2.0)
    print("\n>> Results saved to", LOG_FILE)
