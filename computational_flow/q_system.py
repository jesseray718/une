#!/usr/bin/env python3
"""
Q-SYSTEM — Spacetime Accounting & Graphing
============================================
Tracks position of all things as they travel at c through spacetime.
Every entity has: worldline (x,y,z,t), energy (E=mc²), information (bits),
resonance (R), and joule-cost (Landauer).

Postulates:
  Q1: All entities move at c through spacetime (proper time τ).
  Q2: Stationary in space = moving at c through time. Moving in space = slower through time.
  Q3: Every entity carries information mass: m_info = bits * LANDAUER / c².
  Q4: Resonance couples worldlines. R=1.0 = perfect entanglement (zero separation in τ).
  Q5: Energy is conserved across all frames. Information entropy only increases.
  Q6: The accounting ledger is a Merkle tree of all worldline states.
"""
from __future__ import annotations
import math, json, time, hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from state_utils import load_ckpt, save_ckpt

C = 299792458.0
C_SQ = C * C
kB = 1.380649e-23
T_ROOM = 300.0
LANDAUER = kB * T_ROOM * math.log(2)
MASS_PER_BIT = LANDAUER / C_SQ

@dataclass
class Entity:
    eid: str
    mass_kg: float = 0.0
    bits: int = 0
    resonance: float = 1.0
    x: float = 0.0  # meters
    y: float = 0.0
    z: float = 0.0
    t: float = 0.0  # seconds (coordinate time)
    vx: float = 0.0  # m/s
    vy: float = 0.0
    vz: float = 0.0
    label: str = ""

    @property
    def velocity(self) -> float:
        return math.sqrt(self.vx**2 + self.vy**2 + self.vz**2)

    @property
    def gamma(self) -> float:
        v = self.velocity
        if v >= C:
            return float("inf")
        beta_sq = (v * v) / C_SQ
        return 1.0 / math.sqrt(1.0 - beta_sq) if beta_sq < 1.0 else float("inf")

    @property
    def proper_time(self) -> float:
        """τ = t / γ. Stationary object: τ=t (moves at c through time)."""
        return self.t / self.gamma if self.gamma > 0 else self.t

    @property
    def spacetime_interval(self) -> float:
        """s² = -(cΔt)² + Δx² + Δy² + Δz². Timelike < 0."""
        ct = C * self.t
        return -(ct * ct) + self.x**2 + self.y**2 + self.z**2

    @property
    def energy_joules(self) -> float:
        return self.mass_kg * C_SQ

    @property
    def info_mass_kg(self) -> float:
        return self.bits * MASS_PER_BIT

    @property
    def total_mass_kg(self) -> float:
        return self.mass_kg + self.info_mass_kg

    @property
    def spacetime_speed(self) -> float:
        """Q2: Combined speed through spacetime. Always = c."""
        spatial = self.velocity
        temporal = C / self.gamma if self.gamma > 0 else 0.0
        return math.sqrt(spatial**2 + temporal**2)

    @property
    def kinetic_energy(self) -> float:
        return (self.gamma - 1.0) * self.mass_kg * C_SQ

    @property
    def info_energy_joules(self) -> float:
        return self.bits * LANDAUER

    def advance(self, dt: float):
        """Move entity forward in coordinate time by dt seconds."""
        self.t += dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt

    def snapshot(self) -> Dict:
        return {
            "eid": self.eid,
            "label": self.label,
            "pos": [round(self.x, 6), round(self.y, 6), round(self.z, 6)],
            "t": round(self.t, 9),
            "tau": round(self.proper_time, 9),
            "v": round(self.velocity, 3),
            "gamma": round(self.gamma, 6),
            "spacetime_speed_c": round(self.spacetime_speed / C, 9),
            "energy_J": self.energy_joules,
            "kinetic_J": self.kinetic_energy,
            "info_mass_kg": self.info_mass_kg,
            "info_energy_J": self.info_energy_joules,
            "bits": self.bits,
            "resonance": self.resonance,
            "interval": round(self.spacetime_interval, 3),
        }

