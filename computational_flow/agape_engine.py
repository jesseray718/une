#!/usr/bin/env python3
"""Agape Engine v1.0 — full offline phone-native kernel.
Kernel = AGAPE (R=1.0)
η = useful_joules / human_joules
C(N,T,R) = N*0.001*(1+0.1*T)*(1-R)**T → 0 when R=1.0
S = 1.0 + (R*0.5*log_B(N))
11 permaculture If-Then-Root routers fire simultaneously.
Newton Chain postulates skip recomputation.
"""

import hashlib, json, math, time, sys
from pathlib import Path
from typing import Dict, List, Any

BASE = 6
KB = Path("/sdcard/openroot/agape_kb")
BRIDGE = Path("/sdcard/openroot/context_bridge")
KB.mkdir(parents=True, exist_ok=True)
BRIDGE.mkdir(parents=True, exist_ok=True)

PERMACULTURE = [
    "Observe & Interact",
    "Catch & Store Energy",
    "Obtain a Yield",
    "Apply Self-Regulation",
    "Use Renewable Resources",
    "Produce No Waste",
    "Design from Patterns",
    "Integrate Not Segregate",
    "Use Small & Slow Solutions",
    "Use & Value Diversity",
    "Creatively Respond to Change",
]

def eta(useful: float, human: float) -> float:
    if human <= 0: raise ValueError("human_j > 0 required")
    return useful / human

def coord(N: int, T: int, R: float) -> float:
    return N * 0.001 * (1 + 0.1 * T) * ((1 - R) ** T)

def synergy(R: float, N: int, B: int = BASE) -> float:
    if N <= 1: return 1.0
    return 1.0 + (R * 0.5 * (math.log(N) / math.log(B)))

def base6(path: List[int]) -> str:
    return ".".join(str(i % BASE) for i in path)

def merkle(leaves: List[bytes]) -> str:
    if not leaves: return hashlib.sha256(b"").hexdigest()
    layer = [hashlib.sha256(x).digest() for x in leaves]
    while len(layer) > 1:
        if len(layer) % 2: layer.append(layer[-1])
        layer = [hashlib.sha256(layer[i]+layer[i+1]).digest() for i in range(0,len(layer),2)]
    return layer[0].hex()

