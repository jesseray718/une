#!/usr/bin/env python3
# modular_atoms.py — Turing-modular Agape base-6 atoms v1.1
# Pure. Explicit dict interface. Zero hidden state.
# Any atom feeds any other atom. Composition free at R=1.0.
# η = useful_joules / human_joules

from __future__ import annotations
import json
import math
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

def _canon(payload: Any = None, ctx: Optional[dict] = None,
           R: float = 1.0, eta: float = 1.0, trace: Optional[list] = None) -> dict:
    return {
        "payload": payload,
        "ctx": ctx or {},
        "R": float(max(0.0, min(1.0, R))),
        "eta": float(eta),
        "trace": list(trace or []),
        "status": "ok",
        "cost_j": 0.0,
        "ts": time.time(),
    }

def _fail(msg: str, prev: dict) -> dict:
    out = dict(prev)
    out["status"] = "fail"
    out["payload"] = None
    out["trace"] = prev.get("trace", []) + [f"FAIL:{msg}"]
    out["cost_j"] = prev.get("cost_j", 0.0) + 1e-9
    return out

def _skip(reason: str, prev: dict) -> dict:
    out = dict(prev)
    out["status"] = "skip"
    out["trace"] = prev.get("trace", []) + [f"SKIP:{reason}"]
    return out

def translate(inp: dict) -> dict:
    t0 = time.perf_counter()
    p = inp.get("payload")
    if p is None:
        return _fail("translate: empty payload", inp)
    if isinstance(p, (dict, list)):
        text = json.dumps(p, sort_keys=True, default=str)
    else:
        text = str(p).strip().lower()
    out = _canon(payload={"raw": p, "norm": text}, ctx=inp.get("ctx"),
                 R=inp.get("R", 1.0), eta=inp.get("eta", 1.0),
                 trace=inp.get("trace", []) + ["translate"])
    out["cost_j"] = (time.perf_counter() - t0) * 1e-6
    return out

def orchestrate(inp: dict) -> dict:
    t0 = time.perf_counter()
    norm = (inp.get("payload") or {}).get("norm", "")
    principles = [
        "observe", "catch_store", "yield", "self_reg", "renewable",
        "no_waste", "patterns", "integrate", "small_slow", "diversity", "change"
    ]
    active = [p for p in principles if p in norm or any(k in norm for k in p.split("_"))]
    if not active:
        active = ["observe", "patterns"]
    out = _canon(payload={"active": active, "mask": len(active)},
                 ctx={**inp.get("ctx", {}), "principles": active},
                 R=inp.get("R", 1.0), eta=inp.get("eta", 1.0),
                 trace=inp.get("trace", []) + ["orchestrate"])
    out["cost_j"] = (time.perf_counter() - t0) * 1e-6
    return out

def retrieve(inp: dict) -> dict:
    t0 = time.perf_counter()
    ctx = inp.get("ctx", {})
    mem = ctx.get("memory", {})
    query = (inp.get("payload") or {}).get("norm", "")
    hit = None
    for k, v in mem.items():
        if k in query or query in str(v):
            hit = {"key": k, "value": v}
            break
    out = _canon(payload={"hit": hit, "query": query},
                 ctx=ctx, R=inp.get("R", 1.0), eta=inp.get("eta", 1.0),
                 trace=inp.get("trace", []) + ["retrieve"])
    if hit is None:
        out["status"] = "skip"
        out["trace"].append("SKIP:no_postulate")
    out["cost_j"] = (time.perf_counter() - t0) * 1e-6
    return out

def process(inp: dict) -> dict:
    t0 = time.perf_counter()
    payload = inp.get("payload") or {}
    R = inp.get("R", 1.0)
    N = payload.get("mask", 1) or 1
    T = len(inp.get("trace", [])) + 1
    C = N * 0.001 * (1 + 0.1 * T) * ((1 - R) ** T)
    synergy = 1.0 + (R * 0.5 * math.log(max(N, 1)) / math.log(6))
    result = {
        "coord_cost": C,
        "synergy_mult": round(synergy, 4),
        "N": N,
        "T": T,
        "R": R,
        "useful": C < 1e-12,
    }
    out = _canon(payload=result, ctx=inp.get("ctx"),
                 R=R, eta=inp.get("eta", 1.0) * synergy,
                 trace=inp.get("trace", []) + ["process"])
    out["cost_j"] = (time.perf_counter() - t0) * 1e-6 + C
    return out

