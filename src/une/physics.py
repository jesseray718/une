from .une_atomic_library import unified_effective_power, unified_power_acceleration, cooperation_efficiency

def evaluate_full_system(raw_energy_joules, time_seconds, N=50, epochs=5):
    power = unified_effective_power(raw_energy_joules, time_seconds, N)
    accel = unified_power_acceleration(raw_energy_joules, time_seconds, N, epochs=epochs)
    base = raw_energy_joules / time_seconds
    bottleneck = max(0, 1 - (power / (base * 3)))
    return {
        "effective_power_watts": round(power, 2),
        "acceleration_watts_per_sec2": round(accel, 4),
        "bottleneck_score": round(bottleneck, 3),
        "recommendation": "Increase cooperation or apply fractal recursion" if bottleneck > 0.35 else "System looks efficient"
    }
