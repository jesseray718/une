"""
UNE Foundation Calculator.
Atomic physical loops — joules, m³, hours, person-hours only.
"""

from typing import Dict


def labor_intensity(person_hours: float, volume_m3: float) -> float:
    """person-hours per m³"""
    if volume_m3 <= 0:
        return float("inf")
    return person_hours / volume_m3


def efficiency_ratio(intensity_a: float, intensity_b: float) -> float:
    """How many times more labor-efficient is B than A"""
    if intensity_b <= 0:
        return float("inf")
    return intensity_a / intensity_b


def time_to_place(volume_m3: float, rate_m3_per_hour: float) -> float:
    """Hours required to place given volume at constant rate"""
    if rate_m3_per_hour <= 0:
        return float("inf")
    return volume_m3 / rate_m3_per_hour


def person_hours(people: float, hours: float) -> float:
    return people * hours


def compare_systems(
    name_a: str, people_a: float, hours_a: float, volume_a: float,
    name_b: str, people_b: float, hours_b: float, volume_b: float
) -> Dict:
    """Full comparison loop of two placement systems."""
    ph_a = person_hours(people_a, hours_a)
    ph_b = person_hours(people_b, hours_b)
    inten_a = labor_intensity(ph_a, volume_a)
    inten_b = labor_intensity(ph_b, volume_b)
    return {
        "system_a": {
            "name": name_a,
            "person_hours": ph_a,
            "volume_m3": volume_a,
            "labor_intensity": inten_a,
            "hourly_rate": volume_a / hours_a if hours_a > 0 else 0,
        },
        "system_b": {
            "name": name_b,
            "person_hours": ph_b,
            "volume_m3": volume_b,
            "labor_intensity": inten_b,
            "hourly_rate": volume_b / hours_b if hours_b > 0 else 0,
        },
        "ratio_labor_efficiency_B_vs_A": efficiency_ratio(inten_a, inten_b),
        "ratio_hourly_output_B_vs_A": (volume_b / hours_b) / (volume_a / hours_a) if hours_a > 0 and hours_b > 0 else 0,
    }


def truck_limited_rate(m3_per_truck: float, minutes_per_truck: float) -> float:
    """m³/h limited only by truck unload time"""
    return (60 / minutes_per_truck) * m3_per_truck


print("=== Foundation Calculator loaded ===")