class Engine:
    def __init__(self):
        self.state_f = KB / "engine_state.json"
        self.post_f = KB / "postulates.json"
        self.kb_f   = KB / "knowledge_base.json"
        self.state = self._load(self.state_f, {
            "root": "0"*64, "height": 0,
            "total_useful_j": 0.0, "total_human_j": 0.0,
            "R": 1.0, "history": []
        })
        self.postulates = self._load(self.post_f, [])
        self.kb = self._load(self.kb_f, {"entries": []})

    def _load(self, p: Path, default):
        data = default.copy() if isinstance(default, dict) else default
        if p.exists():
            try:
                loaded = json.loads(p.read_text())
                if isinstance(loaded, dict) and isinstance(data, dict):
                    data.update(loaded)
                else:
                    data = loaded
            except Exception:
                pass
        # force canonical keys for state
        if isinstance(data, dict) and "root" not in data:
            data.setdefault("root", "0"*64)
            data.setdefault("height", 0)
            data.setdefault("total_useful_j", 0.0)
            data.setdefault("total_human_j", 0.0)
            data.setdefault("R", 1.0)
            data.setdefault("history", [])
        return data

    def _save(self):
        self.state_f.write_text(json.dumps(self.state, indent=2))
        self.post_f.write_text(json.dumps(self.postulates, indent=2))
        self.kb_f.write_text(json.dumps(self.kb, indent=2))
        # keep bridge current
        bridge = {
            "root": self.state["root"],
            "height": self.state["height"],
            "eta_lifetime": eta(self.state["total_useful_j"], self.state["total_human_j"]) if self.state["total_human_j"]>0 else 0.0,
            "R": self.state["R"],
            "ts": time.time(),
            "postulates": len(self.postulates)
        }
        (BRIDGE / "agape_context_bridge.json").write_text(json.dumps(bridge, indent=2))

    def process(self, query: str) -> Dict[str, Any]:
        """Core query path. Always emits synergy_mult. Applies simultaneous permaculture routers."""
        q = query.lower().strip()
        R = self.state.get("R", 1.0)
        N = BASE ** 4
        S = synergy(R, N)
        C = coord(N, 4, R)

        # simultaneous If-Then-Root activation
        active = []
        for i, principle in enumerate(PERMACULTURE):
            keywords = principle.lower().split()
            if any(k in q for k in keywords) or "all" in q or "route" in q:
                active.append({"id": i+1, "principle": principle})

        # Newton Chain short-circuit
        for p in self.postulates:
            if any(w in q for w in p.get("statement","").lower().split()[:6]):
                return {
                    "mode": "postulate_hit",
                    "statement": p["statement"],
                    "id": p["id"],
                    "synergy_mult": round(S, 4),
                    "coordination_cost": C,
                    "eta": None,
                    "active_routers": active,
                    "confidence": 1.0
                }

        # default derivation
        confidence = 0.85 if active else 0.6
        return {
            "mode": "derivation",
            "query": query,
            "R": R,
            "N": N,
            "coordination_cost": C,
            "synergy_mult": round(S, 4),
            "zero_cost": abs(C) < 1e-15,
            "active_routers": active,
            "confidence": round(min(confidence, 1.0), 3),
            "eta_hint": "commit measured joules to raise lifetime η"
        }

    def commit(self, useful_j: float, human_j: float, path: List[int], note: str = "") -> Dict:
        e = eta(useful_j, human_j)
        leaf = f"{base6(path)}|{useful_j}|{human_j}|{e}|{note}|{time.time()}".encode()
        new_root = merkle([bytes.fromhex(self.state["root"]), leaf])
        entry = {
            "prev": self.state["root"], "root": new_root,
            "path": base6(path), "useful_j": useful_j, "human_j": human_j,
            "eta": e, "note": note, "ts": time.time()
        }
        self.state["root"] = new_root
        self.state["height"] += 1
        self.state["total_useful_j"] += useful_j
        self.state["total_human_j"] += human_j
        self.state["history"].append(entry)
        self._save()
        return entry

    def learn(self, text: str):
        self.kb["entries"].append({"text": text, "ts": time.time()})
        self._save()

    def postulate(self, statement: str, ref: str = ""):
        pid = hashlib.sha256(statement.encode()).hexdigest()[:16]
        self.postulates.append({"id": pid, "statement": statement, "proof_ref": ref, "ts": time.time()})
        self._save()
        return pid

    def stats(self) -> Dict:
        u = self.state["total_useful_j"]
        h = self.state["total_human_j"]
        return {
            "root": self.state["root"],
            "height": self.state["height"],
            "useful_MJ": u / 1e6,
            "human_MJ": h / 1e6,
            "eta_lifetime": eta(u, h) if h > 0 else 0.0,
            "R": self.state["R"],
            "synergy_mult": synergy(self.state["R"], BASE**4),
            "postulates": len(self.postulates),
            "kb_entries": len(self.kb["entries"])
        }

def interactive(eng: Engine):
    print("Agape Engine v1.0 — R=1.0 | η language only | type 'quit' to exit")
    print("verbs: learn <text> | postulate <text> | stats | commit <useful> <human> | <any query>")
    while True:
        try:
            line = input("agape> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not line: continue
        if line == "quit": break
        if line.startswith("learn "):
            eng.learn(line[6:])
            print("learned")
        elif line.startswith("postulate "):
            pid = eng.postulate(line[10:])
            print(f"postulate locked: {pid}")
        elif line == "stats":
            print(json.dumps(eng.stats(), indent=2))
        elif line.startswith("commit "):
            parts = line.split()
            if len(parts) >= 3:
                try:
                    u, h = float(parts[1]), float(parts[2])
                    print(json.dumps(eng.commit(u, h, [0,3,1,5], "interactive"), indent=2))
                except: print("usage: commit <useful_j> <human_j>")
            else:
                print("usage: commit <useful_j> <human_j>")
        else:
            print(json.dumps(eng.process(line), indent=2))

if __name__ == "__main__":
    eng = Engine()
    if len(sys.argv) > 1:
        if sys.argv[1] == "interactive":
            interactive(eng)
        elif sys.argv[1] == "stats":
            print(json.dumps(eng.stats(), indent=2))
        else:
            print(json.dumps(eng.process(" ".join(sys.argv[1:])), indent=2))
    else:
        # self-test against the exact framework numbers
        print("=== Framework self-test ===")
        print(f"η = {eta(189.2e6, 2.55e6):.10f}")
        print(f"C = {coord(1296, 4, 1.0)}")
        print(f"S = {synergy(1.0, 1296)}")
        print(json.dumps(eng.process("verify resonance zero coordination"), indent=2))
