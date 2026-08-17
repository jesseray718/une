#!/data/data/com.termux/files/usr/bin/python3
import os, json, hashlib
from datetime import datetime, timezone
OPENROOT = "/sdcard/openroot"
LEDGER = f"{OPENROOT}/ledger/lattice_claims.jsonl"
CONTEXT = f"{OPENROOT}/context_bridge/lattice_root_state.json"
os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
os.makedirs(os.path.dirname(CONTEXT), exist_ok=True)
H = {1:{"name":"Orchestrator","node":"A15+Kai9000","role":"GOVERNOR-01","status":"live"},
     2:{"name":"Heavy spoke","node":"OptiPlex 3060","role":"7-8B Q4","status":"pending_boot"},
     3:{"name":"Physical","node":"Black Locust RMH","role":"ΔT+yield","status":"prototype"},
     4:{"name":"Token","node":"ACRE","role":"Merkle mint","status":"ledger_ready"}}
def merkle(leaves):
    layer=[hashlib.sha256(str(x).encode()).hexdigest() for x in leaves]
    while len(layer)>1:
        if len(layer)%2: layer.append(layer[-1])
        layer=[hashlib.sha256((layer[i]+layer[i+1]).encode()).hexdigest() for i in range(0,len(layer),2)]
    return layer[0]
def main():
    print("="*60)
    print("Lattice Root | η = useful_joules / human_joules")
    for k,v in H.items():
        print(f"  {k}. {v['name']:12} — {v['node']} [{v['status']}]")
    print("Next physical: first measured Black Locust burn + mint")
    print("="*60)
    claim={"timestamp":datetime.now(timezone.utc).isoformat(),"hierarchy":H,"R":1.0,"C":0.0,
           "eta":"η = useful_joules / human_joules","next":"measured RMH burn"}
    claim["merkle_root"]=merkle([json.dumps(claim,sort_keys=True), "1.0"])
    claim["claim_id"]=claim["merkle_root"][:16]
    open(LEDGER,"a").write(json.dumps(claim)+"\n")
    open(CONTEXT,"w").write(json.dumps(claim,indent=2))
    print(f"[ACRE] claim_id={claim['claim_id']}")
    print(f"merkle={claim['merkle_root']}")
    print(f"written={LEDGER}")
if __name__=="__main__": main()
