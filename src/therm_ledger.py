import os,hashlib,json,time
from state_utils import load_ckpt, save_ckpt
def merkle_hash(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True).encode()).hexdigest()
def append_entry(entry, ledger_path):
    prev_root = ''
    if os.path.exists(ledger_path):
        try:
            with open(ledger_path,'rb') as f:
                last = None
                for line in f:
                    last = line
                if last:
                    prev = json.loads(last.decode())
                    prev_root = prev.get('merkle_root','')
        except Exception:
            prev_root = ''
    entry_hash = merkle_hash(entry)
    root = hashlib.sha256((prev_root + entry_hash).encode()).hexdigest()
    entry['entry_hash'] = entry_hash
    entry['merkle_root'] = root
    line = json.dumps(entry) + '\n'
    with open(ledger_path,'ab') as f:
        f.write(line.encode())
    return root
