#!/usr/bin/env python3
"""
AGAPE GEOMETRIC CONCRETE CALCULATOR
====================================
Calculates the theoretical strength and flow properties of 
Aero-GFRC based on the "13-Sphere Close Packing" hypothesis.

Hypothesis:
  1. Micro-voids form a Face-Centered Cubic (FCC) lattice (13-sphere clusters).
  2. Zirconium-Glass fibers bind the lattice, creating a continuous truss.
  3. Flow is lubricated by the rolling voids (ball bearing effect).
  
Formulas:
  - Packing Density (FCC): ~0.7405
  - Strength Multiplier: Proportional to Fiber Surface Area / Void Volume
  - Flow Reduction: Inverse of Void Radius (smaller = smoother)
"""
from __future__ import annotations
import math
from dataclasses import dataclass

# Constants
PI = math.pi
DENSITY_WATER = 1000.0  # kg/m^3
DENSITY_ZIRCONIUM = 6000.0  # kg/m^3 approx
FIBER_DENSITY = 2500.0  # kg/m^3

@dataclass
class SphereCluster:
    """Represents a 13-sphere FCC cluster."""
    radius: float  # meters
    count: int = 13
    
    @property
    def volume(self) -> float:
        # Volume of 13 spheres
        return 13 * (4/3) * PI * (self.radius ** 3)
    
    @property
    def surface_area(self) -> float:
        # Surface area of 13 spheres (bonding area for fibers)
        return 13 * 4 * PI * (self.radius ** 2)
    
    @property
    def packing_efficiency(self) -> float:
        # FCC packing efficiency is ~74%
        return 0.7405

class AeroGFRCModel:
    def __init__(self, void_radius_um: float, fiber_volume_pct: float, zirconium_pct: float):
        """
        void_radius_um: Radius of micro-voids in micrometers.
        fiber_volume_pct: Percentage of volume occupied by fibers.
        zirconium_pct: Percentage of fiber mass that is Zirconium.
        """
        self.r = void_radius_um * 1e-6  # convert to meters
        self.fiber_vol = fiber_volume_pct / 100.0
        self.zr_mass_frac = zirconium_pct / 100.0
        
        # Create a representative cluster
        self.cluster = SphereCluster(radius=self.r)
        
    def calculate_properties(self) -> dict:
        # 1. Number of clusters per cubic meter
        # Assuming 20% void volume fraction for optimal flow/strength balance
        void_vol_frac = 0.20 
        num_clusters = void_vol_frac / self.cluster.volume
        
        # 2. Total Fiber Surface Area available for bonding
        # Fibers coat the spheres. More surface area = stronger bond.
        total_surface_area = num_clusters * self.cluster.surface_area
        
        # 3. Theoretical Strength Multiplier
        # Strength scales with Surface Area / Volume (Interface density)
        # Compare to standard concrete (random voids, low surface area)
        std_surface_area = 1000.0 # Arbitrary baseline
        strength_mult = total_surface_area / std_surface_area
        
        # 4. Flow Reduction (Ball Bearing Effect)
        # Smaller radius = more rolling points = less friction
        # Friction reduction factor ~ 1 / r
        flow_reduction = 1.0 / (self.r * 1e6) # Normalize
        
        # 5. Density Calculation
        # Concrete density ~ 2400 kg/m3. We subtract void mass, add fiber mass.
        base_density = 2400.0
        void_mass = void_vol_frac * 1.225 # Air density
        fiber_mass = self.fiber_vol * FIBER_DENSITY
        zr_mass = fiber_mass * self.zr_mass_frac
        
        final_density = base_density - (void_vol_frac * base_density) + fiber_mass
        # Note: Simplified. Actual calculation requires porosity models.
        
        return {
            "void_radius_um": self.r * 1e6,
            "clusters_per_m3": int(num_clusters),
            "total_bonding_area_m2": round(total_surface_area, 2),
            "strength_multiplier": round(strength_mult, 2),
            "flow_reduction_factor": round(flow_reduction, 4),
            "estimated_density_kg_m3": round(final_density, 1),
            "zirconium_reinforcement": "High (20% ZrO2)" if self.zr_mass_frac >= 0.2 else "Standard",
            "packing_type": "Face-Centered Cubic (13-sphere cluster)"
        }

def demo():
    print("AGAPE GEOMETRIC CONCRETE: THE 13-SPHERE PROTOCOL")
    print("=" * 60)
    print("Hypothesis: Micro-voids form FCC lattices (13 spheres).")
    print("Result: Ball bearing flow + Truss-like strength.")
    print("-" * 60)
    
    # Scenario A: Large bubbles (Standard foam concrete)
    print("\n[SCENARIO A: LARGE BUBBLES (100 um)]")
    model_a = AeroGFRCModel(void_radius_um=100, fiber_volume_pct=5, zirconium_pct=20)
    props_a = model_a.calculate_properties()
    print(f"  Clusters/m³: {props_a['clusters_per_m3']:,}")
    print(f"  Bonding Area: {props_a['total_bonding_area_m2']} m²")
    print(f"  Strength Mult: {props_a['strength_multiplier']}x")
    print(f"  Flow Reduction: {props_a['flow_reduction_factor']}")
    
    # Scenario B: Micro-voids (Your Hypothesis: 10 um)
    print("\n[SCENARIO B: MICRO-VOIDS (10 um) - TARGET]")
    model_b = AeroGFRCModel(void_radius_um=10, fiber_volume_pct=5, zirconium_pct=20)
    props_b = model_b.calculate_properties()
    print(f"  Clusters/m³: {props_b['clusters_per_m3']:,}")
    print(f"  Bonding Area: {props_b['total_bonding_area_m2']} m²")
    print(f"  Strength Mult: {props_b['strength_multiplier']}x")
    print(f"  Flow Reduction: {props_b['flow_reduction_factor']}")
    
    # Scenario C: Nano-voids (Extreme: 1 um)
    print("\n[SCENARIO C: NANO-VOIDS (1 um) - LIMIT]")
    model_c = AeroGFRCModel(void_radius_um=1, fiber_volume_pct=5, zirconium_pct=20)
    props_c = model_c.calculate_properties()
    print(f"  Clusters/m³: {props_c['clusters_per_m3']:,}")
    print(f"  Bonding Area: {props_c['total_bonding_area_m2']} m²")
    print(f"  Strength Mult: {props_c['strength_multiplier']}x")
    print(f"  Flow Reduction: {props_c['flow_reduction_factor']}")
    
    print("\n" + "=" * 60)
    print("CONCLUSION:")
    print(f"  Reducing bubble size from 100um to 10um increases strength by {props_b['strength_multiplier']/props_a['strength_multiplier']:.1f}x.")
    print(f"  Flow improves by {props_b['flow_reduction_factor']/props_a['flow_reduction_factor']:.1f}x.")
    print("  The 13-sphere FCC lattice is the key to unlocking this.")
    print("  Next Step: Mix trial with surfactant to achieve 10um bubbles.")

if __name__ == "__main__":
    demo()
