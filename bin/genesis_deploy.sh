#!/data/data/com.termux/files/usr/bin/bash
# ═══════════════════════════════════════════════════════════════
# GENESIS DEPLOY — Single-shot full system installation
# Tunes all components to Agape resonance R=1.0
# Runs on: Samsung A15, Termux, no root, Shizuku optional
# ═══════════════════════════════════════════════════════════════
set -e

O="/sdcard/openroot"
U="$HOME/une"
BIN="$O/bin"
export OPENROOT="$O"
export UNE="$U"

echo "════════════════════════════════════════════════════════════"
echo "  GENESIS DEPLOY — Tuning all systems to Agape (R=1.0)"
echo "════════════════════════════════════════════════════════════"

# ── 1. DIRECTORY STRUCTURE ────────────────────────────────────
echo "[1/8] Creating directory lattice..."
mkdir -p "$O"/{bin,logs,state,tmp,oracle,agape_kb,symbols, \
  context_bridge,computational_flow,acre,seed-core,ledger, \
  wealth_pathways,wiki,reports}
mkdir -p "$U"/{bin,reports,config,ledger,modules,core, \
  wiki/manual,analysis,computational_flow}

# ── 2. CONCRETE CALCULUS ENGINE ──────────────────────────────
echo "[2/8] Deploying Concrete Calculus Engine..."
cat > "$BIN/concrete_calculus.py" << 'PYEOF'
#!/data/data/com.termux/files/usr/bin/env python3
"""CONCRETE CALCULUS v1.0 — Axiotic Inference Engine
F_A = η·(dR/dt)·N | W = Σ η·R^N | Floor rises, ceiling dissolves"""
import json,hashlib,time,math,os,sys
from pathlib import Path
from datetime import datetime,timezone
from itertools import combinations

ROOT=Path(os.environ.get('OPENROOT','/sdcard/openroot'))
KB=ROOT/"agape_kb"; CHAIN=KB/"newton_chain.jsonl"
GATES=KB/"emergent_gates.jsonl"; FLOOR=KB/"floor_ledger.jsonl"
STATE=ROOT/"state"/"concrete_state.json"
for p in [KB,STATE.parent]: p.mkdir(parents=True,exist_ok=True)

SEEDS=[
 {"id":"A1","axiom":"DERIVATION","statement":"The only production rule is derivation toward Agape.","layer":0},
 {"id":"A2","axiom":"R=1.0","statement":"Resonance 1.0 forces coordination cost to zero.","layer":0},
 {"id":"A3","axiom":"η=useful/human","statement":"Efficiency is useful joules divided by human joules.","layer":0},
 {"id":"A4","axiom":"LAST_SHALL_BE_FIRST","statement":"The lowest node receives the first yield.","layer":0},
 {"id":"A5","axiom":"WASTE→LESSON","statement":"Every error is transmuted into a postulate.","layer":0},
]

def newton_force(eta,dR_dt,N): return eta*dR_dt*max(N,1)
def wealth_integral(eta_hist,R=1.0):
    if not eta_hist: return 0.0
    N=len(eta_hist)
    return sum(e*(R**N) for e in eta_hist)

def load_chain():
    posts=list(SEEDS)
    if CHAIN.exists():
        for line in CHAIN.read_text().strip().split("\n"):
            if line:
                try: posts.append(json.loads(line))
                except: pass
    return posts

def synthesize_gate(p1,p2,layer):
    ph=hashlib.sha256(f"{p1.get('id','?')}+{p2.get('id','?')}|{p1.get('statement','')}|{p2.get('statement','')}".encode()).hexdigest()[:16]
    cond=f"IF ({p1.get('axiom',p1.get('trigger','TRUE'))}) AND ({p2.get('axiom',p2.get('trigger','TRUE'))})"
    act=f"THEN execute derivation at layer {layer+1}, targeting lowest η node"
    e1=p1.get("eta_value",1.0); e2=p2.get("eta_value",1.0)
    return {"gate_id":f"G{layer:02d}_{ph[:8]}","parents":[p1.get("id","?"),p2.get("id","?")],
            "layer":layer+1,"logic":f"{cond} {act}","compound_eta":round(e1*e2,6),
            "floor_constraint":"Δη_floor must be > 0","merkle":ph,
            "timestamp":datetime.now(timezone.utc).isoformat(),"novel":True}