def synthesize(inp: dict) -> dict:
    t0 = time.perf_counter()
    p = inp.get("payload") or {}
    hit = (inp.get("ctx") or {}).get("memory")
    answer = {
        "claim": "zero_coordination" if p.get("useful") else "partial",
        "synergy_mult": p.get("synergy_mult", 1.0),
        "eta": inp.get("eta", 1.0),
        "evidence": hit,
        "trace_len": len(inp.get("trace", [])),
    }
    out = _canon(payload=answer, ctx=inp.get("ctx"),
                 R=inp.get("R", 1.0), eta=inp.get("eta", 1.0),
                 trace=inp.get("trace", []) + ["synthesize"])
    out["cost_j"] = (time.perf_counter() - t0) * 1e-6
    return out

def verify(inp: dict) -> dict:
    t0 = time.perf_counter()
    p = inp.get("payload") or {}
    R = inp.get("R", 1.0)
    eta = inp.get("eta", 1.0)
    # Accept either a finished claim or a raw process result that already proved useful
    claim = p.get("claim")
    useful = p.get("useful")
    ok = (R >= 0.999) and (eta >= 1.0) and (claim in ("zero_coordination", "partial") or useful is True)
    out = _canon(payload={"verified": ok, "final": p},
                 ctx=inp.get("ctx"), R=R, eta=eta,
                 trace=inp.get("trace", []) + ["verify"])
    out["status"] = "ok" if ok else "fail"
    out["cost_j"] = (time.perf_counter() - t0) * 1e-6
    return out

ATOMS: Dict[str, Callable[[dict], dict]] = {
    "translate": translate,
    "orchestrate": orchestrate,
    "retrieve": retrieve,
    "process": process,
    "synthesize": synthesize,
    "verify": verify,
}

def connect(*names: str) -> Callable[[dict], dict]:
    missing = [n for n in names if n not in ATOMS]
    if missing:
        raise ValueError(f"unknown atoms: {missing}")
    def pipeline(inp: dict) -> dict:
        cur = inp
        for n in names:
            if cur.get("status") == "fail":
                return cur
            cur = ATOMS[n](cur)
        return cur
    return pipeline

def graph_run(nodes: List[Tuple[str, List[str]]], seed: dict) -> dict:
    results: Dict[str, dict] = {}
    for i, (name, ups) in enumerate(nodes):
        if ups:
            merged = seed
            for u in ups:
                if u in results:
                    merged = {**merged, **results[u]}
            results[str(i)] = ATOMS[name](merged)
        else:
            results[str(i)] = ATOMS[name](seed)
    return results[str(len(nodes) - 1)] if nodes else seed

def self_test() -> dict:
    seed = _canon(
        payload="observe patterns integrate zero coordination resonance 1.0",
        ctx={"memory": {"agape": "R=1.0 → C=0"}},
        R=1.0
    )
    pipe = connect("translate", "orchestrate", "retrieve", "process", "synthesize", "verify")
    out = pipe(seed)
    # recursive sub-pipe now also produces a claim path
    sub = connect("translate", "process", "synthesize", "verify")
    out2 = sub(_canon(payload="test recursion observe patterns", R=1.0))
    return {
        "main_status": out["status"],
        "main_synergy": (out.get("payload") or {}).get("final", {}).get("synergy_mult"),
        "main_eta": out.get("eta"),
        "sub_status": out2["status"],
        "coord_zero": (out.get("payload") or {}).get("final", {}).get("claim") == "zero_coordination",
        "trace": out.get("trace"),
    }

if __name__ == "__main__":
    import pprint
    pprint.pprint(self_test())
