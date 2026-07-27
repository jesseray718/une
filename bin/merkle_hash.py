#!/data/data/com.termux/files/usr/bin/python3
import hashlib, json, sys, os

def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

def merkle_root(leaves):
    if not leaves: return sha256("")
    layer = [sha256(l) for l in leaves]
    while len(layer) > 1:
        if len(layer) % 2 != 0: layer.append(layer[-1])
        layer = [sha256(layer[i] + layer[i+1]) for i in range(0, len(layer), 2)]
    return layer[0]

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "/data/data/com.termux/files/home/une/logs/energy/stream.jsonl"
    if not os.path.exists(path):
        print(json.dumps({"error": "Ledger not found", "path": path})); return
    leaves = [line.strip() for line in open(path) if line.strip()]
    root = merkle_root(leaves)
    print(json.dumps({"merkle_root": root, "leaf_count": len(leaves), "algorithm": "SHA-256"}, indent=2))

if __name__ == "__main__": main()
