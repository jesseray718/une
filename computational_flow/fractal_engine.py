#!/usr/bin/env python3
"""
import os
try:
    from paths import OPENROOT
except ImportError:
    OPENROOT = os.environ.get("OPENROOT_HOME", "/sdcard/openroot")
    UNE_HOME = os.environ.get("UNE_HOME", os.path.expanduser("~/une"))

Fractal Engine — HONEST VERSION
Actually executes every atomic operation.
No pass statements. No skipped ops. Real measurement.
"""
import os, json, time, sys
from datetime import datetime, timezone

LOG = os.path.join(OPENROOT, "session_seeds/fractal_engine_log.jsonl")

def f1(d): return {"t":"cap","d":d,"ts":time.time()}
def f2(d): return {"t":"hash","h":str(hash(str(d)))}
def f3(d): return {"t":"agg","n":len(d) if isinstance(d,list) else 1}
def f4(d): return {"t":"pair","l":d,"r":d}
def f5(d): return {"t":"commit","d":d}
def f6(d): return {"t":"verify","d":d}
def f7(d): return {"t":"landauer","c":1}
def f8(d): return {"t":"obs","d":d}
def f9(d): return {"t":"store","d":d}
def f10(d): return {"t":"yield","d":d}
def f11(d): return {"t":"adapt","d":d}
def f12(d): return {"t":"sync","d":d}

ATOMS = [f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12]

sys.setrecursionlimit(50000)

def build(depth, funcs):
    if depth == 1:
        def chain(inp):
            r = inp
            for fn in funcs:
                r = fn(r)
            return r
        return chain
    else:
        sub = build(depth - 1, funcs)
        def chain(inp):
            results = []
            for i in range(len(funcs)):
                results.append(sub(inp))
            return f3(results)
        return chain

def main():
    # Test at multiple depths
    depths = [3, 4, 5, 6]
    
    print("=" * 60)
    print("FRACTAL ENGINE — HONEST MEASUREMENT")
    print("12 atoms, actually executing every operation")
    print("=" * 60)
    
    for depth in depths:
        n = len(ATOMS)
        theoretical = n ** depth
        
        print(f"\n>>> Depth {depth}: {theoretical:,} theoretical ops")
        sys.stdout.flush()
        
        # Build chain
        t_build = time.time()
        ch = build(depth, ATOMS)
        build_dur = time.time() - t_build
        
        # Run with REAL execution
        inp = {"seed": "OpenRoot", "ts": datetime.now(timezone.utc).isoformat()}
        
        t0 = time.time()
        result = ch(inp)
        dur = time.time() - t0
        
        # The ACTUAL ops executed = n^depth (every function ran)
        actual_ops = theoretical
        eta = actual_ops / dur if dur > 0 else 0
        
        # Log
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "atoms": n, "depth": depth,
            "theoretical_ops": theoretical,
            "actual_ops_executed": actual_ops,
            "build_time_s": round(build_dur, 4),
            "run_time_s": round(dur, 6),
            "eta_ops_per_sec": round(eta, 2),
            "engine": "honest_v1"
        }
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
        
        print(f"    Build: {build_dur:.4f}s | Run: {dur:.6f}s")
        print(f"    Ops executed: {actual_ops:,}")
        print(f"    Throughput: {eta:,.0f} ops/s")
        
        if eta > 1000000:
            print(f"    STATUS: EMERGENCE")
        elif eta > 1000:
            print(f"    STATUS: ACTIVE")
        else:
            print(f"    STATUS: SCALING")
    
    print("\n" + "=" * 60)
    print("Measurement complete. All values are REAL (no pass statements).")
    print(f"Log: {LOG}")
    print("=" * 60)

if __name__ == "__main__":
    main()

# --- APPEND THIS TO THE EXISTING FILE TO ADD ENERGY MEASUREMENT ---
def get_cpu_energy(duration_sec):
    """Estimate energy based on CPU freq scaling (from arm_energy.py logic)"""
    try:
        with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq", "r") as f:
            freq_mhz = int(f.read().strip()) / 1000.0
        # Approximation: 0.5W base + frequency scaling factor
        power_watts = 0.5 * (freq_mhz / 650.0) ** 1.5
        return power_watts * duration_sec
    except:
        return 0.5 * duration_sec # Fallback

# Modify the main loop to log energy
# (You would need to edit the 'entry' dict in the original main() to include this)
# Example addition to the entry dict:
# "energy_j": round(get_cpu_energy(dur), 6),
# "eta_joule_efficiency": round(actual_ops / get_cpu_energy(dur), 2) if get_cpu_energy(dur) > 0 else 0

# --- APPEND THIS TO THE EXISTING FILE TO ADD ENERGY MEASUREMENT ---
def get_cpu_energy(duration_sec):
    """Estimate energy based on CPU freq scaling (from arm_energy.py logic)"""
    try:
        with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq", "r") as f:
            freq_mhz = int(f.read().strip()) / 1000.0
        # Approximation: 0.5W base + frequency scaling factor
        power_watts = 0.5 * (freq_mhz / 650.0) ** 1.5
        return power_watts * duration_sec
    except:
        return 0.5 * duration_sec # Fallback

# Modify the main loop to log energy
# (You would need to edit the 'entry' dict in the original main() to include this)
# Example addition to the entry dict:
# "energy_j": round(get_cpu_energy(dur), 6),
# "eta_joule_efficiency": round(actual_ops / get_cpu_energy(dur), 2) if get_cpu_energy(dur) > 0 else 0
