#!/data/data/com.termux/files/usr/bin/python3
"""
Aerodynamic Harvesting Passive ΔT Vehicle
Micro-Node thermodynamic model — energy-conserving
η = useful_joules / human_joules
"""
import math
import json

# Locked Micro-Node
APERTURE_M2     = 12.0
CHIMNEY_H       = 16.5
CHIMNEY_AREA    = 0.8          # m² throat
LABYRINTH_M3    = 7.0
HOT_TANK_M3     = 2.0
COLD_TANK_M3    = 2.75
RAD_LID_M2      = 6.5

# Physics
RHO_AIR   = 1.2
CP_AIR    = 1005
G         = 9.81
SOLAR     = 931.0              # W/m² Saxton reference
OPTICAL   = 0.82               # volumetric + glazing
THERMAL   = 0.78               # collection efficiency
SYSTEM_ETA = 0.55              # overall to useful work / storage

def max_collectable_W():
    return APERTURE_M2 * SOLAR * OPTICAL * THERMAL

def stack_velocity(delta_t, height=CHIMNEY_H):
    t_avg = 293 + delta_t / 2
    return math.sqrt(2 * G * height * delta_t / t_avg)

def mass_flow(v, area=CHIMNEY_AREA):
    return RHO_AIR * area * v

def model(delta_t=25.0):
    q_in = max_collectable_W()
    v = stack_velocity(delta_t)
    m = mass_flow(v)

    # Power limited by actual heat input, not pure stack formula
    q_useful = q_in * SYSTEM_ETA
    daily_kwh = q_useful * 6.5 / 1000

    return {
        "name": "aerodynamic_harvesting_passive_dt_vehicle",
        "delta_t_K": delta_t,
        "stack_velocity_m_s": round(v, 3),
        "mass_flow_kg_s": round(m, 3),
        "max_collectable_W": round(q_in, 1),
        "useful_power_W": round(q_useful, 1),
        "daily_kWh": round(daily_kwh, 2),
        "aperture_m2": APERTURE_M2,
        "chimney_m": CHIMNEY_H,
        "system_eta": SYSTEM_ETA
    }

if __name__ == "__main__":
    print(json.dumps(model(25.0), indent=2))
    print("---")
    print(json.dumps(model(35.0), indent=2))
