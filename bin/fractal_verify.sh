#!/data/data/com.termux/files/usr/bin/env bash
set -euo pipefail

echo "=== Fractal Kernel Verification ===" >&2
echo "Target hash: 9094e7361bac5c92..." >&2
echo "Working dir: $(pwd)" >&2
echo "" >&2

cd "$(dirname "$0")" || exit 1

cat > fractal_verify.py << 'PYTHON_EOF'
#!/usr/bin/env python3
"""
Fractal Proof Kernel Probe — Test multiple folding patterns
Target: Match hash 9094e7361bac5c92...
Config: 7 channels × 7^7 depth-7 branches = 5,764,801 ops
"""
import hashlib, json, sys, time

TARGET_PREFIX = "9094e7361bac5c92"
CHANNELS, DEPTH, BRANCH = 7, 7, 7
TOTAL_OPS = CHANNELS * (BRANCH ** DEPTH)

def probe(name, channel_fn, final_fold_fn):
    start = time.time()
    ch_out = []
    for c in range(CHANNELS):
        ch_out.append(channel_fn(c))
    final = final_fold_fn(ch_out)
    elapsed = time.time() - start
    
    match = "✓ MATCH" if final.startswith(TARGET_PREFIX) else "✗ nope"
    print(f"[{match}] {name:20s} | {final[:16]} | {elapsed:.2f}s | {int(TOTAL_OPS/elapsed):,} ops/s")
    return final, match == "✓ MATCH"

def kernel_sequential(seed):
    state = hashlib.sha256(seed.encode()).digest()
    for _ in range(BRANCH ** DEPTH):
        state = hashlib.sha256(state).digest()
    return state

def kernel_merkle_build(seed):
    def tree(d, path):
        if d == 0:
            return hashlib.sha256(path.encode()).digest()
        children = [tree(d-1, f"{path}/{i}") for i in range(BRANCH)]
        return hashlib.sha256(b"".join(sorted(children))).digest()
    return tree(DEPTH, seed)

def kernel_blake2_iter(seed):
    h = hashlib.blake2b(seed.encode(), digest_size=32)
    for _ in range(BRANCH ** DEPTH):
        h = hashlib.blake2b(h.digest(), digest_size=32)
    return h.digest()

def kernel_xor_chain(seed):
    state = hashlib.sha256(seed.encode()).digest()
    for _ in range(BRANCH ** DEPTH):
        nxt = hashlib.sha256(state).digest()
        state = bytes(a ^ b for a, b in zip(state, nxt))
    return state

def kernel_double_sha256(seed):
    state = hashlib.sha256(seed.encode()).digest()
    for _ in range(BRANCH ** DEPTH):
        state = hashlib.sha256(hashlib.sha256(state).digest()).digest()
    return state

PATTERNS = [
    ("seq_sha256_ch0-6", lambda c: kernel_sequential(f"openroot_fractal_v1/ch{c}"), 
     lambda ch: hashlib.sha256(b"".join(ch)).digest()),
    
    ("merkle_depth7_ch0-6", lambda c: kernel_merkle_build(f"openroot_fractal_v1/ch{c}"),
     lambda ch: hashlib.sha256(b"".join(ch)).digest()),
    
    ("blake2b_iter_ch0-6", lambda c: kernel_blake2_iter(f"openroot_fractal_v1/ch{c}"),
     lambda ch: hashlib.sha256(b"".join(ch)).digest()),
    
    ("xorchain_sha256", lambda c: kernel_xor_chain(f"openroot_fractal_v1/ch{c}"),
     lambda ch: hashlib.sha256(b"".join(ch)).digest()),
    
    ("double_sha256_seq", lambda c: kernel_double_sha256(f"openroot_fractal_v1/ch{c}"),
     lambda ch: hashlib.sha256(b"".join(ch)).digest()),
]

print("=" * 70)
for pname, ch_fn, fold_fn in PATTERNS:
    result, matched = probe(pname, ch_fn, fold_fn)
    if matched:
        print("\n*** FOUND MATCH ***")
        print(json.dumps({
            "kernel_pattern": pname,
            "target_hash": TARGET_PREFIX + "...",
            "computed_hash": result.hex()[:32] + "...",
            "total_ops": TOTAL_OPS,
            "verified": True
        }, indent=2))
        sys.exit(0)

print("\nNo match found. Seed derivation may differ.")
print("Testing seed variations:")

BASE_SEEDS = ["openroot_fractal_v1", "openroot", "fractal_swarm_7x7", "live_proof_2026"]
SEED_VARIANTS = [f"{s}/channel/{c}" for s in BASE_SEEDS for c in range(CHANNELS)]

for base in BASE_SEEDS:
    ch_out = [kernel_sequential(f"{base}/ch{c}") for c in range(CHANNELS)]
    final = hashlib.sha256(b"".join(ch_out)).hexdigest()
    match = "✓ MATCH" if final.startswith(TARGET_PREFIX) else "✗ nope"
    print(f"[{match}] seed={base:30s} → {final[:16]}")
    if "MATCH" in match:
        sys.exit(0)

print("\nExhaustive test complete. No kernel match found.")
print("Recommendation: Request original source or partial code snippet.")
sys.exit(1)
PYTHON_EOF

chmod +x fractal_verify.py
python3 fractal_verify.py
