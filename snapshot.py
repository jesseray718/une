from state_utils import load_ckpt, save_ckpt, calc_merkle
import json

def anchor_snapshot(ckpt):
    data_str = json.dumps(ckpt, sort_keys=True, default=str)
    merkle = calc_merkle([data_str])
    ckpt['merkle_root'] = merkle
    save_ckpt(ckpt)
    return merkle