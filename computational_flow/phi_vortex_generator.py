#!/data/data/com.termux/files/usr/bin/python3
"""
Optimum φ-vortex panel generator
Produces geometry + performance for any aperture size
Rooted on locked Micro-Node + immortal context
"""
import math
import json
import sys

PHI  = (1 + math.sqrt(5)) / 2
PHI2 = PHI ** 2

def generate(aperture_m2=12.0, stages=3):
    chimney_h = 16.5 * (aperture_m2 / 12.0)**0.5          # scale with sqrt(area)
    chimney_d = chimney_h / PHI2
    throat    = 0.8 * (aperture_m2 / 12.0)

    # Cascade volumes scale with aperture
    scale = aperture_m2 / 12.0
    labyrinth = 7.0 * scale
    hot       = 2.0 * scale
    cold      = 2.75 * scale
    lid       = 6.5 * scale

    # Performance from locked model (scaled)
    base_daily = 25.55
    daily_kwh  = base_daily * scale

    return {
        "aperture_m2": round(aperture_m2, 2),
        "chimney_height_m": round(chimney_h, 2),
        "chimney_diameter_m": round(chimney_d, 3),
        "throat_area_m2": round(throat, 3),
        "H_over_D": round(PHI2, 4),
        "cascade_stages": stages,
        "labyrinth_m3": round(labyrinth, 2),
        "hot_tank_m3": round(hot, 2),
        "cold_tank_m3": round(cold, 2),
        "radiative_lid_m2": round(lid, 2),
        "estimated_daily_kWh": round(daily_kwh, 2),
        "phi": round(PHI, 6)
    }

if __name__ == "__main__":
    sizes = [6.0, 12.0, 24.0, 48.0] if len(sys.argv) == 1 else [float(x) for x in sys.argv[1:]]
    for a in sizes:
        print(json.dumps(generate(a), indent=2))
        print("---")
