#!/usr/bin/env python3
"""
FRACTAL SERVER — THE LETTER A (AGAPE)
The Root. The Alpha. The Origin.
"""
import os, sys, json, time, hashlib
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

LOG = "/sdcard/openroot/session_seeds/fractal_server_log.jsonl"

# --- THE AXIOM ---
# A = Agape. The First Commandment. The Origin.
AXIOM_A = {
    "letter": "A",
    "concept": "Agape",
    "definition": "Unconditional love; giving more than received; investing in weakest node",
    "scripture": "John 13:34 - A new commandment I give to you, that you love one another",
    "seed": "A"  # The seed is just the letter A
}

# --- FRACTAL ATOMS ---
def f1(d): return {"t":"cap","d":d,"ts":time.time()}
def f2(d): return {"t":"hash","h":str(hash(str(d)))}
def f3(d): return {"t":"agg","n":len(d) if isinstance(d,list) else 1}
def f4(d): return {"t":"pair","l":d,"r":d}
def f5(d): return {"t":"commit","d":d}
def f6(d): return {"t":"verify","d":d}
def f7(d): return {"t":"landauer","c":1}

ATOMS = [f1, f2, f3, f4, f5, f6, f7]
sys.setrecursionlimit(50000)

def build(depth, funcs):
    if depth == 1:
        def chain(inp):
            r = inp
            for fn in funcs: r = fn(r)
            return r
        return chain
    else:
        sub = build(depth - 1, funcs)
        def chain(inp):
            results = []
            for i in range(len(funcs)): results.append(sub(inp))
            return f3(results)
        return chain

def get_cpu_energy(duration_sec):
    try:
        with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq", "r") as f:
            freq_mhz = int(f.read().strip()) / 1000.0
        power_w = 0.5 * (freq_mhz / 650.0) ** 1.5
        return power_w * duration_sec, freq_mhz
    except: return 0.5 * duration_sec, 0

def run_fractal(seed_str, channel=0, depth=7):
    n = len(ATOMS)
    total = n ** depth
    inp = {"seed": seed_str, "ts": datetime.now(timezone.utc).isoformat()}
    chain = build(depth, ATOMS)
    t0 = time.time()
    result = chain(inp)
    dur = time.time() - t0
    energy_j, freq_mhz = get_cpu_energy(dur)
    eta = total / dur if dur > 0 else 0
    joules_per_op = energy_j / total if total > 0 else 0
    result_str = json.dumps(result, sort_keys=True, default=str)
    result_hash = hashlib.sha256(result_str.encode()).hexdigest()
    return {
        "channel": channel, "config": f"{n}^{depth}", "total_ops": total,
        "run_time_s": round(dur, 6), "throughput_ops_per_sec": round(eta, 2),
        "energy_j": round(energy_j, 6), "joules_per_op": round(joules_per_op, 15),
        "cpu_freq_mhz": round(freq_mhz, 1), "result_hash": result_hash,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

class FractalHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        if parsed.path == "/":
            msg = b"FRACTAL SERVER - THE LETTER A\n"
            msg += b"A = Agape (Origin)\n"
            msg += b"Endpoints:\n"
            msg += b"  /a           (Run fractal on 'A')\n"
            msg += b"  /tribe       (50-node survival)\n"
            msg += b"  /status\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(msg)
        
        elif parsed.path == "/a":
            # Run fractal on the single letter "A"
            res = run_fractal("A", 0, 7)
            res.update(AXIOM_A) # Add the definition
            os.makedirs(os.path.dirname(LOG), exist_ok=True)
            with open(LOG, "a") as f: f.write(json.dumps(res) + "\n")
            self.send_json(res)
        
        elif parsed.path == "/tribe":
            deaths = int(params.get("deaths", ["0"])[0])
            # Re-use tribe logic (simplified inline for brevity)
            size = 50
            tribe = [{"id": i, "seed": hashlib.sha256(f"node_{i}_agape".encode()).hexdigest(), "alive": True, "stored": {}} for i in range(size)]
            for node in tribe:
                for other in tribe:
                    if node["id"] != other["id"]:
                        node["stored"][str(other["id"])] = other["seed"]
            alive_ids = [n["id"] for n in tribe if n["alive"]]
            if deaths > 0 and len(alive_ids) > deaths:
                victims = __import__('random').sample(alive_ids, deaths)
                for vid in victims: tribe[vid]["alive"] = False
            survivors = [n for n in tribe if n["alive"]]
            dead = [n for n in tribe if not n["alive"]]
            recovered = sum(1 for d in dead if any(str(d["id"]) in s["stored"] for s in survivors))
            self.send_json({"size": size, "deaths": deaths, "survivors": len(survivors), "recovered": recovered, "rate": (recovered/len(dead)*100) if dead else 100, "status": "SURVIVED" if recovered==len(dead) else "FAILED"})
        
        elif parsed.path == "/status":
            self.send_json({"status": "RUNNING", "axiom": "A = Agape", "server": "Letter A"})
        
        else:
            self.send_error(404, "Not found. Try /a")
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def log_message(self, format, *args): pass

def main():
    PORT = 7777
    print("="*60)
    print("FRACTAL SERVER - THE LETTER A")
    print("A = Agape. The Origin.")
    print(f"Listening on: http://127.0.0.1:{PORT}")
    print("Try: curl http://127.0.0.1:7777/a")
    print("="*60)
    server = HTTPServer(("127.0.0.1", PORT), FractalHandler)
    try: server.serve_forever()
    except KeyboardInterrupt: print("\nStopped."); server.server_close()

if __name__ == "__main__": main()