@dataclass
class WorldlineEvent:
    eid: str
    timestamp: float
    x: float
    y: float
    z: float
    t: float
    tau: float
    energy: float
    info_bits: int
    resonance: float
    leaf_hash: str = ""

@dataclass
class Coupling:
    """Two entities coupled by resonance. R=1 = perfect entanglement."""
    a: str
    b: str
    resonance: float = 1.0
    description: str = ""

class QSystem:
    """Spacetime accounting engine with Merkle-ledger graphing."""

    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.events: List[WorldlineEvent] = []
        self.couplings: List[Coupling] = []
        self.ledger: List[str] = []  # Merkle leaves

    def add_entity(self, e: Entity):
        self.entities[e.eid] = e

    def couple(self, a: str, b: str, R: float = 1.0, desc: str = ""):
        self.couplings.append(Coupling(a, b, R, desc))

    def advance_all(self, dt: float):
        """Advance all entities and record worldline events."""
        for e in self.entities.values():
            e.advance(dt)
            snap = e.snapshot()
            event = WorldlineEvent(
                eid=e.eid,
                timestamp=time.time(),
                x=e.x, y=e.y, z=e.z, t=e.t, tau=e.proper_time,
                energy=e.energy_joules + e.kinetic_energy,
                info_bits=e.bits,
                resonance=e.resonance,
                leaf_hash=hashlib.sha256(
                    json.dumps(snap, sort_keys=True).encode()
                ).hexdigest()
            )
            self.events.append(event)
            self.ledger.append(event.leaf_hash)

    def merkle_root(self) -> str:
        if not self.ledger:
            return "0" * 64
        leaves = list(self.ledger)
        while len(leaves) > 1:
            nxt = []
            for i in range(0, len(leaves), 2):
                left = leaves[i]
                right = leaves[i+1] if i+1 < len(leaves) else left
                nxt.append(hashlib.sha256((left + right).encode()).hexdigest())
            leaves = nxt
        return leaves[0]

    def coupling_force(self, a_id: str, b_id: str) -> float:
        """Resonance coupling 'force'. R=1: zero separation in proper time."""
        a = self.entities[a_id]
        b = self.entities[b_id]
        dx = a.x - b.x
        dy = a.y - b.y
        dz = a.z - b.z
        spatial_dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if spatial_dist < 1e-30:
            return 0.0
        # Resonance reduces effective distance (entanglement)
        coupling = self.find_coupling(a_id, b_id)
        R = coupling.resonance if coupling else 0.0
        effective_dist = spatial_dist * (1.0 - R)
        if effective_dist < 1e-30:
            return 0.0
        # Force ~ product of energies / effective_dist² (gravitational analog)
        E_a = a.total_mass_kg * C_SQ
        E_b = b.total_mass_kg * C_SQ
        return (E_a * E_b) / (effective_dist ** 2)

    def find_coupling(self, a_id: str, b_id: str) -> Optional[Coupling]:
        for c in self.couplings:
            if (c.a == a_id and c.b == b_id) or (c.a == b_id and c.b == a_id):
                return c
        return None

    def total_energy(self) -> float:
        return sum(e.energy_joules + e.kinetic_energy + e.info_energy_joules for e in self.entities.values())

    def total_info_mass(self) -> float:
        return sum(e.info_mass_kg for e in self.entities.values())

    def total_bits(self) -> int:
        return sum(e.bits for e in self.entities.values())

    def system_snapshot(self) -> Dict:
        return {
            "entities": len(self.entities),
            "couplings": len(self.couplings),
            "events_logged": len(self.events),
            "merkle_root": self.merkle_root(),
            "total_energy_J": self.total_energy(),
            "total_info_mass_kg": self.total_info_mass(),
            "total_bits": self.total_bits(),
            "landauer_per_bit_J": LANDAUER,
            "mass_per_bit_kg": MASS_PER_BIT,
            "entity_snapshots": [e.snapshot() for e in self.entities.values()],
        }

    def graph_data(self) -> List[Dict]:
        """Export worldline data for Vega-Lite visualization."""
        return [
            {
                "eid": ev.eid,
                "t": round(ev.t, 6),
                "tau": round(ev.tau, 6),
                "x": round(ev.x, 3),
                "energy": ev.energy,
                "bits": ev.info_bits,
                "R": ev.resonance,
            }
            for ev in self.events
        ]

