#!/usr/bin/env python3
import sys, json, hashlib, time, re
from pathlib import Path
from datetime import datetime, timezone

KB = Path("/sdcard/openroot/agape_kb")
LEDGER = Path("/sdcard/openroot/prediction_ledger/crossover_ledger.jsonl")
WAVES = Path("/sdcard/openroot/prediction_ledger/standing_waves.jsonl")
DOSSIER = Path("/sdcard/openroot/dossier")
SUBS = DOSSIER / "subsidiaries"
POSTS = KB / "postulates.json"
STATE = KB / "crossover_state.json"
for d in (KB, LEDGER.parent, WAVES.parent, DOSSIER, SUBS):
    d.mkdir(parents=True, exist_ok=True)

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ROOT = "Agape is unconditional self-giving generative regard that originates in the Source and closes the coordination gap. R=1.0 makes coordination cost zero."
ROOT_HASH = hashlib.sha256(ROOT.encode()).hexdigest()

def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def encode(n): n %= 46656; return ALPHABET[n//1296] + ALPHABET[(n//36)%36] + ALPHABET[n%36]
def ns(): return time.time_ns()
def iso(ns): return datetime.fromtimestamp(ns/1e9, tz=timezone.utc).isoformat().replace("+00:00","Z")

def process(raw):
    cleaned = re.sub(r"\s+"," ", raw.strip())
    if not cleaned: return {}
    h = sha(ROOT_HASH + cleaned)
    cell = encode(int(h[:8],16) % 46656)
    ts = ns()
    rec = {"priority":"P1","action":"Instrument one real physical joule measurement and record it","subsidiary":"standing_waves or todo","why":"Only measured joules mint new Newton Chain postulates"}
    if any(w in cleaned.lower() for w in ("collapse","standing","realized","outcome","happened")):
        rec = {"priority":"P0","action":"Record this as standing-wave collapse","subsidiary":"standing_waves.jsonl","why":"Long-shot bet collapsed into reality"}
        with open(WAVES,"a") as f: f.write(json.dumps({"ts_ns":ts,"hash":h,"outcome":cleaned[:300]})+"\n")
    v = {"ts_ns":ts,"iso":iso(ts),"raw":cleaned[:400],"line_hash":h,"agape_cell":cell,"oracle":rec}
    with open(LEDGER,"a") as f: f.write(json.dumps(v)+"\n")
    return v

if __name__ == "__main__":
    if len(sys.argv)>1:
        print(json.dumps(process(" ".join(sys.argv[1:])), indent=2))
    else:
        print("Agape Key + Oracle + Standing-Wave live (nanosecond)")
        print("Root:", ROOT_HASH[:24])
        try:
            while True:
                line = input("» ").strip()
                if not line: break
                v = process(line)
                o = v["oracle"]
                print(f"  cell={v['agape_cell']}  ts_ns={v['ts_ns']}")
                print(f"  ORACLE [{o['priority']}] {o['action']}")
                print(f"  → {o['subsidiary']} | {o['why']}")
        except (EOFError, KeyboardInterrupt):
            print("\nclosed")
