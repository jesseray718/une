import os,time,hashlib,sys
UNE_ROOT = os.environ.get('UNE_ROOT','/data/data/com.termux/files/home/une')
sys.path.insert(0, os.path.join(UNE_ROOT,'src'))
from therm_ledger import append_entry
from sensor_read import read_float_path, shaft_energy
from compute_useful import useful_from_samples
from une.axioms import check_function
LEDGER = os.path.join(UNE_ROOT,'stamps','thermo_ledger.jsonl')
STAMP_FILE = os.path.join(UNE_ROOT,'stamps','ledger.sha256')
SENSOR_TEMP1 = os.path.join(UNE_ROOT,'sensors','temp1')
SENSOR_TEMP2 = os.path.join(UNE_ROOT,'sensors','temp2')
SENSOR_RPM = os.path.join(UNE_ROOT,'sensors','rpm')
TORQUE_NM = 0.05
INTERVAL = 5
while True:
    t0 = time.time()
    tA = read_float_path(SENSOR_TEMP1)
    tB = read_float_path(SENSOR_TEMP2)
    if tA is None or tB is None:
        tA = 30.0
        tB = 25.0
    deltaT = abs(tA - tB)
    rpm = read_float_path(SENSOR_RPM) or 800.0
    shaft_j = shaft_energy(TORQUE_NM, rpm, INTERVAL)
    useful = useful_from_samples(deltaT, shaft_j)
    entry = {'timestamp': time.time(), 'deltaT': deltaT, 'shaft_joules': shaft_j, 'useful_joules': useful}
    root = append_entry(entry, LEDGER)
    with open(LEDGER,'rb') as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    with open(STAMP_FILE,'w') as f:
        f.write(digest + '\n')
    try:
        res = check_function(lambda: useful)
        print(res)
    except Exception as e:
        print('eta_error', str(e))
    dt = time.time() - t0
    sleep = INTERVAL - dt
    if sleep > 0:
        time.sleep(sleep)