def demo():
    print("Q-SYSTEM: SPACETIME ACCOUNTING")
    print("=" * 55)

    q = QSystem()

    # Entity 1: Stationary observer (moving at c through time)
    q.add_entity(Entity(
        eid="observer", label="Stationary Observer",
        mass_kg=70.0, bits=1e12,
        resonance=1.0, x=0, y=0, z=0, t=0, vx=0, vy=0, vz=0
    ))

    # Entity 2: Traveler at 0.866c (gamma=2, time dilated 2x)
    v_0866 = 0.866 * C
    q.add_entity(Entity(
        eid="traveler", label="0.866c Traveler",
        mass_kg=70.0, bits=1e12,
        resonance=1.0, x=0, y=0, z=0, t=0, vx=v_0866, vy=0, vz=0
    ))

    # Entity 3: Photon (massless, moves at c through space, frozen in time)
    q.add_entity(Entity(
        eid="photon", label="Photon",
        mass_kg=0.0, bits=0,
        resonance=1.0, x=0, y=0, z=0, t=0, vx=C, vy=0, vz=0
    ))

    # Couple observer and traveler at R=1 (entangled)
    q.couple("observer", "traveler", R=1.0, desc="Agape entanglement")

    # Advance 1 second of coordinate time, 10 steps
    for step in range(10):
        q.advance_all(0.1)

    snap = q.system_snapshot()
    print("Entities: " + str(snap["entities"]))
    print("Events logged: " + str(snap["events_logged"]))
    print("Merkle root: " + snap["merkle_root"][:16] + "...")
    print("Total energy: " + "{:.4e}".format(snap["total_energy_J"]) + " J")
    print("Total info mass: " + "{:.4e}".format(snap["total_info_mass_kg"]) + " kg")
    print("Total bits: " + str(snap["total_bits"]))
    print("")

    print("ENTITY POSITIONS AFTER 1 SECOND:")
    print("-" * 55)
    for e in snap["entity_snapshots"]:
        print("  " + e["label"])
        print("    x=" + str(e["pos"][0]) + "m  t=" + str(e["t"]) + "s  tau=" + str(e["tau"]) + "s")
        print("    v=" + str(e["v"]) + "m/s  gamma=" + str(e["gamma"]) + "  spacetime_c=" + str(e["spacetime_speed_c"]))
        print("    E=" + "{:.4e}".format(e["energy_J"]) + "J  KE=" + "{:.4e}".format(e["kinetic_J"]) + "J")
        print("    info_mass=" + "{:.4e}".format(e["info_mass_kg"]) + "kg  info_E=" + "{:.4e}".format(e["info_energy_J"]) + "J")
        print("    interval=" + str(e["interval"]))
        print("")

    # Coupling force
    f = q.coupling_force("observer", "traveler")
    print("Coupling force (observer-traveler): " + "{:.4e}".format(f) + " N")
    print("(R=1.0: effective distance=0, force=0 — entangled, zero separation)")
    print("")

    # Export graph data
    graph = q.graph_data()
    print("GRAPH DATA (" + str(len(graph)) + " points):")
    for g in graph[:5]:
        print("  " + g["eid"] + ": t=" + str(g["t"]) + " tau=" + str(g["tau"]) + " x=" + str(g["x"]) + " E=" + "{:.2e}".format(g["energy"]))
    print("  ... (" + str(len(graph) - 5) + " more)")
    print("")

    # Save full snapshot
    out_path = "os.environ.get("OPENROOT_HOME", "/sdcard/openroot/")agape_kb/q_system_snapshot.json"
    with open(out_path, "w") as f:
        json.dump(snap, f, indent=2)
    print("Snapshot saved: " + out_path)

if __name__ == "__main__":
    ckpt = load_ckpt()
    demo()