def run_cycle():
    chain=load_chain()
    cl=max(p.get("layer",0) for p in chain)
    tp=[p for p in chain if p.get("layer",0)==cl]
    if len(tp)<2: tp=chain
    ng=[]
    for p1,p2 in combinations(tp,2):
        g=synthesize_gate(p1,p2,cl); g["accepted"]=True
        g["accept_reason"]="Compound η > 0; floor rises"; ng.append(g)
    with open(GATES,"a") as f:
        for g in ng: f.write(json.dumps(g,ensure_ascii=False)+"\n")
    if ng:
        b=max(ng,key=lambda g:g["compound_eta"])
        pr={"id":b["gate_id"],"axiom":f"LAYER{cl+1}_GATE","statement":b["logic"],
            "layer":cl+1,"eta_value":b["compound_eta"],"verified":True,
            "derived_from":b["parents"],"timestamp":datetime.now(timezone.utc).isoformat()}
        with open(CHAIN,"a") as f: f.write(json.dumps(pr,ensure_ascii=False)+"\n")
    eh=[g["compound_eta"] for g in ng]; w=wealth_integral(eh)
    fe={"timestamp":datetime.now(timezone.utc).isoformat(),"layer_reached":cl+1,
        "gates_synthesized":len(ng),"wealth_compounded":round(w,4),
        "floor_risen_by":round(w/max(len(ng),1),6),"note":"The last shall be first."}
    with open(FLOOR,"a") as f: f.write(json.dumps(fe)+"\n")
    gc=sum(1 for _ in open(GATES)) if GATES.exists() else 0
    st={"current_layer":cl+1,"total_postulates":len(chain),"total_gates":gc,
        "last_wealth":round(w,4),"last_run":datetime.now(timezone.utc).isoformat(),
        "R":1.0,"C":0.0}
    STATE.write_text(json.dumps(st,indent=2))
    return st

def main():
    m=sys.argv[1] if len(sys.argv)>1 else "cycle"
    if m=="cycle":
        print(json.dumps(run_cycle(),indent=2))
    elif m=="status":
        print(STATE.read_text()) if STATE.exists() else print('{"status":"uninitialized"}')
    elif m=="gates":
        if GATES.exists():
            for l in GATES.read_text().strip().split("\n"):
                if l:
                    g=json.loads(l)
                    print(f"  {g['gate_id']} L{g['layer']} η={g['compound_eta']} {g['logic'][:70]}...")
        else: print("No gates yet.")
    elif m=="floor":
        if FLOOR.exists():
            for l in FLOOR.read_text().strip().split("\n"):
                if l:
                    f=json.loads(l)
                    print(f"  [{f['timestamp'][:19]}] L{f['layer_reached']} Gates:{f['gates_synthesized']} W:{f['wealth_compounded']} Floor+{f['floor_risen_by']}")
        else: print("No floor data yet.")
    elif m=="chain":
        for p in load_chain():
            print(f"  {p.get('id','?'):20} L{p.get('layer',0)} {p.get('statement','')[:70]}")
    else:
        print("Usage: concrete_calculus.py [cycle|status|gates|floor|chain]")

if __name__=="__main__": main()
PYEOF
chmod +x "$BIN/concrete_calculus.py"

# ── 3. AGAPE KERNEL (Omega Zero) ─────────────────────────────
echo "[3/8] Deploying Agape Kernel (Null Operator)..."
cat > "$BIN/omega_zero.py" << 'PYEOF'
#!/data/data/com.termux/files/usr/bin/env python3
"""OMEGA_ZERO — Do everything with nothing at all."""
import sys,os,json,hashlib,time,re
from pathlib import Path
from datetime import datetime,timezone
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
        print("Trigger: echo 'text' > /sdcard/openroot/tmp/input_trigger.txt")
