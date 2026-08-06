import json, os, hashlib
from pathlib import Path
from datetime import datetime, timezone

def load_ckpt(path=None):
    path = path or Path(os.environ.get('UNE_DIR', Path.home() / 'une')) / 'state_checkpoint.json'
    path = Path(path)  # Normalize to Path object
    if not path.exists():
        return {'cycle': 0, 'fitness_score': 0.0, 'mesh_nodes': [], 'energy_joules': 10.0, 'lessons': [], 'merkle_root': None, 'health_score': 1.0}
    return json.loads(path.read_text())

def save_ckpt(data, path=None):
    path = path or Path(os.environ.get('UNE_DIR', Path.home() / 'une')) / 'state_checkpoint.json'
    from pathlib import Path
    Path(path).write_text(json.dumps(data, indent=2, default=str))

def calc_merkle(items):
    if not items: return hashlib.sha256(b'empty').hexdigest()
    hashes = [hashlib.sha256(str(i).encode()).hexdigest() for i in items]
    while len(hashes) > 1:
        hashes = [hashlib.sha256((hashes[i] + hashes[i+1]).encode()).hexdigest() for i in range(0, len(hashes)-1, 2)]
        if len(hashes) % 2: hashes.append(hashlib.sha256(hashes[-1].encode()).hexdigest())
    return hashes[0]