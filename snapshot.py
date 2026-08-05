import json, os, hashlib, subprocess
from pathlib import Path
from state_utils import load_ckpt, save_ckpt, stamp

UNE = Path(os.environ.get("UNE_DIR", str(Path.home() / "une")))

def compute_merkle():
    """Hash all readable .py files, build merkle root."""
    files = sorted(UNE.rglob("*.py"))
    if not files:
        return hashlib.sha256(b"empty").hexdigest()
    leaves = []
    for f in files:
        try:
            h = hashlib.sha256(f.read_bytes()).hexdigest()
            leaves.append(h)
        except (OSError, IOError):
            continue  # skip broken symlinks, permission errors, stale paths
    if not leaves:
        return hashlib.sha256(b"unreadable").hexdigest()
    while len(leaves) > 1:
        pairs = []
        for i in range(0, len(leaves), 2):
            left = leaves[i]
            right = leaves[i+1] if i+1 < len(leaves) else leaves[i]
            pairs.append(hashlib.sha256((left + right).encode()).hexdigest())
        leaves = pairs
    return leaves[0]

def ots_anchor(root_hash):
    try:
        stamp_dir = UNE / "snapshots"
        stamp_dir.mkdir(parents=True, exist_ok=True)
        data_file = stamp_dir / "current_root.txt"
        data_file.write_text(root_hash)
        subprocess.run(["ots", "stamp", str(data_file)],
                       capture_output=True, timeout=60)
        ots_file = stamp_dir / f"{root_hash[:8]}.ots"
        if ots_file.exists():
            return str(ots_file)
    except Exception:
        pass
    return None

def main():
    state = load_ckpt()
    root = compute_merkle()
    state["merkle_root"] = root
    state["timestamp"] = stamp()
    ots_result = ots_anchor(root)
    print(f"[SNAPSHOT] root={root[:16]}... ts={state['timestamp']}")
    if ots_result:
        print(f"[SNAPSHOT] OTS anchored: {ots_result}")
    else:
        print("[SNAPSHOT] OTS skipped")
    save_ckpt(state)

if __name__ == "__main__":
    main()