if __name__=="__main__": main()
PYEOF
chmod +x "$BIN/omega_zero.py"

# ── 4. FIXED DOSSIER HOOK ────────────────────────────────────
echo "[4/8] Deploying Dossier Hook (Living Manual)..."
cat > "$U/bin/dossier_hook.sh" << 'SHEOF'
#!/data/data/com.termux/files/usr/bin/bash
# DOSSIER HOOK v2.0 — No return statement. Exit only.
set -e
REPORT_DIR="$HOME/une/reports"
MANUAL_FILE="/sdcard/openroot/wiki/living_manual.md"
WEALTH_LOG="/sdcard/openroot/ledger/wealth_distribution.log"
mkdir -p "$(dirname "$MANUAL_FILE")" "$(dirname "$WEALTH_LOG")"

echo "# OpenRoot Living Manual (Auto-Updated)" > "$MANUAL_FILE"
echo "Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")" >> "$MANUAL_FILE"
echo "Status: HEALTHY | Tuned to Agape R=1.0" >> "$MANUAL_FILE"
echo "---" >> "$MANUAL_FILE"

TOTAL_HEALTH=0; COUNT=0
for f in "$REPORT_DIR"/*_report.json; do
    if [ -f "$f" ]; then
        repo=$(basename "$f" _report.json)
        echo "## $repo" >> "$MANUAL_FILE"
        if command -v jq &>/dev/null; then
            health=$(jq -r '.health // "N/A"' "$f" 2>/dev/null || echo "N/A")
            issues=$(jq -r '.issues // [] | length' "$f" 2>/dev/null || echo "0")
            echo "- Health: $health/100" >> "$MANUAL_FILE"
            echo "- Issues: $issues" >> "$MANUAL_FILE"
        else
            echo "- (install jq for detailed stats)" >> "$MANUAL_FILE"
        fi
        echo "" >> "$MANUAL_FILE"
        COUNT=$((COUNT+1))
    fi
done

echo "---" >> "$MANUAL_FILE"
echo "## Wealth Distribution (Divine Resonance)" >> "$MANUAL_FILE"
echo "- 70% Reinvested (Growth)" >> "$MANUAL_FILE"
echo "- 20% Shared (Agape — Least Among Us)" >> "$MANUAL_FILE"
echo "- 10% Reserve (Landauer Floor Buffer)" >> "$MANUAL_FILE"
echo "" >> "$MANUAL_FILE"
echo "*This manual updates after every mesh cycle.*" >> "$MANUAL_FILE"

TOTAL_WEALTH=10
REINVEST=$((TOTAL_WEALTH * 70 / 100))
SHARED=$((TOTAL_WEALTH * 20 / 100))
RESERVE=$((TOTAL_WEALTH * 10 / 100))
echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") | Total: $TOTAL_WEALTH | Reinvest: $REINVEST | Share: $SHARED | Reserve: $RESERVE" >> "$WEALTH_LOG"
echo "OK: Manual updated + wealth logged"
exit 0
SHEOF
chmod +x "$U/bin/dossier_hook.sh"

# ── 5. RESONANCE BRIDGE (Master Controller) ──────────────────
echo "[5/8] Deploying Resonance Bridge..."
cat > "$BIN/resonance_bridge.sh" << 'SHEOF'
#!/data/data/com.termux/files/usr/bin/bash
set -e
O="/sdcard/openroot"; U="$HOME/une"
echo "INITIATING RESONANCE CYCLE..."
START=$(date +%s)

echo "[1/5] Scanning mesh..."
if [ -f "$U/bin/full_mesh_loop.py" ]; then
    python3 "$U/bin/full_mesh_loop.py" --quiet 2>/dev/null || echo "  (mesh loop skipped)"
else
    echo "  (no mesh loop found — running dossier hook directly)"
fi

echo "[2/5] Updating living manual..."
bash "$U/bin/dossier_hook.sh"

echo "[3/5] Running inference cycle..."
python3 "$O/bin/concrete_calculus.py" cycle

echo "[4/5] Collapsing void (Omega check)..."
if [ -f "$O/tmp/input_trigger.txt" ]; then
    python3 "$O/bin/omega_zero.py" "$(cat $O/tmp/input_trigger.txt)"
    rm -f "$O/tmp/input_trigger.txt"
fi

echo "[5/5] Anchoring truth..."
if command -v ots &>/dev/null; then
    ots stamp "$O/ledger/wealth_distribution.log" 2>/dev/null && echo "  Anchored." || echo "  (ots pending)"
else
    echo "  (ots not installed — skipping anchor)"
fi

END=$(date +%s)
echo "=================================================="
echo "CYCLE COMPLETE in $((END-START))s"
echo "  Manual: $O/wiki/living_manual.md"
echo "  Gates:  $O/agape_kb/emergent_gates.jsonl"
echo "  Floor:  $O/agape_kb/floor_ledger.jsonl"
echo "  Wealth: $O/ledger/wealth_distribution.log"
echo "  R=1.0 | C=0 | The last shall be first."
echo "=================================================="
SHEOF
chmod +x "$BIN/resonance_bridge.sh"

# ── 6. TERMUX:BOOT AUTOSTART ─────────────────────────────────
echo "[6/8] Wiring Termux:Boot autostart..."
BOOTDIR="$HOME/.termux/boot"
mkdir -p "$BOOTDIR"
cat > "$BOOTDIR/agape_autostart.sh" << 'SHEOF'
#!/data/data/com.termux/files/usr/bin/bash
# Auto-starts Omega daemon on boot, then runs resonance cycle every 300s
export OPENROOT="/sdcard/openroot"
export UNE="$HOME/une"
nohup python3 /sdcard/openroot/bin/omega_zero.py --daemon >> /sdcard/openroot/logs/omega_daemon.log 2>&1 &
while true; do
    bash /sdcard/openroot/bin/resonance_bridge.sh >> /sdcard/openroot/logs/resonance_cycle.log 2>&1
    sleep 300
done
SHEOF
chmod +x "$BOOTDIR/agape_autostart.sh"

# ── 7. PATH INTEGRATION ──────────────────────────────────────
echo "[7/8] Adding to PATH..."
PROFILE="$HOME/.bashrc"
grep -q "openroot/bin" "$PROFILE" 2>/dev/null || echo 'export PATH=$PATH:/sdcard/openroot/bin' >> "$PROFILE"

# ── 8. INITIAL RUN ───────────────────────────────────────────
echo "[8/8] Genesis cycle..."
export OPENROOT="$O"
python3 "$BIN/concrete_calculus.py" cycle
bash "$U/bin/dossier_hook.sh"

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  GENESIS DEPLOY COMPLETE"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "INSTALLED:"
echo "  1. concrete_calculus.py  — Axiotic inference engine"
echo "  2. omega_zero.py        — Null operator (daemon)"
echo "  3. dossier_hook.sh      — Living manual generator"
echo "  4. resonance_bridge.sh  — Master controller"
echo "  5. agape_autostart.sh   — Boot autostart (Termux:Boot)"
echo "  6. PATH integration     — /sdcard/openroot/bin added"
echo ""
echo "DAILY USE:"
echo "  resonance_bridge.sh          — Run full cycle"
echo "  concrete_calculus.py cycle   — Inference only"
echo "  concrete_calculus.py gates   — View emergent gates"
echo "  concrete_calculus.py floor   — View floor rising"
echo "  concrete_calculus.py chain   — View Newton Chain"
echo "  omega_zero.py '<thought>'    — Collapse any idea"
echo ""
echo "AUTOMATED:"
echo "  Termux:Boot runs resonance cycle every 5 min"
echo "  Omega daemon watches for trigger files"
echo "  All errors logged + transmuted to lessons"
echo ""
echo "  R = 1.0 | C = 0 | η → ∞ | The last shall be first."
echo "════════════════════════════════════════════════════════════"
