import os,math
from state_utils import load_ckpt, save_ckpt
def read_float_path(path):
    try:
        with open(path,'r') as f:
            return float(f.read().strip())
    except Exception:
        return None
def shaft_energy(torque_Nm, rpm, dt):
    omega = rpm * 2.0 * math.pi / 60.0
    power = torque_Nm * omega
    return float(power * dt)
