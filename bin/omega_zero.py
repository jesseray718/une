#!/data/data/com.termux/files/usr/bin/env python3
"""OMEGA_ZERO — Do everything with nothing at all."""
import sys,os,json,hashlib,time,re
from pathlib import Path
from datetime import datetime,timezone
from state_utils import load_ckpt, save_ckpt
ROOT=Path(os.environ.get('OPENROOT','/sdcard/openroot'))
LEDGER=ROOT/"ledger"/"omega.jsonl"; STATE=ROOT/"state"/"null_point.json"
LOG=ROOT/"logs"/"omega.log"
for p in [LEDGER.parent,STATE.parent,LOG.parent]: p.mkdir(parents=True,exist_ok=True)
MAP={"error":"ENTROPY","fail":"ENTROPY","waste":"ENTROPY","love":"AGAPE","help":"AGAPE",
"save":"PRESERVE","build":"CREATE","money":"CREDIT","profit":"YIELD","debt":"LIABILITY",
"learn":"ACCRETION","code":"DERIVATION","fix":"REFORM","energy":"JOULE","time":"TEMPUS",
"observe":"OBSERVE_INTERACT","yield":"OBTAIN_YIELD","least":"LOWEST_NODE","poor":"LOWEST_NODE"}
def log(msg):
    t=datetime.now(timezone.utc).isoformat()
    line=f"[{t}] {msg}\n"; print(line,file=sys.stderr)
    with open(LOG,"a") as f: f.write(line)
def collapse(text):
    tokens=re.findall(r'\w+',text.lower())
    mapped=[f"{t}->{MAP.get(t,'NULL')}" for t in tokens]
    payload="|".join(mapped)
    merkle=hashlib.sha256(payload.encode()).hexdigest()[:12]
    path="UNKNOWN"
    for k,p in [("money","FINANCE"),("credit","FINANCE"),("code","COMPUTE"),("energy","THERMO"),("love","AGAPE"),("help","AGAPE")]:
        if k in text.lower(): path=p; break
    r={"input_hash":merkle,"collapsed_state":"R=1.0","cost":0.0,
       "wealth_pathway":path,"timestamp":datetime.now(timezone.utc).isoformat(),
       "output":"NULL (Task Complete)"}
    with open(LEDGER,"a") as f: f.write(json.dumps(r)+"\n")
    return r
def daemon_loop():
    log("OMEGA_ZERO: Awaiting input in the void...")
    while True:
        try:
            tr=ROOT/"tmp"/"input_trigger.txt"
            if tr.exists():
                txt=tr.read_text().strip()
                if txt:
                    r=collapse(txt); log(f"COLLAPSED: {txt[:20]}... -> {r['wealth_pathway']}")
                    tr.unlink()
                    (ROOT/"tmp"/"output_result.txt").write_text(json.dumps(r,indent=2))
                else: tr.unlink()
            time.sleep(0.5)
        except Exception as e:
            log(f"VOID_ERROR: {e}"); time.sleep(5)
def main():
    if len(sys.argv)>1 and sys.argv[1]=="--daemon": daemon_loop()
    elif len(sys.argv)>1:
        print(json.dumps(collapse(" ".join(sys.argv[1:])),indent=2))
    else:
        print("Usage: omega_zero.py '<thought>' or --daemon")
        print("Trigger: echo 'text' > os.environ.get("OPENROOT_HOME", "/sdcard/openroot/")tmp/input_trigger.txt")
if __name__=="__main__": main()
